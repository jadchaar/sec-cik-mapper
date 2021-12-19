"""Provides a :class:`BaseMapper` class for mapping CIKs, tickers, and company names.."""

import sys
from collections import defaultdict
from pathlib import Path

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import Dict, List, Union
else:
    from typing import Dict, List, Union  # pragma: no cover

import pandas as pd
import requests

from .retrievers import BaseRetriever
from .types import CompanyData, FieldIndices, Fields


class BaseMapper:
    def __new__(cls, *args, **kwargs):
        """BaseMapper should not be directly instantiated,
        so throw an error on instantiation.

        More info: https://stackoverflow.com/a/7990308/3820660
        """
        if cls is BaseMapper:
            raise TypeError(
                f"{cls.__name__} cannot be directly instantiated. "
                "Please instantiate the StockMapper and MutualFundMapper "
                "classes instead."
            )
        return object.__new__(cls, *args, **kwargs)

    def _get_indices_from_fields(self, fields: Fields) -> FieldIndices:
        """Get list indices from field names."""
        return {field: fields.index(field) for field in fields}

    def _get_mapping_metadata_from_sec(self, retriever: BaseRetriever) -> pd.DataFrame:
        """Get company metadata (CIK, ticker, company name) from SEC."""
        resp = requests.get(retriever.source_url)
        resp.raise_for_status()
        data = resp.json()

        fields: Fields = data["fields"]
        field_indices: FieldIndices = self._get_indices_from_fields(fields)

        company_data: CompanyData = data["data"]
        transformed_data: List[Dict[str, str]] = []

        for cd in company_data:
            transformed_data.append(
                retriever.transform(field_indices, cd),
            )

        return pd.DataFrame(transformed_data)

    def _form_key_to_value_list_mapping(self, keys, values) -> Dict[str, List[str]]:
        """Form mapping from key to list of values."""
        # Example: numerous CIKs map to multiple tickers (e.g. Banco Santander),
        # so we must keep a list of tickers for each unique CIK.
        mapping = defaultdict(list)
        for key, value in zip(keys, values):
            mapping[key].append(value)
        return dict(mapping)

    def get_cik_to_ticker_mapping(self) -> Dict[str, List[str]]:
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
        return self._form_key_to_value_list_mapping(cik_col, ticker_col)

    def get_ticker_to_cik_mapping(self) -> Dict[str, str]:
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
        return dict(zip(ticker_col, cik_col))

    def get_raw_dataframe(self) -> pd.DataFrame:
        return self.mapping_metadata

    def save_metadata_to_csv(self, path: Union[str, Path]) -> None:
        """Save company stock metadata (CIK, ticker, company name,
        and exchange) or mutual fund metadata (CIK, ticker, series ID,
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
