import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from app import app

load_figure_template('LUX')

GBADSLOGOB = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-Black-sm.png"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "8rem",
    "left": 0,
    "bottom": "2rem",
    "width": "24rem",
    "padding": "2rem 2rem 2rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

ACTIVE_TAB_STYLE = {
    "color": "#FFA500"
}

CONTENT_STYLE = {
    "top":"8rem",
    "margin-left": "25rem",
    "margin-right": "8rem",
    "bottom": "2rem",
    "padding": "7rem 2rem 2rem",
    "overflow": "scroll"
}

###-------------Components------------------------------------


title = html.Div([
                    html.Img(src=GBADSLOGOB, className="header-logo"),
                    html.H2('Livestock Population')
                ],
                style={"padding": "1rem 1rem", "position":"fixed"}
                )

tabs = html.Div([
    
    html.H1(" "),
    html.H2(" "),
        dbc.Tabs(
            [
                dbc.Tab(label="Graph", active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label="Map",active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Download Data', active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Metadata', active_label_style=ACTIVE_TAB_STYLE)
            ],
        id='tabs', style={"padding": "1rem 1rem", "position":"fixed"})
]
)

###--------------Build the layout------------------------------------

app_layout = html.Div(

    children = [
        dbc.Row(children = [
            dbc.Col(title),
            dbc.Col(tabs)
        ]
        ),
        dbc.Row(children = [html.Div(id='tabs-content')]),
        dcc.Store(id='store')
        ]
)

