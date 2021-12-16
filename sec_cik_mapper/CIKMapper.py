from collections import defaultdict
from pathlib import Path
from typing import Dict, Sequence, Union

import pandas as pd
import requests

# More info: https://www.sec.gov/os/webmaster-faq#ticker-cik
COMPANY_TICKERS_SEC_URL = "https://www.sec.gov/files/company_tickers.json"


class CIKMapper:
    def __init__(self):
        self.mapping_metadata = self._get_mapping_metadata_from_sec()

    def _get_mapping_metadata_from_sec(self) -> pd.DataFrame:
        resp = requests.get(COMPANY_TICKERS_SEC_URL)
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
        # Numerous CIKs map to multiple tickers (e.g. Banco Santander),
        # so we must keep a list of tickers for each unique CIK.
        cik_mapping = defaultdict(list)
        for cik, value in zip(cik_col, value_col):
            cik_mapping[cik].append(value)
        return cik_mapping

    def get_cik_to_ticker_mapping(self) -> Dict[str, Sequence[str]]:
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return self._form_cik_mapping(cik_col, ticker_col)

    def get_ticker_to_cik_mapping(self) -> Dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return dict(zip(ticker_col, cik_col))

    def get_cik_to_company_name_mapping(self) -> Dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(cik_col, company_name_col))

    def get_ticker_to_company_name_mapping(self) -> Dict[str, str]:
        ticker_col = self.mapping_metadata["Ticker"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(ticker_col, company_name_col))

    def save_metadata_to_csv(self, path: Union[str, Path]) -> None:
        # TODO: let users specify which of the 3 columns to sort on
        # E.g. sort rows on ticker: mapping_metadata.sort_values(["Ticker"])
        self.mapping_metadata.to_csv(path, index=False)
