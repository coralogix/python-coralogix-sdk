Coralogix Python SDK
====================

.. image:: https://img.shields.io/pypi/v/coralogix_logger.svg
    :target: https://pypi.python.org/pypi/coralogix_logger

.. image:: https://img.shields.io/pypi/l/coralogix_logger.svg
    :target: https://raw.githubusercontent.com/coralogix/python-coralogix-sdk/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/coralogix_logger.svg
    :target: https://pypi.python.org/pypi/coralogix_logger

.. image:: https://img.shields.io/pypi/wheel/coralogix_logger.svg
    :target: https://pypi.python.org/pypi/coralogix_logger

.. image:: https://img.shields.io/pypi/status/coralogix_logger.svg
    :target: https://pypi.python.org/pypi/coralogix_logger

.. image:: https://travis-ci.org/coralogix/python-coralogix-sdk.svg?branch=master
    :target: https://travis-ci.org/coralogix/python-coralogix-sdk

.. image:: https://readthedocs.org/projects/python-coralogix-sdk/badge/?version=latest
    :target: https://python-coralogix-sdk.readthedocs.io/en/latest/

.. image:: https://codecov.io/gh/coralogix/python-coralogix-sdk/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/coralogix/python-coralogix-sdk

.. image:: https://api.codeclimate.com/v1/badges/474f12c23edee33936b9/maintainability
   :target: https://codeclimate.com/github/coralogix/python-coralogix-sdk/maintainability

.. image:: https://api.codeclimate.com/v1/badges/474f12c23edee33936b9/test_coverage
   :target: https://codeclimate.com/github/coralogix/python-coralogix-sdk/test_coverage

.. image:: https://img.shields.io/github/issues/coralogix/python-coralogix-sdk.svg
    :target: https://github.com/coralogix/python-coralogix-sdk

.. image:: https://img.shields.io/github/issues-pr/coralogix/python-coralogix-sdk.svg
    :target: https://github.com/coralogix/python-coralogix-sdk

.. image:: https://img.shields.io/github/contributors/coralogix/python-coralogix-sdk.svg
    :target: https://github.com/coralogix/python-coralogix-sdk/graphs/contributors

This package provides logging suites integrated with `Coralogix` logs analytics platform.
To see how to use it, please read `Coralogix Python SDK Docs <https://coralogix.com/docs/integrations/sdks/python-sdk/>`_.

Region Selection
================

The SDK requires a Coralogix region to be specified. You can specify the region in two ways:

1. **Environment Variable**: Set the ``CORALOGIX_REGION`` environment variable to one of the supported regions.

2. **Code Parameter**: Pass the ``region`` parameter when initializing the logger.

**Note**: The region is mandatory. If no region is provided (neither as a parameter nor via environment variable), the SDK will raise a ``ValueError``.

Supported regions:
- **AP1** - Mumbai (AWS: ap-south-1)
- **AP2** - Singapore (AWS: ap-southeast-1)
- **AP3** - Jakarta (AWS: ap-southeast-3)
- **EU1** - Ireland (AWS: eu-west-1)
- **EU2** - Stockholm (AWS: eu-north-1)
- **US1** - Ohio (AWS: us-east-2)
- **US2** - N. Virginia (AWS: us-east-1)

Example usage:

.. code-block:: python

    from coralogix.handlers import CoralogixLogger

    # Using region parameter
    logger = CoralogixLogger(
        private_key="YOUR_PRIVATE_KEY",
        app_name="MyApp",
        subsystem="backend",
        region="EU1"
    )

    # Or set via environment variable
    # export CORALOGIX_REGION=EU1
