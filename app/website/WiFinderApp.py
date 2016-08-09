from flask import Flask, render_template, g, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3
from hardwire_models import *
from werkzeug import secure_filename
import os

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure,output_file,show
from bokeh.models import LinearAxis, Range1d
import pandas as pd
from bokeh.layouts import gridplot


WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

WiFinderApp.secret_key = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8b\x0c\x9f'  # session key random generated from os

db = "WiFinderDBv03.db"

dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

UPLOAD_FOLDER = dir_path + '/tmp/'
ALLOWED_EXTENSIONS = set(['zip'])

WiFinderApp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# login required decorator
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
    '''login page for website'''
    # userdata = query("SELECT * FROM USER;")
    # print(userdata)
    error = None
    if request.method == 'POST':
        # if request.form['username'] != 'shauna' or request.form['password'] != 'wifinder':
        #     error = 'Invalid Credentials. Please try again.'
        # else:
        #     session['logged_in'] = True
        #     return redirect(url_for('index'))
        user = request.form['username']
        user_exists = query("SELECT * FROM USER WHERE email=\'{}\';".format(user))
        # print(user_exists)
        # for user in user_exists:
        #   print(user[1])
        #   print(user[2])
        if request.form['password'] != user[2]:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', title='Login', error=error)


@WiFinderApp.route('/logout')
def logout():
    session.pop("logged_in", None)
    flash("You have just been logged out!")
    return redirect(url_for('login'))

@WiFinderApp.route("/index")
@login_required
def index():
    '''load homepage'''
    return render_template("index.html",
                           title='Home')

@WiFinderApp.route("/")
@login_required
def WiFinderHTML():
    '''Render HTML template'''
    return render_template("estimator.html")


@WiFinderApp.route("/explore")
@login_required
def explore():
    '''explore page for website'''
    timedata = query("SELECT DISTINCT Hour FROM CLASS;")
    roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduledata = query("SELECT DISTINCT Module FROM CLASS;")
    datedata = query("SELECT DISTINCT Datetime FROM CLASS;")

    # get values from form
    room = request.args.get('Room')
    datetime = request.args.get('Date')
    time = request.args.get('Time')

    df = pd.read_sql_query(
        "SELECT W.Log_Count, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy, O.OccID FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON C.ClassID = O.ClassID WHERE R.RoomID = \'{}\' AND W.Datetime =\'{}\' GROUP BY W.LogID;".format(
            room, datetime), connectDB())

    df['Time'] = df['Time'].apply(pd.to_datetime)

    if room and datetime:
        p = figure(width=800, height=500, x_axis_type="datetime", )
        p.extra_y_ranges = {"foo": Range1d(start=0, end=1)}

        p.line(df['Time'], df['Log_Count'], color='red', legend='Log Count')
        p.line(df['Time'], df['Reg_Students'], color='green', legend='Registered Students')
        p.line(df['Time'], df['Capacity'], color='blue', legend='Capacity')
        p.line(df['Time'], df['Occupancy'] * 100, color='orange', legend='Occupancy')

        p.add_layout(LinearAxis(y_range_name="foo"), 'left')

        print(df.head(5))

        script, div = components(p)
        return render_template(
            'explore.html',
            script=script,
            div=div,
            rooms=roomdata,
            times=timedata,
            modules=moduledata,
            dates=datedata
        )
    # else:
    #     df = pd.read_sql_query(
    #         "SELECT W.Log_Count, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy, O.OccID FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON C.ClassID = O.ClassID WHERE R.RoomID = 'B002' AND W.Datetime = '2015-11-12' GROUP BY W.LogID;",
    #         connectDB())


    #     df['Time'] = df['Time'].apply(pd.to_datetime)
    #     p = figure(width=800, height=250, x_axis_type="datetime", )
    #     p.extra_y_ranges = {"foo": Range1d(start=0, end=1)}

    #     p.line(df['Time'], df['Log_Count'], color='red', legend='Log Count')
    #     p.line(df['Time'], df['Reg_Students'], color='green', legend='Registered Students')
    #     p.line(df['Time'], df['Capacity'], color='blue', legend='Capacity')
    #     p.line(df['Time'], df['Occupancy'] * 100, color='orange', legend='Occupancy')

    #     p.add_layout(LinearAxis(y_range_name="foo"), 'left')

    #     p2 = figure(width=800, height=250, x_axis_type="datetime", x_range=p.x_range, )
    #     p2.line(df['Time'], df['Log_Count'], color='red', legend='Log Count')

    #     r = gridplot([[p, p2]], toolbar_location=None)

    #     script, div = components(r)
    #     return render_template(
    #         'explore.html',
    #         script=script,
    #         div=div,
    #         rooms=roomdata,
    #         times=timedata,
    #         modules=moduledata,
    #         dates=datedata
    #     )
    return render_template('explore.html',
                          rooms=roomdata,
                          times=timedata,
                          dates=datedata) 

