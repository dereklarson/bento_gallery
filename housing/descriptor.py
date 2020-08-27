# NOTE Text from Zillow Research page
zhvi = """ The ZHVI was launched in 2006, and in its most recent iteration
prior to publication of November 2019 data it was calculated as the median
Zestimate value for a fixed (over time) set of homes in a given area,
representing that area’s median home value."""

zri = """ The Zillow Rent Index (ZRI) is a dollar-valued index intended to
capture typical market rent for a given segment (IE, multifamily or
single-family units) and/or geography (IE for a given ZIP code, city, county,
state or metro) by leveraging Rent Zestimates."""

map_text = {
    "Zillow Home Value Index": zhvi,
    "Zillow Rent Index": zri,
    "default": "Some metrics here are missing data, which skews the color scale.",
}

map_page = {
    "dataid": "zillow_2020",
    "subtitle": "Metrics for 2020 from Zillow",
    "banks": {
        "info": {"type": "info", "args": {"text": map_text}},
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
            "args": {"key": "state", "text_key": "state"},
        },
    },
    "layout": [["statemap"]],
    "sidebar": ["info", "axes", "_top10"],
    "connections": {"axes": {"info", "statemap", "top10"}},
}

trend_page = {
    "dataid": "zillow_time",
    "subtitle": "House value since 1996 from Zillow",
    "banks": {
        "filters": {
            "type": "selector",
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
