import sqlite3
#
#
conn = sqlite3.connect('dash.db')
c = conn.cursor()
#
# # Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS transactions_tbl (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        category TEXT,
        amount INTEGER,
        method TEXT,
        type TEXT
    )
''')

# # Initialize 'students' row if it doesn't exist
# c.execute("INSERT OR IGNORE INTO transactions_tbl (description, category, amount, method, type) VALUES ('Shopping Spree', 'leisure',  30, 'card', 'IN')")
#
# "INSERT OR IGNORE INTO transactions_tbl (description, category, amount, method, type) VALUES ('Shopping Spree', 'leisure',  30, 'card', 'IN')"
# conn.commit()
# conn.close()

#
# # Fetch all rows from the query
# c.execute('DELETE FROM transactions WHERE id = 17')
# rows = c.fetchall()
#
# # Iterate over the rows and print them
# for row in rows:
#     print(row)
#
# # Close the cursor and the connection
# c.close()
# conn.close()

import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object
cur = conn.cursor()

# SQL command to add a new column
# Replace 'table_name' with your table's name
# Replace 'new_column_name' with your new column's name
# Replace 'column_type' with your new column's type (e.g., TEXT, INTEGER, etc.)
c.execute('ALTER TABLE transactions_tbl ADD COLUMN date TEXT')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
