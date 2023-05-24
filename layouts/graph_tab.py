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

    match animal:
        case 'Cattle':
            table = CATTLE_DF
        case 'Sheep':
            table = SHEEP_CATEGORY_DF
        case 'Goats':
            table = GOATS_CATEGORY_DF

    df = filterdf(year_list,'year',table)
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

    match animal:
        case 'Cattle':
            table = CATTLE_HEALTH_DF
        case 'Sheep':
            table = SHEEP_HEALTH_DF
        case 'Goats':
            table = GOATS_HEALTH_DF
        case 'Camels':
            table = CAMELS_HEALTH_DF
        case 'Horses':
            table = HORSES_HEALTH_DF
        case 'Donkeys':
            table = DONKEYS_HEALTH_DF
        case 'Mules':
            table = MULES_HEALTH_DF

    df = filterdf(year_list,'year',table)
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

    match animal:
        case 'Cattle':
            table = CATTLE_DF
            table2 = CATTLE_HEALTH_DF
        case 'Sheep':
            table = SHEEP_CATEGORY_DF
            table2 = SHEEP_HEALTH_DF
        case 'Goats':
            table = GOATS_CATEGORY_DF
            table2 = GOATS_HEALTH_DF
        case 'Camels':
            table = CAMELS_CATEGORY_DF
            table2 = CAMELS_HEALTH_DF
        case 'Horses':
            table = HORSES_CATEGORY_DF
            table2 = HORSES_HEALTH_DF
        case 'Donkeys':
            table = DONKEYS_CATEGORY_DF
            table2 = DONKEYS_HEALTH_DF
        case 'Mules':
            table = MULES_CATEGORY_DF
            table2 = MULES_HEALTH_DF
            
    df = filterdf(year_list,'year',table)
    df = df[df.id == 0]
    df = df.sort_values(by='year')
    healthdf = filterdf(year_list,'year',table2)
    healthdf = healthdf[healthdf.id == 0]
    healthdf = healthdf.sort_values(by='year')
    df.index = healthdf.index

    
    match animal:
        case 'Cattle':
            df['male_total'] = df['male_lt_6mo'] + df['male_6mo_lt_1yr'] + df['male_1yr_lt_3yrs'] + df['male_3yrs_lt_10yrs'] + df['male_gte_10yrs']
            df['female_total'] = df['female_lt_6mo'] + df['female_6mo_lt_1yr'] + df['female_1yr_lt_3yrs'] + df['female_3yrs_lt_10yrs'] + df['female_gte_10yrs']
        case 'Sheep' | 'Goats':
            df['male_total'] = df['male_lt_6mo'] + df['male_6mo_lt_1yr'] + df['male_1yr_lt_2yrs'] + df['male_gte_2yrs']
            df['female_total'] = df['female_lt_6mo'] + df['female_6mo_lt_1yr'] + df['female_1yr_lt_2yrs'] + df['female_gte_2yrs']
        case 'Camels':
            df['male_total'] = df['male_lt_4yrs'] + df['male_gte_4yrs']
            df['female_total'] = df['female_lt_4yrs'] + df['female_gte_4yrs']
        case 'Horses' | 'Donkeys' | 'Mules':
            df['male_total'] = df['male_lt_3yrs'] + df['male_gte_3yrs']
            df['female_total'] = df['female_lt_3yrs'] + df['female_gte_3yrs']
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

    match animal:
        case 'Cattle':
            table = CATTLE_HEALTH_DF
        case 'Sheep':
            table = SHEEP_HEALTH_DF
        case 'Goats':
            table = GOATS_HEALTH_DF
        case 'Camels':
            table = CAMELS_HEALTH_DF
        case 'Poultry':
            table = POULTRY_HEALTH_DF
        case 'Horses':
            table = HORSES_HEALTH_DF
        case 'Donkeys':
            table = DONKEYS_HEALTH_DF
        case 'Mules':
            table = MULES_HEALTH_DF

    df = filterdf(year_list,'year',table)
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

def get_vaccinated_fig(demographic, animal, year, regionCode):
    region = ""
    year_list = list(range(year[0], year[-1]+1))

    if (demographic == 'National'):
        match animal:
            case 'Cattle':
                table = CATTLE_DF
                table2 = CATTLE_HEALTH_DF
            case 'Sheep':
                table = SHEEP_CATEGORY_DF
                table2 = SHEEP_HEALTH_DF
            case 'Goats':
                table = GOATS_CATEGORY_DF
                table2 = GOATS_HEALTH_DF
            case 'Camels':
                table = CAMELS_CATEGORY_DF
                table2 = CAMELS_HEALTH_DF

        df = filterdf(year_list,'year',table)
        df = df[df.id == 0]
        healthdf = filterdf(year_list,'year',table2)
        healthdf = healthdf[healthdf.id == 0]
    else:
        df = filterdf(year_list,'year',CATTLE_REG_POPULATION_DF)
        df = df[df.flag == regionCode]
        healthdf = filterdf(year_list,'year',CATTLE_REG_HEALTH_DF)
        healthdf = healthdf[healthdf.flag == regionCode]
        match regionCode:
            case 'AF':
                region = 'Afar '
            case 'AM':
                region = 'Amhara '
            case 'OR':
                region = 'Oromia '
            case 'SN':
                region = 'SNNP '
    df = df.sort_values(by='year')
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
    fig_title = f'{region}Proportion of {animal} vaccinated against diseases by {demographic}'   

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

