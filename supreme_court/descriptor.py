trend_page = {
    "dataid": "supreme",
    "banks": {
        "axis": {"type": "axis_controls", "args": {"use": "y"}},
        "series": {
            "type": "graph",
            "args": {
                "x_column": "date",
                "x_scale": "date",
                "category": "normal",
                "color": "chief",
                "keys": ["date", "chief"],
            },
        },
    },
    "layout": [["axis", "window"], ["series"]],
    "connections": {"axis": {"series"}, "window": {"series"},},
}

descriptor = {
    "name": "simple",
    "appbar": {
        "title": "Supreme Court Cases",
        "subtitle": "1946 - now, data from WUSTL",
        "image": "usflag.jpg",
    },
    "data": {"supreme": {"module": "supreme_court.df_supreme"},},
    "pages": {"trend": trend_page,},
}
