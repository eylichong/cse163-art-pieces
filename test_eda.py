"""
Esme LiChong
CSE 163 Final Project: tests for eda.py

Tests use test_data/artworks_test.csv, a small file I made by hand in
the same format as the real data, including prices written different
ways, a repeated header row, and missing values. The expected answers
were worked out by hand from that file.
"""

import eda

TEST_FILES = ["test_data/artworks_test.csv"]


def test_parse_price():
    assert eda.parse_price("$110.5M") == 110500000
    assert eda.parse_price("$20.9K") == 20900
    assert eda.parse_price("$378") == 378


def test_get_year():
    assert eda.get_year("https://test/meules-1890-w:c3") == 1890
    assert eda.get_year("https://test/head-w:e5") is None
    assert eda.get_year("https://test/victor-25448-w:a1") is None


def test_simplify_medium():
    assert eda.simplify_medium("acrylic on canvas") == "acrylic"
    assert eda.simplify_medium("oil on canvas") == "oil"
    assert eda.simplify_medium("ink on paper") == "paper"
    assert eda.simplify_medium("lithograph") == "other"


def test_clean():
    df = eda.clean(eda.load_data(TEST_FILES))
    assert len(df) == 6
    assert list(df["sale_price"]) == [110500000, 4500000, 110700000,
                                      47900, 1900000, 8900]
    assert list(df["last_sale_price"]) == [20900, 1200000, 2500000, 4000,
                                           1600000, 378]


def test_missing_values():
    df = eda.clean(eda.load_data(TEST_FILES))
    missing = df.isna().sum()
    assert missing["medium"] == 1
    assert missing["year_made"] == 1
    assert missing["image_url"] == 1


def test_median_price_by():
    df = eda.clean(eda.load_data(TEST_FILES))
    medians = eda.median_price_by(df, "artist")
    assert medians["JEAN MICHEL BASQUIAT (b. 1960 d. 1988)"] == 57500000
    assert medians["CLAUDE MONET (b. 1840 d. 1926)"] == 110700000


def main():
    test_parse_price()
    test_get_year()
    test_simplify_medium()
    test_clean()
    test_missing_values()
    test_median_price_by()
    print("All tests passed!")


if __name__ == "__main__":
    main()
