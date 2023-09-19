import os
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import json
from dash.exceptions import PreventUpdate
from utils import newS3TicketLib as s3f
from datetime import datetime
from utils import secure_rds as secure
from utils import rds_functions as rds

from app import app
from layouts import layout, data_tab, graph_tab, metadata_tab, map_tab, styling

# Access AWS Credentials and establish session
access, secret = s3f.get_keys('utils/')
s3_resource = s3f.credentials_resource ( access, secret )
s3_client = s3f.credentials_client ( access, secret )

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


divBorder = {
    # "border": "2px solid black",
    "border-radius": "1rem",
    "background-color": "#ffffff",
    "padding": "1rem 1rem",
}

commentHeading = {
    "color": "#FFA500",
    "display": "inline-block",
    # "width":"10rem",
    "padding": "0rem 2rem 0rem 0rem"
}

commentSubheading = {
    "color": "#707070",
    "display": "inline-block",

}

commentDate = {
    "color": "#A0A0A0",
    "display": "inline-block",
    "float": "right",
}

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

# comment table tabs
@app.callback(
        Output('comment-tabs-content', 'children'),
        Input('demographic', 'value'),
        Input('animal', 'value'),
        Input('table', 'value'),
        Input('year', 'value'),
        # Output('comments', 'children'),
        [Input('comment-tabs', 'active_tab')]
)
def render_content(demographic, animal, table, year, tab):
    if tab == 'tab-0':
        # empty approved folder
        # files = os.listdir('approved/')
        # for f in files:
        #     os.remove('approved/'+f)

        #get new comments
        conn = secure.connect_public()
        cur = conn.cursor()
        fieldstring = "created,tablename,subject,message,name,email,ispublic,reviewer"
        #change to not include time
        querystring = f"dashboard='datastories' AND tablename LIKE '{demographic} {animal} {table}%'"
        querystr = rds.setQuery ("gbads_comments", fieldstring, querystring, "")
        comments = rds.execute ( cur, querystr )
        conn.close()
        print(comments)
        child = []

        for row in comments:
            print(row)
            child.append(html.Div(children=[
                html.H5(row[4] if row[6] == True else 'Anonymous', style=commentHeading),
                html.H6(row[1], style=commentSubheading),
                html.H6(row[0][:-9], style=commentDate),
                html.H6(row[2]),
                html.H6(row[3]),
            ],
            style = divBorder
            ))
            child.append(html.Br())

        # response = s3_client.list_objects_v2( Bucket='gbads-comments', Prefix='approved/')
        # for content in response.get('Contents', []):
        #     # print(content['Key'])
        #     if content['Key'] != 'approved/':
        #         s3f.s3Download(s3_resource, 'gbads-comments', content['Key'], content['Key'])
        #         with open(content['Key']) as file:
        #             data = json.load(file)
        #             #append comment to list
        #             # if data['isPublic'] == True:
        #             #     child.append(html.H5(data['name']))
        #             # else:
        #             #     child.append(html.H5('Anonymous'))
        #             # child.append(html.H6(data['message']))
        #             # child.append(html.Br())
        #             child.append(html.Div(children=[
        #                 html.H5(data['name'] if data['isPublic'] == True else 'Anonymous', style=commentHeading),
        #                 html.H6(data['table'], style=commentSubheading),
        #                 html.H6(data['created'][:-16], style=commentDate),
        #                 html.H6(data['message']),
        #             ],
        #             style = divBorder
        #             ))
        #             child.append(html.Br())

        # print(list)
        # arr = []
        # arr.append(html.H6('test'))
        # arr.append(html.H6('test2'))
        # print(child)
        return dbc.Row(children=
            [
                html.Div(id='comments', children=child)
            ],
            style=COMMENT_STYLE,
        )
    elif tab == 'tab-1':
        return styling.comment_add

# Comment table changing
@app.callback(
    Output('comments-table','value'),
    Input('demographic', 'value'),
    Input('animal', 'value'),
    Input('table', 'value'),
    Input('year', 'value'),
)
def update_comment_table(demographic, animal, table, year):
    return f'{demographic} {animal} {table} {year[0]}-{year[-1]}'

# Comment Submition
@app.callback(
        Output('com', 'children'),
        # Output('comments-button', 'n_clicks'),
        Output('comments-subject', 'value'),
        Output('comments-message', 'value'),
        Output('comments-name', 'value'),
        Output('comments-email', 'value'),
        Output('comments-isPublic', 'value'),
        Input('comments-button', 'n_clicks'),
        State('comments-table', 'value'),
        State('comments-subject', 'value'),
        State('comments-message', 'value'),
        State('comments-name', 'value'),
        State('comments-email', 'value'),
        State('comments-isPublic', 'value'),
)
def submit_comment(n_clicks, table, subject, message, name, email, isPublic):
    if subject == '':
        return f'Subject is required', subject, message, name, email, isPublic;
    if message == '':
        return f'Message is required', subject, message, name, email, isPublic;
    if n_clicks > 0:
        # create comment file
        created = datetime.now()
        comment = {
            "created": f'{created}',
            "dashboard": 'datastories',
            "table": table,
            "subject": subject,
            "message": message,
            "name": name,
            "email": email,
            "isPublic": True if isPublic == "Yes" else False,
            "reviewer": ''
        }
        filename = f'{created}.json'
        with open(filename, "w") as outfile:
            json.dump(comment, outfile)
        # upload comment file
        ret = s3f.s3Upload ( s3_resource, 'gbads-comments', filename, f"underreview/{filename}" )
        #delete comment file
        os.remove(filename)
        if ( ret == -1 ):
            return f'Error: Unable to submit comment', '', '', '', '', 'No';
        return f'Submitted Successfully', '', '', '', '', 'No';
    return f'', '', '', '', '', 'No';
    
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