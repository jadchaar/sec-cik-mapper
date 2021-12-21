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
