#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from io import StringIO
from contextlib import redirect_stdout
from .helpers import TestCase
from coralogix.handlers.debug import DebugLogger


class TestDebugLogger(TestCase):
    def test_debug_mode(self):
        self.assertIsInstance(DebugLogger.debug_mode, bool)

    def test_log(self):
        log_message = 'Test message'

        f = StringIO()
        with redirect_stdout(f):
            DebugLogger.log('DEBUG', log_message)
        output = f.getvalue()

        self.assertIn(log_message, output)

    def test_debug(self):
        log_message = 'Test message'

        f = StringIO()
        with redirect_stdout(f):
            DebugLogger.debug(log_message)
        output = f.getvalue()

        self.assertIn('[DEBUG]', output)
        self.assertIn(log_message, output)

    def test_info(self):
        log_message = 'Test message'

        f = StringIO()
        with redirect_stdout(f):
            DebugLogger.info(log_message)
        output = f.getvalue()

        self.assertIn('[INFO]', output)
        self.assertIn(log_message, output)

    def test_warning(self):
        log_message = 'Test message'

        f = StringIO()
        with redirect_stdout(f):
            DebugLogger.warning(log_message)
        output = f.getvalue()

        self.assertIn('[WARNING]', output)
        self.assertIn(log_message, output)

    def test_error(self):
        log_message = 'Test message'

        f = StringIO()
        with redirect_stdout(f):
            DebugLogger.error(log_message)
        output = f.getvalue()

        self.assertIn('[ERROR]', output)
        self.assertIn(log_message, output)

    def test_exception(self):
        log_message = 'Test message'

        f = StringIO()
        with redirect_stdout(f):
            DebugLogger.exception(log_message, Exception('Test exception'))
        output = f.getvalue()

        self.assertIn('[ERROR]', output)
        self.assertIn(log_message, output)

    def test_exception_fails(self):
        f = StringIO()
        with redirect_stdout(f):
            DebugLogger.exception(34, Exception('Test exception'))
        output = f.getvalue()
        self.assertTrue(output.startswith('Failed to print log:'))
