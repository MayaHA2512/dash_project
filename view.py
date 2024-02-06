import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from model import model
import dash_ag_grid as dag

model_cfg = model()

g = 1
card_content = [
    dbc.CardHeader("Add transaction"),
    dbc.CardBody(
        [
            html.Div([
                dbc.Input(id='description-box', type='text', style={'margin-bottom': '10px'}),
                dbc.Input(id='input-box', type='text', style={'margin-bottom': '10px'}),
                dbc.Select(
                    id="select",
                    options=[
                        {"label": "Cash", "value": "cash"},
                        {"label": "Credit Card", "value": "credit"},
                        {"label": "Debit Card", "value": "debit"},
                    ], style={'margin-bottom': '7px'}
                ),
dbc.Select(
                    id="category",
                    options=[
                        {"label": "Bills", "value": "bills"},
                        {"label": "Tuition fees", "value": "tuition fees"},
                        {"label": "Books", "value": "books"},
                    ], style={'margin-bottom': '7px'}
                ),
                dbc.Button('Save', id='save-button', style={'margin-bottom': '7px', 'margin-right': '4px'},
                           color='secondary'),
                dbc.Button('Spend', id='spend-button', style={'margin-bottom': '7px'}, color='secondary'),
            ], ),
        ], className="d-flex justify-content-center align-items-center"
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
                [dbc.Col(card, width=4, style={'margin-left': '15px'}),
                 dbc.Col(
                     dag.AgGrid(
                         id='transaction-table',
                         rowData=(model_cfg.get_data_df()).to_dict('records'),
                         className='ag-theme-alpine-dark',
                         columnDefs=[{"field": i} for i in (model_cfg.get_data_df()).columns],
                     )
                 ),
                 ]),
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