@WiFinderApp.route("/register")
def register():
    '''registration page for website'''
    # unique= query("SELECT DISTINCT username FROM User;")
    return render_template("register.html",
                           title='Registration')


# @WiFinderApp.route("/results", methods=['GET'])
# @login_required
# def results():
#     '''results page for website'''
#     room = request.args.get('Room')
#     datetime = request.args.get('Date')
#     time = request.args.get('Time')
#     print(room, datetime, time)
#     cur = get_db().cursor()
#     subdata = cur.execute("""SELECT AVG(W.Log_Count)
#         FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID
#         JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON R.RoomID = O.Room
#         WHERE R.RoomID = \'{}\' AND W.Datetime = \'{}\' AND W.Hour = \'{}\'
#         AND strftime('%M', W.Time) BETWEEN \"15\" AND \"45\";""".format(room, datetime, time))
#     return render_template("results.html",
#                            title='Results',
#                            result=subdata.fetchone()[0])


@WiFinderApp.route("/estimator", methods=['GET'])
@login_required
def estimator():
    '''estimates three model functions'''

    timedata = query("SELECT DISTINCT Hour FROM CLASS;")
    roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduledata = query("SELECT DISTINCT Module FROM CLASS;")
    datedata = query("SELECT DISTINCT Datetime FROM CLASS;")

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

    glyph_dict = {'Empty': 'remove-circle',  # these aren't strictly necessary at the moment
                  'Occupied': 'ok-circle',  # however, i'm going to retool the results page to be shorter
                  'Low': 'arrow-down',  # and then these will be less useless
                  'Medium': 'arrow-right',
                  'High': 'arrow-up'}

    if room and time and datetime:
        linear_estimate = linear_predictor(query_result)
        tertiary_estimate = tertiary_classifier(query_result)
        binary_estimate = binary_classifier(query_result)

        # these return statements are ugly - these will hopefully be fixed but work for now.
        # maybe url redirects would be better?
        return render_template("estimator.html",
                               title='Estimations',
                               linear_estimate=linear_estimate,
                               binary_estimate=binary_estimate,
                               tertiary_estimate=tertiary_estimate,
                               binary_glyph=glyph_dict[binary_estimate],
                               tertiary_glyph=glyph_dict[tertiary_estimate],
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


@WiFinderApp.route("/updatemodel", methods=['GET'])
@login_required
def update_model():

    # This does nothing yet. Need a way to pass a value saying whether to do this or not.
    # eventually, though, this will call:

    # import Linear_Regression_Creator
    # import Logistic_Regression_Creator

    # this will execute both scripts

    return render_template("update_model.html", title='Update Model')

@WiFinderApp.route("/modelupdated", methods=['GET'])
@login_required
def model_updated():


    import Linear_Regression_Creator
    import Logistic_Regression_Creator

    return render_template("model_updated.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@WiFinderApp.route("/datainput", methods=['GET', 'POST'])
@login_required
def data_input():
    cf = os.listdir(WiFinderApp.config['UPLOAD_FOLDER'],)
    if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(WiFinderApp.config['UPLOAD_FOLDER'], filename))
          flash(filename + " uploaded successfully")
          return render_template("data_input.html",
                  current_files= cf,
                               title='Data Input')
      else:
          filename = secure_filename(file.filename)
          flash("Upload unsuccessful")
    return render_template("data_input.html",
            current_files= cf, title='Data Input')

@WiFinderApp.route("/lectureinput")
@login_required
def input():
    '''page for lecturers to upload a survey form'''
    timeinput = query("SELECT DISTINCT Hour FROM CLASS;")
    roominput = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduleinput = query("SELECT DISTINCT Module FROM CLASS;")
    return render_template("lectureinput.html",
                           title='Home',
                           rooms_input=roominput,
                           times_input=timeinput,
                           modules_input=moduleinput)


if __name__ == "__main__":
    WiFinderApp.run()
