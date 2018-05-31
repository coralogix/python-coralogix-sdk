#!/usr/bin/python
# -*- coding: utf-8 -*-

from .helpers import TestCase
from coralogix.constants import Coralogix


class TestConstants(TestCase):
    def test_map_severity(self):
        self.assertEqual(Coralogix.map_severity(0), Coralogix.Severity.DEBUG)
        self.assertEqual(Coralogix.map_severity(10), Coralogix.Severity.DEBUG)
        self.assertEqual(Coralogix.map_severity(20), Coralogix.Severity.INFO)
        self.assertEqual(Coralogix.map_severity(30), Coralogix.Severity.WARNING)
        self.assertEqual(Coralogix.map_severity(40), Coralogix.Severity.ERROR)
        self.assertEqual(Coralogix.map_severity(50), Coralogix.Severity.CRITICAL)
        self.assertEqual(Coralogix.map_severity('default'), Coralogix.Severity.INFO)
        self.assertEqual(Coralogix.map_severity(13), Coralogix.Severity.INFO)
