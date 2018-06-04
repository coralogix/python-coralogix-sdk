#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger default constants
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from .handlers.debug import DebugLogger

DebugLogger.debug_mode = True
DebugLogger.warning(
    'Import from "coralogix.coralogix_logger" is deprecated '
    'and will be removed in future versions! Please use "coralogix.handlers" instead.'
)

from .handlers.coralogix import CoralogixLogger
