import json
import os
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


def clean_reading(df, labels):
    """Books read in the last 12 months (survey, 2022 only)."""
    # 1. Keep only real countries
    df = df[df["geo"].isin(EU27)]

    # 2. Keep one unit (%) and all education levels together
    df = df[(df["unit"] == "PC") & (df["isced11"] == "TOTAL")]

    # 3. Give columns clear names
    df = df.rename(columns={"geo": "country_code", "time": "year", "n_book": "books_read"})

    # 4. Add the readable label for the number of books
    df["books_read_label"] = df["books_read"].map(labels)

    # 5. Fix data types
    df["year"] = df["year"].astype(int)

    # 6. Drop empty values and duplicates
    df = df.dropna(subset=["value"]).drop_duplicates()

    # 7. Keep only the columns we need (value = % of people in that group)
    return df[["country_code", "year", "sex", "age", "books_read", "books_read_label", "value", "flag"]]


# Which keywords are print or digital
KEYWORD_FORMAT = {
    "Kindle":   "digital",
    "e-reader": "digital",
}


def clean_trends(folder="data/raw/trends"):
    """Combine one Google Trends CSV per country into one long table."""
    tables = []
    for file in sorted(os.listdir(folder)):
        if not file.endswith(".csv"):
            continue
        df = pd.read_csv(os.path.join(folder, file))
        df["country_code"] = file.replace(".csv", "")
        df = df.drop(columns=["isPartial"], errors="ignore")
        # Wide (one column per keyword) -> long (one row per keyword)
        df = df.melt(id_vars=["date", "country_code"], var_name="keyword", value_name="interest")
        tables.append(df)

    df = pd.concat(tables, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["format"] = df["keyword"].map(KEYWORD_FORMAT)
    return df[["date", "country_code", "keyword", "format", "interest"]]


def read_raw(dataset_code):
    with open(f"data/raw/{dataset_code}.json") as f:
        return json.load(f)


def run_all_transforms():
    """Clean every raw file and save it into data/clean/."""
    os.makedirs("data/clean", exist_ok=True)

    data = read_raw("isoc_ec_ibgs")
    tables = {
        "book_purchases": clean_purchases(jsonstat_to_df(data), get_labels(data, "indic_is")),
    }
    data = read_raw("ilc_scp27")
    tables["reading"] = clean_reading(jsonstat_to_df(data), get_labels(data, "n_book"))
    tables["trends"] = clean_trends()

    for name, df in tables.items():
        df.to_csv(f"data/clean/{name}.csv", index=False)
        print(f"Saved data/clean/{name}.csv ({len(df)} rows)")


# This part only runs when you run this file directly
if __name__ == "__main__":
    run_all_transforms()
