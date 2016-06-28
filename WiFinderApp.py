from flask import Flask, render_template
import sqlite3

WiFinderApp = Flask(__name__, static_url_path="/app/website/static")

WiFinderApp.debug = True

WiFinderApp.db = "wifinderDB.db"

@WiFinderApp.route("/")
def WiFinderHTML():
	'''Render HTML template'''
	return render_template("index.html")

def connectDB():
	'''DB connection'''
	return sqlite3.connect(WiFinderApp.db)

if __name__ == "__main__":
	WiFinderApp.run()
