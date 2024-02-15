import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc

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


ACTIVE_TAB_STYLE = {
    "color": "#FFA500"
}

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

comment_tabs = html.Div([
    dbc.Tabs(
        [
            dbc.Tab(label="Comment Section", active_label_style=ACTIVE_TAB_STYLE),
            dbc.Tab(label="Add a Comment",active_label_style=ACTIVE_TAB_STYLE),
        ],
    id='comment-tabs', style={"padding": "1rem 1rem", "position":"fixed"})
]
)

comment_area = html.Div(
    children = [
        dbc.Row(children=[
            dbc.Col(comment_tabs),
        ]),
        dbc.Row(children = [html.Div(id='comment-tabs-content')]),
        ],
        # style=TAB_STYLE
)

comment_add = dbc.Row(children=
    [
        html.H4("Add a Comment"),
        html.Hr(),
        html.H6(" "),
        html.Div([
            html.H6("Table:", style={'display': 'inline-block', 'width':'7rem'}),
            dcc.Input(id='comments-table',
                type='text',
                readOnly=True,
                disabled = True,
                style={'display': 'inline-block', 'width':'30rem'}
            )
        ]),
        html.H6(" "),
        html.Div([
            html.H6("Subject:", style={'display': 'inline-block', 'width':'7rem'}),
            dcc.Input(id='comments-subject',
                type='text',
                required=True,
                style={'display': 'inline-block', 'width':'30rem'}
            )
        ]),
        html.H6(" "),
        html.H6("Message:"),
        html.H6(" "),
        dcc.Textarea(id='comments-message',
            placeholder='Message',
            required=True,
            style={'width':'100%'},
        ),
        html.H6(" "),
        html.Div([
            html.H6("Name:", style={'display': 'inline-block', 'width':'5rem'}),
            dcc.Input(id='comments-name',
                type='text',
                style={'display': 'inline-block', 'width':'20rem'}
            ),
            # html.H6(" ", style={'display': 'inline-block', 'width':'4rem'}),
            html.H6(" Email:", style={'display': 'inline-block', 'width':'5rem'}),
            dcc.Input(id='comments-email',
                type='text',
                style={'display': 'inline-block', 'width':'20rem'}
            )
        ]),
        html.H6(" "),
        html.Div([
            html.H6("Permission to Publish on Dashboard:", style={'display': 'inline-block', 'width':'23rem'}),
            dcc.RadioItems(id='comments-isPublic',
                options=['Yes', 'No'],
                value='No',
                inline=True,
                style={'display': 'inline-block'}
            ),
        ]),
        html.H6(""),
        html.Button('SUBMIT', id='comments-button', n_clicks=0, style={'height':'2rem','width':'5rem'}),
        html.H6(""),
        html.Div(id='com', children='Enter a value and press submit'),

    ],
    style=COMMENT_STYLE,
)