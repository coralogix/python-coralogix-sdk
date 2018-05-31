#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger default constants
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from enum import IntEnum


class Coralogix(object):
    """
    Default constants for Coralogix Logger
    """

    class Severity(IntEnum):
        """
        List of levels for logs records
        """
        DEBUG = 1
        VERBOSE = 2
        INFO = 3
        WARNING = 4
        ERROR = 5
        CRITICAL = 6

    SEVERITY_MAPPER = {
        0: Severity.DEBUG,
        10: Severity.DEBUG,
        20: Severity.INFO,
        30: Severity.WARNING,
        40: Severity.ERROR,
        50: Severity.CRITICAL,
        'default': Severity.INFO,
    }

    # Maximum log buffer size
    MAX_LOG_BUFFER_SIZE = 12 * 1024 ** 2  # 12mb

    # Maximum chunk size
    MAX_LOG_CHUNK_SIZE = 1.5 * 1024 ** 2  # 1.5 mb

    # Bulk send interval in normal mode
    NORMAL_SEND_SPEED_INTERVAL = 500.0 / 1000

    # Bulk send interval in fast mode
    FAST_SEND_SPEED_INTERVAL = 100.0 / 1000

    # Coralogix logs url
    CORALOGIX_LOG_URL = 'https://api.coralogix.com:443/api/v1/logs'

    # Coralogix time delay url
    CORALOGIX_TIME_DELTA_URL = 'https://api.coralogix.com:443/sdk/v1/time'

    # Timeout for time-delay request
    TIME_DELAY_TIMEOUT = 1

    # Default private key
    FAILED_PRIVATE_KEY = 'no private key'

    # Default application name
    NO_APP_NAME = 'NO_APP_NAME'

    # Default subsystem name
    NO_SUB_SYSTEM = 'NO_SUB_NAME'

    # Default log file name
    LOG_FILE_NAME = 'coralogix.sdk.log'

    # Default http timeout
    HTTP_TIMEOUT = 30

    # Number of attempts to retry http post
    HTTP_SEND_RETRY_COUNT = 5

    # Interval between failed http post requests
    HTTP_SEND_RETRY_INTERVAL = 2

    # Coralogix category
    CORALOGIX_CATEGORY = 'CORALOGIX'

    # Sync time update interval
    SYNC_TIME_UPDATE_INTERVAL = 5  # minutes

    @classmethod
    def map_severity(cls, severity):
        """
        Maps Python's logging library severities to Coralogix's
        :param severity: Python severity value
        :type severity: int or str
        :return: Coralogix severity
        :rtype: int
        """
        if severity in cls.SEVERITY_MAPPER:
            return cls.SEVERITY_MAPPER[severity]
        return cls.SEVERITY_MAPPER['default']
