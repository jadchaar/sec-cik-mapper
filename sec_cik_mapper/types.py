from typing import Dict, List, Set, Union

from typing_extensions import Literal, TypedDict


class StockFieldIndices(TypedDict):
    cik: int
    ticker: int
    name: int
    exchange: int


class MutualFundFieldIndices(TypedDict):
    cik: int
    symbol: int
    seriesId: int
    classId: int


FieldIndices = Union[StockFieldIndices, MutualFundFieldIndices]

StockFields = Literal["cik", "name", "ticker", "exchange"]

MutualFundFields = Literal["cik", "seriesId", "classId", "symbol"]

Fields = Union[StockFields, MutualFundFields]

CompanyData = List[List[Union[int, str]]]

KeyToValueSet = Dict[str, Set[str]]
