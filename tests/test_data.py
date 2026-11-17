import pandas as pd

EU27 = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU",
        "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]


# --- book_purchases ---

def test_only_eu_countries():
    df = pd.read_csv("data/clean/book_purchases.csv")
    assert df["country_code"].isin(EU27).all()


def test_percentages_make_sense():
    df = pd.read_csv("data/clean/book_purchases.csv")
    assert df["value"].between(0, 100).all()


def test_no_duplicate_rows():
    df = pd.read_csv("data/clean/book_purchases.csv")
    assert not df.duplicated(["country_code", "year", "indicator"]).any()


# --- reading ---

def test_reading_only_eu_countries():
    df = pd.read_csv("data/clean/reading.csv")
    assert df["country_code"].isin(EU27).all()


def test_reading_groups_add_up_to_100():
    """The four 'books read' groups should cover everyone (allowing for rounding)."""
    df = pd.read_csv("data/clean/reading.csv")
    totals = df.groupby(["country_code", "year", "sex", "age"])["value"].sum()
    assert totals.between(99, 101).all()


# --- trends ---

def test_trends_interest_between_0_and_100():
    df = pd.read_csv("data/clean/trends.csv")
    assert df["interest"].between(0, 100).all()


def test_trends_every_keyword_has_a_format():
    df = pd.read_csv("data/clean/trends.csv")
    assert df["format"].isin(["print", "digital"]).all()


# --- countries seed ---

def test_countries_seed_has_all_27():
    df = pd.read_csv("seeds/countries.csv")
    assert sorted(df["country_code"]) == sorted(EU27)
    assert df["region"].isin(["Nordic", "Western", "Southern", "Central-Eastern"]).all()
