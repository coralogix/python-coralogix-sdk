#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from .helpers import TestCase
from coralogix.constants import Coralogix
from coralogix.handlers.coralogix import CoralogixLogger


class TestCoralogixLogger(TestCase):
    def create_logger(self):
        return CoralogixLogger(
            private_key=self.PRIVATE_KEY,
            app_name=self.APP_NAME,
            subsystem=self.SUBSYSTEM_NAME
        )

    def test_set_debug_mode(self):
        self.assertTrue(CoralogixLogger.set_debug_mode(debug_mode=True))
        self.assertFalse(CoralogixLogger.set_debug_mode(debug_mode=False))

    def test_get_logger(self):
        self.assertIsInstance(
            CoralogixLogger.get_logger(),
            CoralogixLogger
        )

    def test_get_logger_fault(self):
        from coralogix.manager import LoggerManager
        LoggerManager.configured = False
        with self.assertRaises(Exception):
            CoralogixLogger.get_logger()

    def test_log(self):
        self.assertIsNone(
            self.create_logger().log(
                Coralogix.Severity.INFO,
                'Test message!'
            )
        )

    def test_log_by_severity(self):
        self.assertIsNone(
            self.create_logger().__getattr__('debug')(
                Coralogix.Severity.DEBUG,
                'Test message!'
            )
        )

    def test_fault_log_severity(self):
        with self.assertRaises(NotImplementedError):
            self.create_logger().__getattr__('invalid')(
                Coralogix.Severity.DEBUG,
                'Test message!'
            )

    def test_flush_message(self):
        self.assertIsNone(
            self.create_logger().flush_messages()
        )

    def test_emit(self):
        from logging import LogRecord, DEBUG
        self.assertIsNone(
            self.create_logger().emit(
                LogRecord(
                    'log',
                    DEBUG,
                    15,
                    'no path',
                    'Test message',
                    [],
                    None
                )
            )
        )
