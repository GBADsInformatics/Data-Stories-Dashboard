from __future__ import annotations
import json
from logging import disable
from operator import gt
from os.path import exists
import requests
import numpy as np
import pandas as pd
import math
import urllib.parse
import dash
from dash import dcc,html,dash_table,callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date, datetime
from functools import wraps
from flask import session, redirect
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from dash.exceptions import PreventUpdate
from layouts import *
from dash.dependencies import Input, Output, State
# from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
import json
from textwrap import dedent

# Importing dataset
DATAFRAME = pd.read_csv('datasets/example_data.csv')
CATTLE_DF = pd.read_csv('datasets/eth_csa_cattle_category.csv')
CATTLE_HEALTH_DF = pd.read_csv('datasets/eth_csa_cattle_health.csv')

# Insert data cleaning here
COUNTRIES = sorted(DATAFRAME['Country'].unique())
YEARS = sorted(CATTLE_DF['year'].unique())

METASET = 'datasets/metadata/'
METADATA_SOURCES = {
    'EXAMPLE DATA':{ # Datasources added in this section needs to be updated in layouts.py line 205
        'METADATA': METASET+'ExampleMetadata.csv', # The displayed meta data table
        'DOWNLOAD': METASET+'ExampleMetadata.json', # For download as json button
        'PROVENANCE': METASET+'ExampleProvenance.txt', # Provenance for dataset
    },
}
METADATA_OTHER = {
    'GLOSSARY':{
        'CSV': METASET+'MetadataGlossary.csv',
    },
}


def filterdf(code, column, df):
    if code is None:
        return df
    if isinstance(code,list):
        if len(code) == 0:
            return df
        return df[df[column].isin(code)]
    return df[df[column]==code]


# PROFILE_KEY = 'profile'
# JWT_PAYLOAD = 'jwt_payload'

def init_dashboard(server):
            
    dash_app = dash.Dash(__name__,
        server=server,
        title='Template Dashboard',
        routes_pathname_prefix="/dash/",
        external_stylesheets=[
            # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP
        ],
    )
    # Setting active page
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False)
    ],id='page-content')
    init_callbacks(dash_app)
    return dash_app.server

