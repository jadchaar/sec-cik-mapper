import json
from pathlib import Path

import pandas as pd

from sec_cik_mapper import CIKMapper


def test_mapper_initialization(mapper: CIKMapper):
    df = mapper.mapping_metadata

    # Verify dataframe rows
    assert len(df) > 0

    # Verify dataframe columns
    df_columns = list(df.columns)
    assert len(df_columns) == 3
    assert "CIK" in df_columns
    assert "Ticker" in df_columns
    assert "Company Name" in df_columns

    validate_dataframe_content(df)


def validate_dataframe_content(df):
    for cik, ticker, company in zip(df["CIK"], df["Ticker"], df["Company Name"]):
        assert isinstance(cik, str) and len(cik) == 10
        assert isinstance(cik, str) and len(ticker) > 0
        assert isinstance(company, str) and len(company) > 0


def test_get_cik_to_ticker_mapping(mapper: CIKMapper):
    cik_to_ticker_mapping = mapper.get_cik_to_ticker_mapping()
    assert len(cik_to_ticker_mapping) == mapper.mapping_metadata.CIK.nunique()

    # Deal with CIKs mapping to multiple tickers
    num_tickers = 0
    for tickers in cik_to_ticker_mapping.values():
        assert isinstance(tickers, list)
        num_tickers += len(tickers)

    assert num_tickers == len(mapper.mapping_metadata.CIK)


def test_get_ticker_to_cik_mapping(mapper: CIKMapper):
    ticker_to_cik_mapping = mapper.get_ticker_to_cik_mapping()
    assert len(ticker_to_cik_mapping) == len(mapper.mapping_metadata)


def test_get_cik_to_company_name_mapping(mapper: CIKMapper):
    cik_to_company_name_mapping = mapper.get_cik_to_company_name_mapping()
    assert len(cik_to_company_name_mapping) == mapper.mapping_metadata.CIK.nunique()


def test_get_get_ticker_to_company_name_mapping(mapper: CIKMapper):
    ticker_to_company_name_mapping = mapper.get_ticker_to_company_name_mapping()
    assert len(ticker_to_company_name_mapping) == len(mapper.mapping_metadata)


def test_save_metadata_to_csv(mapper: CIKMapper, tmp_path: Path):
    tmp_csv_path = tmp_path / "temp.csv"
    mapper.save_metadata_to_csv(tmp_csv_path)
    assert tmp_csv_path.exists()
    df = pd.read_csv(tmp_csv_path)
    assert len(df) == len(mapper.mapping_metadata)


def test_validate_auto_generated_mappings(
    mapper: CIKMapper, auto_generated_mappings_path: Path
):
    validate_num_files(auto_generated_mappings_path)
    validate_csv(mapper, auto_generated_mappings_path)
    validate_json(mapper, auto_generated_mappings_path)


def validate_num_files(auto_generated_mappings_path: Path):
    all_generated_mapping_files = list(auto_generated_mappings_path.glob("*"))
    assert len(all_generated_mapping_files) == 5

    generated_mapping_csv_files = list(auto_generated_mappings_path.glob("*.csv"))
    assert len(generated_mapping_csv_files) == 1

    generated_mapping_json_files = list(auto_generated_mappings_path.glob("*.json"))
    assert len(generated_mapping_json_files) == 4


def validate_csv(mapper: CIKMapper, auto_generated_mappings_path: Path):
    csv_path = auto_generated_mappings_path / "cik_mapping.csv"
    assert csv_path.exists()
    df = pd.read_csv(csv_path)
    assert len(df) == len(mapper.mapping_metadata)


def validate_json(mapper: CIKMapper, auto_generated_mappings_path: Path):
    json_path = auto_generated_mappings_path / "cik_to_ticker.json"
    with json_path.open() as f:
        json_obj = json.load(f)
    assert len(json_obj) == mapper.mapping_metadata.CIK.nunique()

    json_path = auto_generated_mappings_path / "cik_to_company_name.json"
    with json_path.open() as f:
        json_obj = json.load(f)
    assert len(json_obj) == mapper.mapping_metadata.CIK.nunique()

    json_path = auto_generated_mappings_path / "ticker_to_cik.json"
    with json_path.open() as f:
        json_obj = json.load(f)
    assert len(json_obj) == len(mapper.mapping_metadata)

    json_path = auto_generated_mappings_path / "ticker_to_company_name.json"
    with json_path.open() as f:
        json_obj = json.load(f)
    assert len(json_obj) == len(mapper.mapping_metadata)
