from dash import html, dcc
from flask import Flask
from model import model
from view import FinanceView
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/', suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])
model = model()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    FinanceView().navbar(),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        database_items = model.get_data()
        return FinanceView.success_layout(database_items)
    elif pathname == '/login':
        return FinanceView.login_layout()


@app.callback(
    [Output('url', 'pathname',allow_duplicate=True),
     Output('login-output', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value')],
prevent_initial_call=True


)
def login_auth(n_clicks, username, password):
    if username == 'admin' and password == 'admin':
        return '/', f'Login Successful {username}'
    else:
        return dash.no_update, 'Incorrect username or password'


@app.callback(
    Output('balance', 'children'),
    [Input('save-button', 'n_clicks'),
     Input('spend-button', 'n_clicks'),],
    [State('input-box', 'value'),
     State('balance', 'children')],
prevent_initial_call=True
)
def update_output(save_clicks, spend_clicks, user_input, current_val):
    print('inputs', save_clicks, spend_clicks, user_input, current_val)
    button_clicked = dash.ctx.triggered_id
    if button_clicked == 'save-button':
        new_balance = model.update_balance(current=current_val, new_val=user_input)
        print('save button balance', new_balance)
        return new_balance
    elif button_clicked == 'spend-button':
        new_balance = model.spend_balance(current=current_val, new_val=user_input)
        return new_balance





@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('logout-button', 'n_clicks')],
prevent_initial_call=True

)
def logout(n_clicks):
    return '/login' if n_clicks else dash.no_update



if __name__ == '__main__':
    app.run_server(debug=True)
