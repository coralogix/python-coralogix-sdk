#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger Handler
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from __future__ import print_function
from logging import Handler
from threading import current_thread
from ..constants import Coralogix
from ..manager import LoggerManager
from .debug import DebugLogger


class CoralogixLogger(Handler):
    """
    Coralogix logger main class. This class send logs to Coralogix server.
    It is possible to use this class as a handler for the standard Python logger.
    """

    def __init__(self, private_key=None, app_name=None, subsystem=None,
                 category=None, sync_time=False):
        """
        Initialize Coralogix Logger
        :param private_key: Private key for Coralogix
        :type private_key: str
        :param app_name: User application name
        :type app_name: str
        :param subsystem: Name of subsystem name(frontend, backend, etc.)
        :type subsystem: str
        :param category: Log record category
        :type category: str
        :param sync_time: Synchronize time with Coralogix servers (default: False)
        :type sync_time: bool
        """
        self.configure(private_key, app_name, subsystem, sync_time)
        self._category = category if category is not None else Coralogix.CORALOGIX_CATEGORY
        Handler.__init__(self)

    @classmethod
    def set_debug_mode(cls, debug_mode=True):
        """
        Enable debug mode; prints internal log messages to stdout
        :param debug_mode: Debug Logger mode
        :type debug_mode: bool
        :return: Current Debug logger mode
        :rtype: bool
        """
        DebugLogger.debug_mode = debug_mode
        return DebugLogger.debug_mode

    def emit(self, record):
        """
        Send log record
        :param record: Log record object
        :type record: LogRecord
        """
        self.log(
            Coralogix.map_severity(record.levelno),
            self.format(record),
            record.name,
            record.module,
            record.funcName,
            record.thread
        )

    @classmethod
    def configure(cls, private_key, app_name, sub_system, sync_time=False):
        """
        Configure Coralogix logger with customer specific values
        :param private_key: Coralogix account private key
        :type private_key: str
        :param app_name: User application name
        :type app_name: str
        :param sub_system: Name of subsystem name(frontend, backend, etc.)
        :type sub_system: str
        :param sync_time: Synchronize time with Coralogix servers (default: False)
        :type sync_time: bool
        """
        if not LoggerManager.configured:
            private_key = private_key if private_key and not private_key.isspace() \
                else Coralogix.FAILED_PRIVATE_KEY
            app_name = app_name if app_name and not app_name.isspace() \
                else Coralogix.NO_APP_NAME
            sub_system = sub_system if sub_system and not sub_system.isspace() \
                else Coralogix.NO_SUB_SYSTEM

            LoggerManager.configure(
                sync_time=sync_time,
                privateKey=private_key,
                applicationName=app_name,
                subsystemName=sub_system
            )

    @classmethod
    def get_logger(cls, name=Coralogix.CORALOGIX_CATEGORY):
        """
        Return a new instance of CoralogixLogger
        :param name: Name of logger
        :type name: str
        :return: CoralogixLogger instance
        :rtype: CoralogixLogger
        """
        if LoggerManager.configured:
            return CoralogixLogger(category=name)
        else:
            raise Exception('Logger Manager is not configured!')

    def log(self, severity, message, category=None, classname='', methodname='', thread_id=''):
        """
        Logs a message on this logger
        :param severity: Log record severity(level)
        :type severity: int
        :param message: Log record content
        :type message: str
        :param category: Log record category (default: None)
        :type category: str
        :param classname: Name of class which send log (default: "")
        :type classname: str
        :param methodname: Name of class method which send log (default: "")
        :type methodname: str
        :param thread_id: ID of thread from which log was sent (default: "")
        :type thread_id: str
        """
        category = category if category else self._category
        thread_id = str(thread_id)
        thread_id = thread_id if thread_id and (not thread_id.isspace()) else current_thread().ident
        LoggerManager.add_logline(
            message,
            severity,
            category,
            className=classname,
            methodName=methodname,
            threadId=thread_id
        )

    def __getattr__(self, severity):
        """
        Send log with some severity by it name
        :param severity: Log record severity(level)
        :type severity: str
        :return: Log sending with severity procedure wrapper
        """
        severity = severity.upper()
        if hasattr(Coralogix.Severity, severity):
            def wrapper(message, category=None, classname='', methodname='', thread_id=''):
                """
                Log sending procedure wrapper
                :param message: Log record content
                :type message: str
                :param category: Log record category (default: None)
                :type category: str
                :param classname: Name of class which send log (default: "")
                :type classname: str
                :param methodname: Name of class method which send log (default: "")
                :type methodname: str
                :param thread_id: ID of thread from which log was sent (default: "")
                :type thread_id: str
                """
                self.log(
                    getattr(Coralogix.Severity, severity),
                    message,
                    category,
                    classname,
                    methodname,
                    thread_id
                )

            return wrapper
        else:
            DebugLogger.error('Invalid severity name "{0:s}"!'.format(severity.lower()))
            raise NotImplementedError('Severity name is invalid!')

    @staticmethod
    def flush_messages():
        """
        Flush logs records queue
        """
        LoggerManager.flush()
