import json
import pandas as pd


def jsonstat_to_df(data):
    """Turn Eurostat's JSON-stat format into a normal table."""
    dim_names = data["id"]      # e.g. ["freq", "indic_is", "unit", "geo", "time"]
    sizes = data["size"]        # e.g. [1, 4, 2, 30, 10]

    # For each dimension, get its codes in the right order
    dim_codes = []
    for name in dim_names:
        index = data["dimension"][name]["category"]["index"]   # e.g. {"DE": 0, "FR": 1}
        if isinstance(index, dict):
            codes = sorted(index, key=index.get)
        else:
            codes = index
        dim_codes.append(codes)

    rows = []
    for position, value in data["value"].items():
        i = int(position)

        # Work out the "odometer" digits for this position
        digits = []
        for size in reversed(sizes):
            digits.append(i % size)
            i = i // size
        digits.reverse()

        # Build one row: {"geo": "DE", "time": "2023", ..., "value": 12.5}
        row = {}
        for k, name in enumerate(dim_names):
            row[name] = dim_codes[k][digits[k]]
        row["value"] = value
        row["flag"] = data.get("status", {}).get(position)   # notes like "p" = provisional
        rows.append(row)

    return pd.DataFrame(rows)


def get_labels(data, dimension):
    """Get the readable names for a dimension's codes."""
    return data["dimension"][dimension]["category"]["label"]


# The 27 EU countries (Eurostat uses "EL" for Greece)
EU27 = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU",
        "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]


def clean_purchases(df, labels):
    # 1. Keep only real countries (drop totals like "EU27_2020")
    df = df[df["geo"].isin(EU27)]

    # 2. Keep one unit (% of all people) and one group (everyone)
    df = df[(df["unit"] == "PC_IND") & (df["ind_type"] == "IND_TOTAL")]

    # 3. Give columns clear names
    df = df.rename(columns={"geo": "country_code", "time": "year", "indic_is": "indicator"})

    # 4. Add the readable indicator name
    df["indicator_label"] = df["indicator"].map(labels)

    # 5. Fix data types: year should be a number, not text
    df["year"] = df["year"].astype(int)

    # 6. Drop empty values and duplicates
    df = df.dropna(subset=["value"]).drop_duplicates()

    # 7. Keep only the columns we need, in a nice order
    return df[["country_code", "year", "indicator", "indicator_label", "value", "flag"]]


# This part only runs when you run this file directly
if __name__ == "__main__":
    with open("data/raw/book_purchases_all.json") as f:
        data = json.load(f)

    raw = jsonstat_to_df(data)
    clean = clean_purchases(raw, get_labels(data, "indic_is"))
    clean.to_csv("data/clean/book_purchases.csv", index=False)
    print(clean.head())
    print("Clean rows:", len(clean))
