import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "8rem",
    "left": 0,
    "bottom": "2rem",
    "width": "21rem",
    "padding": "2rem 2rem 2rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

CONTENT_STYLE_TABLES = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "5rem 2rem 2rem",
    "overflow": "scroll",
    "position": "fixed"
}

CONTENT_STYLE_GRAPHS = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "5rem 2rem 2rem",
    "position": "fixed"
}

MAP_STYLE = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "7rem 2rem 2rem",
    "overflow": "scroll",
}

plot_config = {'displayModeBar': True,
          'displaylogo': False}

sidebar_download = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6("Select multiple:", id='choice-title'),
                dcc.RadioItems(
                ['Species', 'Countries'], 'Species', inline=True, id='choice', persistence_type='session', persistence=True
                ),
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value='faostat', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country', value = 'Canada', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species', value = ['Cattle'], persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Start year:"),
                dcc.Dropdown(id = 'start year', value = 1996, persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("End year:"),
                dcc.Dropdown(id = 'end year', value = 2020, persistence_type='session', persistence=True)
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

sidebar = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6("Select multiple:", id='choice-title'),
                dcc.RadioItems(
                ['Species', 'Countries'], 'Species', inline=True, id='choice', persistence_type='session',persistence=True
                ),
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value='faostat', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country', value = 'Canada', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species', value = ['Cattle'],persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Start year:"),
                dcc.Dropdown(id = 'start year', value = 1996, persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("End year:"),
                dcc.Dropdown(id = 'end year', value = 2020, persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Graph type:"),
                dcc.Dropdown(id = 'plot', value = 'stacked bar', options = ['stacked bar','scatter line'], persistence_type='session', persistence=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

sidebar_map = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value = 'faostat', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Country:"),
                dcc.Dropdown(id = 'country-map', value = 'Canada', multi=True,persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species-map', value = 'Cattle', multi=False,persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Year:"),
                dcc.Dropdown(id = 'year-map', value = 1990,persistence_type='session', persistence=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)