#******************* Figure functions *******************# 
def get_poultry_fig(country, year):
    
    # Filtering the dataframe to only include specific years/countries
    year_list = []
    y_value = year[0]
    y_max = year[-1]
    while y_value <= y_max:
        year_list.append(y_value)
        y_value += 1
    
    df = filterdf(country,'Country',DATAFRAME)
    df = filterdf(year_list,'Year',df)
    

    # Creating graph
    fig_title = \
        f'Percentage of Laying Hens by '+\
        f'Production System '+\
        f'{"in All Countries" if country is None or len(country) == 0 else "in " + ",".join(df["Country"].unique())}'

    fig = px.line(
        df, 
        x='Year',
        y='Total',
        color='Country',
        title=fig_title,
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    
    fig.update_layout(
        margin={"r":10,"t":45,"l":10,"b":10},
        font=dict(
            size=16,
        )
    )
    fig.layout.autosize = True

    return fig

def get_sex_distribution_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')

    df['male'] = df['male_lt_6mo'] + df['male_6mo_lt_1yr'] + df['male_1yr_lt_3yrs'] + df['male_3yrs_lt_10yrs'] + df['male_gte_10yrs']
    df['female'] = df['female_lt_6mo'] + df['female_6mo_lt_1yr'] + df['female_1yr_lt_3yrs'] + df['female_3yrs_lt_10yrs'] + df['female_gte_10yrs']
    df_melt = df.melt(id_vars='year', value_vars=['male', 'female'], var_name='Sex', value_name='Population') 
    
    # Creating graph
    fig_title = f'{animal} Sex Distribution by {demographic}'   

    fig = px.line(
        df_melt, 
        x='year',
        y='Population',
        color = 'Sex',
        labels={'year':'Year'},
        title=fig_title,
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    
    fig.update_layout(
        margin={"r":10,"t":45,"l":10,"b":10},
        font=dict(
            size=16,
        )
    )
    fig.layout.autosize = True

    return fig

def get_breed_sex_distribution_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')

    df['male'] = df['male_indigenous'] + df['male_hybrid'] + df['male_exotic']
    df['female'] = df['female_indigenous'] + df['female_hybrid'] + df['female_exotic']
    df_melt = df.melt(id_vars='year', value_vars=['male', 'female'], var_name='Sex', value_name='Population') 
    
    # Creating graph
    fig_title = f'{animal} Breed Sex Distribution by {demographic}'   

    fig = px.line(
        df_melt, 
        x='year',
        y='Population',
        color = 'Sex',
        labels={'year':'Year'},
        title=fig_title,
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    
    fig.update_layout(
        margin={"r":10,"t":45,"l":10,"b":10},
        font=dict(
            size=16,
        )
    )
    fig.layout.autosize = True

    return fig

def get_perc_mortality_distribution_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_HEALTH_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')
    
    df['male'] = df['male_deaths'] / df['total_deaths'] * 100
    df['female'] = df['female_deaths'] / df['total_deaths'] *100
    df_melt = df.melt(id_vars='year', value_vars=['male', 'female'], var_name='Sex', value_name='% Deaths') 
    
    # Creating graph
    fig_title = f'{animal} Mortality Distribution by total population and {demographic}'   

    fig = px.bar(
        df_melt, 
        x='year',
        y='% Deaths',
        color = 'Sex',
        labels={'year':'Year'},
        title=fig_title,
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    
    fig.update_layout(
        margin={"r":10,"t":45,"l":10,"b":10},
        font=dict(
            size=16,
        )
    )
    fig.layout.autosize = True

    return fig


def get_perc_sex_mortality_distribution_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')
    healthdf = filterdf(year_list,'year',CATTLE_HEALTH_DF)
    healthdf = healthdf[healthdf.id == 0]
    healthdf = healthdf.sort_values(by='year')
    df.index = healthdf.index

    
    df['male_total'] = df['male_lt_6mo'] + df['male_6mo_lt_1yr'] + df['male_1yr_lt_3yrs'] + df['male_3yrs_lt_10yrs'] + df['male_gte_10yrs']
    df['female_total'] = df['female_lt_6mo'] + df['female_6mo_lt_1yr'] + df['female_1yr_lt_3yrs'] + df['female_3yrs_lt_10yrs'] + df['female_gte_10yrs']
    df['male'] = healthdf['male_deaths'] / df['male_total'] *100
    df['female'] = healthdf['female_deaths'] / df['female_total'] * 100
    df_melt = df.melt(id_vars='year', value_vars=['male', 'female'], var_name='Sex', value_name='% Deaths') 

    # Creating graph
    fig_title = f'{animal} Mortality Distribution from sex population and {demographic}'   

    fig = px.bar(
        df_melt, 
        x='year',
        y='% Deaths',
        color = 'Sex',
        labels={'year':'Year'},
        title=fig_title,
        color_discrete_sequence=px.colors.qualitative.Dark24,
        barmode='group'
    )
    
    fig.update_layout(
        margin={"r":10,"t":45,"l":10,"b":10},
        font=dict(
            size=16,
        )
    )
    fig.layout.autosize = True

    return fig


def get_cause_mortality_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_HEALTH_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')
    
    df['disease'] = df[f'{animal.lower()}_death_disease'] / df['total_deaths'] * 100
    df['other'] = df[f'{animal.lower()}_death_other'] / df['total_deaths'] *100
    df_melt = df.melt(id_vars='year', value_vars=['disease', 'other'], var_name='% Death by', value_name='% Deaths') 
    
    # Creating graph
    fig_title = f'{animal} Mortality Distribution by total population and {demographic}'   

    fig = px.bar(
        df_melt, 
        x='year',
        y='% Deaths',
        color = '% Death by',
        labels={'year':'Year'},
        title=fig_title,
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    
    fig.update_layout(
        margin={"r":10,"t":45,"l":10,"b":10},
        font=dict(
            size=16,
        )
    )
    fig.layout.autosize = True

    return fig

def get_vaccinated_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')
    healthdf = filterdf(year_list,'year',CATTLE_HEALTH_DF)
    healthdf = healthdf[healthdf.id == 0]
    healthdf = healthdf.sort_values(by='year')
    df.index = healthdf.index
    
    healthdf.loc[healthdf[f'{animal.lower()}_vac_total'] == -1, f'{animal.lower()}_vac_total'] = None
    healthdf.loc[healthdf[f'{animal.lower()}_vac_anthrax'] == -1, f'{animal.lower()}_vac_anthrax'] = None
    healthdf.loc[healthdf[f'{animal.lower()}_vac_blackleg'] == -1, f'{animal.lower()}_vac_blackleg'] = None
    healthdf.loc[healthdf[f'{animal.lower()}_vac_pleuro_pneumonia'] == -1, f'{animal.lower()}_vac_pleuro_pneumonia'] = None
    healthdf.loc[healthdf[f'{animal.lower()}_vac_hemorrhagic_septicemia'] == -1, f'{animal.lower()}_vac_hemorrhagic_septicemia'] = None
    healthdf.loc[healthdf[f'{animal.lower()}_vac_rinderpest'] == -1, f'{animal.lower()}_vac_rinderpest'] = None
    healthdf.loc[healthdf[f'{animal.lower()}_vac_other'] == -1, f'{animal.lower()}_vac_other'] = None

    healthdf['total'] = healthdf[f'{animal.lower()}_vac_total'] / df[f'{animal.lower()}_total'] * 100
    healthdf['anthrax'] = healthdf[f'{animal.lower()}_vac_anthrax'] / df[f'{animal.lower()}_total'] * 100
    healthdf['blackleg'] = healthdf[f'{animal.lower()}_vac_blackleg'] / df[f'{animal.lower()}_total'] * 100
    healthdf['pleuro pneumonia'] = healthdf[f'{animal.lower()}_vac_pleuro_pneumonia'] / df[f'{animal.lower()}_total'] * 100
    healthdf['hemorrhagic septicemia'] = healthdf[f'{animal.lower()}_vac_hemorrhagic_septicemia'] / df[f'{animal.lower()}_total'] * 100
    healthdf['rinderpest'] = healthdf[f'{animal.lower()}_vac_rinderpest'] / df[f'{animal.lower()}_total'] * 100
    healthdf['other'] = healthdf[f'{animal.lower()}_vac_other'] / df[f'{animal.lower()}_total'] * 100
    df_melt = healthdf.melt(id_vars='year', value_vars=['total', 'anthrax', 'blackleg', 'pleuro pneumonia', 'hemorrhagic septicemia', 'rinderpest', 'other'], var_name='vaccination type', value_name='% vaccinated') 

    # Creating graph
    fig_title = f'Proportion of {animal} vaccinated against diseases by {demographic}'   

    fig = px.line(
        df_melt, 
        x='year',
        y='% vaccinated',
        color = 'vaccination type',
        labels={'year':'Year'},
        title=fig_title,
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )
    
    fig.update_layout(
        margin={"r":10,"t":45,"l":10,"b":10},
        font=dict(
            size=16,
        )
    )
    fig.layout.autosize = True

    return fig


# isLoggedIn = False
# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         global isLoggedIn
#         if PROFILE_KEY not in session:
#             isLoggedIn = False
#             return redirect('/login')
#         isLoggedIn = True
#         return f(*args, **kwargs)
#     return decorated

# def checkRole():
#     isRole = False
#     y = json.dumps(session[JWT_PAYLOAD])
#     person_dict = json.loads(y)
#     p = (person_dict["http://gbad.org/roles"]) # This link sends you to the Ground Based Air Defense website lmao
#     stringver = json.dumps(p)
#     print(stringver)
#     if 'Verified User' in stringver:
#         isRole = True
#     else:
#         isRole = False
#     return isRole

# def getJWT(personDict,userCat):
#     p = (personDict[userCat])
#     stringVer = json.dumps(p)
#     s1 = stringVer.replace("[]","")
#     strippedString = s1.strip('"')
#     return strippedString

# @requires_auth
# def getUserContent():
#     y = json.dumps(session[JWT_PAYLOAD])
#     personDict = json.loads(y)
#     userEmail = getJWT(personDict,"email")
#     print(userEmail)
#     return userEmail


##CALLBACKS -------------------------------------------------------------------------------------------------------------------------------------------------------------
def init_callbacks(dash_app):
    
    # # Callbacks to handle login components
    # @dash_app.callback(
    #     Output(component_id='login-button', component_property='style'),
    #     Input('url', 'pathname')
    # )
    # @requires_auth
    # def login_button(pathname):
    #     checkRole()
    #     return {'margin-left': '5px', 'display': 'none'}
    
    # @dash_app.callback(
    #     Output(component_id='logout-button', component_property='style'),
    #     Input('url', 'pathname')
    # )
    # @requires_auth
    # def logout_button(pathname):
    #     return {'margin-top': '10px', 'margin-right':'10px', 'float': 'right'}

    # # Callback to handle feedback.
    # @dash_app.callback(
    #     Output('feedback-text', 'value'),
    #     Output('feedback-button', 'disabled'),
    #     Output('feedback-text', 'disabled'),
    #     Input("feedback-button", "n_clicks"),
    #     State('feedback-text', 'value')
    # )
    # def feedback_box(n, text):
    #     if (n > 0 and text != None and text != ""):
    #         outF = open("feedback.txt", "a")
    #         outF.writelines('["'+text+'"]\n')
    #         outF.close()
    #         return\
    #             "Thank you for your feedback",\
    #             True,\
    #             True
    #     else:
    #         print("no")
    
    # Callback to handle changing the page based on the pathname provided.
    @dash_app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == '/dash/':
            layout = page_1
        else:
            layout = "404"
        return layout


    ##################################
    # Laying Hens Specific Callbacks #
    ##################################

    # Update stored options
    @dash_app.callback(
        Output('stored-options', 'data'),
        [State('tabs', 'value')],
        # Input('options-countries-a', 'value'),
        Input('options-countries-b', 'value'),
        Input('options-year-a', 'value'),
        Input('options-year-b', 'value'),
    )
    def update_stored_options_a(tab, drop1b, drop2a, drop2b):
        if tab == 'tab-2':
            return {'options-country':drop1b,'options-year':drop2b}
        else:
            return {'options-year':drop2a}


    # Update options values on changing tab
    @dash_app.callback(
        # Output('options-countries-a', 'value'),
        Output('options-countries-b', 'value'),
        Output('options-year-a', 'value'),
        Output('options-year-b', 'value'),
        [Input('tabs', 'value')],
        State('stored-options', 'data'),
    )
    def options_on_tab_change(selected_tab,stored_options):
        if stored_options is None:
            return None, [2005, YEARS[-1]], [2005, YEARS[-1]]
        return stored_options['options-country'],\
            stored_options['options-year'],stored_options['options-year']


    # Init dropdowns
    @dash_app.callback(
        # Output('options-countries-a', 'options'),
        Output('options-countries-b', 'options'),
        Output('year-container-a', 'children'),
        Output('year-container-b', 'children'),
        Input('dummy_div', 'children'),
    )
    def dropdown_options(_a):
        year1 = [
            html.H5("Year",style={"margin":"0.4rem 0 0.2rem 0"}),
            html.Div(
                className='year-slider-container',
                children=[
                    dcc.RangeSlider(
                        step=1, 
                        min=2005,
                        max=YEARS[-1],
                        value=[2005, YEARS[-1]],
                        marks=None,
                        id='options-year-a',
                        className='year-slider',
                        tooltip={"placement": "top", "always_visible": True},
                        dots=True,
                    )
                ]
            ),
        ]
        year2 = [
            html.H5("Year",style={"margin":"0.4rem 0 0.2rem 0"}),
            html.Div(
                className='year-slider-container',
                children=[
                    dcc.RangeSlider(
                        step=1, 
                        min=YEARS[0],
                        max=YEARS[-1],
                        value=[YEARS[0], YEARS[-1]],
                        marks=None,
                        id='options-year-b',
                        className='year-slider',
                        tooltip={"placement": "top", "always_visible": True},
                        dots=True,
                    )
                ]
            ),
        ]

        # Creating year slider
        return COUNTRIES,\
            year1,year2

    # Displaying graph
    # @dash_app.callback(
    #     Output('graph-container', 'children'),
    #     Input('options-countries-a', 'value'),
    #     Input('options-year-a', 'value'),
    # )
    # def create_graph(country, year):
        
    #     # Filtering the dataframe to only include specific years/countries
    #     year_list = []
    #     y_value = year[0]
    #     y_max = year[-1]
    #     while y_value <= y_max:
    #         year_list.append(y_value)
    #         y_value += 1
        
    #     df = filterdf(country,'Country',DATAFRAME)
    #     df = filterdf(year_list,'Year',df)
        

    #     # Creating graph
    #     fig_title = \
    #         f'Percentage of Laying Hens by '+\
    #         f'Production System '+\
    #         f'{"in All Countries" if country is None or len(country) == 0 else "in " + ",".join(df["Country"].unique())}'

    #     fig = px.line(
    #         df, 
    #         x='Year',
    #         y='Total',
    #         color='Country',
    #         title=fig_title,
    #         color_discrete_sequence=px.colors.qualitative.Dark24,
    #     )
        
    #     fig.update_layout(
    #         margin={"r":10,"t":45,"l":10,"b":10},
    #         font=dict(
    #             size=16,
    #         )
    #     )
    #     fig.layout.autosize = True

    #     return dcc.Graph(className='main-graph-size', id="main-graph", figure=fig)

    # Displaying graph
    @dash_app.callback(
        Output('graph-container', 'children'),
        Input('demographic-dropdown', 'value'),
        Input('animal-dropdown', 'value'),
        Input('table-dropdown', 'value'),
        # Input('options-countries-a', 'value'),
        Input('options-year-a', 'value'),
    )
    def create_graph(demographic, animal, table, year):

        match table:
            # case "test Poultry":
            #     fig = get_poultry_fig(country, year)
            case "Sex Distribution":
                fig = get_sex_distribution_fig(demographic, animal, year)
            case "Breed Sex Distribution":
                fig = get_breed_sex_distribution_fig(demographic, animal, year)
            case "Mortality Distribution":
                fig = get_perc_mortality_distribution_fig(demographic, animal, year)
            case "Mortality Distribution by Sex":
                fig = get_perc_sex_mortality_distribution_fig(demographic, animal, year)
            case "Mortality by Cause":
                fig = get_cause_mortality_fig(demographic, animal, year)
            case "Vaccination":
                fig = get_vaccinated_fig(demographic, animal, year)

        return dcc.Graph(className='main-graph-size', id="main-graph", figure=fig)

    # Updating Datatable
    @dash_app.callback(
        Output('data-table-container','children'),
        Input('options-countries-b', 'value'),
        Input('options-year-b', 'value'),
    )
    def render_table(country,year):
        
        # Filtering the dataframe to only include specific years/countries
        year_list = []
        y_value = year[0]
        y_max = year[-1]
        while y_value <= y_max:
            year_list.append(y_value)
            y_value += 1

        df = filterdf(country,'Country',DATAFRAME)        
        df = filterdf(year_list,'Year',df)


        # Rendering the data table
        cols = [{"name": i, "id": i,"hideable":True} for i in df.columns]
        cols[0] = {"name": "ID", "id": cols[0]["id"],"hideable":True}
        datatable = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=cols,
            export_format="csv",
        )
        return datatable


    # Updating Alert
    @dash_app.callback(
        Output('alert-container','children'),
        # Input('options-countries-a', 'value'),
        Input('options-year-a', 'value'),
    )
    def render_alert(year):
        amsg = None

        # ADD LOGIC HERE TO CREATE ALERT MESSAGES
        # amsg syntax:
        # amsg = ['Please choose 1 type when graphing multiple countries.','danger']

        if amsg is None: 
            return None
        else:
            return dbc.Alert([html.H5('Warning'),amsg[0]], color=amsg[1])
    
    
    ### Updating METADATA ###
    @dash_app.callback(
        Output('metadata-container','children'),
        Output('download-container','children'),
        Output('meta-type','data'),
        Input('meta-gbads-button','n_clicks'),
        Input('provenance-button','n_clicks'),
        Input('glossary-button','n_clicks'),
        Input('meta-source-dropdown','value'),
        State('meta-type','data'),
    )
    def update_meta(MetaButton,ProvButton,GlossButton,MetaValue,MetaType):        
        # Filtering data with the menu values
        pressed = callback_context.triggered[0]['prop_id'].split('.')[0]
        df = ''
        downloadButton = ''
        meta=MetaType

        if (pressed == 'meta-source-dropdown' and MetaType == 'meta') or pressed == 'meta-gbads-button' or pressed == '':
            meta = 'meta'
            df = pd.read_csv(METADATA_SOURCES[MetaValue]['METADATA'], names=['Col1', 'Col2'])
            # # UNCOMMENT FOR DOWNLOAD AS JSON BUTTON
            # req = requests.get(METADATA_SOURCES[MetaValue]['DOWNLOAD'])
            # json_data = json.dumps(req.json(), indent=2, ensure_ascii=False).replace('#', '%23')
            # downloadButton = html.A(
            #     href=f"data:text/json;charset=utf-8,{json_data}",
            #     children='Download Metadata',download=METADATA_SOURCES[MetaValue]['DOWNLOAD'].split('/')[-1],id='meta-download-button',className='download-button'
            # )
        elif (pressed == 'meta-source-dropdown' and MetaType == 'pro') or pressed == 'provenance-button':
            meta = 'pro'
            with open(METADATA_SOURCES[MetaValue]['PROVENANCE']) as file:
                df = dcc.Markdown(file.readlines())
            return df,downloadButton,meta
        elif pressed == 'glossary-button':
            df = pd.read_csv(METADATA_OTHER['GLOSSARY']['CSV'], names=['Col1', 'Col2'])

        datatable = dash_table.DataTable(
            data=df.to_dict('records'),
            # Removing header
            css=[{'selector': 'tr:first-child','rule': 'display: none'}],
            # Adding hyperlinks
            columns=[
                {'name': 'Col1', 'id': 'Col1'},
                {'name': 'Col2', 'id': 'Col2', 'presentation': 'markdown'}
            ],
            # Styling
            style_cell={'textAlign': 'left'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'Col1',
                    },
                    'fontWeight': 'bold'
                }
            ],
            cell_selectable=True,
        )
        return datatable,downloadButton,meta