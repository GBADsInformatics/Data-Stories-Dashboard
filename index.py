import os
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json
from dash.exceptions import PreventUpdate

from app import app
from layouts import layout, data_tab, graph_tab, metadata_tab, map_tab

###--------------Read in data-----------------------------------

eurostat = pd.read_csv('data/eurostat.csv')
faostat = pd.read_csv('data/faostat.csv')
faotier1 = pd.read_csv('data/faotier1.csv')
woah = pd.read_csv('data/oie.csv')
unfccc = pd.read_csv('data/unfccc.csv')

def get_df(choice): 

    if choice == 'eurostat': 
        return(eurostat)
    elif choice == 'faostat':
        return(faostat)
    elif choice == 'faotier1': 
        return(faotier1)
    elif choice == 'woah':
        return(woah)
    elif choice == 'unfccc':
        return(unfccc)

def prep_df(df, country, species, start, end): 

    # Determine types 
    if type(country) == str: 
        df = df[df['country'] == country]
    else: 
        df = df[df['country'].isin(country)]
    
    if type(species) == str: 
        df = df[df['species'] == species]
    else: 
        df = df[df['species'].isin(species)]

    df = df[df['year'].between(start,end)]

    return(df)
    
app.layout = layout.app_layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'active_tab')])
def render_content(tab):
    if tab == 'tab-0':
        return graph_tab.content
    elif tab == 'tab-1':
        return map_tab.content
    elif tab == 'tab-2':
       return data_tab.content
    elif tab == 'tab-3':
        return metadata_tab.metadata_content

# Organize options of selecting multiple
@app.callback(
    Output('country','multi'),
    Output('species','multi'),
    Input('tabs','active_tab'),
    Input('choice','value')
)
def update_multiples(at, choice):

    if choice == 'Species': 
        return(False, True)
    else: 
        return(True, False)
      
# Update all dropdowns
@app.callback(
    Output('country','options'),
    Output('species','options'),
    Output('start year','options'),
    Output('end year','options'),
    Input('dataset','value'),
)
def update_all_dd(data):

    df = get_df(data)
    
    country_options = df['country'].unique().tolist()
    
    species_options = df['species'].unique().tolist()

    df = df.sort_values(by=['year'])
    
    years = df['year'].unique()

    return(country_options, species_options, years, years) 

# Initialize year slider 
@app.callback(
        Output('year', 'value'),
        Output('year', 'min'),
        Output('year', 'max'),
        Input('tabs','active_tab'),
    )
def options_on_tab_change(at):
    return [graph_tab.YEARS[0], graph_tab.YEARS[-1]], graph_tab.YEARS[0], graph_tab.YEARS[-1]
 
# Update species 
# @app.callback(
#     Output('species','options'),
#     [Input('country', 'value'),
#      Input('dataset','value')]
# )
# def update_species_dd(country, data):

    # Get dataset 
    # df = get_df(data)

    # # Set default 
    # if country == str:
    #     print(f"User has selected no country options: {country}")

    # elif type(country) == list and len(country) > 1:
    #     df = df[df['country'].isin(country)]

    # elif type(country) == list: 
    #     df = df.loc[df['country'] == country]
    
    # species_options = df['species'].unique().tolist()

    # return(species_options) 

# Initialize dataset dropdown
@app.callback(
    Output('dataset','options'),
    Input('tabs','active_tab'),
)
def dataset_drop(at):

    dataset_options = ['eurostat','faostat','faotier1','woah','unfccc']

    return(dataset_options)

# Update year options 
# @app.callback(
#     Output('start year','options'),
#     Output('end year','options'),
#     Input('dataset','value'),
# )
# def update_year_dropdown(data): 

#     df = get_df(data)

    # Determine types to filter df 
    # if type(country) == str: 
    #     df = df[df['country'] == country]
    #     df = df[df['species'].isin(species)]
    # else: 
    #     df = df[df['species'] == species]
    #     df = df[df['country'].isin(country)]

    # df = df.sort_values(by=['year'])
    # years = df['year'].unique()

    # return years, years

# Updating tables dropdown on Demographic change
@app.callback(
        Output('animal', 'options'),
        Output('animal', 'value'),
        Input('demographic', 'value'),
)
def update_dropdowns(demographic):
    match demographic:
        case 'National':
            return ['Cattle', 'Poultry', 'Sheep', 'Goats', 'Camels', 'Horses', 'Donkeys', 'Mules'], 'Cattle'
        case 'Regional':
            return ['Cattle'], 'Cattle', 
        
