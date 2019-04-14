Implementation
==============

Adding `Coralogix` logging handler in your logging system:

.. code-block:: python

    import logging
    # For version 1.*
    from coralogix.coralogix_logger import CoralogixLogger
    # For version 2.*
    from coralogix.handlers import CoralogixLogger

    PRIVATE_KEY = "[YOUR_PRIVATE_KEY_HERE]"
    APP_NAME = "[YOUR_APPLICATION_NAME]"
    SUB_SYSTEM = "[YOUR_SUBSYSTEM_NAME]"

    # Get an instance of Python standard logger.
    logger = logging.getLogger("Python Logger")

    # Get a new instance of Coralogix logger.
    coralogix_handler = CoralogixLogger(PRIVATE_KEY, APP_NAME, SUB_SYSTEM)

    # Add coralogix logger as a handler to the standard Python logger.
    logger.addHandler(coralogix_handler)

    # Send message
    logger.info("Hello World!")


Also, you can configure the SDK with `dictConfig` for `Python` `logging` library:

.. code-block:: python

    import logging

    PRIVATE_KEY = '[YOUR_PRIVATE_KEY_HERE]'
    APP_NAME = '[YOUR_APPLICATION_NAME]'
    SUB_SYSTEM = '[YOUR_SUBSYSTEM_NAME]'

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s]: %(levelname)s: %(message)s',
            }
        },
        'handlers': {
            'coralogix': {
                'class': 'coralogix.handlers.CoralogixLogger',
                'level': 'DEBUG',
                'formatter': 'default',
                'private_key': PRIVATE_KEY,
                'app_name': APP_NAME,
                'subsystem': SUB_SYSTEM,
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': [
                'coralogix',
            ]
        },
        'loggers': {
            'backend': {
                'level': 'DEBUG',
                'handlers': [
                    'coralogix',
                ]
            }
        }
    })
