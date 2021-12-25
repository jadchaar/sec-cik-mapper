"""StockMapper usage example. Assumes current working directory
is the examples folder.
"""

import sys

sys.path.append("..")

from pathlib import Path  # noqa: E402

from sec_cik_mapper import StockMapper  # noqa: E402

FILENAME = "example_mappings.csv"
N = 3

mapper = StockMapper()


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

cik_to_company_name = mapper.cik_to_company_name
print_n_items(cik_to_company_name)

ticker_to_company_name = mapper.ticker_to_company_name
print_n_items(ticker_to_company_name)

ticker_to_exchange = mapper.ticker_to_exchange
print_n_items(ticker_to_exchange)

exchange_to_tickers = mapper.exchange_to_tickers
print_n_items(exchange_to_tickers)

cik_to_exchange = mapper.cik_to_exchange
print_n_items(cik_to_exchange)

exchange_to_ciks = mapper.exchange_to_ciks
print_n_items(exchange_to_ciks)

print(mapper.raw_dataframe)
