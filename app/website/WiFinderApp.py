from flask import Flask, render_template, g
import sqlite3

WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

# WiFinderApp.db = "wifinderDB.db"
db = "timetable2.sqlite"


def connectDB():
    '''Connects to an Sqlite3 database'''
    return sqlite3.connect(db)


def get_db():
    '''Checks for a DB connection. If not found, calls connect_to_database to establish connection'''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connectDB()
    return db

def query(sqlcode):
    '''wrapper function to execute queries against set DB'''

    cur = get_db().cursor()
    data = cur.execute(sqlcode)

    return data


@WiFinderApp.route("/")
def WiFinderHTML():
    '''Render HTML template'''
    return render_template("index.html")


@WiFinderApp.route("/search")
def search():
    '''search page for website'''

    timedata = query("SELECT DISTINCT time FROM timetable_table;")
    roomdata = query("SELECT DISTINCT room FROM timetable_table;")
    moduledata = query("SELECT DISTINCT module FROM timetable_table;")
    alldata = query("SELECT * FROM timetable_table;")



    return render_template("search.html",
                           title='Search',
                           rooms=roomdata,
                           times=timedata,
                           modules=moduledata,
                           densities=alldata)


@WiFinderApp.route("/layout")
def layout():
    '''load base template - only here to prototype design'''

    return render_template("page_layout.html",
                           title='Layout')


if __name__ == "__main__":
    WiFinderApp.run()
