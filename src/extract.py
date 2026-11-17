import requests   # tool for calling APIs
import json       # tool for saving JSON files

# 1. The address of the data we want
url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_ec_ibgs"

# 2. Extra options: which country, which language
options = {"geo": "DE", "lang": "EN"}

# 3. Call the API 
response = requests.get(url, params=options, timeout=60)

# 4. Stop with an error if something went wrong
response.raise_for_status()

# 5. Turn the reply into Python data
data = response.json()

# 6. Save it, untouched, into data/raw/
with open("data/raw/book_purchases_DE.json", "w") as f:
    json.dump(data, f, indent=2)

print("Done! Saved the data.")