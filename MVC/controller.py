from dash import html, dcc
from flask import Flask
from model import model
from view import FinanceView
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_ag_grid as dag

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/', suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.DARKLY])
model = model()
_view = FinanceView()

app.layout = html.Div([  # the base layout and we append on this design when building other pages
    dcc.Location(id='url', refresh=False),  # collecting the base url
    FinanceView().navbar(),
    html.Div(id='page-content')  # empty container
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        database_items = model.get_data()  # getting the transactions that have been saved into the db from previous
        # sessions
        return FinanceView.success_layout(database_items)
    elif pathname == '/login':
        return FinanceView.login_layout()
    elif pathname == '/budgets':
        return FinanceView().budget_layout()


@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),  # provide input which is what triggers the callback -> Output
     # which is what type of object or filter you want to return -> States refer to collecting what values are in a
     # component at that moment in time e.g. what a user has entered an input field component
     # finally
     Output('login-output', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value')],
    prevent_initial_call=True

)
def login_auth(n_clicks, username, password):
    if username == 'admin' and password == 'admin':
        return '/', ''
    else:
        return dash.no_update, ''


@app.callback(
    Output("alert", "is_open"),
    Output("alert-auto", "is_open"),
    Output('balance', 'children'),
    [Input('save-button', 'n_clicks'),
     Input('spend-button', 'n_clicks'), ],
    [State('input-box', 'value'),
     State('select', 'value'),
     State('category', 'value'),
     State('description-box', 'value'),
     State('balance', 'children'),
     State("alert-auto", "is_open"),
     State("alert", "is_open")
     ],
    prevent_initial_call=True
)
def update_output(save_clicks, spend_clicks, user_input, selected_val, category, description, current_val,
                  success_isopen, alert_isopen):
    print('inputs', save_clicks, spend_clicks, user_input, current_val)
    button_clicked = dash.ctx.triggered_id
    if button_clicked == 'save-button':  # error handling for user input ensure that the input for 'amount' isn't a
        # number
        try:
            val = int(user_input)
            if type(description) == str and val > 0 and val is not None:
                # the function below appends the data to the db and when the refresh button is hit it will trigger
                # the pie chart table to update with the new transactions
                new_balance = model.update_balance(current=current_val, new_val=user_input,
                                                   selected_method=selected_val,
                                                   category=category, description=description)
                print('save button balance', new_balance)
                return alert_isopen, not success_isopen, new_balance  # adding feedback upon user clicking button to
                # prevent accidental clicking
        except ValueError:
            print("That's not an int!")
            return current_val, success_isopen, not alert_isopen  # return an error message if the input is wrong

    elif button_clicked == 'spend-button':
        try:
            val = int(user_input)
            if type(description) == str and val > 0:
                new_balance = model.spend_balance(current=current_val, new_val=user_input,
                                                   selected_method=selected_val,
                                                   category=category, description=description)
                print('save button balance', new_balance)
                return alert_isopen, not success_isopen, new_balance
        except ValueError:
            print("That's not an int!")
            return current_val, success_isopen, not alert_isopen


@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('logout-button', 'n_clicks')],
    prevent_initial_call=True

)
def logout(n_clicks):
    return '/login' if n_clicks else dash.no_update  # callback for logging out button to redirect to log in button


@app.callback(

    Output('transaction-table', 'rowData'),
    Output('pie_chart', 'figure'),
    [Input('refresh-button', 'n_clicks')],
    prevent_initial_call=True
)
def update(n_clicks):  # this callback updates the ag grid and pie chart with updated transactions that have been added during the current session
    if n_clicks is not None:
        pie_chart = _view.pie_chart()
        table_data = model.get_data_df().to_dict('records')
        return table_data, pie_chart


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
