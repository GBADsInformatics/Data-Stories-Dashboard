import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "9rem",
    "left": 0,
    "bottom": "1rem",
    "width": "21rem",
    "padding": "2rem 2rem 2rem",
    "background-color": "#f8f9fa",
    "overflow": "auto"
}

# COMMENT_STYLE = {
#     "position": "fixed",
#     "top": "14rem",
#     "left": "61rem",
#     "bottom": "1rem",
#     "right": "2rem",
#     "width": "21rem",
#     "padding": "2rem 2rem 2rem",
#     "background-color": "#f8f9fa",
#     "overflow": "auto"
# }

# TAB_STYLE = {
#     "position": "fixed",
#     "top": "8rem",
#     "left": "61rem",
#     "bottom": "1rem",
#     "right": "2rem",
#     "width": "21rem",
#     "padding": "2rem 2rem 2rem",
#     "background-color": "#f8f9fa",
#     "overflow": "auto"
# }


COMMENT_STYLE = {
    "position": "fixed",
    "top": "42rem",
    "left": "21rem",
    "bottom": "1rem",
    "right": "2rem",
    # "width": "21rem",
    "padding": "2rem 2rem 2rem",
    "background-color": "#f8f9fa",
    "overflow": "auto"
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
    "top":"4rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "5rem 2rem 2rem",
    "position": "fixed"
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
                html.H6("Demographic:"),
                dcc.Dropdown(
                    id='demographic',
                    options=['National', 'Regional'],
                    value='National',
                    clearable=False,
                    persistence_type='session', persistence=True
                ),
                html.H6(" "),
                html.H6("Animal"),
                dcc.Dropdown(
                    id='animal',
                    options=['Cattle', 'Poultry', 'Sheep', 'Goats', 'Camels', 'Horses', 'Donkeys', 'Mules'],
                    value='Cattle',
                    clearable=False,
                    persistence_type='session', persistence=True
                ),
                html.H6(" "),
                html.H6("Table"),
                dcc.Dropdown(
                    id='table',
                    options=['Sex Distribution', 'Breed Sex Distribution', 'Mortality Distribution', 'Mortality Distribution by Sex', 'Mortality by Cause', 'Vaccination'],
                    value='Sex Distribution',
                    clearable=False,
                    persistence_type='session', persistence=True
                ),
                html.H6(" "),
                html.H6("Year"),
                html.H6(" "),
                dcc.RangeSlider(
                    step=1, 
                    marks=None,
                    value=[0,0],
                    id='year',
                    className='year-slider',
                    tooltip={"placement": "top", "always_visible": True},
                    dots=True,
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)