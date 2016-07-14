import os
import csv
import sqlite3

conn = sqlite3.connect('WiFinderDBv01.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ROOM
	(Room TEXT PRIMARY KEY NOT NULL,
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

cur.executemany('INSERT INTO ROOM (Room, Capacity, Building, Campus) VALUES (?, ?, ?, ?);', to_db_room)
cur.executemany('INSERT INTO CLASS (ClassID, Hour, Datetime, Room, Module, Reg_Students) VALUES (?, ?, ?, ?, ?, ?);', to_db_class)
cur.executemany('INSERT INTO WIFI_LOGS (Time, Hour, Datetime, Room, Log_Count, ClassID) VALUEs (?, ?, ?, ?, ?, ?);', to_db_log)
conn.commit()
conn.close()