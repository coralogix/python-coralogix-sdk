#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
from coralogix.constants import Coralogix
from coralogix.handlers.debug import DebugLogger


class TestCase(unittest.TestCase):
    def setUp(self):
        self.PRIVATE_KEY = os.environ.get('PRIVATE_KEY', Coralogix.FAILED_PRIVATE_KEY)
        self.APP_NAME = os.environ.get('APP_NAME', Coralogix.NO_APP_NAME)
        self.SUBSYSTEM_NAME = os.environ.get('SUBSYSTEM_NAME', Coralogix.NO_SUB_SYSTEM)
        DebugLogger.debug_mode = True

    def tearDown(self):
        from coralogix.manager import LoggerManager
        LoggerManager.stop()
