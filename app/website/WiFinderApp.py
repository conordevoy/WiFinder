from flask import Flask, render_template, g
import sqlite3

WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

# WiFinderApp.db = "wifinderDB.db"
db = "wifinderDB.db"


def connectDB():
    '''Connects to an Sqlite3 database'''
    return sqlite3.connect(db)


def get_db():
    '''Checks for a DB connection. If not found, calls connect_to_database to establish connection'''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connectDB()
    return db


@WiFinderApp.route("/")
def WiFinderHTML():
    '''Render HTML template'''
    return render_template("index.html")


@WiFinderApp.route("/searchfake")
def search_page():
    '''Load demo search page - artificial data to test jinja connections'''

    return render_template("search.html",
                           title='Search',
                           rooms=['B002', 'quack', 'B004'],
                           times=[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                           days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                           densities=['0%', '25%', '50%', '75%', '100%'])


@WiFinderApp.route("/searchreal")
def search_real():
    '''load search page with real data - test to check db connection'''

    cur = get_db().cursor()
    roomdata = cur.execute("SELECT * FROM B02 WHERE pid < 10;")

    return render_template("search.html",
                           title='Search',
                           rooms=roomdata,
                           times=[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                           days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                           densities=['0%', '25%', '50%', '75%', '100%'])


@WiFinderApp.route("/layout")
def layout():
    '''load base layout - just to display basic template, not intended as standalone page'''

    return render_template("page_layout.html",
                           title='Layout')


if __name__ == "__main__":
    WiFinderApp.run()
