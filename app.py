import os
import dash 
import dash_bootstrap_components as dbc 

app = None
if 'BASE_URL' in os.environ:
    app = dash.Dash(
        __name__,
        title='GBADs Data Stories Dashboard V2',
        external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.LUX],
        requests_pathname_prefix=os.environ['BASE_URL']+'/'
    )
else:
    app = dash.Dash(
        __name__,
        title='GBADs Data Stories Dashboard V2',
        external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.LUX]
    )