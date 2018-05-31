#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Coralogix Logger handlers package
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from .coralogix import CoralogixLogger
from .debug import DebugLogger

__all__ = ['CoralogixLogger', 'DebugLogger']
