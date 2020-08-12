description = """
This dashboard attempts to shine a little light on the US Supreme Court, by showing data
from a few annualized metrics: cases decided, 'progressivity', and decision splits.
Progressivity was qualified by the data source (WUSTL Supreme Court Database).
The point color represents the chief justice presiding over the court, and the tooltip
text provides the details.
"""

trend_page = {
    "dataid": "supreme",
    "banks": {
        "axis": {"type": "axis_controls", "width": 3, "args": {"use": "y"}},
        "info": {"type": "info", "width": 9, "args": {"text": description}},
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
    "layout": [["axis", "info"], ["series"]],
    "connections": {"axis": {"series"}},
}

descriptor = {
    "name": "simple",
    "theme": "sparse",
    "theme_dict": {"color__on_primary": "white"},
    "appbar": {"title": "Supreme Court Cases", "image": "usflag.jpg",},
    "data": {"supreme": {"module": "supreme_court.df_supreme"},},
    "pages": {"trend": trend_page,},
}
