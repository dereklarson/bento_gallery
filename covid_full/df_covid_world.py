import pandas as pd
from iso3166 import countries
from fuzzywuzzy import fuzz
from bento.common import util, logger
from bento.common.structure import PathConf

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


def join_reference_data(idf, filename, on_key, filters=(), col_map=None):
    raw_df = PathConf.data.read(filename)
    if col_map:
        raw_df = raw_df[col_map.keys()].rename(columns=col_map)
    for (key, value) in filters:
        raw_df = raw_df[raw_df[key] == value].drop(key, axis=1)
    agg_df = raw_df.groupby(on_key).sum().drop("Unnamed: 0", axis=1)
    join_df = idf.join(agg_df, on=on_key)
    return join_df


def load_covid_raw_data(data_path):
    df = pd.read_csv(data_path, parse_dates=["Date"])
    # logging.info(f"*** Loaded DF from {data_path} with {len(df)} rows***")
    df = util.snakify_column_names(df)
    raw_df = df.rename(columns={"confirmed": "cases"})
    # logging.debug("Removing Diamond Princess and renaming Korea, South => RoK")
    raw_df = raw_df[raw_df["country"] != "Diamond Princess"]
    raw_df.loc[raw_df["country"] == "Korea, South", "country"] = "Korea, Republic of"
    return raw_df


def process_covid_raw_data(idf):
    normalize_countries(idf)
    idf = idf.groupby(["date", "country", "alpha3"]).sum().reset_index()
    pop_file = "population/ref_world_pop"
    idf = join_reference_data(
        idf, pop_file, on_key=["country"], filters=[("year", 2016)]
    )
    # logging.info(f"*** Loaded population data from {pop_file} ***")
    return idf


def load(repobase=PathConf.data.path):
    filename = "countries-aggregated.csv"
    data_path = f"{repobase}/covid-19/data/{filename}"
    raw_df = load_covid_raw_data(data_path)
    pdf = process_covid_raw_data(raw_df)

    # TODO Add automatic type checking and separate log/linear from types
    data = {
        "df": pdf,
        "keys": ["country"],
        "types": {"date": "date", "cases": int, "deaths": int, "population": int,},
    }
    data["columns"] = list(data["types"].keys())

    return data
