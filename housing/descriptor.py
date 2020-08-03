map_page = {
    "dataid": "zillow_2020",
    "subtitle": "Metrics for 2020 from Zillow",
    "banks": {
        "axes": {
            "type": "axis_controls",
            "width": 3,
            "args": {"use": "z", "scale": False, "z.default": "Zillow Rent Index"},
        },
        "statemap": {
            "type": "graph",
            "args": {"category": "map", "variant": "choropleth", "geo": "states"},
        },
        "top10": {
            "type": "ranking",
            "open": False,
            "width": 3,
            "args": {"key": "state", "nformat": ".2f"},
        },
    },
    "layout": [["statemap"]],
    "sidebar": ["axes", "_top10"],
    "connections": {"axes": {"statemap", "top10"}},
}

trend_page = {
    "dataid": "zillow_time",
    "subtitle": "House value since 1996 from Zillow",
    "banks": {
        "filters": {
            "type": "filter_set",
            "width": 6,
            "args": {
                "columns": ["County"],
                "County.default": [
                    "San Francisco County",
                    "New York County",
                    "Miami-Dade County",
                ],
            },
        },
        "analytics": {"type": "analytics_set", "args": {"vertical": False}},
        "series": {
            "type": "graph",
            "args": {
                "x_column": "date",
                "x_scale": "date",
                "y_column": "Value",
                "category": "normal",
            },
        },
    },
    "layout": [["filters", "analytics"], ["series"]],
    "connections": {"analytics": {"series"}, "filters": {"series"},},
}

descriptor = {
    "name": "simple",
    "theme": "dark sparse flat",
    "appbar": {"title": "US Housing Market"},
    "data": {
        "zillow_2020": {"module": "housing.df_housing"},
        "zillow_time": {"module": "housing.df_series"},
    },
    "pages": {"map": map_page, "trend": trend_page,},
}
