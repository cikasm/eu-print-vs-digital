import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # draw straight to files, no window
import matplotlib.pyplot as plt
from sqlalchemy import text
from load import get_engine

# Colors (checked to be colorblind-safe together)
BLUE = "#2a78d6"
ORANGE = "#eb6834"
TEXT = "#0b0b0b"
MUTED = "#6b6a63"
GRID = "#e4e3dd"

# One shared look for every chart: no box, light grid, quiet axes
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb",
    "axes.edgecolor": GRID,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": TEXT,
    "font.size": 10,
})


def run_query(path):
    """Run a SQL file from sql/analysis/ and return the result as a DataFrame."""
    with open(path) as f:
        # text() makes the "%" signs in our SQL comments safe
        return pd.read_sql(text(f.read()), get_engine())


def chart_ebooks_by_region():
    df = run_query("sql/analysis/01_ebooks_by_region.sql")
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(df["region"], df["avg_pct"], color=BLUE, width=0.6)
    ax.bar_label(bars, fmt="%.1f%%", padding=3)       # number on top of each bar
    ax.set_title("E-book buying by EU region, 2023", loc="left", fontweight="bold")
    ax.set_ylabel("% of people who bought e-books online")
    ax.grid(axis="y", color=GRID)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig("docs/ebooks_by_region.png", dpi=150)
    plt.close(fig)


def chart_digital_share():
    df = run_query("sql/analysis/03_print_vs_digital_by_country.sql")
    df = df.sort_values("digital_share_pct")          # biggest at the top
    fig, ax = plt.subplots(figsize=(7, 8))
    ax.barh(df["country_name"], df["digital_share_pct"], color=BLUE, height=0.7)
    ax.axvline(50, color=MUTED, linestyle="--", linewidth=1)
    ax.text(50.5, -0.9, "50% = as many digital as print buyers", color=MUTED, fontsize=9)
    ax.set_title("Digital share of online book buying, 2023", loc="left", fontweight="bold")
    ax.set_xlabel("Digital buyers as % of (print + digital) buyers")
    ax.set_xlim(0, 70)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig("docs/digital_share_by_country.png", dpi=150)
    plt.close(fig)


def chart_search_interest():
    df = run_query("sql/analysis/05_search_interest_by_year.sql")
    lines = {"Kindle": BLUE, "e-reader": ORANGE}
    fig, ax = plt.subplots(figsize=(7, 4))
    for keyword, color in lines.items():
        part = df[df["keyword"] == keyword]
        ax.plot(part["year"], part["avg_interest"], color=color, linewidth=2,
                marker="o", markersize=6, label=keyword)
        last = part.iloc[-1]                          # label the end of each line
        ax.annotate(keyword, (last["year"], last["avg_interest"]),
                    xytext=(8, 0), textcoords="offset points", va="center", color=TEXT)
    ax.set_title("Google search interest by year (average of 10 EU countries)",
                 loc="left", fontweight="bold")
    ax.set_ylabel("Search interest (0-100)")
    ax.set_xticks(sorted(df["year"].unique()))
    ax.set_xlim(right=df["year"].max() + 0.8)        # room for the end labels
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", color=GRID)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig("docs/search_interest.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    chart_ebooks_by_region()
    chart_digital_share()
    chart_search_interest()
    print("Saved 3 charts in docs/")
