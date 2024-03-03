import sqlite3
import datetime
import pandas as pd


class model:
    def __init__(self, db_name='finance.db'):
        self.db_name = db_name

    def connect_to_data_db(self, description, category, amount, method, type):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        c.execute(
            "INSERT OR IGNORE INTO transactions_tbl (description, category, amount, method, type, date) VALUES (?, ?, "
            "?, ?, ?, ?)",
            (description, category, amount, method, type, formatted_datetime))  # adding data to the database table
        # upon clicking 'save' or 'spend' button
        print('saved data into table')
        conn.commit()

    def get_data(self):
        items = []
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_input (input_text text)''')
        for row in c.execute('SELECT * FROM user_input'):  # getting all the transactions data
            items.append(' '.join(map(str, row)))
        conn.close()
        return items

    def get_balance(self):
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        c.execute('SELECT balance FROM wallet WHERE id = 1')
        balance = c.fetchone()[0]  # a separate table holds the current balance and this is updated when a
        # transaction is computed
        print('balance:', balance)
        return f"{balance:.2f}"

    def update_balance(self, description, category, current, new_val, selected_method):
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        new_balance = float(new_val) + float(current)  # updating the old balance with new transactions
        self.connect_to_data_db(description=description, category=category, amount=new_val, method=selected_method,
                                type='IN')
        print('balance saving into db')
        c.execute('UPDATE wallet SET balance = balance + ? WHERE id = 1', (new_val,))
        conn.commit()
        return f"{new_balance:.2f}"

    def spend_balance(self, description, category, current, new_val, selected_method):
        conn = sqlite3.connect('dash.db')
        c = conn.cursor()
        new_balance = float(current) - float(new_val)
        self.connect_to_data_db(description=description, category=category, amount=new_val, method=selected_method,
                                type='OUT')
        print(new_balance)
        print('balance saving into db')
        c.execute('UPDATE wallet SET balance = balance - ? WHERE id = 1', (new_val,))
        conn.commit()
        return f"{new_balance:.2f}"

    def get_data_df(self):  # get a dataframe of the data in the transactions table of the db
        conn = sqlite3.connect('dash.db')
        query = 'SELECT * FROM transactions_tbl'
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df






