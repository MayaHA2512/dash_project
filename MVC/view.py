import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from MVC.model import model
import dash_ag_grid as dag
import plotly.express as px
from components.card import Card
from setup.config import Config

model_cfg = model()
config = Config()


class FinanceView:
    def __init__(self):
        pass

    @staticmethod
    def pie_chart():
        df = model_cfg.get_data_df()
        pie_chart = px.pie(df, values='amount', names='category', width=350, height=350)
        pie_chart = pie_chart.update_traces(
            textfont=dict(color='white'))  # making modifications to the pie chart styling
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
                        dbc.Input(id='description-box', type='text', style={'margin-bottom': '10px'},
                                  placeholder='Description'),
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
                            options=[{'label': val, 'value': val} for val in config.get_categories()],
                            style={'margin-bottom': '7px'},
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
        card = Card()  # initiating card class with default styling already embedded, just need to provide card body
        # content
        card.card_body = card_content
        return card.create_card()

    @staticmethod
    def login_layout():
        return html.Div([
            html.H4('Please Log In', style={'padding': '15px'}),
            dbc.Input(id='username-input', placeholder='Enter your username', type='text',
                      style={'margin-left': '15px', 'margin-bottom': '10px', 'width': '300px'}),
            html.Br(),
            dbc.Input(id='password-input', placeholder='Enter your password', type='password',
                      style={'margin-left': '15px', 'margin-bottom': '10px', 'width': '300px'}),
            html.Br(),
            dbc.Button('Login', id='login-button', style={'margin-left': '15px', 'margin-bottom': '10px'},  # adding
                       # components for the ui which we make interactive in the callbacks which can be seen in the
                       # controller.py file
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
            dbc.Alert(  # adding messages when components are interacted with to reduce accidental double clicking and
                # adding values to the system
                "Transaction added successfully!",
                id="alert-auto",
                is_open=False,
                duration=4000,
                style={'border-radius': '4px'}
            ),
            dbc.Alert(
                "Error whilst adding transactions, check details and try again",
                id="alert",
                is_open=False,
                duration=4000,
                color='danger',
                style={'border-radius': '4px'}
            ),
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
        data = model_cfg.get_data_df()
        graph = px.line(data, y='amount', x='date')
        trn_table_data = data.groupby('category').agg({'amount': 'sum', 'type': 'first', }).reset_index()
        type_table_data = data.groupby('method').agg({'amount': 'sum', 'category': 'first'}).reset_index()
        card = Card()
        card.set_card_body([
            html.H4('Financial term of the day: Index'),
            html.Br(),
            html.H6('An index measures the price performance of a basket \n'
                    'of securities using a standardized metric and \n'
                    'methodology.')
        ])
        completed_quote_card = card.create_card()
        return dbc.Container([  # Use dbc.Container to wrap the row for proper alignment and padding
            dbc.Row([  # Wrap the columns in a dbc.Row to layout them horizontally
                dbc.Col([
                    dcc.Graph(figure=graph, id='graph'),
                    self.budget_card_maker()

                ], width=6),
                dbc.Col([
                    dbc.Container(id='budgets', children=[
                        dag.AgGrid(
                            style={'height': '270px'},
                            id='trn-table',
                            rowData=trn_table_data.to_dict('records'),
                            className='ag-theme-alpine-dark',
                            columnDefs=[{"field": i} for i in
                                        trn_table_data.columns],
                        ),
                        dag.AgGrid(
                            id='trn-table',
                            rowData=(type_table_data).to_dict('records'),
                            className='ag-theme-alpine-dark',
                            columnDefs=[{"field": i} for i in
                                        (type_table_data).columns],
                            style={'height': '270px'}
                        ),
                        completed_quote_card

                    ])
                ], width=6)
            ])
        ], fluid=True)

    def navbar(self):
        navbar = dbc.NavbarSimple(
            children=[
                dbc.DropdownMenu(
                    id='menu-dropdown',
                    children=[
                        dbc.DropdownMenuItem("More pages", header=True),  # adding the routes that trigger the url
                        # based callback so that app switches to desired page upon clicking item in menu
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

    def budget_card_maker(self):
        balance = float(model_cfg.get_balance())
        needs = 0
        fun = 0
        school = 0
        data = model_cfg.get_data_df()
        for index, row in data.iterrows():
            category = row[2]
            if category in ['Rent/Mortgage', 'Petrol/Fuel', 'Food', 'bills']:
                needs += row[3]
            elif category in ['Clothes', 'Events']:
                fun += row[3]
            elif category in ['Books', 'tuition fees', 'books', 'leisure']:
                school += row[3]
        recommended_school_pc = (30 / 100) * balance
        recommended_needs_pc = (50 / 100) * balance
        recommended_fun_pc = (20 / 100) * balance

        actual_school_pc = (school / recommended_school_pc) * 100
        actual_needs_pc = (needs / recommended_needs_pc) * 100
        actual_fun_pc = (fun / recommended_fun_pc) * 100

        card_content = [
            dbc.CardHeader("Categories"),
            dbc.CardBody(
                [
                    html.Div(
                        children=[
                        html.H6('school'),
                        dbc.Progress(label='{}% used'.format("{:.2f}".format(actual_school_pc)), value=actual_school_pc, color="primary",
                                     className="my-2", style={"height": "30px", "width": "300px"}),
                        html.H6('needs'),
                        dbc.Progress(label='{}% used'.format("{:.2f}".format(actual_needs_pc)), value=actual_needs_pc, color="primary",
                                     className="my-2", style={"height": "30px", "width": "300px"}),
                        html.H6('fun'),
                        dbc.Progress(label='{}% used'.format("{:.2f}".format(actual_fun_pc)), value=actual_fun_pc, color="primary",
                                     className="my-2", style={"height": "30px", "width": "300px"}),
                    ], style={'display': 'flex', 'flex-direction': 'column'})

                ], className="d-flex justify-content-center align-items-center",
                style={"height": "100px"}
            ),
        ]
        card = dbc.Card(card_content, color="dark", inverse=True, style={'height': '400px'})
        return card
