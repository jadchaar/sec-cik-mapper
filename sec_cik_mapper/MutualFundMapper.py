"""Provides a :class:`MutualFundMapper` class for mapping CIKs, tickers, and company names.."""

from typing import Dict, ClassVar

from .BaseMapper import BaseMapper
from .retrievers import MutualFundRetriever

from .types import CompanyData, FieldIndices, Fields, KeyToValueSet

import pandas as pd

class MutualFundMapper(BaseMapper):
    """A :class:`MutualFundMapper` object.

    Usage::

        >>> from sec_cik_mapper import MutualFundMapper

        # Create a MutualFundMapper instance
        >>> mutualFundMapper = MutualFundMapper()
    """
    def __init__(self) -> None:
        super().__init__(MutualFundRetriever())

    @property
    def cik_to_series_ids(self) -> KeyToValueSet:
        cik_col = self.mapping_metadata["CIK"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_key_to_value_set_mapping(cik_col, series_id_col)

    @property
    def ticker_to_series_id(self) -> KeyToValueSet:
        ticker_col = self.mapping_metadata["CIK"]
        series_id_col = self.mapping_metadata["Series ID"]
        return dict(zip(ticker_col, series_id_col))

    @property
    def series_id_to_cik(self) -> Dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        series_id_col = self.mapping_metadata["Series ID"]
        return dict(zip(series_id_col, cik_col))

    @property
    def series_id_to_tickers(self) -> KeyToValueSet:
        ticker_col = self.mapping_metadata["Ticker"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_key_to_value_set_mapping(series_id_col, ticker_col)

    @property
    def series_id_to_class_ids(self) -> KeyToValueSet:
        class_id_col = self.mapping_metadata["Class ID"]
        series_id_col = self.mapping_metadata["Series ID"]
        return self._form_key_to_value_set_mapping(series_id_col, class_id_col)

    @property
    def ticker_to_class_id(self) -> KeyToValueSet:
        ticker_col = self.mapping_metadata["CIK"]
        class_id_col = self.mapping_metadata["Class ID"]
        return dict(zip(ticker_col, class_id_col))

    @property
    def cik_to_class_ids(self) -> KeyToValueSet:
        cik_col = self.mapping_metadata["CIK"]
        class_id_col = self.mapping_metadata["Class ID"]
        return self._form_key_to_value_set_mapping(cik_col, class_id_col)

    @property
    def class_id_to_cik(self) -> KeyToValueSet:
        cik_col = self.mapping_metadata["CIK"]
        class_id_col = self.mapping_metadata["Class ID"]
        return dict(zip(class_id_col, cik_col))

    @property
    def class_id_to_ticker(self) -> KeyToValueSet:
        ticker_col = self.mapping_metadata["Ticker"]
        class_id_col = self.mapping_metadata["Class ID"]
        return dict(zip(class_id_col, ticker_col))
