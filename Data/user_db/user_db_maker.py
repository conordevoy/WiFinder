import os
import sqlite3

conn = sqlite3.connect('UserDBv01.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS USER
	(userID INTEGER PRIMARY KEY AUTOINCREMENT,
	name Text NOT NULL,
	email TEXT NOT NULL,
	password TEXT NOT NULL,
	# date_created TEXT NOT NULL,
	permission TEXT NOT NULL);''')

# cur.executemany('INSERT INTO USER (name, email, password, permission) VALUES ('admin', 'admin@ucd.ie', 'wifinder', 'A');')
# cur.executemany('INSERT INTO USER (name, email, password, permission) VALUES ('user', 'user@ucd.ie', 'password', 'U');')