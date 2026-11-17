import os
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


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("data/clean/book_purchases.csv")
    load_table(df, "book_purchases")
