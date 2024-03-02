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
    elif pathname == '/budgets':
        return FinanceView().budget_layout()


@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),
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
    if button_clicked == 'save-button':
        try:
            val = int(user_input)
            if type(description) == str and val > 0:
                new_balance = model.update_balance(current=current_val, new_val=user_input,
                                                   selected_method=selected_val,
                                                   category=category, description=description)
                print('save button balance', new_balance)
                return  alert_isopen, not success_isopen, new_balance
        except ValueError:
            print("That's not an int!")
            return current_val, success_isopen, not alert_isopen

    elif button_clicked == 'spend-button':
        try:
            val = int(user_input)
            if type(description) == str and val > 0:
                new_balance = model.update_balance(current=current_val, new_val=user_input,
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
    return '/login' if n_clicks else dash.no_update


@app.callback(

    Output('transaction-table', 'rowData'),
    Output('pie_chart', 'figure'),
    [Input('refresh-button', 'n_clicks')],
    prevent_initial_call=True
)
def update(n_clicks):
    if n_clicks is not None:
        pie_chart = _view.pie_chart()
        table_data = model.get_data_df().to_dict('records')
        return table_data, pie_chart


@app.callback(
    Output('budgets', 'children', allow_duplicate=True),
    [Input('add-button', 'n_clicks')],
    State('budget-category-dropdown', 'value'),
    State('budget-input', 'value'),
    State('budgets', 'children'),
    prevent_initial_call=True

)
def update(n_clicks, cat_chosen, user_input, budgets_list):
    print(n_clicks, user_input, cat_chosen, budgets_list)
    model.publish_budget_to_db(category=cat_chosen, user_input=user_input)
    new_card = _view.budget_card_maker(user_input, cat_chosen)
    budgets_list.append(new_card)
    return budgets_list


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
