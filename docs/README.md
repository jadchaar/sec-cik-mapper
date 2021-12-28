# sec-cik-mapper

[![Tests](https://github.com/jadchaar/sec-cik-mapper/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/jadchaar/sec-cik-mapper/actions/workflows/continuous_integration.yml)
[![Update Mappings Daily CRON Job](https://github.com/jadchaar/cik-mapper/actions/workflows/update_mappings_daily_cron_job.yml/badge.svg?event=schedule)](https://github.com/jadchaar/sec-cik-mapper/actions/workflows/update_mappings_daily_cron_job.yml)
[![Coverage](https://codecov.io/gh/jadchaar/sec-cik-mapper/branch/main/graph/badge.svg)](https://pypi.org/project/sec_cik_mapper/)
[![PyPI Version](https://img.shields.io/pypi/v/sec-cik-mapper.svg)](https://pypi.org/project/sec_cik_mapper/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/sec-cik-mapper.svg)](https://pypi.org/project/sec_cik_mapper/)
[![License](https://img.shields.io/pypi/l/sec-cik-mapper.svg)](https://pypi.org/project/sec_cik_mapper/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

**sec-cik-mapper** is a Python package for generating mappings between stock and mutual fund identifier data provided by the SEC.

## Features

- Generate up-to-date mappings from the SEC as native Python dictionaries
- Mappings for both stocks and mutual funds
- Mapping data exposed as a raw pandas dataframe for custom data processing and usage
- Full support for PEP 484-style type hints and the [mypy type checker](https://mypy.readthedocs.io/en/stable/)
- [Pre-generated mappings](https://github.com/jadchaar/sec-cik-mapper/tree/main/mappings), updated daily, available from GitHub and jsDelivr for use outside of Python
- Support for Python 3.6+

## Supported Mappings

Mappings can be formed between the following SEC identifiers and metadata:

| Key       | Value           | `StockMapper` | `MutualFundMapper` |
|:---------:| --------------- | ------------- | ------------------ |
| CIK       | Set(Tickers)    | ✅             | ✅                  |
| CIK       | Company Name    | ✅             |                    |
| CIK       | Exchange        | ✅             |                    |
| Exchange  | Set(CIKs)       | ✅             |                    |
| Exchange  | Set(Tickers)    | ✅             |                    |
| Ticker    | CIK             | ✅             | ✅                  |
| Ticker    | Company Name    | ✅             |                    |
| Ticker    | Exchange        | ✅             |                    |
| CIK       | Set(Series IDs) |               | ✅                  |
| CIK       | Set(Class IDs)  |               | ✅                  |
| Class ID  | CIK             |               | ✅                  |
| Class ID  | Ticker          |               | ✅                  |
| Series ID | CIK             |               | ✅                  |
| Series ID | Set(Class IDs)  |               | ✅                  |
| Series ID | Set(Tickers)    |               | ✅                  |
| Ticker    | Class ID        |               | ✅                  |
| Ticker    | Series ID       |               | ✅                  |
