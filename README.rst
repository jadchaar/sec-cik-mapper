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

**sec-cik-mapper** is a Python package for generating mappings between stock and mutual fund identifier data provided by the SEC.

Features
--------

- Generate up-to-date mappings from the SEC as native Python dictionaries
- Mappings for both stocks and mutual funds
- Mapping data exposed as a raw pandas dataframe for custom data processing and usage
- Full support for PEP 484-style type hints and the `mypy type checker <https://mypy.readthedocs.io/en/stable/>`_
- `Pre-generated mappings <https://github.com/jadchaar/sec-cik-mapper/tree/main/mappings>`_, updated daily, available from GitHub and jsDelivr for use outside of Python
- Support for Python 3.6+

Supported Mappings
^^^^^^^^^^^^^^^^^^

Mappings can be formed between the following SEC identifiers and metadata:

+-----------+-----------------+-----------------+----------------------+
|    Key    |      Value      | ``StockMapper`` | ``MutualFundMapper`` |
+===========+=================+=================+======================+
| CIK       | Set(Tickers)    | ✅              | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| CIK       | Company Name    | ✅              |                      |
+-----------+-----------------+-----------------+----------------------+
| CIK       | Exchange        | ✅              |                      |
+-----------+-----------------+-----------------+----------------------+
| Exchange  | Set(CIKs)       | ✅              |                      |
+-----------+-----------------+-----------------+----------------------+
| Exchange  | Set(Tickers)    | ✅              |                      |
+-----------+-----------------+-----------------+----------------------+
| Ticker    | CIK             | ✅              | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Ticker    | Company Name    | ✅              |                      |
+-----------+-----------------+-----------------+----------------------+
| Ticker    | Exchange        | ✅              |                      |
+-----------+-----------------+-----------------+----------------------+
| CIK       | Set(Series IDs) |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| CIK       | Set(Class IDs)  |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Class ID  | CIK             |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Class ID  | Ticker          |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Series ID | CIK             |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Series ID | Set(Class IDs)  |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Series ID | Set(Tickers)    |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Ticker    | Class ID        |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+
| Ticker    | Series ID       |                 | ✅                   |
+-----------+-----------------+-----------------+----------------------+

Quick Start
-----------

Installation
^^^^^^^^^^^^

Install and update this package using `pip <https://pip.pypa.io/en/stable/getting-started/>`_:

.. code-block:: console

    $ pip install -U sec-cik-mapper

Basic Usage
^^^^^^^^^^^

**Stocks**

.. code-block:: python

    >>> from sec_cik_mapper import StockMapper
    >>> from pathlib import Path

    # Initialize a stock mapper instance
    >>> mapper = StockMapper()

    # Get mapping from CIK to tickers
    >>> mapper.cik_to_tickers
    {'0000320193': {'AAPL'}, '0000789019': {'MSFT'}, '0001652044': {'GOOG', 'GOOGL'}, ...}

    # Get mapping from ticker to CIK
    >>> mapper.ticker_to_cik
    {'AAPL': '0000320193', 'MSFT': '0000789019', 'GOOG': '0001652044', ...}

    # Get mapping from CIK to company name
    >>> mapper.cik_to_company_name
    {'0000320193': 'Apple Inc.', '0000789019': 'Microsoft Corp', '0001652044': 'Alphabet Inc.', ...}

    # Get mapping from ticker to company name
    >>> mapper.ticker_to_company_name
    {'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corp', 'GOOG': 'Alphabet Inc.', ...}

    # Get mapping from ticker to exchange
    >>> mapper.ticker_to_exchange
    {'AAPL': 'Nasdaq', 'MSFT': 'Nasdaq', 'GOOG': 'Nasdaq', ...}

    # Get mapping from exchange to tickers
    >>> mapper.exchange_to_tickers
    {'Nasdaq': {'CYRN', 'OHPAW', 'SANW', ...}, 'NYSE': {'PLAG', 'TDW-WTB', 'RS', ...}, 'OTC': {'ZICX', 'LTGJ', 'AVNI', ...}, ...}

    # Get mapping from CIK to exchange
    >>> mapper.cik_to_exchange
    {'0000320193': 'Nasdaq', '0000789019': 'Nasdaq', '0001652044': 'Nasdaq', ...}

    # Get mapping from exchange to CIKs
    >>> mapper.exchange_to_ciks
    {'Nasdaq': {'0000779544', '0001508171', '0001060955', ...}, 'NYSE': {'0000764478', '0000008818', '0001725057', ...}, 'OTC': {'0001044676', '0001592411', '0001284452', ...}, ...}

    # Save CIK, ticker, exchange, and company name mappings to a CSV file
    >>> csv_path = Path("example_mappings.csv")
    >>> mapper.save_metadata_to_csv(csv_path)

    # Get raw pandas dataframe
    >>> mapper.raw_dataframe
                  CIK  Ticker                                  Name Exchange
    0      0000320193    AAPL                            Apple Inc.   Nasdaq
    1      0000789019    MSFT                        Microsoft Corp   Nasdaq
    2      0001652044    GOOG                         Alphabet Inc.   Nasdaq
    3      0001018724    AMZN                        Amazon Com Inc   Nasdaq
    4      0001318605    TSLA                           Tesla, Inc.   Nasdaq
    ...           ...     ...                                   ...      ...
    13184  0001866816   OLITU             Omnilit Acquisition Corp.   Nasdaq
    13185  0001870778   OHAAU               Opy Acquisition Corp. I   Nasdaq
    13186  0001873324   PEPLW    Pepperlime Health Acquisition Corp   Nasdaq
    13187  0001877557  WEL-UN  Integrated Wellness Acquisition Corp     NYSE
    13188  0001877787  ZGN-WT   Ermenegildo Zegna Holditalia S.P.A.     NYSE

    [13189 rows x 4 columns]

