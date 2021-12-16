sec-cik-mapper
==============

.. image:: https://github.com/jadchaar/sec-cik-mapper/actions/workflows/continuous_integration.yml/badge.svg
    :alt: Tests
    :target: https://github.com/jadchaar/sec-cik-mapper/actions/workflows/continuous_integration.yml

.. image:: https://github.com/jadchaar/cik-mapper/actions/workflows/update_mappings_daily_cron_job.yml/badge.svg?event=schedule
    :alt: Update Mappings Daily CRON Job
    :target: https://github.com/jadchaar/sec-cik-mapper/actions/workflows/update_mappings_daily_cron_job.yml

.. image:: https://codecov.io/gh/jadchaar/sec-cik-mapper/branch/main/graph/badge.svg
    :alt: Coverage Status
    :target: https://codecov.io/gh/jadchaar/sec-cik-mapper

.. image:: https://img.shields.io/pypi/v/sec-cik-mapper.svg
    :alt: PyPI Version
    :target: https://python.org/pypi/sec-cik-mapper

.. image:: https://img.shields.io/pypi/pyversions/sec-cik-mapper.svg
    :alt: Supported Python Versions
    :target: https://python.org/pypi/sec-cik-mapper

.. image:: https://img.shields.io/pypi/l/sec-cik-mapper.svg
    :alt: License
    :target: https://python.org/pypi/sec-cik-mapper

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style: Black
    :target: https://github.com/python/black

Quick Start
-----------

Installation
^^^^^^^^^^^^

Install and update this package using `pip <https://pip.pypa.io/en/stable/quickstart/>`_:

.. code-block:: console

    $ pip install -U sec-cik-mapper

Basic Usage
^^^^^^^^^^^

.. code-block:: python

    >>> from sec_cik_mapper import CIKMapper
    >>> from pathlib import Path

    # Initialize a CIK mapper instance
    >>> cikMapper = CIKMapper()

    # Save full CIK, ticker, and company name mapping to a CSV file
    >>> csv_path = Path("cik_mapping.csv")
    >>> cikMapper.save_metadata_to_csv(csv_path)

    # Get a dictionary mapping CIK to a list of tickers
    >>> cikMapper.get_cik_to_ticker_mapping()
    {'0000320193': ['AAPL'], '0000789019': ['MSFT'], '0001652044': ['GOOG', 'GOOGL'], '0001018724': ['AMZN'], '0001326801': ['FB'], '0001318605': ['TSLA'], '0000040545': ['GE'], '0001067983': ['BRK-A', 'BRK-B'], '0001046179': ['TSM'], '0000019617': ['JPM', 'JPM-PC', 'JPM-PD', 'JPM-PJ', 'JPM-PK', 'JPM-PL', 'JPM-PM', 'AMJ'], ...}

    # Get a dictionary mapping ticker to CIK
    >>> cikMapper.get_ticker_to_cik_mapping()
    {'AAPL': '0000320193', 'MSFT': '0000789019', 'GOOG': '0001652044', 'AMZN': '0001018724', 'FB': '0001326801', 'TSLA': '0001318605', 'GE': '0000040545', 'BRK-A': '0001067983', 'TSM': '0001046179', 'JPM': '0000019617', ...}

    # Get a dictionary mapping CIK to company name
    >>> cikMapper.get_cik_to_company_name_mapping()
    {'0000320193': 'Apple Inc.', '0000789019': 'Microsoft Corp', '0001652044': 'Alphabet Inc.', '0001018724': 'Amazon Com Inc', '0001326801': 'Meta Platforms, Inc.', '0001318605': 'Tesla, Inc.', '0000040545': 'General Electric Co', '0001067983': 'Berkshire Hathaway Inc', '0001046179': 'Taiwan Semiconductor Manufacturing Co Ltd', '0000019617': 'Jpmorgan Chase & Co', ...}

    # Get a dictionary mapping ticker to company name
    >>> cikMapper.get_ticker_to_company_name_mapping()
    {'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corp', 'GOOG': 'Alphabet Inc.', 'AMZN': 'Amazon Com Inc', 'FB': 'Meta Platforms, Inc.', 'TSLA': 'Tesla, Inc.', 'GE': 'General Electric Co', 'BRK-A': 'Berkshire Hathaway Inc', 'TSM': 'Taiwan Semiconductor Manufacturing Co Ltd', 'JPM': 'Jpmorgan Chase & Co', ...}

CIK, Ticker, and Company Name Mappings
--------------------------------------

CIK, ticker, and company name mappings are also available for download (e.g. manually or via automated
scripts/CURL requests) from the following URL: https://github.com/jadchaar/sec-cik-mapper/tree/main/auto_generated_mappings.
The mapping files are updated daily via an `automated CRON job <https://github.com/jadchaar/sec-cik-mapper/actions/workflows/update_mappings_daily_cron_job.yml>`_,
which fetches, processes, and uploads the latest mapping data from the SEC.

The mapping files are broken down as follows:

* `cik_mapping.csv <https://github.com/jadchaar/sec-cik-mapper/blob/main/auto_generated_mappings/cik_mapping.csv>`_
    * CSV file containing the following columns: CIK, Ticker, and Company Name
* `cik_to_company_name.json <https://github.com/jadchaar/sec-cik-mapper/blob/main/auto_generated_mappings/cik_to_company_name.json>`_
    * JSON file mapping CIK to company name
* `cik_to_ticker.json <https://github.com/jadchaar/sec-cik-mapper/blob/main/auto_generated_mappings/cik_to_ticker.json>`_
    * JSON file mapping CIK to ticker
* `ticker_to_cik.json <https://github.com/jadchaar/sec-cik-mapper/blob/main/auto_generated_mappings/ticker_to_cik.json>`_
    * JSON file mapping ticker to CIK
* `ticker_to_company_name.json <https://github.com/jadchaar/sec-cik-mapper/blob/main/auto_generated_mappings/ticker_to_company_name.json>`_
    * JSON file mapping ticker to company name

Contributing
------------

If you encounter a bug or would like to see a new company filing or feature added to **sec-cik-mapper**, please `file an issue <https://github.com/jadchaar/sec-cik-mapper/issues>`_ or `submit a pull request <https://help.github.com/en/articles/creating-a-pull-request>`_.

Documentation
-------------

For full documentation, please visit `sec-cik-mapper.readthedocs.io <https://sec-cik-mapper.readthedocs.io>`_.
