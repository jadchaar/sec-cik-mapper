import sys

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import List, Literal, TypedDict, Union
else:
    from typing import List, Literal, TypedDict, Union  # pragma: no cover


class StockFieldIndices(TypedDict):
    cik: int
    ticker: int
    name: int
    exchange: int


class MutualFundFieldIndices(TypedDict):
    cik: int
    ticker: int
    seriesId: int
    classId: int


FieldIndices = Union[StockFieldIndices, MutualFundFieldIndices]


StockFields = Literal["cik", "name", "ticker", "exchange"]


MutualFundFields = Literal["cik", "seriesId", "classId", "symbol"]


Fields = Union[StockFields, MutualFundFields]

CompanyData = List[List[Union[int, str]]]
