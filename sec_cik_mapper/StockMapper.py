"""Provides a :class:`StockMapper` class for mapping CIKs, tickers,
exchanges, and company names."""

from typing import ClassVar, Dict

from .BaseMapper import BaseMapper
from .retrievers import StockRetriever
from .types import KeyToValueSet


class StockMapper(BaseMapper):
    """A :class:`StockMapper` object.

    Usage::

        >>> from sec_cik_mapper import StockMapper
        >>> stock_mapper = StockMapper()
    """

    _retriever: ClassVar[StockRetriever] = StockRetriever()

    def __init__(self) -> None:
        """Constructor for the :class:`StockMapper` class."""
        super().__init__(StockMapper._retriever)

    @property
    def cik_to_company_name(self) -> Dict[str, str]:
        """Get CIK to company name mapping.

        Usage::

            >>> from sec_cik_mapper import StockMapper
            >>> stock_mapper = StockMapper()
            >>> stock_mapper.cik_to_company_name
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
            >>> stock_mapper = StockMapper()
            >>> stock_mapper.ticker_to_company_name
            {'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corp', 'GOOG': 'Alphabet Inc.', ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        company_name_col = self.mapping_metadata["Name"]
        return self._form_kv_mapping(ticker_col, company_name_col)

    @property
    def ticker_to_exchange(self) -> Dict[str, str]:
        """Get ticker to exchange mapping.

        Usage::

            >>> from sec_cik_mapper import StockMapper
            >>> stock_mapper = StockMapper()
            >>> stock_mapper.ticker_to_exchange
            {'AAPL': 'Nasdaq', 'MSFT': 'Nasdaq', 'GOOG': 'Nasdaq', ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_mapping(ticker_col, exchange_col)

    @property
    def exchange_to_tickers(self) -> KeyToValueSet:
        """Get exchange to tickers mapping.

        Usage::

            >>> from sec_cik_mapper import StockMapper
            >>> stock_mapper = StockMapper()
            >>> stock_mapper.exchange_to_tickers
            {'Nasdaq': {'CYRN', 'OHPAW', ...}, 'NYSE': {'PLAG', 'TDW-WTB', ...}, ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_set_mapping(exchange_col, ticker_col)

    @property
    def cik_to_exchange(self) -> Dict[str, str]:
        """Get CIK to exchange mapping.

        Usage::

            >>> from sec_cik_mapper import StockMapper
            >>> stock_mapper = StockMapper()
            >>> stock_mapper.cik_to_exchange
            {'0000320193': 'Nasdaq', '0000789019': 'Nasdaq', '0001652044': 'Nasdaq', ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_mapping(cik_col, exchange_col)

    @property
    def exchange_to_ciks(self) -> KeyToValueSet:
        """Get exchange to CIKs mapping.

        Usage::

            >>> from sec_cik_mapper import StockMapper
            >>> stock_mapper = StockMapper()
            >>> stock_mapper.exchange_to_ciks
            {'Nasdaq': {'0000779544', ...}, 'NYSE': {'0000764478', ...}, ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        exchange_col = self.mapping_metadata["Exchange"]
        return self._form_kv_set_mapping(exchange_col, cik_col)
