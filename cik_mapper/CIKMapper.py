import json

import pandas as pd
import requests

# More info: https://www.sec.gov/os/webmaster-faq#ticker-cik
COMPANY_TICKERS_SEC_URL = "https://www.sec.gov/files/company_tickers.json"


class CIKMapper:
    def __init__(self):
        self.mapping_metadata: pd.DataFrame = self._get_mapping_metadata()
        print(self.mapping_metadata)

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

    def save_metadata_to_csv(self, path) -> None:
        self.mapping_metadata.to_csv(path, index=False)

    def save_metadata_to_markdown(self, path) -> None:
        self.mapping_metadata.to_markdown(path, index=False)


cikMapper = CIKMapper()
auto_generated_mappings_base = "auto_generated_mappings"

cik_to_ticker_mapping = cikMapper.get_cik_to_ticker_mapping()
with open(
    f"{auto_generated_mappings_base}/cik_to_ticker.json", "w", encoding="utf-8"
) as f:
    json.dump(cik_to_ticker_mapping, f, ensure_ascii=False, sort_keys=True, indent=4)

ticker_to_cik_mapping = cikMapper.get_ticker_to_cik_mapping()
with open(
    f"{auto_generated_mappings_base}/ticker_to_cik.json", "w", encoding="utf-8"
) as f:
    json.dump(ticker_to_cik_mapping, f, ensure_ascii=False, sort_keys=True, indent=4)

cik_to_title_mapping = cikMapper.get_cik_to_title_mapping()
with open(
    f"{auto_generated_mappings_base}/cik_to_title.json", "w", encoding="utf-8"
) as f:
    json.dump(cik_to_title_mapping, f, ensure_ascii=False, sort_keys=True, indent=4)

ticker_to_title_mapping = cikMapper.get_ticker_to_title_mapping()
with open(
    f"{auto_generated_mappings_base}/ticker_to_title.json", "w", encoding="utf-8"
) as f:
    json.dump(ticker_to_title_mapping, f, ensure_ascii=False, sort_keys=True, indent=4)

save_path = f"{auto_generated_mappings_base}/cik_ticker_company_name_table"
cikMapper.save_metadata_to_csv(f"{save_path}.csv")
cikMapper.save_metadata_to_markdown(f"{save_path}.md")
