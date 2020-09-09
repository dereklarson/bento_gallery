import pandas as pd


def load():
    filename = "hotel/sample_hotel_data.csv"
    df = pd.read_csv(filename)
    data = {
        "df": df,
        "keys": ["home_city", "dest_city"],
    }
    data["types"] = {
        "distance": float,
        "home_pop": int,
        "dest_pop": int,
        "hotel_size": int,
        "conversion": int,
    }
    return data
