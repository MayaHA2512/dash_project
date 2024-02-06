import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from model import model

model_cfg = model()
g = 1
card_content = [
    dbc.CardHeader("Add transaction"),
    dbc.CardBody(
        [
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
            html.Div([
                dcc.Input(id='input-box', type='text', style={'margin-left': '7px', 'margin-bottom': '10px'}),
                dcc.Dropdown(['Cash', 'Credit', 'Debit'], 'Spending method', id='demo-dropdown',
                             style={'border-radius': '0px', 'margin-left': '3px', 'width': '200px', 'margin-bottom': '10px'}),
                html.Button('Save', id='save-button', style={'margin-left': '7px', 'margin-bottom': '10px'}),
                html.Button('Spend', id='spend-button', style={'margin-left': '7px', 'margin-bottom': '10px'}),
            ], ),
        ]
    ),
]
card = dbc.Card(card_content, color="dark", inverse=True)


class FinanceView:

    @staticmethod
    def login_layout():
        return html.Div([
            html.H4('Please Log In', style={'padding': '15px'}),
            dcc.Input(id='username-input', placeholder='Enter your username', type='text',
                      style={'margin-left': '15px', 'margin-bottom': '10px'}),
            html.Br(),
            dcc.Input(id='password-input', placeholder='Enter your password', type='password',
                      style={'margin-left': '15px', 'margin-bottom': '10px'}),
            html.Br(),
            html.Button('Login', id='login-button', style={'margin-left': '15px', 'margin-bottom': '10px'}),
            html.Div(id='login-output', style={'margin-left': '15px'})
        ])

    def success_layout(self):
        return html.Div([dbc.Row([
            html.Div([
                html.H4('Welcome back!', style={'margin-left': '15px'}),
                html.H4('Balance: £', style={'margin-left': '15px'}),
                html.H4(model_cfg.get_balance(), id='balance', style={'margin-left': '0px'}),
                html.Button('Logout', id='logout-button', style={'margin-left': '15px', 'margin-bottom': '10px'}),
            ], style={'display': 'flex'}),
            dbc.Row(
                dbc.Col(card, width=4, style={'border-radius': '0px', 'margin-left': '15px'}),
            ),
        ]),
        ])

    def navbar(self):
        navbar = dbc.NavbarSimple(
            brand='Student Finance Tracker',
            brand_href='/',
            color='secondary',
            dark=True,
            fluid=True,
            style={'padding-top': '8px', 'padding-bottom': '8px', 'margin-bottom': '12px'}
        )
        return navbar
