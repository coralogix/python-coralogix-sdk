Flask
=====

To enable `Flask` logging to `Coralogix` you can use the following code template:

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from logging.config import dictConfig
    from flask import Flask

    dictConfig({
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
                'private_key': '[YOUR_PRIVATE_KEY_HERE]',
                'app_name': '[YOUR_APPLICATION_NAME]',
                'subsystem': '[YOUR_SUBSYSTEM_NAME]',
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

    app = Flask(__name__)

    ...
