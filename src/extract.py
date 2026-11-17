import requests   # tool for calling APIs
import json       # tool for saving JSON files

# 1. The address of the data we want
#    (Eurostat dataset: internet purchases of goods and services, 2020 onwards)
url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ec_ibgs"

# 2. Only the book-related indicators (print vs digital).
#    Note: Eurostat changed the digital indicators in 2024.
BOOK_INDICATORS = [
    "I_BBOOKNLG",   # PRINT:   printed books, magazines or newspapers (2020+)
    "I_BBOOKNLS",   # DIGITAL: e-books, online magazines/newspapers (until 2023)
    "I_BBOOK2",     # DIGITAL: e-books or audio books as downloads (2024+)
    "I_BBOOKNLS2",  # DIGITAL: paid subscriptions to online news/magazines (2024+)
]

# 3. Extra options: language + indicators (no "geo" filter = all countries)
options = {"lang": "EN", "indic_is": BOOK_INDICATORS}

# 4. Call the API
response = requests.get(url, params=options, timeout=60)

# 5. Stop with an error if something went wrong
response.raise_for_status()

# 6. Turn the reply into Python data
data = response.json()

# 7. Save it, untouched, into data/raw/
with open("data/raw/book_purchases_all.json", "w") as f:
    json.dump(data, f, indent=2)

print("Done! Saved the data.")
