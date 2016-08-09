from flask import Flask, render_template, g, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3
from hardwire_models import *
from werkzeug import secure_filename
import os

WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

WiFinderApp.secret_key = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8b\x0c\x9f'  # session key random generated from os

db = "WiFinderDBv02.db"

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
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'shauna' or request.form['password'] != 'wifinder':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('estimator'))
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
    '''search page for website'''
    timedata = query("SELECT DISTINCT Hour FROM CLASS;")
    roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduledata = query("SELECT DISTINCT Module FROM CLASS;")
    datedata = query("SELECT DISTINCT Datetime FROM WIFI_LOGS;")
    return render_template("explore.html",
                           title='Explore',
                           rooms=roomdata,
                           times=timedata,
                           modules=moduledata,
                           dates=datedata)

@WiFinderApp.route("/register")
def register():
    '''search page for website'''
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
                               dates=datedata,
                               room_check=room,
                               date_check=datetime,
                               time_check=time)

    else:
        return render_template("estimator.html",
                               title='Estimations',
                               rooms=roomdata,
                               times=timedata,
                               modules=moduledata,
                               dates=datedata)


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

@WiFinderApp.route("/explore2")
def explore2():

    def true_count(a, b, c): return int(bool(a)) + int(bool(b)) + int(bool(c))

    def select_time_value(day, date, hour):
        if true_count(day, date, hour) != 1:
            time_error = "Please choose exactly one time value."
            print(time_error)


        if true_count(day, date, hour) == 1:
                if bool(day) == 1:
                    return "AND strftime('%w', w.Datetime) = {day}".format(day=day)
                if bool(date) == 1:
                    return 'AND w.Datetime = "{date}"'.format(date=date)
                if bool(hour) == 1:
                    return "AND  strftime('%H', w.Time) = {hour}".format(hour=hour)

    def select_filter_value(room, module):
        if true_count(room, module, None) > 1:
            filter_error = "Please choose exactly one filter value."
            print(filter_error)
            return 'ERROR IN FILTER FUNCTION' + str(true_count(room, module, None)) + str(room) + str(module)

        if true_count(room, module, None) == 1:
                if bool(room) == 1:
                    return "AND r.RoomID = '{room}'".format(room=room)
                if bool(module) == 1:
                    return "AND c.Module = {module}".format(module=module)

    def select_y_axis_value(occupancy_requested, count_requested, capacity_requested):

        stem = ''
        if bool(occupancy_requested) == 1:
            stem += 'o.Occupancy' + ', '
        if bool(count_requested) == 1:
            stem += 'w.Log_Count' + ', '
        if bool(capacity_requested) == 1:
            stem += 'r.Capacity'

        if stem.count(",") >= stem.count("."):
            index = stem.rfind(",")
            stem = stem[:index] + stem[index + 1:]

        return stem


    day_dict = {'Monday': 1,
                'Tuesday': 2,
                'Wednesday': 3,
                'Thursday': 4,
                'Friday': 5}

    rooms_available = query("SELECT DISTINCT RoomID FROM ROOM;")
    modules_available = query("SELECT DISTINCT Module FROM CLASS;")
    dates_available = query("SELECT DISTINCT Datetime FROM CLASS;")
    hours_available = query("SELECT DISTINCT Hour FROM CLASS")


    room_value = request.args.get('Room')
    date_value = request.args.get('Date')
    day_value = request.args.get('Day')
    hour_value = request.args.get('Hour')
    module_value = request.args.get('Module')
    occupancy_requested = request.args.get('Occupancy_check')
    capacity_requested = request.args.get('Capacity_check')
    count_requested = request.args.get('Count_check')

    time_value = select_time_value(day_value, date_value, hour_value)
    filter_value = select_filter_value(room_value, module_value)
    yaxis_value = select_y_axis_value(occupancy_requested, count_requested, capacity_requested)

    if true_count(time_value, filter_value, yaxis_value) == 3:
        explore_query = """SELECT {y_axis_selector}
                            FROM WIFI_LOGS w JOIN OCCUPANCY o JOIN ROOM r JOIN CLASS c
                            WHERE o.ClassID = w.ClassID
                            AND c.ClassID = o.ClassID
                            AND r.RoomID = o.Room
                            {time_selector}
                            {filter_selector}
                            """.format(y_axis_selector=yaxis_value,
                                       time_selector=time_value,
                                       filter_selector=filter_value)

        return render_template("explore2.html",
                                rooms=rooms_available,
                                modules=modules_available,
                                dates=dates_available,
                                days=day_dict,
                                hours=hours_available,
                               returned_data=explore_query,
                                which_path=true_count(time_value, filter_value, yaxis_value),
                               values = ['room', room_value,
                                     'module',
                                     module_value,
                                     'date', date_value,
                                     'day', day_value,
                                     'hour', hour_value,
                                    'occupancy', occupancy_requested,
                                     'capacity', capacity_requested,
                                     'count', count_requested,
                                    'time', time_value,
                                     'filter', filter_value,
                                     'yaxis', yaxis_value])

    if 1 <= true_count(time_value, filter_value, yaxis_value) < 3 :
        selection_error = 'Please select one value from each list.'

        return render_template("explore2.html",
                           rooms=rooms_available,
                           modules=modules_available,
                           dates=dates_available,
                           days=day_dict,
                           hours=hours_available,
                            error = selection_error,
                               which_path=true_count(time_value, filter_value, yaxis_value),
                               values = ['room', room_value,
                                     'module',
                                     module_value,
                                     'date', date_value,
                                     'day', day_value,
                                     'hour', hour_value,
                                    'occupancy', occupancy_requested,
                                     'capacity', capacity_requested,
                                     'count', count_requested,
                                    'time', time_value,
                                     'filter', filter_value,
                                     'yaxis', yaxis_value])


    return render_template("explore2.html",
                           rooms=rooms_available,
                           modules=modules_available,
                           dates=dates_available,
                           days=day_dict,
                           hours=hours_available,
                           which_path = true_count(time_value, filter_value, yaxis_value),
                           values = ['room', room_value,
                                     'module',
                                     module_value,
                                     'date', date_value,
                                     'day', day_value,
                                     'hour', hour_value,
                                    'occupancy', occupancy_requested,
                                     'capacity', capacity_requested,
                                     'count', count_requested,
                                    'time', time_value,
                                     'filter', filter_value,
                                     'yaxis', yaxis_value])




@WiFinderApp.route("/layout")
def layout():
    '''load base template - only here to prototype design'''
    return render_template("page_layout.html",
                           title='Layout')

if __name__ == "__main__":
    WiFinderApp.run()
