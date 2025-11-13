#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
from .helpers import TestCase
from coralogix.constants import Coralogix
from coralogix.handlers.coralogix import CoralogixLogger
from coralogix.manager import LoggerManager


class TestRegion(TestCase):
    def setUp(self):
        super(TestRegion, self).setUp()
        # Reset LoggerManager state
        LoggerManager.configured = False
        LoggerManager._region = None
        # Clear environment variable to test parameter passing
        if 'CORALOGIX_REGION' in os.environ:
            self._old_region = os.environ.pop('CORALOGIX_REGION')
        else:
            self._old_region = None

    def tearDown(self):
        # Restore environment variable
        if self._old_region:
            os.environ['CORALOGIX_REGION'] = self._old_region
        super(TestRegion, self).tearDown()

    def test_get_log_url_with_region(self):
        """Test that get_log_url returns correct URL for each region"""
        test_cases = [
            ('AP1', 'https://ingress.ap1.coralogix.com/logs/v1/singles'),
            ('AP2', 'https://ingress.ap2.coralogix.com/logs/v1/singles'),
            ('AP3', 'https://ingress.ap3.coralogix.com/logs/v1/singles'),
            ('EU1', 'https://ingress.eu1.coralogix.com/logs/v1/singles'),
            ('EU2', 'https://ingress.eu2.coralogix.com/logs/v1/singles'),
            ('US1', 'https://ingress.us1.coralogix.com/logs/v1/singles'),
            ('US2', 'https://ingress.us2.coralogix.com/logs/v1/singles'),
        ]
        
        for region, expected_url in test_cases:
            with self.subTest(region=region):
                url = Coralogix.get_log_url(region)
                self.assertEqual(url, expected_url)

    def test_get_time_delta_url_with_region(self):
        """Test that get_time_delta_url returns correct URL for each region"""
        test_cases = [
            ('AP1', 'https://ingress.ap1.coralogix.com/sdk/v1/time'),
            ('AP2', 'https://ingress.ap2.coralogix.com/sdk/v1/time'),
            ('AP3', 'https://ingress.ap3.coralogix.com/sdk/v1/time'),
            ('EU1', 'https://ingress.eu1.coralogix.com/sdk/v1/time'),
            ('EU2', 'https://ingress.eu2.coralogix.com/sdk/v1/time'),
            ('US1', 'https://ingress.us1.coralogix.com/sdk/v1/time'),
            ('US2', 'https://ingress.us2.coralogix.com/sdk/v1/time'),
        ]
        
        for region, expected_url in test_cases:
            with self.subTest(region=region):
                url = Coralogix.get_time_delta_url(region)
                self.assertEqual(url, expected_url)

    def test_get_log_url_without_region_raises_error(self):
        """Test that get_log_url raises ValueError when region is not provided"""
        with self.assertRaises(ValueError) as context:
            Coralogix.get_log_url(None)
        
        self.assertIn('CORALOGIX_REGION is mandatory', str(context.exception))

    def test_get_time_delta_url_without_region_raises_error(self):
        """Test that get_time_delta_url raises ValueError when region is not provided"""
        with self.assertRaises(ValueError) as context:
            Coralogix.get_time_delta_url(None)
        
        self.assertIn('CORALOGIX_REGION is mandatory', str(context.exception))

    def test_get_log_url_with_invalid_region_raises_error(self):
        """Test that get_log_url raises ValueError for invalid region"""
        with self.assertRaises(ValueError) as context:
            Coralogix.get_log_url('INVALID')
        
        self.assertIn('Invalid region', str(context.exception))

    def test_get_time_delta_url_with_invalid_region_raises_error(self):
        """Test that get_time_delta_url raises ValueError for invalid region"""
        with self.assertRaises(ValueError) as context:
            Coralogix.get_time_delta_url('INVALID')
        
        self.assertIn('Invalid region', str(context.exception))

    def test_get_log_url_with_environment_variable(self):
        """Test that get_log_url uses CORALOGIX_REGION environment variable"""
        os.environ['CORALOGIX_REGION'] = 'US1'
        url = Coralogix.get_log_url(None)
        self.assertEqual(url, 'https://ingress.us1.coralogix.com/logs/v1/singles')

    def test_get_time_delta_url_with_environment_variable(self):
        """Test that get_time_delta_url uses CORALOGIX_REGION environment variable"""
        os.environ['CORALOGIX_REGION'] = 'US1'
        url = Coralogix.get_time_delta_url(None)
        self.assertEqual(url, 'https://ingress.us1.coralogix.com/sdk/v1/time')

    def test_get_log_url_parameter_overrides_environment(self):
        """Test that region parameter takes precedence over environment variable"""
        os.environ['CORALOGIX_REGION'] = 'US1'
        url = Coralogix.get_log_url('EU1')
        self.assertEqual(url, 'https://ingress.eu1.coralogix.com/logs/v1/singles')

    def test_get_time_delta_url_parameter_overrides_environment(self):
        """Test that region parameter takes precedence over environment variable"""
        os.environ['CORALOGIX_REGION'] = 'US1'
        url = Coralogix.get_time_delta_url('EU1')
        self.assertEqual(url, 'https://ingress.eu1.coralogix.com/sdk/v1/time')

    def test_logger_with_region_parameter(self):
        """Test that CoralogixLogger accepts region parameter"""
        logger = CoralogixLogger(
            private_key=self.PRIVATE_KEY,
            app_name=self.APP_NAME,
            subsystem=self.SUBSYSTEM_NAME,
            region='AP1'
        )
        self.assertIsNotNone(logger)
        self.assertEqual(LoggerManager._region, 'AP1')

    def test_logger_with_environment_region(self):
        """Test that CoralogixLogger uses CORALOGIX_REGION environment variable"""
        os.environ['CORALOGIX_REGION'] = 'EU2'
        logger = CoralogixLogger(
            private_key=self.PRIVATE_KEY,
            app_name=self.APP_NAME,
            subsystem=self.SUBSYSTEM_NAME
        )
        self.assertIsNotNone(logger)
        self.assertEqual(LoggerManager._region, 'EU2')

    def test_logger_region_case_insensitive(self):
        """Test that region is case-insensitive"""
        logger = CoralogixLogger(
            private_key=self.PRIVATE_KEY,
            app_name=self.APP_NAME,
            subsystem=self.SUBSYSTEM_NAME,
            region='eu1'  # lowercase
        )
        self.assertIsNotNone(logger)
        self.assertEqual(LoggerManager._region, 'EU1')  # Should be uppercase

    def test_manager_configure_with_region(self):
        """Test that LoggerManager.configure stores region"""
        LoggerManager.configure(
            sync_time=False,
            privateKey=self.PRIVATE_KEY,
            applicationName=self.APP_NAME,
            subsystemName=self.SUBSYSTEM_NAME,
            region='US2'
        )
        self.assertEqual(LoggerManager._region, 'US2')

    def test_manager_configure_with_environment_region(self):
        """Test that LoggerManager.configure uses environment variable if region not provided"""
        os.environ['CORALOGIX_REGION'] = 'AP2'
        LoggerManager.configure(
            sync_time=False,
            privateKey=self.PRIVATE_KEY,
            applicationName=self.APP_NAME,
            subsystemName=self.SUBSYSTEM_NAME
        )
        self.assertEqual(LoggerManager._region, 'AP2')

    def test_all_regions_supported(self):
        """Test that all expected regions are in REGIONS dictionary"""
        expected_regions = {'AP1', 'AP2', 'AP3', 'EU1', 'EU2', 'US1', 'US2'}
        self.assertEqual(set(Coralogix.REGIONS.keys()), expected_regions)

