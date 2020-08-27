main_page = {
    # This defines what dataframe the page will presume to use by default
    # Individual banks can set their data source via {"args": {"dataid": ...}}
    "dataid": "stock",
    "banks": {
        # The simplest bank entry: a uid key with the type specified in the dictionary
        "analytics": {"type": "analytics_set"},
        "interval": {"type": "date_slider", "args": {"variant": "range"}},
        # Supply args to the bank to control its behavior and appearance
        # In this case, we're indicating the filter dropdowns should stack vertically
        "symbols": {"type": "selector"},  # , "args": {"columns": ["symbol"]}},
        "traces": {
            "type": "graph",
            # These arguments are passed into the method that constructs the bank
            "args": {"mode": "lines",},
        },
    },
    # Defines a 2D grid of banks, determining their layout on the page
    "layout": [["symbols", "interval", "analytics"], ["traces"]],
    # Lastly, this specifies which banks feed their outputs as inputs to other banks.
    # Callbacks will be generated via the template based on these.
    "connections": {
        "symbols": {"traces"},
        "interval": {"traces"},
        "analytics": {"traces"},
    },
}

descriptor = {
    "name": "beginner_tutorial",
    # Supply theme keywords to quickly change the look
    # E.g. dark, flat, sparse
    "theme": "dark",
    "appbar": {
        "title": "Tech Stock Prices",
        "subtitle": "A simple Bento starting point",
    },
    "data": {"stock": {"module": "bento.sample_data.stock"}},
    "pages": {"main": main_page},
}
