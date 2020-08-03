import os
import pandas as pd

from bento.common import logger

logging = logger.fancy_logger(__name__)

abbr_to_name = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

name_to_abbr = {state: abbrev for abbrev, state in abbr_to_name.items()}


def join_reference_data(idf, data_path, filename, on_key, filters=(), col_map=None):
    raw_df = pd.read_csv(f"{data_path}/{filename}")
    if col_map:
        raw_df = raw_df[col_map.keys()].rename(columns=col_map)
    for (key, value) in filters:
        raw_df = raw_df[raw_df[key] == value].drop(key, axis=1)
    agg_df = raw_df.groupby(on_key).sum().drop("Unnamed: 0", axis=1)
    join_df = idf.join(agg_df, on=on_key)
    return join_df


def process_df(data_path):
    filename = "nyt-covid-states/us-counties.csv"
    idf = pd.read_csv(f"{data_path}/{filename}", parse_dates=["date"])
    exclude = ["Guam", "Northern Mariana Islands", "Puerto Rico", "Virgin Islands"]
    idf = idf[~idf.state.isin(exclude)]
    idf["combined"] = idf.county + "|" + idf.state + "|" + idf.fips.astype(str)
    mindex = pd.MultiIndex.from_product(
        [idf.date.unique(), idf.combined.unique()], names=["date", "combined"]
    )
    idf = idf.set_index(["date", "combined"]).reindex(mindex).reset_index()
    idf[["county", "state", "fips"]] = idf["combined"].str.split("|", expand=True)
    idf["fips"] = idf["fips"].astype(float)
    idf["state_abbr"] = idf["state"].map(name_to_abbr)
    idf["county"] = idf["county"] + (", " + idf["state_abbr"]).fillna("")
    idf = idf.drop(["combined"], axis=1).fillna(0)

    # Add population reference
    pop_file = "population/ref_county_pop.csv"
    odf = join_reference_data(idf, data_path, pop_file, on_key=["fips"])
    odf["fips"] = odf["fips"].astype(str).str.replace("\.0", "").str.zfill(5)  # noqa
    odf["cases_per_100k"] = odf["cases"] * 1e5 / odf["population"]
    odf["deaths_per_100k"] = odf["deaths"] * 1e5 / odf["population"]
    odf = odf.drop(["population"], axis=1)
    return odf


def load():
    data_path = f"{os.environ['APP_HOME']}/{os.environ['DATA_DIR']}"
    data = {
        "df": process_df(data_path),
        "keys": ["fips", "county", "state"],
        "types": {
            "date": "date",
            "cases": int,
            "deaths": int,
            "cases_per_100k": float,
            "deaths_per_100k": float,
        },
    }
    return data
