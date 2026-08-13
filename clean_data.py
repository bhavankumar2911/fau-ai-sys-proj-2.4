import os
import unicodedata

import pandas as pd

from constants import ASSIGNMENT_FOLDER_PATH

def create_valid_word_list(input_file, output_file):
    cities = pd.read_csv(input_file)

    cities = cities[
        cities["population"] >= 100_000
    ]

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

    valid_words = cities[
        ["city_ascii", "population"]
    ].copy()

    valid_words["city_ascii"] = (
        valid_words["city_ascii"].str.upper()
    )

    valid_words = valid_words.drop_duplicates(
        subset="city_ascii"
    )

    valid_words = valid_words.rename(
        columns={"city_ascii": "word"}
    )

    valid_words.to_csv(
        output_file,
        index=False
    )

create_valid_word_list(
    os.path.join(
        ASSIGNMENT_FOLDER_PATH,
        "worldcities.csv"
    ),
    os.path.join(
        './',
        "valid_cities.csv"
    )
)