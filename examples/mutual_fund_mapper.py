"""MutualFundMapper usage example. Assumes current working directory
is the examples folder.
"""

import sys

sys.path.append("..")

from pathlib import Path  # noqa: E402

from sec_cik_mapper import MutualFundMapper  # noqa: E402

FILENAME = "example_mappings.csv"
N = 3

mapper = MutualFundMapper()


def print_n_items(_dict):
    first_n_items = list(_dict.items())[:N]
    new_dict = {}
    for k, v in first_n_items:
        if isinstance(v, set):
            # Get first N items from list then convert back to set
            # Required since sets are not subscriptable
            new_dict[k] = set(list(v)[:N])
        else:
            new_dict[k] = v
    print(new_dict)
    print("====================")


csv_path = Path(FILENAME)
mapper.save_metadata_to_csv(csv_path)

cik_to_tickers = mapper.cik_to_tickers
print_n_items(cik_to_tickers)

ticker_to_cik = mapper.ticker_to_cik
print_n_items(ticker_to_cik)

cik_to_series_ids = mapper.cik_to_series_ids
print_n_items(cik_to_series_ids)

ticker_to_series_id = mapper.ticker_to_series_id
print_n_items(ticker_to_series_id)

series_id_to_cik = mapper.series_id_to_cik
print_n_items(series_id_to_cik)

series_id_to_tickers = mapper.series_id_to_tickers
print_n_items(series_id_to_tickers)

series_id_to_class_ids = mapper.series_id_to_class_ids
print_n_items(series_id_to_class_ids)

ticker_to_class_id = mapper.ticker_to_class_id
print_n_items(ticker_to_class_id)

cik_to_class_ids = mapper.cik_to_class_ids
print_n_items(cik_to_class_ids)

class_id_to_cik = mapper.class_id_to_cik
print_n_items(class_id_to_cik)

class_id_to_ticker = mapper.class_id_to_ticker
print_n_items(class_id_to_ticker)

print(mapper.raw_dataframe)
