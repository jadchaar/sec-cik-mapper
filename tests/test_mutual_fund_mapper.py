from typing import Dict

import pandas as pd

from sec_cik_mapper import MutualFundMapper


def test_mutual_fund_mapper_initialization(mutual_fund_mapper: MutualFundMapper):
    df = mutual_fund_mapper.raw_dataframe

    # Verify dataframe rows
    assert len(df) > 0

    # Verify dataframe columns
    df_columns = list(df.columns)
    assert len(df_columns) == 4
    assert "CIK" in df_columns
    assert "Ticker" in df_columns
    assert "Series ID" in df_columns
    assert "Class ID" in df_columns

    validate_dataframe_content(df)


def validate_dataframe_content(df: pd.DataFrame):
    for cik, ticker, seriesId, classId in zip(
        df["CIK"], df["Ticker"], df["Series ID"], df["Class ID"]
    ):
        assert isinstance(cik, str) and len(cik) == 10
        # SEC outputs blank tickers for some mutual funds
        assert isinstance(ticker, str)
        assert isinstance(seriesId, str) and len(seriesId) > 0
        assert isinstance(classId, str) and len(classId) > 0


def test_cik_to_tickers(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    cik_to_tickers = mutual_fund_mapper.cik_to_tickers
    assert len(cik_to_tickers) == mutual_fund_mapper.raw_dataframe.CIK.nunique()

    # Deal with CIKs mapping to multiple tickers
    num_tickers = 0
    for cik, tickers in cik_to_tickers.items():
        assert isinstance(tickers, set)
        num_tickers += len(tickers)
        assert len(cik) == 10

    df = mutual_fund_mapper.raw_dataframe.Ticker
    assert num_tickers == df[df != ""].nunique()

    ticker = vtsax_mutual_fund["ticker"]
    cik = vtsax_mutual_fund["cik"]
    assert cik in cik_to_tickers
    assert ticker in cik_to_tickers[cik]


def test_ticker_to_cik(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    ticker_to_cik = mutual_fund_mapper.ticker_to_cik
    df = mutual_fund_mapper.raw_dataframe.Ticker
    assert len(ticker_to_cik) == df[df != ""].nunique()

    ticker = vtsax_mutual_fund["ticker"]
    cik = vtsax_mutual_fund["cik"]
    assert ticker in ticker_to_cik
    assert len(ticker_to_cik[ticker]) == 10
    assert ticker_to_cik[ticker] == cik


def test_cik_to_series_ids(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    cik_to_series_ids = mutual_fund_mapper.cik_to_series_ids
    assert len(cik_to_series_ids) == mutual_fund_mapper.raw_dataframe.CIK.nunique()

    series_id = vtsax_mutual_fund["seriesId"]
    cik = vtsax_mutual_fund["cik"]
    assert cik in cik_to_series_ids
    assert series_id in cik_to_series_ids[cik]


def test_ticker_to_series_id(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    ticker_to_series_id = mutual_fund_mapper.ticker_to_series_id
    df = mutual_fund_mapper.raw_dataframe.Ticker
    assert len(ticker_to_series_id) == df[df != ""].nunique()

    ticker = vtsax_mutual_fund["ticker"]
    series_id = vtsax_mutual_fund["seriesId"]
    assert ticker in ticker_to_series_id
    assert ticker_to_series_id[ticker] == series_id


def test_series_id_to_cik(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    series_id_to_cik = mutual_fund_mapper.series_id_to_cik
    assert (
        len(series_id_to_cik) == mutual_fund_mapper.raw_dataframe["Series ID"].nunique()
    )

    cik = vtsax_mutual_fund["cik"]
    series_id = vtsax_mutual_fund["seriesId"]
    assert series_id in series_id_to_cik
    assert series_id_to_cik[series_id] == cik


def test_series_id_to_tickers(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    series_id_to_tickers = mutual_fund_mapper.series_id_to_tickers
    df = mutual_fund_mapper.raw_dataframe
    ticker_df = mutual_fund_mapper.raw_dataframe["Ticker"]
    assert len(series_id_to_tickers) == df[ticker_df != ""]["Series ID"].nunique()

    ticker = vtsax_mutual_fund["ticker"]
    series_id = vtsax_mutual_fund["seriesId"]
    assert series_id in series_id_to_tickers
    assert ticker in series_id_to_tickers[series_id]


def test_series_id_to_class_ids(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    series_id_to_class_ids = mutual_fund_mapper.series_id_to_class_ids
    assert (
        len(series_id_to_class_ids)
        == mutual_fund_mapper.raw_dataframe["Series ID"].nunique()
    )

    class_id = vtsax_mutual_fund["classId"]
    series_id = vtsax_mutual_fund["seriesId"]
    assert series_id in series_id_to_class_ids
    assert class_id in series_id_to_class_ids[series_id]


def test_ticker_to_class_id(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    ticker_to_class_id = mutual_fund_mapper.ticker_to_class_id
    df = mutual_fund_mapper.raw_dataframe.Ticker
    assert len(ticker_to_class_id) == df[df != ""].nunique()

    class_id = vtsax_mutual_fund["classId"]
    ticker = vtsax_mutual_fund["ticker"]
    assert ticker in ticker_to_class_id
    assert ticker_to_class_id[ticker] == class_id


def test_cik_to_class_ids(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    cik_to_class_ids = mutual_fund_mapper.cik_to_class_ids
    assert len(cik_to_class_ids) == mutual_fund_mapper.raw_dataframe.CIK.nunique()

    class_id = vtsax_mutual_fund["classId"]
    cik = vtsax_mutual_fund["cik"]
    assert cik in cik_to_class_ids
    assert class_id in cik_to_class_ids[cik]


def test_class_id_to_cik(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    class_id_to_cik = mutual_fund_mapper.class_id_to_cik
    assert (
        len(class_id_to_cik) == mutual_fund_mapper.raw_dataframe["Class ID"].nunique()
    )

    class_id = vtsax_mutual_fund["classId"]
    cik = vtsax_mutual_fund["cik"]
    assert class_id in class_id_to_cik
    assert class_id_to_cik[class_id] == cik


def test_class_id_to_ticker(
    mutual_fund_mapper: MutualFundMapper, vtsax_mutual_fund: Dict[str, str]
):
    class_id_to_ticker = mutual_fund_mapper.class_id_to_ticker
    df = mutual_fund_mapper.raw_dataframe.Ticker
    assert len(class_id_to_ticker) == df[df != ""].nunique()

    class_id = vtsax_mutual_fund["classId"]
    ticker = vtsax_mutual_fund["ticker"]
    assert class_id in class_id_to_ticker
    assert class_id_to_ticker[class_id] == ticker
