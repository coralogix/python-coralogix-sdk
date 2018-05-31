#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger internal debug logger
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from __future__ import print_function
import sys
import datetime
import traceback


class DebugLogger(object):
    """
    A private class to print debugging messages from CoralogixLogger
    """

    debug_mode = False

    @classmethod
    def log(cls, level, message, exception=None):
        """
        Logs a message with level on this logger
        :param level: Level of the log record
        :type level: str
        :param message: Log record content
        :type message: str
        :param exception: Some exception which logs
        :type exception: Exception
        """
        if not cls.debug_mode:
            return
        try:
            if exception:
                print(
                    '{0:s} - [{1:s}]\t-\t{2:s}\nEXCEPTION: {3}'.format(
                        datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f'),
                        level,
                        message,
                        exception
                    )
                )
                traceback.print_exc(file=sys.stdout)
            else:
                print(
                    '{0:s} - [{1:s}]\t-\t{2:s}'.format(
                        datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f'),
                        level,
                        message
                    )
                )
        except Exception as exc:
            print('Failed to print log: {0}'.format(exc))

    @classmethod
    def debug(cls, message):
        """
        Logs a message with level DEBUG on this logger
        :param message: Log record content
        :type message: str
        """
        cls.log('DEBUG', message)

    @classmethod
    def info(cls, message):
        """
        Logs a message with level INFO on this logger
        :param message: Log record content
        :type message: str
        """
        cls.log('INFO', message)

    @classmethod
    def warning(cls, message):
        """
        Logs a message with level WARNING on this logger
        :param message: Log record content
        :type message: str
        """
        cls.log('WARNING', message)

    @classmethod
    def error(cls, message):
        """
        Logs a message with level ERROR on this logger
        :param message: Log record content
        :type message: str
        """
        cls.log('ERROR', message)

    @classmethod
    def exception(cls, message, exception=None):
        """
        Logs an exception with level ERROR on this logger
        :param message: Log record content
        :type message: str
        :param exception: Exception instance
        :type exception: Exception
        """
        cls.log('ERROR', message, exception=exception)
