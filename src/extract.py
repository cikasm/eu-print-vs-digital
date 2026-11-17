import json
import os
import requests

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"

# Only the book-related indicators from isoc_ec_ibgs (print vs digital).
# Note: Eurostat changed the digital indicators in 2024 (see notes.md).
BOOK_INDICATORS = [
    "I_BBOOKNLG",   # PRINT:   printed books, magazines or newspapers (2020+)
    "I_BBOOKNLS",   # DIGITAL: e-books, online magazines/newspapers (until 2023)
    "I_BBOOK2",     # DIGITAL: e-books or audio books as downloads (2024+)
    "I_BBOOKNLS2",  # DIGITAL: paid subscriptions to online news/magazines (2024+)
]

# Every Eurostat dataset the pipeline downloads: code -> filters
DATASETS = {
    "isoc_ec_ibgs": {"indic_is": BOOK_INDICATORS},        # online book purchases
    "ilc_scp27": None,                                     # books read (survey)
    "prc_hicp_midx": {                                     # prices
        # books, stationery, all items (CP0953 is "misc. printed matter", not stationery)
        # This series uses the old COICOP codes and stops at 2025-12 (see notes.md).
        "coicop": ["CP0951", "CP0954", "CP00"],
        "unit": "I15",                                     # index where 2015 = 100
    },
}


def extract_eurostat(dataset_code, filters=None):
    """Download any Eurostat dataset and save it untouched."""
    params = {"lang": "EN"}
    if filters:
        params.update(filters)

    print(f"Downloading {dataset_code}...")
    response = requests.get(BASE_URL + dataset_code, params=params, timeout=120)
    response.raise_for_status()

    os.makedirs("data/raw", exist_ok=True)
    path = f"data/raw/{dataset_code}.json"
    with open(path, "w") as f:
        json.dump(response.json(), f)
    print(f"Saved {path}")
    return path


def extract_all_eurostat():
    """Download every dataset in DATASETS."""
    for code, filters in DATASETS.items():
        extract_eurostat(code, filters)


if __name__ == "__main__":
    extract_all_eurostat()
