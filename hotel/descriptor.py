scatter_page = {
    "dataid": "hotel",
    "banks": {
        "axes": {
            "type": "axis_controls",
            "axes": ["x", "y", "size"],
            "symbol.default": "conversion",
            "scale": True,
        },
        # "filters": {"type": "selector", "columns": ("hotel_size", "home_pop"),},
        "scatter": {
            "type": "graph",
            "category": "normal",
            "subvariant": "training",
            "symbol_column": "conversion",
            "mode": "markers",
        },
    },
    "layout": [["axes", "filters"], ["scatter"]],
    "connections": {"axes": {"scatter"}, "filters": {"scatter"}},
}

data_page = {
    "banks": {
        "hotel_table": {
            "type": "data_table",
            "args": {
                "dataid": "hotel",
                "default": [
                    "home_city",
                    "home_pop",
                    "dest_city",
                    "dest_pop",
                    "distance",
                    "hotel_size",
                    "conversion",
                ],
            },
        },
    },
    "layout": [["hotel_table"]],
    "connections": {},
}

descriptor = {
    "name": "allen",
    "theme": "dark sparse flat",
    "theme_dict": {"color__primary": "#fc7f03"},
    "appbar": {
        "title": "Generated Hotel Data",
        "subtitle": "Interactively viewing train data",
    },
    "data": {"hotel": {"module": "hotel.df_hotel"}},
    "pages": {"data": data_page, "scatter": scatter_page},
}
