Configuration under uWSGI
=========================

By default `uWSGI` does not enable threading support within the Python interpreter core. This means it is not possible to create background threads from `Python` code. As the Coralogix logger relies on being able to create background threads (for sending logs), this option is required.

You can enable threading either by passing **--enable-threads** to uWSGI command line:

.. code-block:: bash

    $ uwsgi wsgi.ini --enable-threads

Another option is to enable threads in your wsgi.ini file:

**wsgi.ini:**

.. code-block:: python

    ...
    enable-threads = true
    ...