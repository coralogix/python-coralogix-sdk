#!/usr/bin/python
# -*- coding: utf-8 -*-

from .helpers import TestCase
from coralogix.constants import Coralogix
from coralogix.manager import LoggerManager


class TestLoggerManager(TestCase):
    def test_initialize(self):
        self.assertIsNone(
            LoggerManager.initialize()
        )

    def test_configure(self):
        LoggerManager.configure(
            sync_time=False,
            privateKey=self.PRIVATE_KEY,
            applicationName=self.APP_NAME,
            subsystemName=self.SUBSYSTEM_NAME
        )
        self.assertIsInstance(LoggerManager.configured, bool)
        self.assertTrue(LoggerManager.configured)
        self.assertIsInstance(LoggerManager._sync_time, bool)
        self.assertFalse(LoggerManager._sync_time)
        self.assertIsInstance(LoggerManager._bulk_template, dict)

    def test_add_logline(self):
        self.assertIsNone(
            LoggerManager.add_logline(
                'Test message!',
                Coralogix.Severity.INFO,
                Coralogix.CORALOGIX_CATEGORY,
            )
        )

    def test_add_logline_fails(self):
        mutex_backup = LoggerManager._mutex
        LoggerManager._mutex = None

        self.assertIsNone(
            LoggerManager.add_logline(
                'Test message!',
                Coralogix.Severity.INFO,
                Coralogix.CORALOGIX_CATEGORY,
            )
        )

        LoggerManager._mutex = mutex_backup

    def test_add_logling_overflow(self):
        chunk_size = Coralogix.MAX_LOG_CHUNK_SIZE
        Coralogix.MAX_LOG_CHUNK_SIZE = 5

        self.assertIsNone(
            LoggerManager.add_logline(
                'Test message!',
                Coralogix.Severity.INFO,
                Coralogix.CORALOGIX_CATEGORY,
            )
        )

        Coralogix.MAX_LOG_CHUNK_SIZE = chunk_size

    def test_add_logline_restart_thread(self):
        LoggerManager._process = None
        self.assertIsNone(
            LoggerManager.add_logline(
                'Test message!',
                Coralogix.Severity.INFO,
                Coralogix.CORALOGIX_CATEGORY,
            )
        )

    def test_add_logline_severity(self):
        self.assertIsNone(
            LoggerManager.add_logline(
                'Test message!',
                'DEBUG',
                Coralogix.CORALOGIX_CATEGORY,
            )
        )

    def test_add_logline_default_severity(self):
        self.assertIsNone(
            LoggerManager.add_logline(
                'Test message!',
                7,
                Coralogix.CORALOGIX_CATEGORY,
            )
        )

    def test_update_time_delta_interval(self):
        self.assertIsNone(
            LoggerManager.update_time_delta_interval()
        )

    def test_internal_run(self):
        self.assertIsNone(
            LoggerManager._internal_run()
        )

    def test_msg2str(self):
        self.assertIsInstance(
            LoggerManager._msg2str('Test message'),
            str
        )

    def test_msg2str_fails(self):
        self.assertIsInstance(
            LoggerManager._msg2str(
                {'msg': -1}
            ),
            str
        )

    def test_send_bulk_with_fails(self):
        from threading import Lock
        LoggerManager._mutex = None

        with self.assertRaises(Exception):
            self.assertIsNone(
                LoggerManager._send_bulk()
            )

        LoggerManager._mutex = Lock()

    def test_send_bulk_with_time_sync(self):
        self.assertIsNone(
            LoggerManager._send_bulk(True)
        )