# regional figures
def get_population_fig_by_sex(demographic, animal, year, sex):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_REG_POPULATION_DF)
    df = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', df)
    df = df.sort_values(by='year')
    
    df['Population'] = df[f'{sex}_lt_6mo'] + df[f'{sex}_6mo_lt_1yr'] + df[f'{sex}_1yr_lt_3yrs'] + df[f'{sex}_3yrs_lt_10yrs'] + df[f'{sex}_gte_10yrs']
    df = df.replace('AF', 'Afar')
    df = df.replace('AM', 'Amhara')
    df = df.replace('OR', 'Orormia')
    df = df.replace('SN', 'SNNP')
    # Creating graph
    fig_title = f'{sex.capitalize()} {animal} Population as Calculated from Age Population Statistics by {demographic}'

    fig = px.line(
        df, 
        x='year',
        y='Population',
        color = 'flag',
        labels={'year':'Year', 'flag':'Region'},
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

def get_perc_sex_mortality_distribution_fig_by_sex(demographic, animal, year, sex):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_REG_POPULATION_DF)
    df = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', df)
    df = df.sort_values(by=['year', 'flag'])

    healthdf = filterdf(year_list,'year',CATTLE_REG_HEALTH_DF)
    healthdf = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', healthdf)
    healthdf = healthdf.sort_values(by=['year', 'flag'])
    df.index = healthdf.index

    df['total'] = df[f'{sex}_lt_6mo'] + df[f'{sex}_6mo_lt_1yr'] + df[f'{sex}_1yr_lt_3yrs'] + df[f'{sex}_3yrs_lt_10yrs'] + df[f'{sex}_gte_10yrs']
    df['% Deaths'] = healthdf[f'{sex}_deaths'] / df['total'] * 100
    df = df.replace('AF', 'Afar')
    df = df.replace('AM', 'Amhara')
    df = df.replace('OR', 'Orormia')
    df = df.replace('SN', 'SNNP')

    # Creating graph
    fig_title = f'Percentage {sex.capitalize()} Mortality by {sex.capitalize()} {animal} Population and {demographic}'   

    fig = px.line(
        df, 
        x='year',
        y='% Deaths',
        color = 'flag',
        labels={'year':'Year', 'flag':'Region'},
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

def get_disease_mortality_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_REG_HEALTH_DF)
    df = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', df)
    df = df.sort_values(by='year')
    
    df['% Deaths'] = df[f'{animal.lower()}_death_disease'] / df['total_deaths'] * 100
    df = df.replace('AF', 'Afar')
    df = df.replace('AM', 'Amhara')
    df = df.replace('OR', 'Orormia')
    df = df.replace('SN', 'SNNP')

    # Creating graph
    fig_title = f'{animal} Mortality by Disease and {demographic}'   

    fig = px.line(
        df, 
        x='year',
        y='% Deaths',
        color = 'flag',
        labels={'year':'Year', 'flag':'Region'},
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

def get_other_mortality_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_REG_HEALTH_DF)
    df = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', df)
    df = df.sort_values(by='year')
    
    df['% Deaths'] = df[f'{animal.lower()}_death_other'] / df['total_deaths'] * 100
    df = df.replace('AF', 'Afar')
    df = df.replace('AM', 'Amhara')
    df = df.replace('OR', 'Orormia')
    df = df.replace('SN', 'SNNP')
    
    # Creating graph
    fig_title = f'{animal} Mortality by Non-Disease and {demographic}'   

    fig = px.line(
        df, 
        x='year',
        y='% Deaths',
        color = 'flag',
        labels={'year':'Year', 'flag':'Region'},
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

# Poultry figures
def get_population_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',POULTRY_INV_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')
    
    df['total'] = df[f'total_{animal.lower()}']
    df['cocks'] = df['total_cocks']
    df['cockerels'] = df['total_cockerels']
    df['pullets'] = df['total_pullets']
    df['non-laying hens'] = df['total_nonlaying_hens']
    df['laying hens'] = df['total_laying_hens']
    df['chicks'] = df['total_chicks']
    df_melt = df.melt(id_vars='year', value_vars=['total', 'cocks', 'cockerels', 'pullets', 'non-laying hens', 'laying hens', 'chicks'], var_name='poultry type', value_name='population') 

    # Creating graph
    fig_title = f'{animal} Population by Type by {demographic}'

    fig = px.line(
        df_melt, 
        x='year',
        y='population',
        color = 'poultry type',
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

def get_mortality_fig(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',POULTRY_HEALTH_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')

    # Creating graph
    fig_title = f'Total {animal} Mortality by {demographic}'

    fig = px.line(
        df, 
        x='year',
        y='total_deaths',
        # color = 'poultry type',
        labels={'year':'Year', 'total_deaths':'no. Deaths'},
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

def get_eggs_fig(demographic, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',POULTRY_EGGS_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')

    df.loc[df['total_egg_prod_indigenous'] == -1, 'total_egg_prod_indigenous'] = None
    df.loc[df['total_egg_prod_hybrid'] == -1, 'total_egg_prod_hybrid'] = None
    df.loc[df['total_egg_prod_exotic'] == -1, 'total_egg_prod_exotic'] = None
    
    df['indigenous'] = df['total_egg_prod_indigenous']
    df['hybrid'] = df['total_egg_prod_hybrid']
    df['exotic'] = df['total_egg_prod_exotic']
    df_melt = df.melt(id_vars='year', value_vars=['indigenous', 'hybrid', 'exotic'], var_name='breed', value_name='Total Egg Production') 

    # Creating graph
    fig_title = f'Poultry Egg Population by Breed by {demographic}'

    fig = px.line(
        df_melt, 
        x='year',
        y='Total Egg Production',
        color = 'breed',
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

