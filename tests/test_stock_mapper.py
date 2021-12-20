from pathlib import Path

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


def validate_dataframe_content(df):
    for cik, ticker, company, exchange in zip(
        df["CIK"], df["Ticker"], df["Name"], df["Exchange"]
    ):
        assert isinstance(cik, str) and len(cik) == 10
        assert isinstance(cik, str) and len(ticker) > 0
        assert isinstance(company, str) and len(company) > 0
        assert isinstance(exchange, str) and len(exchange) > 0


def test_cik_to_ticker(stock_mapper: StockMapper):
    cik_to_tickers = stock_mapper.cik_to_tickers
    assert len(cik_to_tickers) == stock_mapper.raw_dataframe.CIK.nunique()

    # Deal with CIKs mapping to multiple tickers
    num_tickers = 0
    for tickers in cik_to_tickers.values():
        assert isinstance(tickers, set)
        num_tickers += len(tickers)

    assert num_tickers == len(stock_mapper.raw_dataframe.CIK)


def test_ticker_to_cik(stock_mapper: StockMapper):
    ticker_to_cik = stock_mapper.ticker_to_cik
    assert len(ticker_to_cik) == len(stock_mapper.raw_dataframe)


def test_cik_to_company_name(stock_mapper: StockMapper):
    cik_to_company_name = stock_mapper.cik_to_company_name
    assert len(cik_to_company_name) == stock_mapper.raw_dataframe.CIK.nunique()


def test_ticker_to_company_name(stock_mapper: StockMapper):
    ticker_to_company_name = stock_mapper.ticker_to_company_name
    assert len(ticker_to_company_name) == len(stock_mapper.raw_dataframe)


def test_save_metadata_to_csv(stock_mapper: StockMapper, tmp_path: Path):
    tmp_csv_path = tmp_path / "temp.csv"
    stock_mapper.save_metadata_to_csv(tmp_csv_path)
    assert tmp_csv_path.exists()
    df = pd.read_csv(tmp_csv_path)
    assert len(df) == len(stock_mapper.raw_dataframe)


# def test_validate_auto_generated_mappings(
#     stock_mapper: StockMapper, auto_generated_mappings_path: Path
# ):
#     validate_num_files(auto_generated_mappings_path)
#     validate_csv(mapper, auto_generated_mappings_path)
#     validate_json(mapper, auto_generated_mappings_path)


# def validate_num_files(auto_generated_mappings_path: Path):
#     all_generated_mapping_files = list(auto_generated_mappings_path.glob("*"))
#     assert len(all_generated_mapping_files) == 5

#     generated_mapping_csv_files = list(auto_generated_mappings_path.glob("*.csv"))
#     assert len(generated_mapping_csv_files) == 1

#     generated_mapping_json_files = list(auto_generated_mappings_path.glob("*.json"))
#     assert len(generated_mapping_json_files) == 4


# def validate_csv(stock_mapper: StockMapper, auto_generated_mappings_path: Path):
#     csv_path = auto_generated_mappings_path / "cik_mapping.csv"
#     assert csv_path.exists()
#     df = pd.read_csv(csv_path)
#     assert len(df) == len(mapper.mapping_metadata)


# def validate_json(stock_mapper: StockMapper, auto_generated_mappings_path: Path):
#     json_path = auto_generated_mappings_path / "cik_to_ticker.json"
#     with json_path.open() as f:
#         json_obj = json.load(f)
#     assert len(json_obj) == mapper.mapping_metadata.CIK.nunique()

#     json_path = auto_generated_mappings_path / "cik_to_company_name.json"
#     with json_path.open() as f:
#         json_obj = json.load(f)
#     assert len(json_obj) == mapper.mapping_metadata.CIK.nunique()

#     json_path = auto_generated_mappings_path / "ticker_to_cik.json"
#     with json_path.open() as f:
#         json_obj = json.load(f)
#     assert len(json_obj) == len(mapper.mapping_metadata)

#     json_path = auto_generated_mappings_path / "ticker_to_company_name.json"
#     with json_path.open() as f:
#         json_obj = json.load(f)
#     assert len(json_obj) == len(mapper.mapping_metadata)
