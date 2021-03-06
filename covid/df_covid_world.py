import os
import pandas as pd
from bento.common import datautil, logger, util

logging = logger.fancy_logger(__name__)


def load_covid_raw_data(data_path, filename, nrows=None):
    read_args = {}
    if nrows:
        read_args["nrows"] = nrows
    idf = pd.read_csv(f"{data_path}/{filename}", parse_dates=["Date"], **read_args)
    idf = util.snakify_column_names(idf)
    raw_df = idf.rename(columns={"confirmed": "cases"})
    raw_df = raw_df[raw_df["country"] != "Diamond Princess"]
    raw_df.loc[raw_df["country"] == "Korea, South", "country"] = "Korea, Republic of"
    return raw_df


def add_country_reference(raw_df, ref_df):
    # Drop some hard to handle, more obscure areas
    drop_entries = [
        "West Bank and Gaza",
        "Kosovo",
        "Holy See",
        "MS Zaandam",
        "Eritrea",
        "Western Sahara",
    ]
    idf = raw_df.copy()
    idf = idf.loc[~idf.country.isin(drop_entries)]

    # Change some unrecognized entries
    modifications = {
        "Burma": ("country", "Myanmar"),
        "US": ("country", "United States"),
    }
    for name, mod in modifications.items():
        idf.loc[idf.country == name, mod[0]] = mod[1]

    reference = tuple(ref_df["country"].unique())
    mismatch = set(idf["country"].unique()) - set(reference)
    for country in mismatch:
        match_name = datautil.fuzzy_search(country, reference)
        # logging.debug(f"Missing '{country}', assigning {match_name}")
        idf.loc[idf.country == country, "country"] = match_name
    logging.info(f"Total country name mismatches: {len(mismatch)}")
    idf = idf.join(ref_df.set_index("country"), on="country")
    return idf


def process_covid_data(idf):
    idf["cases_per_100k"] = idf["cases"] * 1e5 / idf["population"]
    idf["deaths_per_100k"] = idf["deaths"] * 1e5 / idf["population"]
    idf = idf.drop(["population", "recovered"], axis=1)
    return idf


def load(nrows=None):
    data_path = f"{os.environ['APP_HOME']}/{os.environ['DATA_DIR']}"
    filename = f"covid-19/data/countries-aggregated.csv"
    raw_df = load_covid_raw_data(data_path, filename, nrows=nrows)

    ref_df = util.df_loader("world_country_reference.csv")
    jdf = add_country_reference(raw_df, ref_df)
    pdf = process_covid_data(jdf)
    data = datautil.autostructure(pdf)
    return data
