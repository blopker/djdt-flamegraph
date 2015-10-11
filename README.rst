
===============================
DjDT Flame Graph
===============================

.. image:: https://raw.githubusercontent.com/23andMe/djdt-flamegraph/master/fireman.png

Get a flame graph of the current request, right in Django.

.. image:: https://travis-ci.org/23andMe/djdt-flamegraph.svg?branch=master
        :target: https://travis-ci.org/23andMe/djdt-flamegraph

.. image:: https://img.shields.io/pypi/v/djdt_flamegraph.svg
        :target: https://pypi.python.org/pypi/djdt_flamegraph

Screenshot
----------

.. image:: https://raw.githubusercontent.com/23andMe/djdt-flamegraph/master/flamegraph-screenshot.png

Features
--------

* Uses https://github.com/brendangregg/FlameGraph to generate a flamegraph right in the debug panel.

Install
-------
* Add ``djdt_flamegraph`` to your ``requirements.txt``.
* Add ``djdt_flamegraph.FlamegraphPanel`` to ``DEBUG_TOOLBAR_PANELS``.
* Run your server with ``python manage.py runserver --nothreading --noreload``

Notes
-----
* ``ValueError at /: signal only works in main thread``: Flame graphs can only be generated in a single threaded server.
* Flame graphs are disabled by default. You'll have to enable it by clicking the checkbox next to it in the Debug Toolbar.
* Probably won't work on Windows.

Development
-----------
This panel comes with an example Django app to test with. Just run ``make example`` and the server should start running.
