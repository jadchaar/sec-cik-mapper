from pathlib import Path
from typing import Dict

import pandas as pd

from sec_cik_mapper import StockMapper


def test_stock_mapper_initialization(stock_mapper: StockMapper):
    df = stock_mapper.raw_dataframe

    # Verify dataframe rows
    assert len(df) > 0

    # Verify dataframe columns
    df_columns = list(df.columns)
    assert len(df_columns) == 4
    assert "CIK" in df_columns
    assert "Ticker" in df_columns
    assert "Name" in df_columns
    assert "Exchange" in df_columns

    validate_dataframe_content(df)


def validate_dataframe_content(df: pd.DataFrame):
    for cik, ticker, company, exchange in zip(
        df["CIK"], df["Ticker"], df["Name"], df["Exchange"]
    ):
        assert isinstance(cik, str) and len(cik) == 10
        assert isinstance(ticker, str) and len(ticker) > 0
        assert isinstance(company, str) and len(company) > 0
        # SEC outputs blank exchanges for some stocks
        assert isinstance(exchange, str)


def test_cik_to_tickers(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    cik_to_tickers = stock_mapper.cik_to_tickers
    assert len(cik_to_tickers) == stock_mapper.raw_dataframe.CIK.nunique()

    # Deal with CIKs mapping to multiple tickers
    num_tickers = 0
    for cik, tickers in cik_to_tickers.items():
        assert isinstance(tickers, set)
        num_tickers += len(tickers)
        assert len(cik) == 10

    assert num_tickers == len(stock_mapper.raw_dataframe.CIK)

    ticker = apple_stock["ticker"]
    cik = apple_stock["cik"]
    assert cik in cik_to_tickers
    assert ticker in cik_to_tickers[cik]


def test_ticker_to_cik(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    ticker_to_cik = stock_mapper.ticker_to_cik
    assert len(ticker_to_cik) == len(stock_mapper.raw_dataframe)

    ticker = apple_stock["ticker"]
    cik = apple_stock["cik"]
    assert ticker in ticker_to_cik
    assert len(ticker_to_cik[ticker]) == 10
    assert ticker_to_cik[ticker] == cik


def test_cik_to_company_name(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    cik_to_company_name = stock_mapper.cik_to_company_name
    assert len(cik_to_company_name) == stock_mapper.raw_dataframe.CIK.nunique()

    cik = apple_stock["cik"]
    name = apple_stock["name"]
    assert cik in cik_to_company_name
    assert cik_to_company_name[cik] == name


def test_ticker_to_company_name(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    ticker_to_company_name = stock_mapper.ticker_to_company_name
    assert len(ticker_to_company_name) == len(stock_mapper.raw_dataframe)

    ticker = apple_stock["ticker"]
    name = apple_stock["name"]
    assert ticker in ticker_to_company_name
    assert ticker_to_company_name[ticker] == name


def test_ticker_to_exchange(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    ticker_to_exchange = stock_mapper.ticker_to_exchange
    ticker_series = stock_mapper.raw_dataframe["Ticker"]
    exchange_series = stock_mapper.raw_dataframe["Exchange"]
    num_blank = (
        ticker_series[ticker_series == ""].count()
        + exchange_series[exchange_series == ""].count()
    )
    assert len(ticker_to_exchange) == len(stock_mapper.raw_dataframe) - num_blank

    ticker = apple_stock["ticker"]
    exchange = apple_stock["exchange"]
    assert ticker in ticker_to_exchange
    assert ticker_to_exchange[ticker] == exchange


def test_exchange_to_tickers(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    exchange_to_tickers = stock_mapper.exchange_to_tickers
    exchange_series = stock_mapper.raw_dataframe["Exchange"]
    assert len(exchange_to_tickers) == len(
        exchange_series[exchange_series != ""].unique()
    )

    ticker = apple_stock["ticker"]
    exchange = apple_stock["exchange"]
    assert exchange in exchange_to_tickers
    assert isinstance(exchange_to_tickers[exchange], set)
    assert ticker in exchange_to_tickers[exchange]


def test_cik_to_exchange(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    cik_to_exchange = stock_mapper.cik_to_exchange
    df = stock_mapper.raw_dataframe
    assert len(cik_to_exchange) == df[df["Exchange"] != ""]["CIK"].nunique()

    cik = apple_stock["cik"]
    exchange = apple_stock["exchange"]
    assert cik in cik_to_exchange
    assert cik_to_exchange[cik] == exchange


def test_exchange_to_ciks(stock_mapper: StockMapper, apple_stock: Dict[str, str]):
    exchange_to_ciks = stock_mapper.exchange_to_ciks
    df = stock_mapper.raw_dataframe
    assert len(exchange_to_ciks) == df[df["Exchange"] != ""]["Exchange"].nunique()

    cik = apple_stock["cik"]
    exchange = apple_stock["exchange"]
    assert exchange in exchange_to_ciks
    assert cik in exchange_to_ciks[exchange]


def test_raw_dataframe(stock_mapper: StockMapper):
    assert stock_mapper.raw_dataframe.equals(stock_mapper.mapping_metadata)


def test_save_metadata_to_csv(stock_mapper: StockMapper, tmp_path: Path):
    tmp_csv_path = tmp_path / "temp.csv"
    stock_mapper.save_metadata_to_csv(tmp_csv_path)
    assert tmp_csv_path.exists()
    df = pd.read_csv(tmp_csv_path)
    assert len(df) == len(stock_mapper.raw_dataframe)
