"""
Esme LiChong
CSE 163 Final Project: Exploratory Data Analysis

Loads the artist CSV files, cleans them, prints the
summaries for the report, and saves two plots.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_FILES = [
    "data/artworks_andy_warhol.csv",
    "data/artworks_claude_monet.csv",
    "data/artworks_david_hockney.csv",
    "data/artworks_gerhard_richter.csv",
    "data/artworks_jean_michel_basquiat.csv",
    "data/artworks_mark_rothko.csv",
    "data/artworks_piccaso4.csv",
    "data/artworks_zao_wou_ki.csv",
]


def load_data(files):
    """
    Reads each CSV file in the list files and combines all of their rows
    into one DataFrame.
    """
    rows = []
    for file in files:
        df = pd.read_csv(file)
        for i in range(len(df)):
            rows.append(list(df.loc[i]))
    return pd.DataFrame(rows, columns=df.columns)


def parse_price(text):
    """
    Converts a price like "$2.5M", "$143K", or "$378" to a number.
    """
    text = text.replace("$", "").replace(",", "")
    if text.endswith("M"):
        return round(float(text[:-1]) * 1000000)
    elif text.endswith("K"):
        return round(float(text[:-1]) * 1000)
    else:
        return round(float(text))


def get_year(url):
    """
    Returns the year a work was made from its url, or None if the url
    doesn't have one.
    """
    last_four = url.split("-w:")[0][-4:]
    if last_four.isdigit() and 1800 <= int(last_four) <= 2025:
        return int(last_four)
    return None


def simplify_medium(description):
    """
    Groups a medium description like "Oil on canvas" into silkscreen,
    acrylic, oil, paper, or other.
    """
    if pd.isna(description):
        return None
    description = description.lower()
    if "silkscreen" in description:
        return "silkscreen"
    elif "acrylic" in description:
        return "acrylic"
    elif "oil" in description:
        return "oil"
    elif "paper" in description:
        return "paper"
    else:
        return "other"


def clean(df):
    """
    Returns a cleaned copy of df with prices as numbers, a simpler medium
    column, and the year and decade each work was made.
    """
    df = df[df["title"] != "title"].copy()

    df["sale_price"] = df["sale_price"].apply(parse_price)
    df["last_sale_price"] = df["purchase_price"].apply(parse_price)
    df["medium"] = df["description"].apply(simplify_medium)

    df["year_made"] = df["url"].apply(get_year)
    df["decade_made"] = (df["year_made"] // 10) * 10

    columns = ["title", "artist", "medium", "year_made", "decade_made",
               "last_sale_price", "sale_price", "image_url"]
    return df[columns]


def median_price_by(df, column):
    """
    Returns the median sale price for each value of column, highest first.
    """
    medians = df.groupby(column)["sale_price"].median()
    return medians.sort_values(ascending=False)


def print_summaries(df):
    """Prints everything the results section needs."""
    print("Rows, columns:", df.shape)

    print("\nMissing values per column:")
    print(df.isna().sum())
    print("\nPercent missing:")
    print((df.isna().mean() * 100).round(1))

    print("\nNumeric summaries:")
    print(df[["sale_price", "last_sale_price", "year_made"]].describe())

    for col in ["artist", "medium", "decade_made"]:
        print("\nCounts for", col)
        print(df[col].value_counts(dropna=False))
        print("\nMedian sale price by", col)
        print(median_price_by(df, col))

    print("\nCorrelation between sale price and last sale price:")
    print(df["sale_price"].corr(df["last_sale_price"]))

    print("\nShare that sold for $1M or more:")
    print((df["sale_price"] >= 1000000).mean())
    print("Share that sold for more than last time:")
    print((df["sale_price"] > df["last_sale_price"]).mean())


def plot_price_by_artist(df):
    """
    Saves a box plot of sale price for each artist (log scale), sorted
    by median price.
    """
    order = median_price_by(df, "artist").index
    sns.catplot(data=df, x="sale_price", y="artist", kind="box",
                order=order, color="#2a78d6", height=5, aspect=1.6)
    plt.xscale("log")
    plt.xlabel("Sale price (USD, log scale)")
    plt.ylabel("Artist")
    plt.title("Sale Price by Artist")
    plt.savefig("price_by_artist.png", bbox_inches="tight")
    plt.close()


def plot_last_sale_vs_price(df):
    """
    Saves a scatter plot of last sale price vs current sale price (log
    scale). Points above the dashed line sold for more than last time.
    """
    sns.relplot(data=df, x="last_sale_price", y="sale_price",
                color="#2a78d6", alpha=0.5, height=6)
    low = df["last_sale_price"].min()
    high = df["sale_price"].max()
    plt.plot([low, high], [low, high], linestyle="--", color="gray",
             label="Same price as last sale")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Last sale price (USD, log scale)")
    plt.ylabel("Current sale price (USD, log scale)")
    plt.title("Last Sale Price vs Current Sale Price")
    plt.legend()
    plt.savefig("last_sale_vs_price.png", bbox_inches="tight")
    plt.close()


def main():
    df = clean(load_data(DATA_FILES))
    print_summaries(df)
    plot_price_by_artist(df)
    plot_last_sale_vs_price(df)


if __name__ == "__main__":
    main()
