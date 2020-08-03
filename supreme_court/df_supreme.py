import pandas as pd


def load():
    filename = "supreme_court/supreme_court_v1.csv"
    df = pd.read_csv(filename)
    data = {
        "df": df,
        "keys": ["chief"],
    }
    data["types"] = {
        "count": int,
        "avg_progressive": float,
        "avg_split": float,
    }
    return data
