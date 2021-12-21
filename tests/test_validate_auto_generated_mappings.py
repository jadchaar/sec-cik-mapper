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
