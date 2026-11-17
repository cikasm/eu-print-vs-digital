import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()   # reads your .env file


def get_engine():
    """Create a connection to the database."""
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    # "+psycopg2" names the driver; newer SQLAlchemy defaults to a different one
    return create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5432/{db}")


def load_table(df, table_name):
    """Save a DataFrame into the 'staging' area of the database."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
    # "replace" = throw away the old table and write a fresh one
    df.to_sql(table_name, engine, schema="staging", if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into staging.{table_name}")


TABLES = ["book_purchases", "reading", "trends"]


def load_all():
    """Load every clean CSV into its own staging table."""
    for name in TABLES:
        # Parse the date columns so Postgres stores real dates, not text
        dates = ["date"] if name == "trends" else None
        df = pd.read_csv(f"data/clean/{name}.csv", parse_dates=dates)
        load_table(df, name)

    # The country list is written by hand, so it lives in seeds/, not data/clean/
    load_table(pd.read_csv("seeds/countries.csv"), "countries")


def run_sql_file(path):
    """Run every SQL statement in a file."""
    with open(path) as f:
        sql = f.read()
    with get_engine().begin() as conn:
        conn.execute(text(sql))
    print(f"Ran {path}")


if __name__ == "__main__":
    load_all()
