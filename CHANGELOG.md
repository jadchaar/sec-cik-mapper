# Changelog

## 2.0.1 - 12/29/21

- Moved README content from `README.rst` to `README.md` for improved table formatting support.
- Raw pandas dataframe is now sorted on CIK and ticker to produce more consistent output.

## 2.0.0 - 12/25/21

### New

- Full revamp of API. Renamed `CIKMapper` to `StockMapper` and added support for mutual fund mapping capabilities via the `MutualFundMapper`. The `MutualFundMapper` is capable of obtaining mappings between CIKs, tickers, series IDs, and class IDs. The `StockMapper` is capable of obtaining mappings between CIKs, tickers, company names, and exchanges.
- Replaced function calls on mapper objects with properties.
- Added support for creating mappings to and from exchanges via the `StockMapper`.
- Added full support for PEP 484-style type hints.
- Added `raw_dataframe` property to both mappers that exposes the underlying pandas dataframe for additional extensibility.
- Added [examples to GitHub repository](https://github.com/jadchaar/sec-cik-mapper/tree/main/examples) to improve first-time usage.
- Updated naming of JSON and CSV mappings and added support for a number of new auto-generated mappings.
- Improved documentation in README on how to download the auto-generated mappings via curl from GitHub or jsDelivr.

### Internal

- Improved abstractions to reduce code duplication across both mapper classes.
- Migrated PyPI publishing system to [Flit](https://flit.readthedocs.io/).
- Revamped README and documentation. The latest documentation can be found [here](https://sec-cik-mapper.readthedocs.io).
- Full rewrite of tests to support new properties and package APIs.

## 1.0.0 - 12/15/21

- Initial release.
