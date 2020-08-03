import os
import pandas as pd
from iso3166 import countries
from fuzzywuzzy import fuzz
from bento.common import util, logger

logging = logger.fancy_logger(__name__)


def clean_string_name(item):
    return item.strip().replace("*,", "")


@util.memoize
def fuzzy_search(name, corpus, clean=clean_string_name):
    name = clean(name)

    output = ""
    best = 0
    for item in corpus:
        item = clean(item)
        methods = [fuzz.partial_ratio, fuzz.token_sort_ratio]
        ratio = max([method(item, name) for method in methods])
        if ratio == 100:
            return item
        if ratio > best:
            best = ratio
            output = item
    return output


def normalize_countries(idf, column="country", corpus=countries):
    inputs = idf[column].unique()
    for country in inputs:
        entry = corpus.get(country, None)
        if not entry:
            reference_list = (country.apolitical_name for country in countries)
            new = fuzzy_search(country, reference_list)
            # logging.debug(f"Missing '{country}', assigning unicode version")
            entry = corpus.get(new)
        idf.loc[idf[column] == country, "alpha3"] = getattr(entry, "alpha3")
        idf.loc[idf[column] == country, column] = entry.apolitical_name


def join_reference_data(idf, data_path, filename, on_key, filters=(), col_map=None):
    raw_df = pd.read_csv(f"{data_path}/{filename}")
    if col_map:
        raw_df = raw_df.rename(columns=col_map)
    for (key, value) in filters:
        raw_df = raw_df[raw_df[key] == value].drop(key, axis=1)
    agg_df = raw_df.groupby(on_key).sum().drop("Unnamed: 0", axis=1)
    join_df = idf.join(agg_df, on=on_key)
    return join_df


def load_covid_raw_data(data_path, filename):
    df = pd.read_csv(f"{data_path}/{filename}", parse_dates=["Date"])
    # logging.info(f"*** Loaded DF from {data_path} with {len(df)} rows***")
    df = util.snakify_column_names(df)
    raw_df = df.rename(columns={"confirmed": "cases"})
    # logging.debug("Removing Diamond Princess and renaming Korea, South => RoK")
    raw_df = raw_df[raw_df["country"] != "Diamond Princess"]
    raw_df.loc[raw_df["country"] == "Korea, South", "country"] = "Korea, Republic of"
    return raw_df


def process_covid_raw_data(data_path):
    filename = f"covid-19/data/countries-aggregated.csv"
    idf = load_covid_raw_data(data_path, filename)
    normalize_countries(idf)
    idf = idf.groupby(["date", "country", "alpha3"]).sum().reset_index()
    pop_file = "population/ref_world_pop.csv"
    idf = join_reference_data(
        idf,
        data_path,
        pop_file,
        on_key=["alpha3"],
        filters=[("year", 2016)],
        col_map={"country_code": "alpha3"},
    )
    idf["cases_per_100k"] = idf["cases"] * 1e5 / idf["population"]
    idf["deaths_per_100k"] = idf["deaths"] * 1e5 / idf["population"]
    idf = idf.drop(["population", "recovered"], axis=1)
    # logging.info(f"*** Loaded population data from {pop_file} ***")
    return idf


def load():
    data_path = f"{os.environ['APP_HOME']}/{os.environ['DATA_DIR']}"
    data = {
        "df": process_covid_raw_data(data_path),
        "keys": ["country"],
        "types": {
            "date": "date",
            "cases": int,
            "deaths": int,
            "cases_per_100k": float,
            "deaths_per_100k": float,
        },
    }
    data["columns"] = list(data["types"].keys())

    return data
