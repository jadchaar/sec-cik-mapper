"""Provides a :class:`StockMapper` class for mapping CIKs, tickers, and company names.."""

import sys

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import Dict, List
else:
    from typing import Dict, List  # pragma: no cover

from .BaseMapper import BaseMapper
from .retrievers import StockRetriever


class StockMapper(BaseMapper):
    """A :class:`StockMapper` object.

    Usage::

        >>> from sec_cik_mapper import StockMapper

        # Create a StockMapper instance
        >>> stockMapper = StockMapper()
    """

    def __init__(self):
        super().__init__()
        stockRetriever = StockRetriever()
        self.mapping_metadata = self._get_mapping_metadata_from_sec(stockRetriever)

    def get_cik_to_company_name_mapping(self) -> Dict[str, str]:
        """Get CIK to company name mapping.

        Usage::

            >>> from sec_cik_mapper import StockMapper
            >>> from pathlib import Path

            # Initialize a CIK mapper instance
            >>> stockMapper = StockMapper()

            # Get a dictionary mapping CIK to company name
            >>> stockMapper.get_cik_to_company_name_mapping()
            {'0000320193': 'Apple Inc.', '0000789019': 'Microsoft Corp', ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(cik_col, company_name_col))

    def get_ticker_to_company_name_mapping(self) -> Dict[str, str]:
        """Get ticker to company name mapping.

        Usage::

            >>> from sec_cik_mapper import StockMapper
            >>> from pathlib import Path

            # Initialize a CIK mapper instance
            >>> stockMapper = StockMapper()

            # Get a dictionary mapping ticker to company name
            >>> stockMapper.get_ticker_to_company_name_mapping()
            {'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corp', 'GOOG': 'Alphabet Inc.', ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(ticker_col, company_name_col))

    def get_ticker_to_exchange_mapping(self) -> Dict[str, str]:
        ticker_col = self.mapping_metadata["Ticker"]
        exchange_col = self.mapping_metadata["Exchange"]
        return dict(zip(ticker_col, exchange_col))

    def get_exchange_to_ticker_mapping(self) -> Dict[str, List[str]]:
        ticker_col = self.mapping_metadata["Ticker"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_key_to_value_list_mapping(exchange_col, ticker_col)

    def get_cik_to_exchange_mapping(self) -> Dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        exchange_col = self.mapping_metadata["Exchange"]
        return dict(zip(cik_col, exchange_col))

    def get_exchange_to_cik_mapping(self) -> Dict[str, List[str]]:
        cik_col = self.mapping_metadata["CIK"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_key_to_value_list_mapping(exchange_col, cik_col)
