from flask import Flask, render_template, g, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3
from app.website.Modelling_Functions import logistic_classifier
from app.website.Modelling_Functions import hardwire_linear

WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

WiFinderApp.secret_key = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8b\x0c\x9f' #session key random generated from os

db = "WiFinderDBv02.db"

stored_query = """SELECT AVG(W.Log_Count)
        FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID
        JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON R.RoomID = O.Room
        WHERE R.RoomID = \'{}\' AND W.Datetime = \'{}\' AND W.Hour = \'{}\'
        AND strftime('%M', W.Time) BETWEEN \"15\" AND \"45\";"""

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

# route for handling the login page logic
@WiFinderApp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'shauna' or request.form['password'] != 'wifinder':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('search'))
    return render_template('login.html', title='Login', error=error)

@WiFinderApp.route('/logout')
def logout():
    session.pop("logged_in", None)
    flash("You have just been logged out!")
    return redirect(url_for('login'))

@WiFinderApp.route("/")
@login_required
def WiFinderHTML():
    '''Render HTML template'''
    return render_template("index.html")

@WiFinderApp.route("/search")
@login_required
def search():
    '''search page for website'''
    timedata = query("SELECT DISTINCT Hour FROM CLASS;")
    roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduledata = query("SELECT DISTINCT Module FROM CLASS;")
    datedata = query("SELECT DISTINCT Datetime FROM WIFI_LOGS;")
    return render_template("search.html",
                           title='Home',
                           rooms=roomdata,
                           times=timedata,
                           modules=moduledata,
                           dates=datedata)

@WiFinderApp.route("/results", methods=['GET'])
@login_required
def results():
    '''results page for website'''
    room = request.args.get('Room')
    datetime = request.args.get('Date')
    time = request.args.get('Time')
    print(room, datetime, time)
    cur = get_db().cursor()
    subdata = cur.execute("""SELECT AVG(W.Log_Count) 
        FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID 
        JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON R.RoomID = O.Room 
        WHERE R.RoomID = \'{}\' AND W.Datetime = \'{}\' AND W.Hour = \'{}\' 
        AND strftime('%M', W.Time) BETWEEN \"15\" AND \"45\";""".format(room, datetime, time))
    return render_template("results.html", 
                            title='Results',
                            result=subdata.fetchone()[0])

@WiFinderApp.route("/estimator", methods=['GET'])
def estimator():
    '''estimates three model functions'''

    timedata = query("SELECT DISTINCT Hour FROM CLASS;")
    roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduledata = query("SELECT DISTINCT Module FROM CLASS;")
    datedata = query("SELECT DISTINCT Datetime FROM WIFI_LOGS;")

    # get values from form
    room = request.args.get('Room')
    datetime = request.args.get('Date')
    time = request.args.get('Time')


    cur = get_db().cursor()
    average_counts = cur.execute("""SELECT AVG(W.Log_Count)
        FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID
        JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON R.RoomID = O.Room
        WHERE R.RoomID = \'{}\' AND W.Datetime = \'{}\' AND W.Hour = \'{}\'
        AND strftime('%M', W.Time) BETWEEN \"15\" AND \"45\";""".format(room, datetime, time))

    query_result = average_counts.fetchone()[0]

    glyph_dict = {'Empty' : 'remove-circle', # these aren't strictly necessary at the moment
    				'Occupied': 'ok-circle', # however, i'm going to retool the results page to be shorter
    				'Low' : 'arrow-down', # and then these will be less useless
    				'Medium': 'arrow-right',
    				'High': 'arrow-up'}


    if room and time and datetime:
        linear_estimate = hardwire_linear(query_result)
        tertiary_estimate = logistic_classifier(query_result, 'tertiary')
        binary_estimate = logistic_classifier(query_result, 'binary')

    # these return statements are ugly - these will hopefully be fixed but work for now.
        # maybe url redirects would be better?
        return render_template("estimator.html",
                           title='Estimations',
                           linear_estimate = linear_estimate,
                           binary_estimate = binary_estimate,
                           tertiary_estimate = tertiary_estimate,
                           binary_glyph = glyph_dict[binary_estimate],
                           tertiary_glyph = glyph_dict[tertiary_estimate],
                           rooms=roomdata,
                           times=timedata,
                           modules=moduledata,
                           dates=datedata
                           )

    else:
        return render_template("estimator.html",
                   title='Estimations',
                   rooms=roomdata,
                   times=timedata,
                   modules=moduledata,
                   dates=datedata
                   )

@WiFinderApp.route("/layout")
def layout():
    '''load base template - only here to prototype design'''
    return render_template("page_layout.html",
                           title='Layout')

if __name__ == "__main__":
    WiFinderApp.run()