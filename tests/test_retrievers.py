from typing import List, Union

import pytest

from sec_cik_mapper import BaseRetriever, MutualFundRetriever, StockRetriever, types


def test_base_retriever_instantiation_type_error():
    # BaseRetriever cannot be directly instantiated
    with pytest.raises(TypeError):
        _ = BaseRetriever()


def test_retriever_source_urls(
    stock_retriever: StockRetriever, mutual_fund_retriever: MutualFundRetriever
):
    assert len(stock_retriever.source_url) > 0
    assert len(mutual_fund_retriever.source_url) > 0
    assert stock_retriever.source_url != mutual_fund_retriever.source_url


def test_clean_ticker(stock_retriever: StockRetriever):
    # Remove non-alphanumeric characters (except dash)
    assert stock_retriever._clean_ticker("(NWAGX)") == "NWAGX"

    # Keep dashes
    assert stock_retriever._clean_ticker("BRK-A") == "BRK-A"

    # Keep numeric characters
    assert stock_retriever._clean_ticker("FAKE8") == "FAKE8"

    # Make all caps
    assert stock_retriever._clean_ticker("tIcKeR") == "TICKER"


def test_stock_retriever_transform(stock_retriever: StockRetriever):
    field_indices: types.FieldIndices = {
        "cik": 0,
        "name": 1,
        "ticker": 2,
        "exchange": 3,
    }
    company_data: List[Union[int, str]] = [320193, "Apple Inc.", "AAPL", "Nasdaq"]
    expected = {
        "CIK": "0000320193",
        "Ticker": "AAPL",
        "Name": "Apple Inc.",
        "Exchange": "Nasdaq",
    }
    assert stock_retriever.transform(field_indices, company_data) == expected


def test_mutual_fund_retriever_transform(mutual_fund_retriever: MutualFundRetriever):
    field_indices: types.FieldIndices = {
        "cik": 0,
        "seriesId": 1,
        "classId": 2,
        "symbol": 3,
    }
    company_data: List[Union[int, str]] = [2110, "S000009184", "C000024954", "LACAX"]
    expected = {
        "CIK": "0000002110",
        "Ticker": "LACAX",
        "Series ID": "S000009184",
        "Class ID": "C000024954",
    }
    assert mutual_fund_retriever.transform(field_indices, company_data) == expected
