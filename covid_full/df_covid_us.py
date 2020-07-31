import pandas as pd

from bento.common import logger
from bento.common.structure import PathConf

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


def join_reference_data(idf, filename, on_key, filters=(), col_map=None):
    raw_df = PathConf.data.read(filename)
    if col_map:
        raw_df = raw_df[col_map.keys()].rename(columns=col_map)
    for (key, value) in filters:
        raw_df = raw_df[raw_df[key] == value].drop(key, axis=1)
    agg_df = raw_df.groupby(on_key).sum().drop("Unnamed: 0", axis=1)
    join_df = idf.join(agg_df, on=on_key)
    return join_df


def process_df(data_path):
    # Load raw data
    idf = pd.read_csv(data_path, parse_dates=["date"])

    # logging.info(f"*** Loaded DF from {data_path} with {len(idf)} rows***")
    exclude = ["Guam", "Northern Mariana Islands", "Puerto Rico", "Virgin Islands"]
    idf = idf[~idf.state.isin(exclude)]
    idf["state_abbr"] = idf["state"].map(name_to_abbr)
    idf["county"] = idf["county"] + (", " + idf["state_abbr"]).fillna("")

    # Add population reference
    pop_file = "population/ref_county_pop"
    odf = join_reference_data(idf, pop_file, on_key=["fips"])
    odf["fips"] = odf["fips"].astype(str).str.replace("\.0", "").str.zfill(5)  # noqa
    # logging.info(f"*** Loaded population data from {pop_file} ***")
    return odf


def load(repobase=PathConf.data.path):
    filename = "us-counties.csv"
    data_path = f"{repobase}/nyt-covid-states/{filename}"
    data = {
        "df": process_df(data_path),
        "keys": ["fips", "county", "state"],
        "types": {"date": "date", "cases": int, "deaths": int, "population": int,},
    }
    return data
