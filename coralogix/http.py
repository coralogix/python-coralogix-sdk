#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger HTTP sender
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from __future__ import print_function
from threading import Lock
import time
import sys
import requests
from .constants import Coralogix
from .handlers.debug import DebugLogger
from . import __version__


class CoralogixHTTPSender(object):
    """
    HTTP middleware class for sending logs to Coralogix
    """

    _mutex = Lock()
    _timeout = 30

    @classmethod
    def _get_user_agent(cls):
        """
        Generate User-Agent string for HTTP requests
        :return: User-Agent string
        :rtype: str
        """
        python_version = '{}.{}.{}'.format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
        )
        return 'coralogix-python-sdk/{} (Python {})'.format(__version__, python_version)

    @classmethod
    def _init(cls, timeout=None):
        """
        Initialize Coralogix HTTP sender
        :param timeout: Time between sending logs to server (default: None)
        :type timeout: int
        """
        cls._timeout = timeout or Coralogix.HTTP_TIMEOUT

    @classmethod
    def send_request(cls, bulk, url=Coralogix.CORALOGIX_LOG_URL):
        """
        Send request procedure
        :param bulk: Bulk with logs records
        :type bulk: dict
        :param url: Log collector url
        :type url: str
        """
        try:
            cls._mutex.acquire()
            for attempt in range(1, Coralogix.HTTP_SEND_RETRY_COUNT+2):
                try:
                    DebugLogger.info(
                        'About to send bulk to Coralogix server. Attempt number: {0:d}'.format(
                            attempt
                        )
                    )
                    
                    private_key = bulk.get('privateKey', '')
                    
                    # Transform to singles format: array of log objects
                    # Each log entry gets the metadata fields merged in
                    application_name = bulk.get('applicationName', '')
                    subsystem_name = bulk.get('subsystemName', '')
                    log_entries = bulk.get('logEntries', [])
                    
                    # Build singles format payload - direct array of logs
                    singles_payload = []
                    for entry in log_entries:
                        log_object = {
                            'applicationName': application_name,
                            'subsystemName': subsystem_name
                        }
                        # Merge all fields from the log entry
                        log_object.update(entry)
                        
                        singles_payload.append(log_object)
                    
                    headers = {
                        'Authorization': 'Bearer {}'.format(private_key),
                        'Content-Type': 'application/json',
                        'User-Agent': cls._get_user_agent()
                    }
                    
                    response = requests.post(
                        url=url,
                        timeout=cls._timeout,
                        json=singles_payload,
                        headers=headers
                    )
                    DebugLogger.info(
                        'Successfully sent bulk to Coralogix server. Result is: {0:d}'.format(
                            response.status_code
                        )
                    )
                    return
                except Exception as exc:
                    DebugLogger.exception('Failed to send HTTP POST request', exc)
                DebugLogger.error(
                    'Failed to send bulk. Will retry in: {0:d} seconds...'.format(
                        Coralogix.HTTP_SEND_RETRY_INTERVAL
                    )
                )
                time.sleep(Coralogix.HTTP_SEND_RETRY_INTERVAL)
        except Exception as exc:
            DebugLogger.exception('Failed to send HTTP POST request', exc)
        finally:
            if cls._mutex:
                cls._mutex.release()

    @classmethod
    def get_time_sync(cls, url=Coralogix.CORALOGIX_TIME_DELTA_URL):
        """
        A helper method to get Coralogix server current time and calculate the time difference
        :param url: Time synchronization service url
        :type url: str
        :return: Time synchronization status, time delta
        :rtype: tuple
        """
        try:
            cls._mutex.acquire()
            DebugLogger.info('Syncing time with Coralogix server...')
            headers = {
                'User-Agent': cls._get_user_agent()
            }
            response = requests.get(
                url=url,
                timeout=cls._timeout,
                headers=headers
            )
            if response and response.status_code == 200:
                # Server epoch time in milliseconds
                server_time = int(response.content.decode()) / 1e4
                # Local epoch time in milliseconds
                local_time = time.time() * 1e3
                # Time delta
                time_delta = server_time - local_time
                DebugLogger.info(
                    'Server epoch time={}, local epoch time={}; Updating time delta to: {}'.format(
                        server_time,
                        local_time,
                        time_delta
                    )
                )
                return True, time_delta
            return False, 0
        except Exception as exc:
            DebugLogger.exception('Failed to send HTTP GET request', exc)
        finally:
            if cls._mutex:
                cls._mutex.release()
