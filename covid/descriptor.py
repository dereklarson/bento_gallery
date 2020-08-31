globe_text = """
An interactive, visual presentation of world COVID-19 cases by country. Data is from
the 'datasets/covid-19' github repo, and inspiration was drawn from the Johns Hopkins
covid dash.
"""

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
        "info": {
            "type": "info",
            "width": 5,
            "args": {
                "text": globe_text,
                "Div.style": {"lineHeight": 1.5, "fontSize": "1.8rem"},
            },
        },
        "top10": {
            "type": "ranking",
            "width": 3,
            "args": {"key": "country", "text_key": "country"},
            "nformat": ".2f",
        },
        "globemap": {
            "type": "graph",
            "args": {"category": "map", "variant": "choropleth", "geo": "world"},
        },
    },
    "layout": [["agg", "axis", "date", "info"], ["top10", "globemap"],],
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
            "width": 3,
            "args": {"use": "y", "multi": "y", "scale": True},
        },
        "select": {"type": "selector", "width": 9},
        "analytics": {"type": "analytics_set"},
        "trend": {"type": "graph", "args": {"x_column": "date", "x_scale": "date"}},
        "style": {"type": "style_controls", "width": 6},
    },
    "layout": [["axis", "select"], ["analytics", "style"], ["trend"]],
    "connections": {
        "axis": {"trend"},
        "select": {"trend"},
        "analytics": {"trend"},
        "style": {"trend"},
    },
}

usgeo_text = """
Data for US COVID-19 cases is drawn from the New York Times Github repository.
"""

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
        "info": {
            "type": "info",
            "args": {
                "text": usgeo_text,
                "Div.style": {"lineHeight": 1.5, "fontStyle": "italic"},
            },
        },
        "top10": {"type": "ranking", "width": 3, "args": {}},
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
    "layout": [["agg", "map_settings", "axis", "date", "info"], ["top10", "countymap"]],
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
            "type": "selector",
            "width": 4,
            "args": {
                "columns": ["state", "county"],
                "vertical": True,
                "state.default": ["None"],
            },
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

nrows = None
# nrows = 10000

descriptor = {
    "name": "demonstration",
    "theme": "dark",
    "theme_dict": {"color__on_primary": "white", "color__primary": "#329dfa"},
    "appbar": {"title": "COVID Live", "image": "covid-banner-blue.jpg"},
    "data": {
        "covid_us": {"module": "covid.df_covid_us", "args": {"nrows": nrows}},
        "covid_world": {"module": "covid.df_covid_jhworld"},
    },
    "show_help": True,
    "pages": {
        "globe": globe_page,
        "world_trends": world_trends_page,
        "us": usgeo_page,
        "us_trends": us_trends_page,
    },
}
