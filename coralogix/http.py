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
import requests
from .constants import Coralogix
from .handlers.debug import DebugLogger


class CoralogixHTTPSender(object):
    """
    HTTP middleware class for sending logs to Coralogix
    """

    _mutex = Lock()
    _timeout = 30

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
                    response = requests.post(
                        url=url,
                        timeout=cls._timeout,
                        json=bulk
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
            response = requests.get(
                url=url,
                timeout=cls._timeout
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
