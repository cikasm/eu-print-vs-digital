import os
import time
from pytrends.exceptions import TooManyRequestsError
from pytrends.request import TrendReq

KEYWORDS = ["Kindle", "e-reader"]   # reading keywords (max 5 per request)
COUNTRIES = ["DE", "FR", "IT", "ES", "PL", "NL", "SE", "DK", "RO", "EE"]
FOLDER = "data/raw/trends"


def extract_trends():
    """Download Google Trends per country.

    Countries that already have a CSV are skipped, so Google gets fewer requests.
    To refresh everything, delete the data/raw/trends folder first.
    """
    os.makedirs(FOLDER, exist_ok=True)
    pytrends = TrendReq(hl="en-US", tz=0)
    for country in COUNTRIES:
        path = f"{FOLDER}/{country}.csv"
        if os.path.exists(path):
            print(f"Trends for {country}: already downloaded, skipping")
            continue
        print(f"Trends for {country}...")
        try:
            pytrends.build_payload(KEYWORDS, timeframe="today 5-y", geo=country)
            df = pytrends.interest_over_time()
        except TooManyRequestsError:
            # Google is blocking us. Keep what we have; run again in an hour,
            # or download the CSVs by hand from trends.google.com.
            print("Google returned 429 (too many requests). Stopping trends for now.")
            return
        df.to_csv(path)
        time.sleep(15)   # wait, so Google doesn't block us


if __name__ == "__main__":
    extract_trends()
