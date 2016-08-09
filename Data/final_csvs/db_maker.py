import os
import csv
import sqlite3

conn = sqlite3.connect('WiFinderDBv03.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ROOM
	(RoomID TEXT PRIMARY KEY NOT NULL,
	Capacity INT NOT NULL,
	Building TEXT NOT NULL,
	Campus TEXT NOT NULL);''')

cur.execute('''CREATE TABLE IF NOT EXISTS CLASS
	(ClassID TEXT PRIMARY KEY NOT NULL,
	Hour INT NOT NULL,
	Datetime TEXT NOT NULL,
	Room TEXT NOT NULL,
	Module TEXT NOT NULL,
	Reg_Students INT,
	FOREIGN KEY(Room) REFERENCES ROOM(Room));''')

cur.execute('''CREATE TABLE IF NOT EXISTS WIFI_LOGS
	(LogID INTEGER PRIMARY KEY AUTOINCREMENT,
	Time TEXT NOT NULL,
	Hour INT NOT NULL,
	Datetime TEXT NOT NULL,
	Room TEXT NOT NULL,
	Log_Count INT NOT NULL,
	ClassID TEXT NOT NULL,
	FOREIGN KEY(Room) REFERENCES ROOM(Room),
	FOREIGN KEY(ClassID) REFERENCES CLASS(ClassID));''')

cur.execute('''CREATE TABLE IF NOT EXISTS OCCUPANCY
	(OccID INTEGER PRIMARY KEY AUTOINCREMENT,
	Hour INT NOT NULL,
	Datetime TEXT NOT NULL,
	Room TEXT NOT NULL,
	Occupancy REAL NOT NULL,
	ClassID TEXT NOT NULL,
	FOREIGN KEY(Room) REFERENCES ROOM(Room),
	FOREIGN KEY(ClassID) REFERENCES CLASS(ClassID));''')

cur.execute('''CREATE TABLE IF NOT EXISTS USER
	(userID INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT NOT NULL,
	password TEXT NOT NULL,
	permission INT NOT NULL);''')

with open('room_table.csv', 'rt') as f:
	dr = csv.DictReader(f)
	to_db_room = [(i['Room'], i['Capacity'], i['Building'], i['Campus']) for i in dr]
f.close()

with open('timetable_table.csv', 'rt') as f:
	dr = csv.DictReader(f)
	to_db_class = [(i['ID'], i['Hour'], i['Date'], i['Room'], i['Module'], i['Registered_Students']) for i in dr]
f.close()

with open ('logdata_table.csv', 'rt') as f:
	dr = csv.DictReader(f)
	to_db_log = [(i['Time'], i['Hour'], i['Date'], i['Room'], i['Associated_count'], i['ID']) for i in dr]
f.close()

with open('occupancy_table_final.csv', 'rt') as f:
	dr = csv.DictReader(f)
	to_db_occ = [(i['Hour'], i['Date'], i['Room'], i['Occupancy'], i['ID']) for i in dr]
f.close()

cur.executemany('INSERT INTO ROOM (RoomID, Capacity, Building, Campus) VALUES (?, ?, ?, ?);', to_db_room)
cur.executemany('INSERT INTO CLASS (ClassID, Hour, Datetime, Room, Module, Reg_Students) VALUES (?, ?, ?, ?, ?, ?);', to_db_class)
cur.executemany('INSERT INTO WIFI_LOGS (Time, Hour, Datetime, Room, Log_Count, ClassID) VALUES (?, ?, ?, ?, ?, ?);', to_db_log)
cur.executemany('INSERT INTO OCCUPANCY (Hour, Datetime, Room, Occupancy, ClassID) VALUES (?, ?, ?, ?, ?)', to_db_occ)
cur.execute('INSERT INTO USER (email, password, permission) VALUES ("admin@wifinder.ie", "wifinder", 1)')
cur.execute('INSERT INTO USER (email, password, permission) VALUES ("admin@ucd.ie", "admin", 2)')
cur.execute('INSERT INTO USER (email, password, permission) VALUES ("it@ucd.ie", "it", 3)')
cur.execute('INSERT INTO USER (email, password, permission) VALUES ("lecturer@ucd.ie", "lecturer", 4)')
cur.execute('INSERT INTO USER (email, password, permission) VALUES ("viewer", "viewer", 5)')
conn.commit()
conn.close()
