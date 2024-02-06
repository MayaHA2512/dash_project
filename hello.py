import sqlite3


conn = sqlite3.connect('dash.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS wallet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        balance INTEGER
    )
''')

# Initialize 'students' row if it doesn't exist
c.execute('INSERT OR IGNORE INTO wallet (id, balance) VALUES (1, 0)')

conn.commit()
conn.close()
