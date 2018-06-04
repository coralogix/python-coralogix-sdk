Django
======

To enable `Django` logging to `Coralogix` you'll need to add the following lines to your **settings.py**:

.. code-block:: python

    ...

    LOGGING = {
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
                'subsystem': '[YOUR_SUBSYTEM_NAME]',
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
    }