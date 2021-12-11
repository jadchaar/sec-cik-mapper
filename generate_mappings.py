import json
from pathlib import Path

from cik_mapper import CIKMapper


def generate():
    cikMapper = CIKMapper()
    auto_generated_mappings_path = Path("auto_generated_mappings")

    csv_path = auto_generated_mappings_path / "cik_mapping.csv"
    cikMapper.save_metadata_to_csv(csv_path)

    cik_to_ticker_path = auto_generated_mappings_path / "cik_to_ticker.json"
    cik_to_ticker_mapping = cikMapper.get_cik_to_ticker_mapping()
    with cik_to_ticker_path.open("w", encoding="utf-8") as f:
        json.dump(
            cik_to_ticker_mapping, f, ensure_ascii=False, sort_keys=True, indent=2
        )

    ticker_to_cik_path = auto_generated_mappings_path / "ticker_to_cik.json"
    ticker_to_cik_mapping = cikMapper.get_ticker_to_cik_mapping()
    with ticker_to_cik_path.open("w", encoding="utf-8") as f:
        json.dump(
            ticker_to_cik_mapping, f, ensure_ascii=False, sort_keys=True, indent=2
        )

    cik_to_title_path = auto_generated_mappings_path / "cik_to_title.json"
    cik_to_title_mapping = cikMapper.get_cik_to_title_mapping()
    with cik_to_title_path.open("w", encoding="utf-8") as f:
        json.dump(cik_to_title_mapping, f, ensure_ascii=False, sort_keys=True, indent=2)

    ticker_to_title_path = auto_generated_mappings_path / "ticker_to_title.json"
    ticker_to_title_mapping = cikMapper.get_ticker_to_title_mapping()
    with ticker_to_title_path.open("w", encoding="utf-8") as f:
        json.dump(
            ticker_to_title_mapping, f, ensure_ascii=False, sort_keys=True, indent=2
        )


if __name__ == "__main__":
    generate()
