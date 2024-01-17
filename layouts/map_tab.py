import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from dash import dash_table
from layouts import styling 
import json

#******************* import Dataframes *******************#
CATTLE_DF = pd.read_csv('data/eth_csa_cattle_category.csv')
CATTLE_HEALTH_DF = pd.read_csv('data/eth_csa_cattle_health.csv')
SHEEP_CATEGORY_DF = pd.read_csv('data/eth_csa_sheep_category.csv')
SHEEP_HEALTH_DF = pd.read_csv('data/eth_csa_sheep_health.csv')
GOATS_CATEGORY_DF = pd.read_csv('data/eth_csa_goats_category.csv')
GOATS_HEALTH_DF = pd.read_csv('data/eth_csa_goats_health.csv')
CAMELS_CATEGORY_DF = pd.read_csv('data/eth_csa_camels_category.csv')
CAMELS_HEALTH_DF = pd.read_csv('data/eth_csa_camels_health.csv')
HORSES_CATEGORY_DF = pd.read_csv('data/eth_csa_horses_category.csv')
HORSES_HEALTH_DF = pd.read_csv('data/eth_csa_horses_health.csv')
DONKEYS_CATEGORY_DF = pd.read_csv('data/eth_csa_donkeys_category.csv')
DONKEYS_HEALTH_DF = pd.read_csv('data/eth_csa_donkeys_health.csv')
MULES_CATEGORY_DF = pd.read_csv('data/eth_csa_mules_category.csv')
MULES_HEALTH_DF = pd.read_csv('data/eth_csa_mules_health.csv')
POULTRY_INV_DF = pd.read_csv('data/eth_csa_poultry_inventory.csv')
POULTRY_HEALTH_DF = pd.read_csv('data/eth_csa_poultry_health.csv')
POULTRY_EGGS_DF = pd.read_csv('data/eth_csa_poultry_eggs.csv')
CATTLE_REG_HEALTH_DF = pd.read_csv('data/eth_regions_cattle_health.csv')
CATTLE_REG_POPULATION_DF = pd.read_csv('data/eth_regions_cattle_population.csv')

YEARS = sorted(CATTLE_DF['year'].unique())

def filterdf(code, column, df):
    if code is None:
        return df
    if isinstance(code,list):
        if len(code) == 0:
            return df
        return df[df[column].isin(code)]
    return df[df[column]==code]

#******************* Figure functions *******************#
def get_sex_distribution_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    match animal:
        case 'Cattle':
            table = CATTLE_DF
        case 'Sheep':
            table = SHEEP_CATEGORY_DF
        case 'Goats':
            table = GOATS_CATEGORY_DF
        case 'Camels':
            table = CAMELS_CATEGORY_DF
        case 'Horses':
            table = HORSES_CATEGORY_DF
        case 'Donkeys':
            table = DONKEYS_CATEGORY_DF
        case 'Mules':
            table = MULES_CATEGORY_DF

    df = filterdf(year_list,'year',table)
    df = df[df.id == 0]
    df = df.sort_values(by='year')

    match animal:
        case 'Cattle':
            df['male'] = df['male_lt_6mo'] + df['male_6mo_lt_1yr'] + df['male_1yr_lt_3yrs'] + df['male_3yrs_lt_10yrs'] + df['male_gte_10yrs']
            df['female'] = df['female_lt_6mo'] + df['female_6mo_lt_1yr'] + df['female_1yr_lt_3yrs'] + df['female_3yrs_lt_10yrs'] + df['female_gte_10yrs']
        case 'Sheep' | 'Goats':
            df['male'] = df['male_lt_6mo'] + df['male_6mo_lt_1yr'] + df['male_1yr_lt_2yrs'] + df['male_gte_2yrs']
            df['female'] = df['female_lt_6mo'] + df['female_6mo_lt_1yr'] + df['female_1yr_lt_2yrs'] + df['female_gte_2yrs']
        case 'Camels':
            df['male'] = df['male_lt_4yrs'] + df['male_gte_4yrs']
            df['female'] = df['female_lt_4yrs'] + df['female_gte_4yrs']
        case 'Horses' | 'Donkeys' | 'Mules':
            df['male'] = df['male_lt_3yrs'] + df['male_gte_3yrs']
            df['female'] = df['female_lt_3yrs'] + df['female_gte_3yrs']

    table_df = df[['year', 'male', 'female']]
    # table_df.columns = ["Year", "Male", "Female"]
    table_df.rename(columns={'year': 'Year', 'male': 'Male', 'female':'Female'}, inplace=True)
    table_df.insert(3, 'Calc. Total', df['male'] + df['female'])
    table_df.insert(4, 'Total', df[animal.lower()+'_total'])
    # print(animal.lower + '_total')
    # print(table_df.columns)
    print(table_df)
    # Creating graph
    fig_title = f'{demographic} {animal} Sex Distribution'   

    fig = go.Figure(
        data=[go.Table(
            # header=dict(values=['Year', 'Male Pop']),
            header=dict(values=list(table_df.columns)),
            cells=dict(values=[table_df.Year, table_df.Male, table_df.Female, table_df['Calc. Total'], table_df['Total']])
        )]
    )

    # fig = px.line(
    #     df_melt, 
    #     x='year',
    #     y='Population',
    #     color = 'Sex',
    #     labels={'year':'Year'},
    #     title=fig_title,
    #     color_discrete_sequence=px.colors.qualitative.Dark24,
    # )
    
    # fig.update_layout(
    #     margin={"r":10,"t":45,"l":10,"b":10},
    #     font=dict(
    #         size=16,
    #     )
    # )
    # fig.layout.autosize = True

    return fig

# Deprecated. To DELETE
# Potentially switch this to leaflet https://dash-leaflet.herokuapp.com/
my_color_scale = [[0.0, '#4c5c73'], [0.1, '#5D6C81'], [0.2, '#6F7C8F'], [0.3, '#818C9D'], [0.4, '#939DAB'],
                  [0.5, '#A5ADB9'], [0.6, '#B7BDC7'], [0.7, '#C9CED5'], [0.8, '#DBDEE3'], [0.9, '#EDEEF1'],
                  [1.0, '#FFFFFF']]

def create_map(merged_df, dataset, species, year):

    max_val = merged_df['population'].max()
    min_val = merged_df['population'].min()

    title = 'Population of %s in %s by Country <br><sup>Datasource: %s</sup>' % (species, year, dataset)

    fig = px.choropleth(merged_df, 
        locations='ISO3',
        color='population',
        range_color=(0,max_val),
        hover_data=['country', 'population'],
        color_continuous_scale='sunset',
        center={'lat':19, 'lon':11},
    )

    fig.update_geos(
        visible=False, resolution=50,
        showcountries=True, countrycolor="Black"
    )

    fig.update_layout(
        title_text = title,
        legend=dict(orientation='h',
        yanchor="bottom")
    )

    return(fig)

table = dcc.Graph(id = 'table1', config = styling.plot_config)

content = dbc.Row(children=
            [
            styling.sidebar,
            dcc.Loading(id = "loading-icon", 
                children=[
                dbc.Col(table)])
            ], style = styling.CONTENT_STYLE_GRAPHS
        )
