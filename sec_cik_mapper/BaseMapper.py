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
    """A :class:`BaseMapper` object."""

    _headers: ClassVar[Dict[str, str]] = {
        "User-Agent": f"{int(time.time())} {int(time.time())}@gmail.com",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov",
    }

    def __init__(self, retriever: Union[StockRetriever, MutualFundRetriever]) -> None:
        """Constructor for the :class:`BaseMapper` class."""
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
        field_indices = {field: fields.index(field) for field in fields}
        return cast(FieldIndices, field_indices)

    def _get_mapping_metadata_from_sec(self) -> pd.DataFrame:
        """Get company mapping metadata from the SEC as a pandas dataframe,
        sorted by CIK and ticker.
        """
        resp = requests.get(self.retriever.source_url, headers=BaseMapper._headers)
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

        df = pd.DataFrame(transformed_data)
        df.sort_values(by=["CIK", "Ticker"], inplace=True, ignore_index=True)
        return df

    def _form_kv_set_mapping(self, keys: pd.Series, values: pd.Series) -> KeyToValueSet:
        """Form mapping from key to list of values, ignoring blank keys and values.

        Example: numerous CIKs map to multiple tickers (e.g. Banco Santander),
        so we must keep a list of tickers for each unique CIK.
        """
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
        """Get CIK to tickers mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper, StockMapper
            >>> stock_mapper = StockMapper()
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> stock_mapper.cik_to_tickers
            {'0000320193': {'AAPL'}, '0001652044': {'GOOG', 'GOOGL'}, ...}
            >>> mutual_fund_mapper.cik_to_tickers
            {'0000002110': {'CRBYX', 'CEFZX', ...}, '0000002646': {'IIBPX', 'IPISX', ...}, ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return self._form_kv_set_mapping(cik_col, ticker_col)

    @property
    def ticker_to_cik(self) -> Dict[str, str]:
        """Get ticker to CIK mapping.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper, StockMapper
            >>> stock_mapper = StockMapper()
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> stock_mapper.ticker_to_cik
            {'AAPL': '0000320193', 'MSFT': '0000789019', 'GOOG': '0001652044', ...}
            >>> mutual_fund_mapper.ticker_to_cik
            {'LACAX': '0000002110', 'LIACX': '0000002110', 'ACRNX': '0000002110', ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return self._form_kv_mapping(ticker_col, cik_col)

    @property
    def raw_dataframe(self) -> pd.DataFrame:
        """Get raw pandas dataframe.

        Usage::

            >>> from sec_cik_mapper import MutualFundMapper, StockMapper
            >>> stock_mapper = StockMapper()
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> stock_mapper.raw_dataframe
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
            >>> mutual_fund_mapper.raw_dataframe
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
        """
        return self.mapping_metadata

    def save_metadata_to_csv(self, path: Union[str, Path]) -> None:
        """Save stock mapping metadata (CIK, ticker, exchange, and company name)
        or mutual fund mapping metadata (CIK, ticker, series ID, class ID) from
        SEC to CSV.

        Usage::

            >>> from sec_cik_mapper import StockMapper, MutualFundMapper
            >>> from pathlib import Path
            >>> stock_mapper = StockMapper()
            >>> mutual_fund_mapper = MutualFundMapper()
            >>> csv_path = Path("cik_mapping.csv")
            # Save full CIK, ticker, exchange, and company name mapping to a CSV file
            >>> stock_mapper.save_metadata_to_csv(csv_path)
            # Save full CIK, ticker, series ID, and class ID mapping to a CSV file
            >>> mutual_fund_mapper.save_metadata_to_csv(csv_path)
        """
        self.mapping_metadata.to_csv(path, index=False)
