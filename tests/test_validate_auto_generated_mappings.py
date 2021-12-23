import json
from pathlib import Path

import pandas as pd

from sec_cik_mapper import MutualFundMapper, StockMapper

NUM_STOCK_FILES = 9
NUM_CSV_FILES = 1
NUM_MUTUAL_FUND_FILES = 12


def test_validate_num_files_stocks(
    stock_mapper: StockMapper, generated_mappings_path_stocks: Path
):
    all_files = list(generated_mappings_path_stocks.glob("*"))
    assert len(all_files) == NUM_STOCK_FILES

    csv_files = list(generated_mappings_path_stocks.glob("*.csv"))
    assert len(csv_files) == NUM_CSV_FILES

    json_files = list(generated_mappings_path_stocks.glob("*.json"))
    assert len(json_files) == NUM_STOCK_FILES - NUM_CSV_FILES


def test_validate_num_files_mutual_funds(
    mutual_fund_mapper: MutualFundMapper, generated_mappings_path_mutual_funds: Path
):
    all_files = list(generated_mappings_path_mutual_funds.glob("*"))
    assert len(all_files) == NUM_MUTUAL_FUND_FILES

    csv_files = list(generated_mappings_path_mutual_funds.glob("*.csv"))
    assert len(csv_files) == NUM_CSV_FILES

    json_files = list(generated_mappings_path_mutual_funds.glob("*.json"))
    assert len(json_files) == NUM_MUTUAL_FUND_FILES - NUM_CSV_FILES


def test_validate_csv_stocks(
    stock_mapper: StockMapper, generated_mappings_path_stocks: Path
):
    csv_path = generated_mappings_path_stocks / "mappings.csv"
    assert csv_path.exists()

    df = pd.read_csv(csv_path)
    assert len(df) == len(stock_mapper.raw_dataframe)


def test_validate_csv_mutual_funds(
    mutual_fund_mapper: MutualFundMapper, generated_mappings_path_mutual_funds: Path
):
    csv_path = generated_mappings_path_mutual_funds / "mappings.csv"
    assert csv_path.exists()

    df = pd.read_csv(csv_path)
    assert len(df) == len(mutual_fund_mapper.raw_dataframe)


def test_validate_json(
    generated_mappings_path_stocks: Path, generated_mappings_path_mutual_funds: Path
):
    generated_mappings_paths = list(
        generated_mappings_path_stocks.glob("*.json")
    ) + list(generated_mappings_path_mutual_funds.glob("*.json"))
    assert (
        len(generated_mappings_paths)
        == NUM_MUTUAL_FUND_FILES + NUM_STOCK_FILES - 2 * NUM_CSV_FILES
    )

    for json_path in generated_mappings_paths:
        with json_path.open() as f:
            json_obj = json.load(f)
        assert len(json_obj) > 0
