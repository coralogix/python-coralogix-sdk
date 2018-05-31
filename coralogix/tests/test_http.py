#!/usr/bin/python
# -*- coding: utf-8 -*-

from .helpers import TestCase
from coralogix.constants import Coralogix
from coralogix.http import CoralogixHTTPSender


class TestCoralogixHTTPSender(TestCase):
    def test_http_init(self):
        CoralogixHTTPSender._init(30)
        self.assertEqual(CoralogixHTTPSender._timeout, 30)

    def test_get_time_sync(self):
        result, time_delta = CoralogixHTTPSender.get_time_sync()

        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        self.assertIsInstance(time_delta, float)

    def test_get_time_sync_fails(self):
        result, time_delta = CoralogixHTTPSender.get_time_sync(
            url='https://coralogix.com/404'
        )
        self.assertIsInstance(result, bool)
        self.assertEqual(result, False)
        self.assertEqual(time_delta, 0)

    def test_get_time_sync_endpoint_not_found(self):
        self.assertIsNone(
            CoralogixHTTPSender.get_time_sync(
                url='http://not-found/'
            )
        )

    def test_send_request(self):
        import time

        _, time_delta = CoralogixHTTPSender.get_time_sync()

        self.assertIsNone(CoralogixHTTPSender.send_request({
            'privateKey': self.PRIVATE_KEY,
            'applicationName': self.APP_NAME,
            'subsystemName': self.SUBSYSTEM_NAME,
            'logEntries': [
                {
                    'text': 'Test message!',
                    'timestamp': time.time() * 1000 + time_delta,
                    'severity': 3,
                    'category': Coralogix.CORALOGIX_CATEGORY,
                },
            ],
        }))

    def test_send_request_fails(self):
        import time

        _, time_delta = CoralogixHTTPSender.get_time_sync()
        self.assertIsNone(
            CoralogixHTTPSender.send_request(
                bulk={
                    'privateKey': self.PRIVATE_KEY,
                    'applicationName': self.APP_NAME,
                    'subsystemName': self.SUBSYSTEM_NAME,
                    'logEntries': [
                        {
                            'text': 'Test message!',
                            'timestamp': time.time() * 1000 + time_delta,
                            'severity': 3,
                            'category': Coralogix.CORALOGIX_CATEGORY,
                        },
                    ],
                },
                url='http://not-found/'
            )
        )

    def test_send_request_mutex_fails(self):
        import time

        _, time_delta = CoralogixHTTPSender.get_time_sync()

        mutex_backup = CoralogixHTTPSender._mutex
        CoralogixHTTPSender._mutex = None

        self.assertIsNone(
            CoralogixHTTPSender.send_request({
                'privateKey': self.PRIVATE_KEY,
                'applicationName': self.APP_NAME,
                'subsystemName': self.SUBSYSTEM_NAME,
                'logEntries': [
                    {
                        'text': 'Test message!',
                        'timestamp': time.time() * 1000 + time_delta,
                        'severity': 3,
                        'category': Coralogix.CORALOGIX_CATEGORY,
                    },
                ],
            })
        )

        CoralogixHTTPSender._mutex = mutex_backup

    def test_get_time_sync_mutex_fails(self):
        mutex_backup = CoralogixHTTPSender._mutex
        CoralogixHTTPSender._mutex = None

        self.assertIsNone(
            CoralogixHTTPSender.get_time_sync(
                url='http://not-found/'
            )
        )

        CoralogixHTTPSender._mutex = mutex_backup
