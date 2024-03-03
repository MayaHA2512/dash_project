import dash_bootstrap_components as dbc

class Card:
    def __init__(self, style=None):
        if style is None:
            style = {}  # set a default of empty brackets to avoid errors when component only requires default styling
        self.card_body = None
        self.style = style

    def get_card_body(self):  # getter and setter methods instead of directly reassigning card body value to prevent
        # accidental changes
        if self.card_body is None:
            return 'card body not set yet'  # error handling for card body not being set
        else:
            return self.card_body

    def set_card_body(self, card_body):
        self.card_body = card_body

    def create_card(self):
        if self.card_body is not None:
            card = dbc.Card([dbc.CardBody(self.card_body), ], color="dark", inverse=True, style=self.style)  # default styling i.e. dark mode
            return card  # using the card class with predefined styling
        else:
            return 'set card body before creating card'


