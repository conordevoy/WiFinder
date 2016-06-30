from flask import Flask, render_template
import sqlite3

WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

WiFinderApp.db = "wifinderDB.db"

@WiFinderApp.route("/")
def WiFinderHTML():
	'''Render HTML template'''
	return render_template("index.html")

def connectDB():
	'''DB connection'''
	return sqlite3.connect(WiFinderApp.db)

@WiFinderApp.route("/search")
def search_page():
	'''load search page'''

	return render_template("search.html",
						   title = 'Search',
						   rooms = ['B002', 'quack', 'B004'],
						   times = [9, 10, 11, 12 ,13 ,14 ,15 ,16 ,17, 18, 19],
						   days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
						   densities = ['0%', '25%', '50%', '75%', '100%'])

@WiFinderApp.route("/layout")
def layout():
	'''load base layout'''

	return render_template("page_layout.html",
						   title = 'Layout')

if __name__ == "__main__":
	WiFinderApp.run()
