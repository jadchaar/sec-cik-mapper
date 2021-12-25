"""Provides a :class:`MutualFundMapper` class for mapping CIKs, tickers,
series IDs, and class IDs."""

from typing import ClassVar, Dict

from .BaseMapper import BaseMapper
from .retrievers import MutualFundRetriever
from .types import KeyToValueSet


class MutualFundMapper(BaseMapper):
    """A :class:`MutualFundMapper` object.

    Usage::

        >>> from sec_cik_mapper import MutualFundMapper
        >>> mutual_fund_mapper = MutualFundMapper()
    """

    _retriever: ClassVar[MutualFundRetriever] = MutualFundRetriever()

    def __init__(self) -> None:
        """Constructor for the :class:`MutualFundMapper` class."""
        super().__init__(MutualFundMapper._retriever)

    @property
    def cik_to_series_ids(self) -> KeyToValueSet:
        """Get CIK to series ID mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.cik_to_series_ids
            {'0000002110': {'S000009184', 'S000033622', ...}, '0000002646': {'S000008760'}, ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_kv_set_mapping(cik_col, series_id_col)

    @property
    def ticker_to_series_id(self) -> Dict[str, str]:
        """Get ticker to series ID mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.ticker_to_series_id
            {'LACAX': 'S000009184', 'LIACX': 'S000009184', 'ACRNX': 'S000009184', ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_kv_mapping(ticker_col, series_id_col)

    @property
    def series_id_to_cik(self) -> Dict[str, str]:
        """Get series ID to CIK mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.series_id_to_cik
            {'S000009184': '0000002110', 'S000009185': '0000002110', ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_kv_mapping(series_id_col, cik_col)

    @property
    def series_id_to_tickers(self) -> KeyToValueSet:
        """Get series ID to tickers mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.series_id_to_tickers
            {'S000009184': {'CEARX', 'CRBYX', ...}, 'S000009185': {'ACINX', 'CACRX', ...}, ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_kv_set_mapping(series_id_col, ticker_col)

    @property
    def series_id_to_class_ids(self) -> KeyToValueSet:
        """Get series ID to class IDs mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.series_id_to_class_ids
            {'S000009184': {'C000024956', ...}, 'S000009185': {'C000024958', ...}, ...}
        """
        class_id_col = self.mapping_metadata["Class ID"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_kv_set_mapping(series_id_col, class_id_col)

    @property
    def ticker_to_class_id(self) -> Dict[str, str]:
        """Get ticker to class ID mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.ticker_to_class_id
            {'LACAX': 'C000024954', 'LIACX': 'C000024956', 'ACRNX': 'C000024957', ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        class_id_col = self.mapping_metadata["Class ID"]
        return self._form_kv_mapping(ticker_col, class_id_col)

    @property
    def cik_to_class_ids(self) -> KeyToValueSet:
        """Get CIK to class IDs mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.cik_to_class_ids
            {'0000002110': {'C000024958', ...}, '0000002646': {'C000023849', ...}, ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        class_id_col = self.mapping_metadata["Class ID"]
        return self._form_kv_set_mapping(cik_col, class_id_col)

    @property
    def class_id_to_cik(self) -> Dict[str, str]:
        """Get class ID to CIK mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.class_id_to_cik
            {'C000024954': '0000002110', 'C000024956': '0000002110', ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        class_id_col = self.mapping_metadata["Class ID"]
        return self._form_kv_mapping(class_id_col, cik_col)

    @property
    def class_id_to_ticker(self) -> Dict[str, str]:
        """Get class ID to ticker mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> mutual_fund_mapper.class_id_to_ticker
            {'C000024954': 'LACAX', 'C000024956': 'LIACX', 'C000024957': 'ACRNX', ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        class_id_col = self.mapping_metadata["Class ID"]
        return self._form_kv_mapping(class_id_col, ticker_col)