# Updating tables dropdown on animal change
@app.callback(
        Output('table', 'options'),
        Output('table', 'value'),
        Input('animal', 'value'),
        Input('demographic', 'value'),
)
def update_table_dropdown(animal, demographic):
    match demographic:
        case 'National':
            match animal:
                case 'Cattle':
                    return ['Sex Distribution', 'Breed Sex Distribution', 'Mortality Distribution', 'Mortality Distribution by Sex', 'Mortality by Cause', 'Vaccination'], 'Sex Distribution'
                case 'Poultry':
                    return ['Population', 'Total Mortality', 'Mortality by Cause', 'Egg Production'], 'Population'
                case 'Sheep' | 'Goats':
                    return ['Sex Distribution', 'Breed Sex Distribution', 'Mortality Distribution', 'Mortality Distribution by Sex', 'Mortality by Cause', 'Vaccination'], 'Sex Distribution'
                case 'Camels':
                    return ['Sex Distribution', 'Mortality Distribution', 'Mortality Distribution by Sex', 'Mortality by Cause', 'Vaccination'], 'Sex Distribution'
                case 'Horses' | 'Donkeys' | 'Mules':
                    return ['Sex Distribution', 'Mortality Distribution', 'Mortality Distribution by Sex', 'Mortality by Cause'], 'Sex Distribution'
        case 'Regional':
            return ['Male Population', 'Female Population', 'Male Mortality', 'Female Mortality', 'Mortality by Disease', 'Mortality by Other', 'Afar Vaccination', 'Amhara Vaccination', 'Oromia Vaccination', 'SNNP Vaccination'], 'Male Population'

# Display metadata 
@app.callback(
    Output('metadata-table','data'),
    Input('dataset','value'),
    Input('tabs','active_tab')
)
def get_metadata(data, at):
    
    df = metadata_tab.get_metadata_df(data)

    return df.to_dict('records')

# Display graph
# Update graph
# @app.callback(
#     Output('graph1','figure'),
#     Input('country','value'),
#     Input('species','value'),
#     Input('start year', 'value'),
#     Input('end year', 'value'),
#     Input('dataset','value'),
#     Input('plot','value'))
# def update_graph(country, species, start, end, data, plot):

#     if type(country) == list and type(species) == list:
#         raise PreventUpdate

#     df = get_df(data)
#     df = prep_df(df, country, species, start, end)

#     if plot == 'stacked bar':
#         fig = graph_tab.create_bar_plot(df, country, species)
#     elif plot == 'scatter line':
#         fig = graph_tab.create_scatter_plot(df, country, species)

#     return(fig)

