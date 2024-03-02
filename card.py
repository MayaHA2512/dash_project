import dash_bootstrap_components as dbc

class Card:
    def __init__(self, header_name, style=None):
        if style is None:
            style = {}
        self.card_body = None
        self.head_name = header_name
        self.style = style

    def get_card_body(self):
        if self.card_body is None:
            return 'card body not set yet'
        else:
            return self.card_body

    def set_card_body(self, card_body):
        self.card_body = card_body

    def create_card(self):
        if self.card_body is not None:
            card = dbc.Card([dbc.CardBody(self.card_body), ], color="dark", inverse=True, style=self.style)
            return card
        else:
            return 'set card body before creating card'


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

card = Card('Add Budget')
card.set_card_body([
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
)
card = card.create_card()