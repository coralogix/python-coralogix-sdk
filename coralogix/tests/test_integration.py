#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import unittest
from .helpers import TestCase
from coralogix.constants import Coralogix
from coralogix.handlers.coralogix import CoralogixLogger
from coralogix.manager import LoggerManager


class TestIntegration(TestCase):
    """
    Integration tests that send actual HTTP requests to Coralogix.
    
    These tests require valid credentials:
    - PRIVATE_KEY: Your Coralogix private key
    - APP_NAME: Application name
    - SUBSYSTEM_NAME: Subsystem name
    - CORALOGIX_REGION: Region (defaults to EU2)
    """
    
    def setUp(self):
        super(TestIntegration, self).setUp()
        # Reset LoggerManager state
        LoggerManager.configured = False
        LoggerManager._region = None
        # Use provided credentials from environment variables only
        self.test_private_key = os.environ.get('PRIVATE_KEY')
        self.test_app_name = os.environ.get('APP_NAME', 'staging')
        self.test_subsystem = os.environ.get('SUBSYSTEM_NAME', 'coralogix-python-sdk')
        self.test_region = os.environ.get('CORALOGIX_REGION', 'EU2')
        
        # Skip tests if PRIVATE_KEY is not provided
        if not self.test_private_key:
            self.skipTest("PRIVATE_KEY environment variable is required for integration tests")

    def tearDown(self):
        # Flush any remaining logs
        LoggerManager.flush()
        super(TestIntegration, self).tearDown()

    def test_send_log_to_eu2(self):
        """Test sending a log message to EU2 region"""
        logger = CoralogixLogger(
            private_key=self.test_private_key,
            app_name=self.test_app_name,
            subsystem=self.test_subsystem,
            region=self.test_region
        )
        
        # Verify region is set correctly
        self.assertEqual(LoggerManager._region, self.test_region.upper())
        
        # Send a test log message with verification text
        test_message = f'Python SDK logs test is successful - Integration test message - {time.time()}'
        logger.info(test_message)
        
        # Debug: Check what's in the buffer before sending
        import json
        if LoggerManager._buffer:
            print(f"\nDebug: Buffer contains {len(LoggerManager._buffer)} entries")
            for i, entry in enumerate(LoggerManager._buffer):
                entry_text = entry.get('text', 'MISSING')
                print(f"Entry {i}: text='{entry_text}', severity={entry.get('severity')}, category={entry.get('category')}")
                # Verify the test message is in the buffer
                if 'Python SDK logs test is successful' in entry_text:
                    print(f"✓ Verification message found in entry {i}")
        
        # Flush to send immediately
        logger.flush_messages()
        
        # Give it a moment to send
        time.sleep(1)
        
        # If we get here without exception, the request was sent
        # (We can't easily verify the response without mocking, but we can verify no errors)
        self.assertTrue(LoggerManager.configured)

    def test_send_logs_different_severities(self):
        """Test sending logs with different severity levels"""
        logger = CoralogixLogger(
            private_key=self.test_private_key,
            app_name=self.test_app_name,
            subsystem=self.test_subsystem,
            region=self.test_region
        )
        
        timestamp = time.time()
        
        # Send logs with different severities
        logger.debug(f'Debug message - {timestamp}')
        logger.info(f'Info message - {timestamp}')
        logger.warning(f'Warning message - {timestamp}')
        logger.error(f'Error message - {timestamp}')
        logger.critical(f'Critical message - {timestamp}')
        
        # Flush to send immediately
        logger.flush_messages()
        
        # Give it a moment to send
        time.sleep(1)
        
        self.assertTrue(LoggerManager.configured)

    def test_send_multiple_logs(self):
        """Test sending multiple log messages in a batch"""
        logger = CoralogixLogger(
            private_key=self.test_private_key,
            app_name=self.test_app_name,
            subsystem=self.test_subsystem,
            region=self.test_region
        )
        
        timestamp = time.time()
        
        # Send multiple messages
        for i in range(5):
            logger.info(f'Batch message {i+1} - {timestamp}')
        
        # Flush to send immediately
        logger.flush_messages()
        
        # Give it a moment to send
        time.sleep(1)
        
        self.assertTrue(LoggerManager.configured)

    def test_verify_eu2_url(self):
        """Test that EU2 region generates correct URLs"""
        log_url = Coralogix.get_log_url('EU2')
        time_url = Coralogix.get_time_delta_url('EU2')
        
        self.assertEqual(log_url, 'https://ingress.eu2.coralogix.com/logs/v1/singles')
        self.assertEqual(time_url, 'https://ingress.eu2.coralogix.com/sdk/v1/time')

    def test_time_sync_eu2(self):
        """Test time sync endpoint for EU2 region"""
        from coralogix.http import CoralogixHTTPSender
        
        time_url = Coralogix.get_time_delta_url('EU2')
        self.assertEqual(time_url, 'https://ingress.eu2.coralogix.com/sdk/v1/time')
        
        # Test time sync
        result, time_delta = CoralogixHTTPSender.get_time_sync(url=time_url)
        
        self.assertTrue(result, "Time sync should succeed")
        self.assertIsInstance(time_delta, (int, float), "Time delta should be a number")
        print(f"Time sync successful. Time delta: {time_delta} ms")

    def test_time_sync_with_logger(self):
        """Test time sync when using logger with sync_time enabled"""
        logger = CoralogixLogger(
            private_key=self.test_private_key,
            app_name=self.test_app_name,
            subsystem=self.test_subsystem,
            region=self.test_region,
            sync_time=True
        )
        
        # Verify region is set
        self.assertEqual(LoggerManager._region, self.test_region.upper())
        
        # Send a log - this should trigger time sync
        timestamp = time.time()
        logger.info(f'Time sync test - {timestamp}')
        
        # Manually trigger time sync to test it
        LoggerManager.update_time_delta_interval()
        
        # Flush to send
        logger.flush_messages()
        time.sleep(1)
        
        self.assertTrue(LoggerManager.configured)

    def test_send_log_with_custom_category(self):
        """Test sending a log with a custom category"""
        logger = CoralogixLogger(
            private_key=self.test_private_key,
            app_name=self.test_app_name,
            subsystem=self.test_subsystem,
            region=self.test_region,
            category='integration-test'
        )
        
        timestamp = time.time()
        logger.info(f'Custom category test - {timestamp}', category='integration-test')
        
        # Flush to send immediately
        logger.flush_messages()
        
        # Give it a moment to send
        time.sleep(1)
        
        self.assertTrue(LoggerManager.configured)

    def test_environment_variable_region(self):
        """Test that environment variable CORALOGIX_REGION is used"""
        # Set environment variable
        original_region = os.environ.get('CORALOGIX_REGION')
        os.environ['CORALOGIX_REGION'] = 'EU2'
        
        try:
            logger = CoralogixLogger(
                private_key=self.test_private_key,
                app_name=self.test_app_name,
                subsystem=self.test_subsystem
                # No region parameter - should use environment variable
            )
            
            self.assertEqual(LoggerManager._region, 'EU2')
            
            timestamp = time.time()
            logger.info(f'Environment variable test - {timestamp}')
            logger.flush_messages()
            time.sleep(1)
            
            self.assertTrue(LoggerManager.configured)
        finally:
            # Restore original value
            if original_region:
                os.environ['CORALOGIX_REGION'] = original_region
            elif 'CORALOGIX_REGION' in os.environ:
                del os.environ['CORALOGIX_REGION']

