import sqlite3


conn = sqlite3.connect('dash.db')
c = conn.cursor()

# # Create table if it doesn't exist
# c.execute('''
#     CREATE TABLE IF NOT EXISTS transactions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         amount INTEGER,
#         method TEXT
#     )
# ''')
#
# # Initialize 'students' row if it doesn't exist
# c.execute("INSERT OR IGNORE INTO transactions (id, amount, method) VALUES (1, 30, 'card')")
#
#
# conn.commit()
# conn.close()


# Fetch all rows from the query
c.execute('SELECT * FROM transactions')
rows = c.fetchall()

# Iterate over the rows and print them
for row in rows:
    print(row)

# Close the cursor and the connection
c.close()
conn.close()