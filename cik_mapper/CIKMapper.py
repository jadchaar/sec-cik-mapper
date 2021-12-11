import pandas as pd
import requests

# More info: https://www.sec.gov/os/webmaster-faq#ticker-cik
COMPANY_TICKERS_SEC_URL = "https://www.sec.gov/files/company_tickers.json"


class CIKMapper:
    def __init__(self):
        self.mapping_metadata = self._get_mapping_metadata()

    def _get_mapping_metadata(self) -> pd.DataFrame:
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

    def get_cik_to_ticker_mapping(self) -> dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return dict(zip(cik_col, ticker_col))

    def get_ticker_to_cik_mapping(self) -> dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        ticker_col = self.mapping_metadata["Ticker"]
        return dict(zip(ticker_col, cik_col))

    def get_cik_to_title_mapping(self) -> dict[str, str]:
        cik_col = self.mapping_metadata["CIK"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(cik_col, company_name_col))

    def get_ticker_to_title_mapping(self) -> dict[str, str]:
        ticker_col = self.mapping_metadata["Ticker"]
        company_name_col = self.mapping_metadata["Company Name"]
        return dict(zip(ticker_col, company_name_col))

    def save_metadata_to_csv(self, path_or_buf) -> None:
        # TODO: let users specify which of the 3 columns to sort on
        # E.g. sort rows on ticker: mapping_metadata.sort_values(["Ticker"])
        self.mapping_metadata.to_csv(path_or_buf, index=False)
