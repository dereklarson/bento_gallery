globe_page = {
    "dataid": "covid_world",
    "subtitle": "World geographical view by country",
    "banks": {
        "agg": {
            "type": "indicators",
            "width": 3,
            "args": {
                "components": [
                    {"args": {"y_column": "cases"}},
                    {"args": {"y_column": "deaths"}},
                ]
            },
        },
        "axis": {
            "type": "axis_controls",
            "args": {
                "use": "z",
                "z.options": ["cases", "deaths", "cases_per_100k", "deaths_per_100k"],
                "z.default": "cases",
                "scale": False,
            },
        },
        "date": {"type": "date_picker"},
        "top10": {
            "type": "ranking",
            "width": 3,
            "args": {"key": "country"},
            "nformat": ".2f",
        },
        "globemap": {
            "type": "graph",
            "args": {"category": "map", "variant": "choropleth", "geo": "world"},
        },
    },
    "layout": [["agg", "axis", "date"], ["top10", "globemap"],],
    "connections": {
        "axis": {"globemap", "top10"},
        "date": {"globemap", "top10", "agg"},
    },
}

world_trends_page = {
    "dataid": "covid_world",
    "subtitle": "World time-series analysis by country",
    "banks": {
        "axis": {
            "type": "axis_controls",
            "args": {"use": "xy", "multi": "y", "scale": True, "vertical": True},
        },
        "pick_country": {
            "type": "filter_set",
            "width": 4,
            "args": {"columns": ["country"], "country.default": ["Brazil", "Italy"]},
        },
        "analytics": {"type": "analytics_set", "args": {"vertical": True}},
        "trend": {"type": "graph"},
        "style": {"type": "style_controls"},
    },
    "layout": [["axis", "pick_country", "analytics", "style"], ["trend"]],
    "connections": {
        "axis": {"trend"},
        "pick_country": {"trend"},
        "analytics": {"trend"},
        "style": {"trend"},
    },
}

usgeo_page = {
    "dataid": "covid_us",
    "subtitle": "United States geographical view by state/county",
    "banks": {
        "agg": {
            "type": "indicators",
            "width": 3,
            "args": {
                "components": [
                    {"args": {"y_column": "cases"}},
                    {"args": {"y_column": "deaths"}},
                ]
            },
        },
        "axis": {
            "type": "axis_controls",
            "args": {
                "use": "z",
                "z.options": ["cases", "deaths", "cases_per_100k", "deaths_per_100k"],
                "z.default": "cases",
            },
        },
        "date": {"type": "date_picker"},
        "top10": {"type": "ranking", "width": 3, "args": {"nformat": ".2f"}},
        "map_settings": {
            "type": "option_set",
            "args": {
                "components": [
                    {
                        "name": "geo",
                        "label": "Select geography",
                        "options": ["state", "county"],
                    },
                ]
            },
        },
        "countymap": {
            "type": "graph",
            "args": {"category": "map", "variant": "choropleth"},
        },
    },
    "layout": [["agg", "map_settings", "axis", "date"], ["top10", "countymap"]],
    "connections": {
        "axis": {"countymap", "top10"},
        "map_settings": {"countymap", "top10"},
        "date": {"countymap", "top10", "agg"},
    },
}

us_trends_page = {
    "dataid": "covid_us",
    "subtitle": "United States time-series analysis by state/county",
    "banks": {
        "axis": {
            "type": "axis_controls",
            "args": {"use": "xy", "multi": "y", "scale": True, "vertical": True},
        },
        "pick_state": {
            "type": "filter_set",
            "width": 4,
            "args": {"columns": ["state", "county"], "vertical": True},
        },
        "analytics": {"type": "analytics_set", "args": {"vertical": True}},
        "trend": {"type": "graph"},
        "style": {"type": "style_controls"},
    },
    "layout": [["axis", "pick_state", "analytics", "style"], ["trend"]],
    "connections": {
        "axis": {"trend"},
        "pick_state": {"trend"},
        "analytics": {"trend"},
        "style": {"trend"},
    },
}

descriptor = {
    "name": "demonstration",
    "theme": "dark",
    "theme_dict": {},
    "appbar": {"title": "COVID Live"},
    "data": {
        "covid_us": {"module": "covid.df_covid_us"},
        "covid_world": {"module": "covid.df_covid_world"},
    },
    "pages": {
        "globe": globe_page,
        "world_trends": world_trends_page,
        "us": usgeo_page,
        "us_trends": us_trends_page,
    },
}
