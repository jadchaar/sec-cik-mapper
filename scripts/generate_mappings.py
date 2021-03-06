"""Fetch and transform mapping data from SEC."""

import json
import sys
from pathlib import Path

sys.path.append("..")

from sec_cik_mapper import MutualFundMapper, StockMapper  # noqa: E402

mappings_path = Path("../mappings")


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        # Convert to list before JSON serialization
        if isinstance(obj, set):
            return sorted(list(obj))
        return json.JSONEncoder.default(self, obj)


def write_json_to_disk(path, obj):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, sort_keys=True, cls=ComplexEncoder)


def get_functions_to_execute(mapper):
    func_names = dir(mapper)
    func_names_to_ignore = {"save_metadata_to_csv"}
    return list(
        filter(
            lambda func: not func.startswith("_")
            and "_to_" in func
            and func not in func_names_to_ignore,
            func_names,
        )
    )


def execute_and_save_to_disk(save_path, mapper):
    csv_path = save_path / "mappings.csv"
    functions_to_execute = get_functions_to_execute(mapper)
    identifier = type(mapper).__name__

    print(f"[{identifier}]", csv_path.name, end=" ")
    mapper.save_metadata_to_csv(csv_path)
    print("✓")

    for func in functions_to_execute:
        json_save_path = save_path / f"{func}.json"
        print(f"[{identifier}]", json_save_path.name, end=" ")
        output = getattr(mapper, func)
        write_json_to_disk(json_save_path, output)
        print("✓")


def generate_stock_mappings():
    save_path = mappings_path / "stocks"
    mapper = StockMapper()
    execute_and_save_to_disk(save_path, mapper)


def generate_mutual_fund_mappings():
    save_path = mappings_path / "mutual_funds"
    mapper = MutualFundMapper()
    execute_and_save_to_disk(save_path, mapper)


if __name__ == "__main__":
    generate_stock_mappings()
    print("=" * 100)
    generate_mutual_fund_mappings()
