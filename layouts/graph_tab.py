import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from dash import dash_table
from layouts import styling 

def create_bar_plot(df, country, species):

    if type(country) == str:
        color_by = 'species'
        title = 'Population of Livestock in %s' % country
    else: 
        color_by = 'country'
        title = 'Population of %s' % species

    fig = px.bar(df, x='year', y='population', color=color_by,
                 color_discrete_sequence=px.colors.qualitative.Plotly, title = title)

    fig.update_xaxes(
        
        ticklabelmode="period",
        dtick = 1)

    return(fig)

def create_scatter_plot(df, country, species): 

    if type(country) == str:
        color_by = 'species'
        title = 'Population of Livestock in %s' % country
    else: 
        color_by = 'country'
        title = 'Population of %s' % species

    fig = px.line(df, x='year', y='population', color=color_by,
                 color_discrete_sequence=px.colors.qualitative.Plotly, markers=True, title = title)

    fig.update_xaxes(
        
        ticklabelmode="period",
        dtick = 1)
    
    return(fig)

graph = dcc.Graph(id = 'graph1', config = styling.plot_config)

content = dbc.Row(children=
            [
            styling.sidebar,
            dcc.Loading(id = 'loading-icon',
                        children=[
                        dbc.Col(graph)
                        ]
                        )
            ],
            style=styling.CONTENT_STYLE_GRAPHS
        )

