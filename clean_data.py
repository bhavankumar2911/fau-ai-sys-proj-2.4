from pathlib import Path
import unicodedata

import pandas as pd
from pandas import DataFrame


PROJECT_DIRECTORY = Path(__file__).resolve().parent
VALID_CITIES_FILE = PROJECT_DIRECTORY / "valid_cities.csv"
SOURCE_CITIES_FILE = PROJECT_DIRECTORY.parent / "assignment" / "worldcities.csv"


def create_valid_word_list(input_file: Path, output_file: Path) -> None:
    cities = pd.read_csv(input_file)
    cities = cities[cities["population"] >= 100_000]
    cities = cities[
        cities["city_ascii"].apply(
            lambda city: (
                isinstance(city, str)
                and " " not in city
                and "-" not in city
                and not any(
                    unicodedata.category(character) == "Mn"
                    for character in unicodedata.normalize("NFD", city)
                )
            )
        )
    ]

    valid_cities = cities[["city_ascii", "population"]].copy()
    valid_cities["city_ascii"] = valid_cities["city_ascii"].str.upper()
    valid_cities = valid_cities.drop_duplicates(subset="city_ascii")
    valid_cities.to_csv(output_file, index=False)


def load_cleaned_cities_dataframe() -> DataFrame:
    cities = pd.read_csv(VALID_CITIES_FILE)

    if "word" in cities.columns and "city_ascii" not in cities.columns:
        cities = cities.rename(columns={"word": "city_ascii"})

    required_columns = {"city_ascii", "population"}
    missing_columns = required_columns - set(cities.columns)
    if missing_columns:
        raise ValueError(
            f"{VALID_CITIES_FILE.name} is missing required columns: "
            f"{', '.join(sorted(missing_columns))}"
        )

    return cities[["city_ascii", "population"]]


if __name__ == "__main__":
    create_valid_word_list(SOURCE_CITIES_FILE, VALID_CITIES_FILE)
