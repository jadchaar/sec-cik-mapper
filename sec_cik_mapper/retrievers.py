import sys

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import Dict, Final, List, Union
else:
    from typing import Final, Dict, List, Union  # pragma: no cover

from abc import ABCMeta, abstractmethod

from .types import FieldIndices

# See CIK, ticker, and exchange associations section of:
# https://www.sec.gov/os/accessing-edgar-data
_SEC_MAPPING_SOURCE_URL_STOCKS: Final[
    str
] = "https://www.sec.gov/files/company_tickers_exchange.json"
_SEC_MAPPING_SOURCE_URL_MUTUAL_FUNDS: Final[
    str
] = "https://www.sec.gov/files/company_tickers_mf.json"


class BaseRetriever(metaclass=ABCMeta):
    @property
    @abstractmethod
    def source_url(self) -> Final[str]:
        pass

    @abstractmethod
    def transform(self) -> Dict[str, str]:
        pass


class StockRetriever(BaseRetriever):
    @property
    def source_url(self) -> Final[str]:
        return _SEC_MAPPING_SOURCE_URL_STOCKS

    def transform(
        self,
        field_indices: FieldIndices,
        company_data: List[Union[int, str]],
    ) -> Dict[str, str]:
        cik = str(company_data[field_indices["cik"]])
        ticker = str(company_data[field_indices["ticker"]])
        name = str(company_data[field_indices["name"]])
        exchange = str(company_data[field_indices["exchange"]])
        return {
            "CIK": cik.zfill(10),
            "Ticker": ticker.upper(),
            "Company Name": name.title(),
            "Exchange": exchange,
        }


class MutualFundRetriever(BaseRetriever):
    @property
    def source_url(self) -> Final[str]:
        return _SEC_MAPPING_SOURCE_URL_MUTUAL_FUNDS

    def transform(
        self,
        field_indices: FieldIndices,
        company_data: List[Union[int, str]],
    ) -> Dict[str, str]:
        cik = str(company_data[field_indices["cik"]])
        seriesId = str(company_data[field_indices["seriesId"]])
        classId = str(company_data[field_indices["classId"]])
        symbol = str(company_data[field_indices["symbol"]])
        return {
            "CIK": cik.zfill(10),
            "Ticker": symbol,
            "Series ID": seriesId,
            "Class ID": classId,
        }
