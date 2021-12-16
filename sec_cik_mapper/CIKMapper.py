"""Provides a :class:`CIKMapper` class for mapping CIKs, tickers, and company names.."""

from collections import defaultdict
from pathlib import Path
from typing import Dict, Sequence, Union

import pandas as pd
import requests


class CIKMapper:
    """A :class:`CIKMapper` object.

    Usage::

        >>> from sec_cik_mapper import CIKMapper

        # Create a CIKMapper instance
        >>> cikMapper = CIKMapper()
    """

    # More info: https://www.sec.gov/os/webmaster-faq#ticker-cik
    SEC_MAPPING_SOURCE_URL = "https://www.sec.gov/files/company_tickers.json"

    def __init__(self):
        """Constructor for the :class:`CIKMapper` class."""
        self.mapping_metadata = self._get_mapping_metadata_from_sec()

    def _get_mapping_metadata_from_sec(self) -> pd.DataFrame:
        """Get company metadata (CIK, ticker, company name) from SEC."""
        resp = requests.get(self.SEC_MAPPING_SOURCE_URL)
        resp.raise_for_status()
        data = resp.json()
        transformed_data = []

        for company_data in data.values():
            transformed_data.append(
                {
                    "CIK": str(company_data["cik_str"]).zfill(10),
                    "Ticker": company_data["ticker"].upper(),
                    "Company Name": company_data["title"].title(),
                }
            )

        return pd.DataFrame(transformed_data)

    def _form_cik_mapping(self, cik_col, value_col) -> Dict[str, Sequence[str]]:
        """Form mapping from CIK to list of values (e.g. tickers)."""
        # Numerous CIKs map to multiple tickers (e.g. Banco Santander),
        # so we must keep a list of tickers for each unique CIK.
        cik_mapping = defaultdict(list)
        for cik, value in zip(cik_col, value_col):
            cik_mapping[cik].append(value)
        return dict(cik_mapping)

    def get_cik_to_ticker_mapping(self) -> Dict[str, Sequence[str]]:
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
        return self._form_cik_mapping(cik_col, ticker_col)

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

    def get_cik_to_company_name_mapping(self) -> Dict[str, str]:
        """Get CIK to company name mapping.

        Usage::

            >>> from sec_cik_mapper import CIKMapper
            >>> from pathlib import Path

            # Initialize a CIK mapper instance
            >>> cikMapper = CIKMapper()

            # Get a dictionary mapping CIK to company name
            >>> cikMapper.get_cik_to_company_name_mapping()
            {'0000320193': 'Apple Inc.', '0000789019': 'Microsoft Corp', ...}
        """
        cik_col = self.mapping_metadata["CIK"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(cik_col, company_name_col))

    def get_ticker_to_company_name_mapping(self) -> Dict[str, str]:
        """Get ticker to company name mapping.

        Usage::

            >>> from sec_cik_mapper import CIKMapper
            >>> from pathlib import Path

            # Initialize a CIK mapper instance
            >>> cikMapper = CIKMapper()

            # Get a dictionary mapping ticker to company name
            >>> cikMapper.get_ticker_to_company_name_mapping()
            {'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corp', 'GOOG': 'Alphabet Inc.', ...}
        """
        ticker_col = self.mapping_metadata["Ticker"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(ticker_col, company_name_col))

    def save_metadata_to_csv(self, path: Union[str, Path]) -> None:
        """Save company metadata from SEC (CIK, ticker, and company name) to CSV.

        Usage::

            >>> from sec_cik_mapper import CIKMapper
            >>> from pathlib import Path

            # Initialize a CIK mapper instance
            >>> cikMapper = CIKMapper()

            # Save full CIK, ticker, and company name mapping to a CSV file
            >>> csv_path = Path("cik_mapping.csv")
            >>> cikMapper.save_metadata_to_csv(csv_path)
        """
        # TODO: let users specify which of the 3 columns to sort on
        # E.g. sort rows on ticker: mapping_metadata.sort_values(["Ticker"])
        self.mapping_metadata.to_csv(path, index=False)