**Mutual Funds**

.. code-block:: python

    >>> from sec_cik_mapper import MutualFundMapper
    >>> from pathlib import Path

    # Initialize a mutual fund mapper instance
    >>> mapper = MutualFundMapper()

    # Get mapping from CIK to tickers
    >>> mapper.cik_to_tickers
    {'0000002110': {'CRBYX', 'CEFZX', 'CSSRX', ...}, '0000002646': {'IIBPX', 'IPISX', 'IIBTX', ...}, '0000002663': {'IMSXX', 'VMTXX', 'IVMXX', ...}, ...}

    # Get mapping from ticker to CIK
    >>> mapper.ticker_to_cik
    {'LACAX': '0000002110', 'LIACX': '0000002110', 'ACRNX': '0000002110', ...}

    # Get mapping from CIK to series ID
    >>> mapper.cik_to_series_ids
    {'0000002110': {'S000009184', 'S000033622', 'S000009185', ...}, '0000002646': {'S000008760'}, '0000002663': {'S000008702'}, ...}

    # Get mapping from ticker to series ID
    >>> mapper.ticker_to_series_id
    {'LACAX': 'S000009184', 'LIACX': 'S000009184', 'ACRNX': 'S000009184', ...}

    # Get mapping from series ID to CIK
    >>> mapper.series_id_to_cik
    {'S000009184': '0000002110', 'S000009185': '0000002110', 'S000009186': '0000002110', ...}

    # Get mapping from series ID to tickers
    >>> mapper.series_id_to_tickers
    {'S000009184': {'CEARX', 'CRBYX', 'ACRNX', ...}, 'S000009185': {'ACINX', 'CACRX', 'CAIRX', ...}, 'S000009186': {'LAUCX', 'LAUAX', 'CUSAX', ...}, ...}

    # Get mapping from series ID to class IDs
    >>> mapper.series_id_to_class_ids
    {'S000009184': {'C000024956', 'C000122737', 'C000024957', ...}, 'S000009185': {'C000024958', 'C000122739', 'C000097733', ...}, 'S000009186': {'C000024962', 'C000024964', 'C000122740', ...}, ...}

    # Get mapping from ticker to class ID
    >>> mapper.ticker_to_class_id
    {'LACAX': 'C000024954', 'LIACX': 'C000024956', 'ACRNX': 'C000024957', ...}

    # Get mapping from CIK to class IDs
    >>> mapper.cik_to_class_ids
    {'0000002110': {'C000024958', 'C000024969', 'C000024957', ...}, '0000002646': {'C000023849', 'C000074893', 'C000028785', ...}, '0000002663': {'C000023718', 'C000028786', 'C000076529', ...}, ...}

    # Get mapping from class ID to CIK
    >>> mapper.class_id_to_cik
    {'C000024954': '0000002110', 'C000024956': '0000002110', 'C000024957': '0000002110', ...}

    # Get mapping from class ID to ticker
    >>> mapper.class_id_to_ticker
    {'C000024954': 'LACAX', 'C000024956': 'LIACX', 'C000024957': 'ACRNX', ...}

    # Save CIK, ticker, series ID, and class ID mappings to a CSV file
    >>> csv_path = Path("mutual_fund_mappings.csv")
    >>> mapper.save_metadata_to_csv(csv_path)

    # Get raw pandas dataframe
    >>> mapper.raw_dataframe
                  CIK Ticker   Series ID    Class ID
    0      0000002110  LACAX  S000009184  C000024954
    1      0000002110  LIACX  S000009184  C000024956
    2      0000002110  ACRNX  S000009184  C000024957
    3      0000002110  CEARX  S000009184  C000122735
    4      0000002110  CRBRX  S000009184  C000122736
    ...           ...    ...         ...         ...
    29237  0001860434   SIHY  S000072555  C000228888
    29238  0001860434   SIFI  S000072556  C000228889
    29239  0001860434   INNO  S000073580  C000230585
    29240  0001877493    BTF  S000074058  C000231452
    29241  0001877493    VBB  S000075054  C000233857

    [29242 rows x 4 columns]

