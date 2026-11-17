from extract import extract_all_eurostat
from extract_trends import extract_trends
from transform import run_all_transforms
from load import load_all


def main():
    print("=== EXTRACT ===")
    extract_all_eurostat()   # book purchases, reading survey, prices
    extract_trends()         # Google Trends (skips countries already downloaded)

    print("=== TRANSFORM ===")
    run_all_transforms()

    print("=== LOAD ===")
    load_all()

    print("Pipeline finished!")


if __name__ == "__main__":
    main()
