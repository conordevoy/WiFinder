from flask import Flask, render_template, g, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3

WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

WiFinderApp.secret_key = 'hello'

db = "WiFinderDBv02.db"

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Sorry, you need to login first!')
            return redirect(url_for('login'))
    return wrap

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
@login_required
def WiFinderHTML():
    '''Render HTML template'''
    return render_template("index.html")

@WiFinderApp.route("/results")
@login_required
def results():
    '''results page for website'''
    alldata = query("""SELECT W.LogID, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy
                FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID
                JOIN ROOM R ON C.Room = R.RoomID
                JOIN OCCUPANCY O ON R.RoomID = O.Room
                WHERE W.Hour = 9 OR W.Hour = 10 OR W.Hour = 10 OR W.Hour = 11 OR W.Hour = 12 OR W.Hour = 13 OR W.Hour = 14 OR W.Hour = 15 OR W.Hour = 16
                GROUP BY W.LogID;
                """)
    return render_template("results.html",
                            title='Results',
                            result=alldata)

@WiFinderApp.route("/search")
@login_required
def search():
    '''search page for website'''
    timedata = query("SELECT DISTINCT Hour FROM CLASS;")
    roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduledata = query("SELECT DISTINCT Module FROM CLASS;")
    datedata = query("SELECT DISTINCT Datetime FROM WIFI_LOGS;")
    # for row in datedata:
    #     print(row[0])
    return render_template("search.html",
                           title='Home',
                           rooms=roomdata,
                           times=timedata,
                           modules=moduledata,
                           dates=datedata)

# route for handling the login page logic
@WiFinderApp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'shauna' or request.form['password'] != 'wifinder':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("You have just been logged in!")
            return redirect(url_for('search'))
    return render_template('login.html', title='Login', error=error)

@WiFinderApp.route('/logout')
def logout():
    session.pop("logged_in", None)
    flash("You have just been logged out!")
    return redirect(url_for('login'))

@WiFinderApp.route("/layout")
def layout():
    '''load base template - only here to prototype design'''
    return render_template("page_layout.html",
                           title='Layout')


if __name__ == "__main__":
    WiFinderApp.run()