Pre-generated Mappings
----------------------

Pre-generated mappings are also available for download and use outside of Python (e.g. manually or via automated
scripts/curl requests). These mappings are updated daily via a `fully automated daily CRON job <https://github.com/jadchaar/sec-cik-mapper/actions/workflows/update_mappings_daily_cron_job.yml>`_,
which fetches, transforms, validates, and uploads the latest mapping data from the SEC to GitHub
(save location: `github.com/jadchaar/sec-cik-mapper/mappings <https://github.com/jadchaar/sec-cik-mapper/tree/main/mappings>`_).
These mappings are available for download and usage from both GitHub and the `jsDelivr CDN <https://www.jsdelivr.com>`_.

Example Usage
^^^^^^^^^^^^^

Example `curl <https://curl.se/>`_ commands, which download the specified mapping files and saves them to the current working directory:

**Stocks**

Hosted via GitHub:

.. code-block:: console

    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/mappings.csv -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/cik_to_exchange.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/cik_to_tickers.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/ticker_to_exchange.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/cik_to_company_name.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/ticker_to_cik.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/ticker_to_company_name.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/exchange_to_tickers.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/stocks/exchange_to_ciks.json -O

Hosted via jsDelivr CDN:

.. code-block:: console

    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/mappings.csv -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/cik_to_exchange.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/cik_to_tickers.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/ticker_to_exchange.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/cik_to_company_name.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/ticker_to_cik.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/ticker_to_company_name.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/exchange_to_tickers.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/stocks/exchange_to_ciks.json -O

**Mutual Funds**

Hosted via GitHub:

.. code-block:: console

    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/ticker_to_class_id.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/series_id_to_class_ids.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/mappings.csv -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/cik_to_class_ids.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/cik_to_series_ids.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/series_id_to_cik.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/ticker_to_series_id.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/cik_to_tickers.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/class_id_to_cik.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/series_id_to_tickers.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/class_id_to_ticker.json -O
    $ curl https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/mappings/mutual_funds/ticker_to_cik.json -O

Hosted via jsDelivr CDN:

.. code-block:: console

    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/ticker_to_class_id.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/series_id_to_class_ids.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/mappings.csv -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/cik_to_class_ids.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/cik_to_series_ids.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/series_id_to_cik.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/ticker_to_series_id.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/cik_to_tickers.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/class_id_to_cik.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/series_id_to_tickers.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/class_id_to_ticker.json -O
    $ curl https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/mappings/mutual_funds/ticker_to_cik.json -O

Contributing
------------

If you encounter a bug or would like to see a new company filing or feature added to **sec-cik-mapper**, please `file an issue <https://github.com/jadchaar/sec-cik-mapper/issues>`_ or `submit a pull request <https://help.github.com/en/articles/creating-a-pull-request>`_.

Documentation
-------------

For full documentation, please visit `sec-cik-mapper.readthedocs.io <https://sec-cik-mapper.readthedocs.io>`_.
