import sqlite3
#
#
conn = sqlite3.connect('../databases/dash.db')
c = conn.cursor()
#
# # Create table if it doesn't exist

def create_tbl():
    c.execute('''
        CREATE TABLE IF NOT EXISTS budget_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            percentage REAL
        )
    ''')
    conn.commit()
    conn.close()


def delete_data():
    conn = sqlite3.connect('../databases/dash.db')
    c = conn.cursor()

    # Delete all data from the budget_table
    c.execute('DELETE FROM budget_table;')

    # Optionally, reset the autoincrement counter for budget_table
    # This step is only necessary if you want to reset the ID counter
    c.execute('DELETE FROM sqlite_sequence WHERE name="budget_table";')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


#

def get_data():
    c.execute('SELECT * FROM budget_table')
    rows = c.fetchall()
    for row in rows:
        print(row)

# import sqlite3
def add_col():
    conn = sqlite3.connect('../databases/example.db')
    cur = conn.cursor()
    cur.execute('ALTER TABLE transactions_tbl ADD COLUMN date TEXT')
    conn.commit()


def update_val():
    conn = sqlite3.connect('../databases/dash.db')
    c = conn.cursor()
    c.execute('UPDATE wallet SET balance =  ? WHERE id = 1', (327.50,))
    conn.commit()
    conn.close()

def add_row():
    c.execute("INSERT OR IGNORE INTO budget_table (category, percentage) VALUES (?, ?)", ('books', 34.43))
    conn.commit()
    conn.close()

get_data()
