import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table
from layouts import styling 
import pandas as pd

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
def get_sex_distribution_df(demographic, animal, year):
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

    return table_df

def get_breed_sex_distribution_df(demographic, animal, year):
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

    return df_melt

def get_perc_mortality_distribution_df(demographic, animal, year):
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

    return df_melt


def get_perc_sex_mortality_distribution_df(demographic, animal, year):
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

    return df_melt


def get_cause_mortality_df(demographic, animal, year):
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

    return df_melt

def get_vaccinated_df(demographic, animal, year, regionCode):
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

    # healthdf['total'] = healthdf[f'{animal.lower()}_vac_total'] / df[f'{animal.lower()}_total'] * 100
    # healthdf['anthrax'] = healthdf[f'{animal.lower()}_vac_anthrax'] / df[f'{animal.lower()}_total'] * 100
    # healthdf['blackleg'] = healthdf[f'{animal.lower()}_vac_blackleg'] / df[f'{animal.lower()}_total'] * 100
    # healthdf['pleuro pneumonia'] = healthdf[f'{animal.lower()}_vac_pleuro_pneumonia'] / df[f'{animal.lower()}_total'] * 100
    # healthdf['hemorrhagic septicemia'] = healthdf[f'{animal.lower()}_vac_hemorrhagic_septicemia'] / df[f'{animal.lower()}_total'] * 100
    # healthdf['rinderpest'] = healthdf[f'{animal.lower()}_vac_rinderpest'] / df[f'{animal.lower()}_total'] * 100
    # healthdf['other'] = healthdf[f'{animal.lower()}_vac_other'] / df[f'{animal.lower()}_total'] * 100
    # df_melt = healthdf.melt(id_vars='year', value_vars=['total', 'anthrax', 'blackleg', 'pleuro pneumonia', 'hemorrhagic septicemia', 'rinderpest', 'other'], var_name='vaccination type', value_name='% vaccinated') 

    return healthdf.drop(columns=['id', 'cattle_afflicted', 'cattle_treated', 'cattle_death_disease', 'cattle_death_other', 'total_deaths', 'male_deaths', 'female_deaths'])

# regional figures
def get_population_df_by_sex(demographic, animal, year, sex):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_REG_POPULATION_DF)
    df = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', df)
    df = df.sort_values(by='year')
    
    df['Population'] = df[f'{sex}_lt_6mo'] + df[f'{sex}_6mo_lt_1yr'] + df[f'{sex}_1yr_lt_3yrs'] + df[f'{sex}_3yrs_lt_10yrs'] + df[f'{sex}_gte_10yrs']
    df = df.replace('AF', 'Afar')
    df = df.replace('AM', 'Amhara')
    df = df.replace('OR', 'Orormia')
    df = df.replace('SN', 'SNNP')

    return df

def get_perc_sex_mortality_distribution_df_by_sex(demographic, animal, year, sex):
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

    return df

def get_disease_mortality_df(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_REG_HEALTH_DF)
    df = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', df)
    df = df.sort_values(by='year')
    
    df['% Deaths'] = df[f'{animal.lower()}_death_disease'] / df['total_deaths'] * 100
    df = df.replace('AF', 'Afar')
    df = df.replace('AM', 'Amhara')
    df = df.replace('OR', 'Orormia')
    df = df.replace('SN', 'SNNP')

    return df

def get_other_mortality_df(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',CATTLE_REG_HEALTH_DF)
    df = filterdf(['AF', 'AM', 'OR', 'SN'], 'flag', df)
    df = df.sort_values(by='year')
    
    df['% Deaths'] = df[f'{animal.lower()}_death_other'] / df['total_deaths'] * 100
    df = df.replace('AF', 'Afar')
    df = df.replace('AM', 'Amhara')
    df = df.replace('OR', 'Orormia')
    df = df.replace('SN', 'SNNP')

    return df

# Poultry figures
def get_population_df(demographic, animal, year):
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

    return df_melt

def get_mortality_df(demographic, animal, year):
    year_list = list(range(year[0], year[-1]+1))

    df = filterdf(year_list,'year',POULTRY_HEALTH_DF)
    df = df[df.id == 0]
    df = df.sort_values(by='year')

    return df


table = html.Div([
    html.P("Use the selections in the OPTIONS side bar on the left to filter the data and the export button to download the data in csv format."),
    dash_table.DataTable(
            id='datatable',
            export_format='csv',
            style_cell={'textAlign': 'left', 'font-family':'sans-serif'},
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_data={
                'color': 'black',
            },
            style_header={
                'color': 'black',
                'fontWeight': 'bold'
            }
)])

content = dbc.Row(children=
            [
            styling.sidebar,
            dcc.Loading(id = 'loading-icon',
                        children = [
                            dbc.Col(table)
                        ]
                        )
            ],style = styling.CONTENT_STYLE_TABLES
        )