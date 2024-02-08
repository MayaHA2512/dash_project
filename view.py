import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from model import model
import dash_ag_grid as dag
import plotly.express as px

model_cfg = model()


# df = model_cfg.get_data_df()
# pie_chart = px.pie(df, values='amount', names='category')
# pie_chart = pie_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)', )
#

class FinanceView:
    def __init__(self):
        pass

    @staticmethod
    def pie_chart():
        df = model_cfg.get_data_df()
        pie_chart = px.pie(df, values='amount', names='category', width=350, height=350)
        pie_chart = pie_chart.update_traces(textfont=dict(color='white'))
        pie_chart = pie_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0),
                                            legend=dict(font=dict(color='white')))
        return pie_chart

    @staticmethod
    def card():
        card_content = [
            dbc.CardHeader("Add transaction"),
            dbc.CardBody(
                [
                    html.Div([
                        dbc.Input(id='description-box', type='text', style={'margin-bottom': '10px'}, placeholder='Description'),
                        dbc.Input(id='input-box', type='text', style={'margin-bottom': '10px'}, placeholder='Amount'),
                        dbc.Select(
                            id="select",
                            options=[
                                {"label": "Cash", "value": "cash"},
                                {"label": "Credit Card", "value": "credit"},
                                {"label": "Debit Card", "value": "debit"},
                            ], style={'margin-bottom': '7px'},
                            placeholder='Payment method',
                        ),
                        dbc.Select(
                            id="category",
                            options=[
                                {"label": "Bills", "value": "bills"},
                                {"label": "Tuition fees", "value": "tuition fees"},
                                {"label": "Books", "value": "books"},
                            ], style={'margin-bottom': '7px'},
                            placeholder='Category',
                        ),
                        dbc.Button('Save', id='save-button', style={'margin-bottom': '7px', 'margin-right': '4px'},
                                   color='secondary'),
                        dbc.Button('Spend', id='spend-button', style={'margin-bottom': '7px'}, color='secondary'),
                    ], ),
                ], className="d-flex justify-content-center align-items-center"
            ),
        ]
        card = dbc.Card(card_content, color="dark", inverse=True, style={'margin-bottom': '15px'})
        return card

    @staticmethod
    def pie_chart_card():
        card_content = [
            dbc.CardHeader("Spending:"),
            dbc.CardBody(
                [
                    dcc.Graph(id='pie_chart', figure=FinanceView.pie_chart(), )
                ], className="d-flex justify-content-center align-items-center"
            ),
        ]
        card = dbc.Card(card_content, color="dark", inverse=True, style={'height': '400px'})
        return card

    @staticmethod
    def budget_card_maker(amount, category):
        data = model_cfg.get_data_for_budget(category=category)
        total = sum(data)
        percentage_used = round(((total/int(amount)) * 1e2), 2)
        card_content = [
            dbc.CardHeader("%s" % category),
            dbc.CardBody(
                [
                    dbc.Progress(label='{}% used'.format(percentage_used), value=percentage_used, color="primary", className="my-2", style={"height": "30px", "width": "100%"}),
                ], className="d-flex justify-content-center align-items-center",
                style={"height": "100px"}
            ),
        ]
        card = dbc.Card(card_content, color="dark", inverse=True, style={'height': '400px'})
        return card


    @staticmethod
    def login_layout():
        return html.Div([
            html.H4('Please Log In', style={'padding': '15px'}),
            dbc.Input(id='username-input', placeholder='Enter your username', type='text',
                      style={'margin-left': '15px', 'margin-bottom': '10px'}),
            html.Br(),
            dbc.Input(id='password-input', placeholder='Enter your password', type='password',
                      style={'margin-left': '15px', 'margin-bottom': '10px'}),
            html.Br(),
            dbc.Button('Login', id='login-button', style={'margin-left': '15px', 'margin-bottom': '10px'},
                       color='secondary'),
            html.Div(id='login-output', style={'margin-left': '15px'})
        ])

    def success_layout(self):
        card = FinanceView.card()
        return html.Div([dbc.Row([
            html.Div([
                html.H4('Welcome back!', style={'margin-left': '15px'}),
                html.H4('Balance: £', style={'margin-left': '15px'}),
                html.H4(model_cfg.get_balance(), id='balance', style={'margin-left': '0px'}),
                dbc.Button('Logout', id='logout-button', style={'margin-left': '15px', 'margin-bottom': '10px'},
                           color='secondary'),
                dbc.Button('Refresh', id='refresh-button', style={'margin-left': '15px', 'margin-bottom': '10px'},
                           color='secondary'),
            ], style={'display': 'flex'}),
            dbc.Row(
                [dbc.Col([card, FinanceView.pie_chart_card()], width=4,
                         style={'margin-left': '15px'}),
                 dbc.Col([
                     dag.AgGrid(
                         id='transaction-table',
                         rowData=(model_cfg.get_data_df()).to_dict('records'),
                         className='ag-theme-alpine-dark',
                         columnDefs=[{"field": i} for i in (model_cfg.get_data_df()).columns],
                         style={'height': '720px'}
                     ),

                 ]
                 ),
                 ]),
        ])

        ]),

    def budget_layout(self):
        card_content = [
            dbc.CardHeader("Add Budget"),
            dbc.CardBody(
                [
                    dbc.Input(id='budget-input', placeholder='Budget', type='text',
                              ),
                    dbc.Select(
                        id="budget-category-dropdown",
                        style={'margin-bottom': '7px'},
                        options=[
                            {"label": "Bills", "value": "bills"},
                            {"label": "Tuition fees", "value": "tuition fees"},
                            {"label": "Books", "value": "books"},
                        ],
                    ),
                    dbc.Button('Add', id='add-button', style={'margin-left': '15px', 'margin-bottom': '10px'},
                               color='secondary'),
                ], className="d-flex justify-content-center align-items-center"
            ),
        ]
        card = dbc.Card(card_content, color="dark", inverse=True, style={'height': '400px'})
        return dbc.Container([  # Use dbc.Container to wrap the row for proper alignment and padding
            dbc.Row([  # Wrap the columns in a dbc.Row to layout them horizontally
                dbc.Col([
                    html.H4('Budgets page', style={'padding': '15px'}),
                    card
                ], width=6),
                dbc.Col([
                    html.H4('Budgets'),
                    dbc.Container(id='budgets', children=[])
                ], width=6)
            ])
        ], fluid=True)

    def navbar(self):
        navbar = dbc.NavbarSimple(
            children=[
                dbc.DropdownMenu(
                    id='menu-dropdown',
                    children=[
                        dbc.DropdownMenuItem("More pages", header=True),
                        dbc.DropdownMenuItem("Dashboard", href="/"),
                        dbc.DropdownMenuItem("Budgets", href="/budgets"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Pages",
                ),
            ],
            brand='Student Finance Tracker',
            brand_href='/',
            color='secondary',
            dark=True,
            fluid=True,
            style={'padding-top': '8px', 'padding-bottom': '8px', 'margin-bottom': '12px'}
        )
        return navbar
