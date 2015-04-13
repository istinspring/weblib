.. weblib documentation master file, created by
   sphinx-quickstart on Sun Apr 12 13:12:18 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to weblib's documentation!
==================================

Weblib provides tools to solve typical tasks in web scraping:

* processing HTML
* handling text encodings
* controling repeating and parallel tasks
* parsing RSS/ATOM feeds
* preparing data for HTTP requests
* working with DOM tree
* working with text and numeral data
* list of common user agents
* cross-platform file locking
* operations with files and directories

Installation
============

.. code:: bash

    pip install -U weblib


Testing
=======

Install tox package: `pip install tox`
Run the command: `tox`


API
===

.. toctree::
    :maxdepth: 2

    api/content
    api/control
    api/debug
    api/encoding
    api/feed
    api/files
    api/html
    api/http
    api/lock
    api/logs
    api/etree
    api/metric
    api/parser
    api/progress
    api/pwork
    api/rex
    api/russian
    api/system
    api/text
    api/user_agent
    api/watch
    api/work


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