@app.callback(
    Output('graph1', 'figure'),
    Input('demographic', 'value'),
    Input('animal', 'value'),
    Input('table', 'value'),
    Input('year', 'value'),
)
def create_graph(demographic, animal, table, year):
    match demographic:
        case 'National':
            match animal:
                case 'Cattle' | 'Sheep' | 'Goats':
                    match table:
                        case 'Sex Distribution':
                            fig = graph_tab.get_sex_distribution_fig(demographic, animal, year)
                        case 'Breed Sex Distribution':
                            fig = graph_tab.get_breed_sex_distribution_fig(demographic, animal, year)
                        case 'Mortality Distribution':
                            fig = graph_tab.get_perc_mortality_distribution_fig(demographic, animal, year)
                        case 'Mortality Distribution by Sex':
                            fig = graph_tab.get_perc_sex_mortality_distribution_fig(demographic, animal, year)
                        case 'Mortality by Cause':
                            fig = graph_tab.get_cause_mortality_fig(demographic, animal, year)
                        case 'Vaccination':
                            fig = graph_tab.get_vaccinated_fig(demographic, animal, year, "")
                case 'Camels': 
                    match table:
                        case 'Sex Distribution':
                            fig = graph_tab.get_sex_distribution_fig(demographic, animal, year)
                        case 'Mortality Distribution':
                            fig = graph_tab.get_perc_mortality_distribution_fig(demographic, animal, year)
                        case 'Mortality Distribution by Sex':
                            fig = graph_tab.get_perc_sex_mortality_distribution_fig(demographic, animal, year)
                        case 'Mortality by Cause':
                            fig = graph_tab.get_cause_mortality_fig(demographic, animal, year)
                        case 'Vaccination':
                            fig = graph_tab.get_vaccinated_fig(demographic, animal, year, "")
                case 'Horses' | 'Donkeys' | 'Mules': 
                    match table:
                        case 'Sex Distribution':
                            fig = graph_tab.get_sex_distribution_fig(demographic, animal, year)
                        case 'Mortality Distribution':
                            fig = graph_tab.get_perc_mortality_distribution_fig(demographic, animal, year)
                        case 'Mortality Distribution by Sex':
                            fig = graph_tab.get_perc_sex_mortality_distribution_fig(demographic, animal, year)
                        case 'Mortality by Cause':
                            fig = graph_tab.get_cause_mortality_fig(demographic, animal, year)
                case 'Poultry':
                    match table:
                        case 'Population':
                            fig = graph_tab.get_population_fig(demographic, animal, year)
                        case 'Total Mortality':
                            fig = graph_tab.get_mortality_fig(demographic, animal, year)
                        case 'Mortality by Cause':
                            fig = graph_tab.get_cause_mortality_fig(demographic, animal, year)
                        case 'Egg Production':
                            fig = graph_tab.get_eggs_fig(demographic, year)
        case 'Regional':
            match table:
                case 'Male Population':
                    fig = graph_tab.get_population_fig_by_sex(demographic, animal, year, 'male')
                case 'Female Population':
                    fig = graph_tab.get_population_fig_by_sex(demographic, animal, year, 'female')
                case 'Male Mortality':
                    fig = graph_tab.get_perc_sex_mortality_distribution_fig_by_sex(demographic, animal, year, 'male')
                case 'Female Mortality':
                    fig = graph_tab.get_perc_sex_mortality_distribution_fig_by_sex(demographic, animal, year, 'female')
                case 'Mortality by Disease':
                    fig = graph_tab.get_disease_mortality_fig(demographic, animal, year)
                case 'Mortality by Other':
                    fig = graph_tab.get_other_mortality_fig(demographic, animal, year)
                case 'Afar Vaccination':
                    fig = graph_tab.get_vaccinated_fig(demographic, animal, year, "AF")
                case 'Amhara Vaccination':
                    fig = graph_tab.get_vaccinated_fig(demographic, animal, year, "AM")
                case 'Oromia Vaccination':
                    fig = graph_tab.get_vaccinated_fig(demographic, animal, year, "OR")
                case 'SNNP Vaccination':
                    fig = graph_tab.get_vaccinated_fig(demographic, animal, year, "SN")
    return fig

# Update data table 
@app.callback(
    Output('datatable','data'),
    Output('datatable','columns'),
    Input('dataset','value'),
    Input('country','value'), 
    Input('species','value'),
    Input('start year', 'value'),
    Input('end year', 'value'),
    )
def update_table(data, country, species, start, end):

    df = get_df(data)
    df = prep_df(df, country, species, start, end)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

# Update map
# Update year option on map tab
@app.callback(
    Output('species-map','options'),
    Output('country-map','options'),
    Output('year-map','options'),
    Input('dataset','value'),
)
def update_species_map(data): 

    df = get_df(data)
    
    country = df['country'].unique()
    species = df['species'].unique()
    df = df.sort_values(by=['year'])
    year = df['year'].unique()

    return(species, country, year)

@app.callback(
    Output('map','figure'),
    Input('dataset','value'),
    Input('species-map','value'),
    Input('country-map','value'),
    Input('year-map', 'value'),
    )
def update_map(data, species, countries, year):

    df = get_df(data)
    merged_df = df.loc[df['year'] == year]
    merged_df = merged_df.loc[merged_df['species'] == species]

    if type(countries) == str:
        merged_df = merged_df.loc[merged_df['country'] == countries]
    else: 
        merged_df = merged_df.loc[merged_df['country'].isin(countries)]

    fig = map_tab.create_map(merged_df, data, species, year)

    return(fig)

if __name__ == '__main__':
    app.run_server(debug=True)
    app.config['suppress_callback_exceptions'] = True

# return the wsgi app
def returnApp():
    """
    This function is used to create the app and return it to waitress in the docker container
    """
    # If DASH_BASE_URL is set, use DispatcherMiddleware to serve the app from that path
    if 'DASH_BASE_URL' in os.environ:
        from flask import Flask
        from werkzeug.middleware.dispatcher import DispatcherMiddleware
        app.wsgi_app = DispatcherMiddleware(Flask('dummy_app'), {
            os.environ['DASH_BASE_URL']: app.server
        })
        # Added redirect to new path
        @app.wsgi_app.app.route('/')
        def redirect_to_dashboard():
            from flask import redirect
            return redirect(os.environ['DASH_BASE_URL'])
        return app.wsgi_app

    # If no DASH_BASE_URL is set, just return the app server
    return app.server