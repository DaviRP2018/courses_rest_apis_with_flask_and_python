import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text);"
    "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real);"
)

cursor.execute("INSERT INTO items VALUES ('test', 10.99);")

connection.commit()
connection.close()
