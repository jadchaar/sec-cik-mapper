import json
from pathlib import Path
from typing import Any

from cik_mapper import CIKMapper


def write_json_to_disk(path: Path, obj: Any):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, sort_keys=True, indent=2)


def generate():
    cikMapper = CIKMapper()
    auto_generated_mappings_path = Path("auto_generated_mappings")

    csv_path = auto_generated_mappings_path / "cik_mapping.csv"
    cikMapper.save_metadata_to_csv(csv_path)

    cik_to_ticker_path = auto_generated_mappings_path / "cik_to_ticker.json"
    cik_to_ticker_mapping = cikMapper.get_cik_to_ticker_mapping()
    write_json_to_disk(cik_to_ticker_path, cik_to_ticker_mapping)

    ticker_to_cik_path = auto_generated_mappings_path / "ticker_to_cik.json"
    ticker_to_cik_mapping = cikMapper.get_ticker_to_cik_mapping()
    write_json_to_disk(ticker_to_cik_path, ticker_to_cik_mapping)

    cik_to_title_path = auto_generated_mappings_path / "cik_to_title.json"
    cik_to_title_mapping = cikMapper.get_cik_to_title_mapping()
    write_json_to_disk(cik_to_title_path, cik_to_title_mapping)

    ticker_to_title_path = auto_generated_mappings_path / "ticker_to_title.json"
    ticker_to_title_mapping = cikMapper.get_ticker_to_title_mapping()
    write_json_to_disk(ticker_to_title_path, ticker_to_title_mapping)


if __name__ == "__main__":
    generate()
