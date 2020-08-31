import os
import pandas as pd
from bento.common import datautil, logger, util

logging = logger.fancy_logger(__name__)


def load_covid_raw_data(data_path, base, cases, deaths, nrows=None):
    read_args = {}
    if nrows:
        read_args["nrows"] = nrows
    idf = pd.read_csv(f"{data_path}/{base}/{cases}").drop(["Lat", "Long"], axis=1)
    idf = idf.melt(
        id_vars=["Province/State", "Country/Region"],
        var_name="date",
        value_name="cases",
    )
    idf = idf.groupby(["date", "Country/Region"]).sum().reset_index()

    # Add on deaths
    ddf = pd.read_csv(f"{data_path}/{base}/{deaths}").drop(["Lat", "Long"], axis=1)
    ddf = ddf.melt(
        id_vars=["Province/State", "Country/Region"],
        var_name="date",
        value_name="deaths",
    )
    ddf = ddf.groupby(["date", "Country/Region"]).sum()

    idf = idf.join(ddf, on=["date", "Country/Region"]).rename(
        columns={"Country/Region": "country"}
    )
    idf.loc[:, "date"] = pd.to_datetime(idf["date"])
    idf = idf.sort_values("date")
    return idf


def add_country_reference(raw_df, ref_df):
    # Drop some hard to handle, more obscure areas
    drop_entries = [
        "Diamond Princess",
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
        "Korea, South": ("country", "Korea, Republic of"),
    }
    for name, mod in modifications.items():
        idf.loc[idf.country == name, mod[0]] = mod[1]

    reference = tuple(ref_df["country"].unique())
    mismatch = set(idf["country"].unique()) - set(reference)
    for country in mismatch:
        match_name = datautil.fuzzy_search(country, reference)
        logging.debug(f"Missing '{country}', assigning {match_name}")
        idf.loc[idf.country == country, "country"] = match_name
    logging.info(f"Total country name mismatches: {len(mismatch)}")
    idf = idf.join(ref_df.set_index("country"), on="country")
    return idf


def process_covid_data(idf):
    idf["cases_per_100k"] = idf["cases"] * 1e5 / idf["population"]
    idf["deaths_per_100k"] = idf["deaths"] * 1e5 / idf["population"]
    idf = idf.drop(["population"], axis=1)
    return idf


def load(nrows=None):
    data_path = f"{os.environ['APP_HOME']}/{os.environ['DATA_DIR']}"
    base = f"jhopkins-covid-19/csse_covid_19_data/csse_covid_19_time_series"
    cases = "time_series_covid19_confirmed_global.csv"
    deaths = "time_series_covid19_deaths_global.csv"
    raw_df = load_covid_raw_data(data_path, base, cases, deaths)

    ref_df = util.df_loader("world_country_reference.csv")
    jdf = add_country_reference(raw_df, ref_df)
    pdf = process_covid_data(jdf)
    data = datautil.autostructure(pdf)
    return data
