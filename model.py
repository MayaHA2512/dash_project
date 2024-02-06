import sqlite3

class model:
    def __init__(self, db_name='finance.db'):
        self.db_name = db_name

    def connect_to_data_db(self, amount, method):
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO transactions (amount, method) VALUES (?, ?)", (amount, method))
        print('saved data into table')
        conn.commit()


    def get_data(self):
        items = []
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_input (input_text text)''')
        for row in c.execute('SELECT * FROM user_input'):
            items.append(' '.join(map(str, row)))
        conn.close()
        return items

    def save_data(self, input_text):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_input (input_text text)''')
        c.execute("INSERT INTO user_input VALUES (?)", (input_text,))
        conn.commit()
        conn.close()

    def get_balance(self):
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        c.execute('SELECT balance FROM wallet WHERE id = 1')
        balance = c.fetchone()[0]
        print('balance:', balance)
        return f"{balance:.2f}"

    def update_balance(self, current, new_val, selected_method):
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        new_balance = float(new_val) + float(current)
        self.connect_to_data_db(new_val, selected_method)
        print('balance saving into db')
        c.execute('UPDATE wallet SET balance = balance + ? WHERE id = 1', (new_val,))
        conn.commit()
        return f"{new_balance:.2f}"

    def spend_balance(self, current, new_val, selected_method):
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        new_balance = float(current) - float(new_val)
        self.connect_to_data_db(new_val, selected_method)
        print(new_balance)
        print('balance saving into db')
        c.execute('UPDATE wallet SET balance = balance - ? WHERE id = 1', (new_val,))
        conn.commit()
        return f"{new_balance:.2f}"
# logic to calculate and save to db
# create connect to db fn
