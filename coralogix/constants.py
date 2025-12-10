#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger default constants
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

import os
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

    # Legacy constants removed - use get_log_url(region) and get_time_delta_url(region) instead
    # Regions are now mandatory as per Coralogix endpoint deprecation (March 31, 2026)
    # Coralogix logs url
    CORALOGIX_LOG_URL = os.environ.get('CORALOGIX_LOG_URL', 'https://ingress.coralogix.com:443/api/v1/logs')

    # Coralogix time delay url
    CORALOGIX_TIME_DELTA_URL = os.environ.get('CORALOGIX_TIME_DELTA_URL', 'https://ingress.coralogix.com:443/sdk/v1/time')


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

    # Supported Coralogix regions
    REGIONS = {
        'AP1': 'ap1',
        'AP2': 'ap2',
        'AP3': 'ap3',
        'EU1': 'eu1',
        'EU2': 'eu2',
        'US1': 'us1',
        'US2': 'us2',
    }

    # Default region (used when no region is specified)
    DEFAULT_REGION = None

    @classmethod
    def get_log_url(cls, region=None):
        """
        Get Coralogix log URL for the specified region
        :param region: Coralogix region (AP1, AP2, AP3, EU1, EU2, US1, US2)
        :type region: str or None
        :return: Log URL for the region
        :rtype: str
        :raises ValueError: If region is not provided and CORALOGIX_REGION environment variable is not set
        """
        # Use parameter if provided, otherwise check environment variable
        if not region:
            env_region = os.environ.get('CORALOGIX_REGION')
            if env_region:
                region = env_region.upper()
        
        # Region is mandatory - raise error if not provided
        if not region:
            raise ValueError(
                'CORALOGIX_REGION is mandatory. Please provide a region parameter or set the '
                'CORALOGIX_REGION environment variable. Supported regions: AP1, AP2, AP3, EU1, EU2, US1, US2'
            )
        
        # Validate region
        if region.upper() not in cls.REGIONS:
            raise ValueError(
                'Invalid region "{}". Supported regions: AP1, AP2, AP3, EU1, EU2, US1, US2'.format(region)
            )
        
        region_lower = cls.REGIONS[region.upper()]
        return 'https://ingress.{}.coralogix.com/logs/v1/singles'.format(region_lower)

    @classmethod
    def get_time_delta_url(cls, region=None):
        """
        Get Coralogix time delta URL for the specified region
        :param region: Coralogix region (AP1, AP2, AP3, EU1, EU2, US1, US2)
        :type region: str or None
        :return: Time delta URL for the region
        :rtype: str
        :raises ValueError: If region is not provided and CORALOGIX_REGION environment variable is not set
        """
        # Use parameter if provided, otherwise check environment variable
        if not region:
            env_region = os.environ.get('CORALOGIX_REGION')
            if env_region:
                region = env_region.upper()
        
        # Region is mandatory - raise error if not provided
        if not region:
            raise ValueError(
                'CORALOGIX_REGION is mandatory. Please provide a region parameter or set the '
                'CORALOGIX_REGION environment variable. Supported regions: AP1, AP2, AP3, EU1, EU2, US1, US2'
            )
        
        # Validate region
        if region.upper() not in cls.REGIONS:
            raise ValueError(
                'Invalid region "{}". Supported regions: AP1, AP2, AP3, EU1, EU2, US1, US2'.format(region)
            )
        
        region_lower = cls.REGIONS[region.upper()]
        return 'https://ingress.{}.coralogix.com/sdk/v1/time'.format(region_lower)

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
