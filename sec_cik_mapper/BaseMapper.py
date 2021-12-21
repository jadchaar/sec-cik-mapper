"""Provides a :class:`BaseMapper` class for mapping stock and mutual
fund data from the SEC."""

import time
from collections import defaultdict
from pathlib import Path
from typing import ClassVar, Dict, List, Union, cast

import pandas as pd
import requests

from .retrievers import MutualFundRetriever, StockRetriever
from .types import CompanyData, FieldIndices, Fields, KeyToValueSet


class BaseMapper:
    headers: ClassVar[Dict[str, str]] = {
        "User-Agent": f"{int(time.time())} {int(time.time())}@gmail.com",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov",
    }

    def __init__(self, retriever: Union[StockRetriever, MutualFundRetriever]) -> None:
        self.retriever = retriever
        self.mapping_metadata = self._get_mapping_metadata_from_sec()

    def __new__(cls, *args, **kwargs):
        """BaseMapper should not be directly instantiated,
        so throw an error on instantiation.

        More info: https://stackoverflow.com/a/7990308/3820660
        """
        if cls is BaseMapper:
            raise TypeError(
                f"{cls.__name__} cannot be directly instantiated. "
                "Please instantiate the StockMapper and/or MutualFundMapper "
                "classes instead."
            )
        return object.__new__(cls, *args, **kwargs)

    def _get_indices_from_fields(self, fields: Fields) -> FieldIndices:
        """Get list indices from field names."""
        return cast(FieldIndices, {field: fields.index(field) for field in fields})

    def _get_mapping_metadata_from_sec(self) -> pd.DataFrame:
        """Get company metadata from SEC."""
        resp = requests.get(self.retriever.source_url, headers=BaseMapper.headers)
        resp.raise_for_status()
        data = resp.json()

        fields: Fields = data["fields"]
        field_indices: FieldIndices = self._get_indices_from_fields(fields)

        company_data: CompanyData = data["data"]
        transformed_data: List[Dict[str, str]] = []

        for cd in company_data:
            transformed_data.append(
                self.retriever.transform(field_indices, cd),
            )

        return pd.DataFrame(transformed_data)

    def _form_kv_set_mapping(self, keys: pd.Series, values: pd.Series) -> KeyToValueSet:
        """Form mapping from key to list of values, ignoring blank keys and values"""
        # Example: numerous CIKs map to multiple tickers (e.g. Banco Santander),
        # so we must keep a list of tickers for each unique CIK.
        mapping = defaultdict(set)
        for key, value in zip(keys, values):
            # Ignore blank keys and values
            if key and value:
                mapping[key].add(value)
        return dict(mapping)

    def _form_kv_mapping(self, keys: pd.Series, values: pd.Series) -> Dict[str, str]:
        """Form key-value mapping, ignoring blank keys and values."""
        return {k: v for k, v in zip(keys, values) if k and v}

    @property
    def cik_to_tickers(self) -> KeyToValueSet:
        """Get CIK to ticker mapping.

        Usage::

            >>> from sec_cik_mapper import CIKMapper
            >>> from pathlib import Path

            # Initialize a CIK mapper instance
            >>> cikMapper = CIKMapper()

            # Get a dictionary mapping CIK to a list of tickers
            >>> cikMapper.get_cik_to_ticker_mapping()
            {'0000320193': ['AAPL'], '0001652044': ['GOOG', 'GOOGL'], ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return self._form_kv_set_mapping(cik_col, ticker_col)

    @property
    def ticker_to_cik(self) -> Dict[str, str]:
        """Get ticker to CIK mapping.

        Usage::

            >>> from sec_cik_mapper import CIKMapper
            >>> from pathlib import Path

            # Initialize a CIK mapper instance
            >>> cikMapper = CIKMapper()

            # Get a dictionary mapping ticker to CIK
            >>> cikMapper.get_ticker_to_cik_mapping()
            {'AAPL': '0000320193', 'MSFT': '0000789019', 'GOOG': '0001652044', ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return self._form_kv_mapping(ticker_col, cik_col)

    @property
    def raw_dataframe(self) -> pd.DataFrame:
        return self.mapping_metadata

    def save_metadata_to_csv(self, path: Union[str, Path]) -> None:
        """Save company stock metadata (CIK, ticker, exchange, and
        company name) or mutual fund metadata (CIK, ticker, series ID,
        class ID) from SEC to CSV.

        Usage::

            >>> from sec_cik_mapper import StockMapper, MutualFundMapper
            >>> from pathlib import Path

            >>> stockMapper = StockMapper()
            >>> mutualFundMapper = MutualFundMapper()
            >>> csv_path = Path("cik_mapping.csv")

            # Save full CIK, ticker, exchange, and company name mapping to a CSV file
            >>> stockMapper.save_metadata_to_csv(csv_path)

            # Save full CIK, ticker, series ID, and class ID mapping to a CSV file
            >>> mutualFundMapper.save_metadata_to_csv(csv_path)
        """
        self.mapping_metadata.to_csv(path, index=False)
