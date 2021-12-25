"""Generate curl commands for docs."""

import csv
import sys
from pathlib import Path

import requests

GENERATED_MAPPINGS_PATH = Path("../auto_generated_mappings")

if not GENERATED_MAPPINGS_PATH.exists():
    print(f"Folder does not exist: {GENERATED_MAPPINGS_PATH.resolve()}")
    print("Ensure that your current working directory is the scripts folder.")
    sys.exit(1)

BASE_URL_GH_RAW = "https://raw.githubusercontent.com/jadchaar/sec-cik-mapper/main/auto_generated_mappings"  # noqa: B950
BASE_URL_JSDELIVR = (
    "https://cdn.jsdelivr.net/gh/jadchaar/sec-cik-mapper@main/auto_generated_mappings"
)
CURL_TEMPLATE = "curl {0} -O"

RST_TEMPLATE = """
**GitHub**

.. code-block:: console

{0}

**jsDelivr**

.. code-block:: console

{1}
"""


def generate_urls():
    print("Generating URLs...", end=" ")
    url_map = {
        "gh": [],
        "jsdelivr": [],
    }
    for mapping_type in GENERATED_MAPPINGS_PATH.glob("*"):
        mapping_folder = GENERATED_MAPPINGS_PATH / mapping_type
        for file_path in mapping_folder.glob("*"):
            full_url_gh_raw = f"{BASE_URL_GH_RAW}/{mapping_type.name}/{file_path.name}"
            full_url_jsdelivr = (
                f"{BASE_URL_JSDELIVR}/{mapping_type.name}/{file_path.name}"
            )
            validate_urls([full_url_gh_raw, full_url_jsdelivr])
            url_map["gh"].append(full_url_gh_raw)
            url_map["jsdelivr"].append(full_url_jsdelivr)
    print("✓")
    return url_map


def print_curl_commands(url_map):
    print("Generating RST output...", end=" ")
    output_gh = []
    for gh_url in url_map["gh"]:
        curl_cmd = CURL_TEMPLATE.format(gh_url)
        output_gh.append(f"\t$ {curl_cmd}")

    output_jsdelivr = []
    for jsdelivr_url in url_map["jsdelivr"]:
        curl_cmd = CURL_TEMPLATE.format(jsdelivr_url)
        output_jsdelivr.append(f"\t$ {curl_cmd}")

    formatted_rst = RST_TEMPLATE.format(
        "\n".join(output_gh), "\n".join(output_jsdelivr)
    )
    print("✓")
    print(formatted_rst)


def validate_urls(urls):
    """Validate URLs by making a GET request, checking status code, and attempting to parse."""
    for url in urls:
        resp = requests.get(url)
        resp.raise_for_status()
        if url.endswith(".json"):
            # Parse JSON
            assert resp.json() is not None, f"Invalid URL: {url}"
        else:
            # Parse CSV
            assert csv.DictReader(resp.iter_lines()) is not None, f"Invalid URL: {url}"


if __name__ == "__main__":
    url_map = generate_urls()
    print_curl_commands(url_map)
