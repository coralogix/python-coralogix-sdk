#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger threading manager
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from __future__ import print_function
import os
import time
import copy
import json
import socket
import signal
import atexit
from threading import Thread, Lock, current_thread
from .constants import Coralogix
from . import __version__ as logger_version
from .handlers.debug import DebugLogger
from .http import CoralogixHTTPSender


class LoggerManager(object):
    """
    Coralogix Logger Manager
    """

    configured = False

    @classmethod
    def initialize(cls):
        """
        Logger Manager initialize procedure
        """
        cls._bulk_template = {
            'privateKey': Coralogix.FAILED_PRIVATE_KEY,
            'applicationName': Coralogix.NO_APP_NAME,
            'subsystemName': Coralogix.NO_SUB_SYSTEM
        }
        cls._time_delta_last_update = 0
        cls._time_delta = 0
        cls._mutex = Lock()
        cls._sync_time = False
        cls._init()

    @classmethod
    def _init(cls):
        """
        Logger Manager threading initialize
        """
        cls._stop = False
        cls._thread = None
        cls._buffer = []
        cls._buffer_size = 0
        cls._process = os.getpid()
        cls._run()

    @classmethod
    def configure(cls, sync_time, **kwargs):
        """
        Configure logger with client details
        :param sync_time: Synchronize time with Coralogix servers (default: False)
        :type sync_time: bool
        """
        try:
            kwargs.update({'computerName': socket.gethostname().strip()})
            cls._bulk_template = copy.deepcopy(kwargs)
            cls._sync_time = bool(sync_time)
            DebugLogger.info('Successfully configured Coralogix logger')
            cls.send_init_message()
            cls.configured = True
        except Exception as exc:
            if not cls._stop:
                DebugLogger.exception('Failed to configure Coralogix logger', exc)
                cls.configured = False
        return cls.configured

    @classmethod
    def send_init_message(cls):
        """
        Send initialization message to Coralogix for check connection
        """
        cls.add_logline(
            'The Application Name {} and Subsystem Name {} from the Python SDK, '
            'version {} has started to send data'.format(
                cls._bulk_template['applicationName'],
                cls._bulk_template['subsystemName'],
                logger_version
            ),
            Coralogix.Severity.INFO,
            Coralogix.CORALOGIX_CATEGORY,
            threadId=current_thread().ident
        )

    @classmethod
    def add_logline(cls, message, severity, category, **kwargs):
        """
        Add log line to queue
        :param message: Log record content
        :type message: str
        :param severity: Log record severity(level)
        :type severity: int
        :param category: Log record category (default: None)
        :type category: str
        """
        try:
            if not cls._mutex:
                return
            cls._mutex.acquire()
            # This is very important!
            # When forking, we will get here with a new process id.
            # For each new child fork we must create a new watcher thread.
            if os.getpid() != cls._process:
                cls._init()

            if cls._buffer_size < Coralogix.MAX_LOG_BUFFER_SIZE:
                # Validate message
                message = cls._msg2str(message) if message and not str(message).isspace() \
                    else 'EMPTY_STRING'

                # Validate severity
                if cls._is_number(severity) and str(severity):
                    severity = int(severity)
                else:
                    severity = int(Coralogix.Severity.DEBUG)

                if int(Coralogix.Severity.DEBUG) > severity or severity > int(Coralogix.Severity.CRITICAL):
                    severity = int(Coralogix.Severity.DEBUG)

                # Validate category
                category = str(category) if category and (not category.isspace()) \
                    else Coralogix.CORALOGIX_CATEGORY

                # Combine a log-entry from the must parameters together with the optional one.
                new_entry = {
                    'text': message,
                    'timestamp': time.time() * 1000 + cls._time_delta,
                    'severity': severity,
                    'category': category,
                }
                new_entry.update(kwargs)

                new_entry_size = len(json.dumps(new_entry).encode('utf8'))
                if Coralogix.MAX_LOG_CHUNK_SIZE <= new_entry_size:
                    # if log message is too big, throw it;
                    DebugLogger.warning(
                        'add_logline(): received log message too big of size= {} MB, bigger than '
                        'max_log_chunk_size= {}; throwing...'.format(
                            new_entry_size / 1024 ** 2, Coralogix.MAX_LOG_CHUNK_SIZE
                        )
                    )
                    return

                cls._buffer.append(new_entry)
                # Update the buffer size to reflect the new size.
                cls._buffer_size += len(json.dumps(new_entry).encode('utf8'))
        except Exception as exc:
            if not cls._stop:
                DebugLogger.exception('Failed to add log to buffer', exc)
        finally:
            if cls._mutex:
                cls._mutex.release()

    @classmethod
    def _msg2str(cls, message):
        """
        Convert log message string to compatible format
        :param message: Log record content
        :type message: str or dict
        :return: JSON encoded message
        :rtype: str
        """
        try:
            if type(message) is str:
                return message
            elif type(message) is dict:
                return json.dumps(message)
            else:
                return message
        except Exception:
            if not cls._stop:
                return str(message)

    @classmethod
    def _send_bulk(cls, time_sync=True):
        """
        Send bulk from the buffer
        :param time_sync: Synchronize time with Coralogix servers (default: True)
        :type time_sync: bool
        """
        try:
            cls._mutex.acquire()

            if not cls.configured:
                return

            if time_sync:
                cls.update_time_delta_interval()

            # Total buffer size
            size = len(cls._buffer)
            if size < 1:
                DebugLogger.info('Buffer is empty, there is nothing to send!')
                return

            # If the size is bigger than the maximum allowed chunk size then split it by half.
            # Keep splitting it until the size is less than MAX_LOG_CHUNK_SIZE
            while (len(json.dumps(cls._buffer[:size]).encode('utf8')) > Coralogix.MAX_LOG_CHUNK_SIZE) \
                    and size > 1:
                size = int(size / 2)

            # We must take at least one value.
            # If the first message is bigger than MAX_LOG_CHUNK_SIZE
            # we need to take it anyway.
            size = size if size > 0 else 1

            DebugLogger.info('Checking buffer size. Total log entries is: {}'.format(size))
            cls._bulk_template['logEntries'] = cls._buffer[:size]
            cls._buffer[:size] = []

            # Extract from the buffer size the total amount of the logs we removed from the buffer
            cls._buffer_size -= (len(json.dumps(cls._bulk_template['logEntries']).encode('utf8')) - size * 2)

            # Make sure we are always positive
            cls._buffer_size = max(cls._buffer_size, 0)
        except Exception as exc:
            DebugLogger.exception('Failed to send bulk', exc)
        finally:
            cls._mutex.release()

        DebugLogger.info(
            'Buffer size after removal is: {0:d}'.format(
                len(json.dumps(cls._buffer).encode('utf8'))-2
            )
        )

        if cls._bulk_template['logEntries']:
            CoralogixHTTPSender.send_request(cls._bulk_template)

    @classmethod
    def update_time_delta_interval(cls):
        """
        Sync log timestamps with Coralogix server
        """
        try:
            # If more than 5 minutes passed from the last sync update
            if time.time() - cls._time_delta_last_update >= 60 * Coralogix.SYNC_TIME_UPDATE_INTERVAL:
                result, _time_delta = CoralogixHTTPSender.get_time_sync()
                if result:
                    cls._time_delta = _time_delta
                    cls._time_delta_last_update = time.time()
        except Exception as exc:
            if not cls._stop:
                DebugLogger.exception('Failed to update time sync', exc)

    @classmethod
    def _run(cls):
        """
        Start a new timer thread to watch the Logger Manager queue
        """
        try:
            cls._thread = Thread(target=cls._internal_run)
            cls._thread.daemon = True
            cls._thread.name = 'coralogix-sending-thread'
            cls._thread.start()
        except Exception as exc:
            if not cls._stop:
                DebugLogger.exception('Failed to start buffer worker thread', exc)

    @classmethod
    def flush(cls):
        """
        Flush all messages in buffer and send them immediately on the current thread
        """
        DebugLogger.info('Flush buffer before exit')
        cls._send_bulk(time_sync=False)

    @classmethod
    def stop(cls):
        """
        Stop logger execution
        """
        DebugLogger.info('Stopping buffer thread')
        cls._stop = True

    @classmethod
    def _is_number(cls, number):
        """
        Check if number is integer
        :param number: Input value
        :return: Check result
        :rtype: bool
        """
        return isinstance(number, int)

    @classmethod
    def _internal_run(cls):
        """
        Start timer execution. The timer should send every X seconds logs from the buffer
        """
        try:
            while True:
                if cls._stop:
                    cls.flush()
                    return
                # Send log bulk
                cls._send_bulk(time_sync=cls._sync_time)

                # Check: when is the next time we should send logs?
                # If we already have at least half of the max chunk size
                # then we are working in fast mode
                if cls._buffer_size > (Coralogix.MAX_LOG_CHUNK_SIZE / 2):
                    next_check_interval = Coralogix.FAST_SEND_SPEED_INTERVAL
                else:
                    next_check_interval = Coralogix.NORMAL_SEND_SPEED_INTERVAL

                DebugLogger.debug(
                    'Next buffer check is scheduled in {} seconds'.format(next_check_interval)
                )
                time.sleep(next_check_interval)
        except Exception as exc:
            try:
                if not cls._stop:
                    DebugLogger.exception('Exception from the main buffer loop:', exc)
            except Exception:
                pass


LoggerManager.initialize()


def handler(signum, frame):
    """
    Handler wrapper
    :param signum: Termination signal code
    :type signum: int
    :param frame: Current frame
    """
    _handler()


def _handler():
    """
    Thread termination event
    """
    try:
        LoggerManager.stop()
        if LoggerManager._thread:
           LoggerManager._thread.join()
    except Exception:
        pass


# Register thread events
atexit.register(_handler)
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
