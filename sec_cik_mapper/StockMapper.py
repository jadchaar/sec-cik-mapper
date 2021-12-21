"""Provides a :class:`StockMapper` class for mapping CIKs, tickers,
exchanges, and company names."""

from typing import ClassVar, Dict, Union

from .BaseMapper import BaseMapper
from .retrievers import MutualFundRetriever, StockRetriever
from .types import KeyToValueSet


class StockMapper(BaseMapper):
    """A :class:`StockMapper` object.

    Usage::

        >>> from sec_cik_mapper import StockMapper

        # Create a StockMapper instance
        >>> stockMapper = StockMapper()
    """

    _retriever: ClassVar[Union[MutualFundRetriever, StockRetriever]] = StockRetriever()

    def __init__(self) -> None:
        super().__init__(StockMapper._retriever)

    @property
    def cik_to_company_name(self) -> Dict[str, str]:
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
        company_name_col = self.mapping_metadata["Name"]
        return self._form_kv_mapping(cik_col, company_name_col)

    @property
    def ticker_to_company_name(self) -> Dict[str, str]:
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
        company_name_col = self.mapping_metadata["Name"]
        return self._form_kv_mapping(ticker_col, company_name_col)

    @property
    def ticker_to_exchange(self) -> Dict[str, str]:
        ticker_col = self.mapping_metadata["Ticker"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_mapping(ticker_col, exchange_col)

    @property
    def exchange_to_tickers(self) -> KeyToValueSet:
        ticker_col = self.mapping_metadata["Ticker"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_set_mapping(exchange_col, ticker_col)

    @property
    def cik_to_exchange(self) -> Dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_mapping(cik_col, exchange_col)

    @property
    def exchange_to_ciks(self) -> KeyToValueSet:
        cik_col = self.mapping_metadata["CIK"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_set_mapping(exchange_col, cik_col)
