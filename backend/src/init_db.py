import sqlite3

connection = sqlite3.connect('database.db')

with open('/Users/brodytrue/coding-projects/web/chatapp/backend/src/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO messages (content) VALUES (?)", 
            ('Content for the first post.',))

cur.execute("INSERT INTO messages (content) VALUES (?)", 
            ('This is the second post!',))

connection.commit()
connection.close()