import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table
from layouts.styling import SIDEBAR_STYLE, CONTENT_STYLE_TABLES
import pandas as pd

def get_metadata_df(choice): 

    if choice == 'eurostat': 
        return(m_eurostat)
    elif choice == 'faostat':
        return(m_faostat)
    elif choice == 'faotier1': 
        return(m_faotier1)
    elif choice == 'woah':
        return(m_woah)
    elif choice == 'unfccc':
        return(m_unfccc)
    
###--------------Read in metadata-----------------------------------
m_eurostat = pd.read_csv('data/m_eurostat.csv')
m_faostat = pd.read_csv('data/m_faostat.csv')
m_faotier1 = pd.read_csv('data/m_faotier1.csv')
m_woah = pd.read_csv('data/m_oie.csv')
m_unfccc = pd.read_csv('data/m_unfccc.csv')

table = html.Div([
    html.P("Select a dataset on the left sidebar to view the metadata."),
    dash_table.DataTable(
            id='metadata-table',
            export_format='csv',
            style_cell={'textAlign': 'left', 'font-family':'sans-serif'},
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_data={
                'color': 'black',
            }
)])

sidebar_metadata = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset',value ='faostat', persistence=True, persistence_type='session'),
                html.H6(" ")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id = "sidebar-metadata",
    style=SIDEBAR_STYLE,
)

metadata_content = dbc.Row(
            [
            sidebar_metadata,
            dbc.Col(table, style = CONTENT_STYLE_TABLES)
            ]
)
