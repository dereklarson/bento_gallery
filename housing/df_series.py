import pandas as pd


def load():
    filename = "housing/zillow_housing_history.csv"
    df = pd.read_csv(filename)
    df.loc[:, "fips"] = df.fips.astype(str).str.zfill(5)
    data = {
        "df": df,
        "keys": ["County", "State", "fips"],
    }
    data["types"] = {
        "date": "date",
        "Value": float,
    }
    return data
