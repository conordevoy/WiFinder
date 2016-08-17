from flask import Flask, render_template, g, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3
from hardwire_models import *
from werkzeug import secure_filename
import os
from datetime import datetime

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure,output_file,show
from bokeh.charts import Scatter, HeatMap
from bokeh.models import LinearAxis, Range1d, ColumnDataSource, HoverTool
import pandas as pd
from bokeh.layouts import gridplot
from SQL_queries import *
from bokeh_functions import *

WiFinderApp = Flask(__name__, static_url_path="/static")

WiFinderApp.debug = True

WiFinderApp.secret_key = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8b\x0c\x9f'  # session key random generated from os

db = "WiFinderDBv03test.db"

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
    return sqlite3.connect(db, timeout=10)


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
        for user in user_exists:
          # print(user[1])
          # print(user[2])
          if request.form['password'] != user[2]:
              flash('Invalid Credentials. Please try again.')
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
@WiFinderApp.route("/exploreview")
@login_required
def view():
    '''load explore base page'''
    return render_template("exploreview.html",
                           title='Home')
@WiFinderApp.route("/")
@login_required
def WiFinderHTML():
    '''Render HTML template'''
    return redirect(url_for('login'))



@WiFinderApp.route("/register")
def register():
    '''registration page for website'''
    # unique= query("SELECT DISTINCT username FROM User;")
    return render_template("register.html",
                           title='Registration')



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

    if room != 'default' and time != 'default' and datetime != 'default' and room != None and time != None and datetime != None:
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
    elif room == None and time == None and datetime == None:
        pass
    else:
        flash('You need to input all three values')

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

@WiFinderApp.route("/evaluator")
def evaluator():
    '''returns appraisal data for rooms'''

    roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")

    # Gives the average occupancy of all survey data for that room
    average_room_occupancy_query = '''
                                SELECT AVG(Occupancy)
                                FROM OCCUPANCY
                                WHERE Room = "{}"
                                '''
    # gives the avg occupancy of survey data, discounting the 0's
    # this how the CSI do it.
    CSI_average_room_occupancy_query = '''
                                SELECT AVG(Occupancy)
                                FROM OCCUPANCY
                                WHERE Room = "{}"
                                AND Occupancy > 0
                                '''


    average_connections_query = '''
                                Select AVG(Log_Count)
                                From WIFI_LOGS
                                Where Hour BETWEEN "9" and "17"
                                AND strftime('%w', Datetime) BETWEEN "1" and "5"
                                And Room = "{}"
                                '''

    base_rate_query = '''
                    SELECT COUNT(Occupancy)
                    from Occupancy o
                    where Room = "{}"
                    '''

    unused_rate_query = '''
                    SELECT COUNT(case when o.Occupancy  =  0 then 1 else NULL end) as unused
                    from Occupancy o
                    where Room = "{}"
                    '''

    room_evaluation = []
    headings = ['Room', 'Average Occupancy', 'Average Frequency of Use',\
                'Average Utilisation', 'Average Connections', 'Rating']

    roomdata = ['B002', 'B003', 'B004']

    for room in roomdata:

        name = room
        average_count = query(average_connections_query.format(room)).fetchone()[0]
        average_occupancy = query(average_room_occupancy_query.format(room)).fetchone()[0]
        number_of_slots = query(base_rate_query.format(room)).fetchone()[0]
        unused_slots = query(unused_rate_query.format(room)).fetchone()[0]

        frequency_of_use = int(((unused_slots/number_of_slots) -1) * -100)
        average_occupancy = int(average_occupancy * 100)
        average_count = int(average_count)
        utilisation = (average_occupancy * frequency_of_use) / 100

        def rating(frequency):

            if frequency < 49:
                return 'Poor'
            elif frequency > 59:
                return 'Good'
            elif 49 <= frequency <= 59:
                return 'Fair'
            else:
                return 'Error: Did not match frequency rating.'

        def add_percent_sign(int): return str(int) + '%'

        # the add % for frequency is placed in metrics to avoid conflict with the 'rating' function
        # trips error due to comparison with string. e.g. '34%' < 49
        average_occupancy = add_percent_sign(average_occupancy)
        average_count = add_percent_sign(average_count)
        utilisation = add_percent_sign(utilisation)

        rating = rating(frequency_of_use)

        metrics = [name, average_occupancy, add_percent_sign(frequency_of_use), utilisation, average_count, rating]

        room_evaluation.append(metrics)


    return render_template("evaluator.html",
                               title='Estimations',
                               rooms=room_evaluation,
                                headings=headings)



@WiFinderApp.route("/lectureinput", methods=['GET'])
@login_required
def input():
    '''page for lecturers to upload a survey form'''
    timeinput = query("SELECT DISTINCT Hour FROM CLASS;")
    roominput = query("SELECT DISTINCT RoomID FROM ROOM;")
    moduleinput = query("SELECT DISTINCT Module FROM CLASS;")

    room = request.args.get('Room')
    time = request.args.get('Time')
    date = datetime.now().strftime("%Y-%m-%d")
    occupancy = request.args.get('Occupancy')
    print(room, time, date, occupancy)

    if room != 'default' and time != 'default' and occupancy != 'default' and room != None and time != None and occupancy != None:
        classID = (time+date+room)
        print(classID)
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO OCCUPANCY (Hour, Datetime, Room, Occupancy, ClassID)
            VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')
            ;""".format(time, date, room, occupancy, classID))
        conn.commit()
        flash("Upload Successful!")
    elif room == None and time == None and occupancy == None:
        pass
    else:
        flash('You need to input all three values')
    return render_template("lectureinput.html",
                           title='Home',
                           rooms_input=roominput,
                           times_input=timeinput,
                           modules_input=moduleinput)

@WiFinderApp.route("/correlation")
def correlator_plot():

    roomdata = query(get_all_rooms)
    datedata = query(get_all_dates)

    # get values from form
    room = request.args.get('Room')
    datetime = request.args.get('Date')

    if room and datetime:
        plot = correlatorPlot(datetime, room)
        script, div = components(plot)
        # error = None

        return render_template(
            'explore_correlation.html',
            script=script,
            div=div,
            # error=error,
            rooms=roomdata,
            dates=datedata
                )
    else:
        return render_template("explore_correlation.html",
                               title='Estimations',
                               rooms=roomdata,
                               dates=datedata,
                               )


@WiFinderApp.route("/simple")
def simple_mapper():
    '''allows for mutliple easy to read charts to be rendered'''

    roomdata = query(get_all_rooms)
    datedata = query(get_all_dates)
    chartdata = ['Histogram', 'Bar']

    # get values from form
    room = request.args.get('Room')
    datetime = request.args.get('Date')
    chartpick = request.args.get('Chart')

    if room and datetime:
        plot = simplePlotter(room, datetime, chartpick)
        script, div = components(plot)
        # error= chartpick

        return render_template(
            'explore_simple.html',
            script=script,
            div=div,
            # error=error,
            rooms=roomdata,
            dates=datedata,
            charts=chartdata
            )
    else:
        return render_template("explore_simple.html",
                               title='Estimations',
                               rooms=roomdata,
                               dates=datedata,
                               charts=chartdata
                               )

@WiFinderApp.route("/heatmap", methods=['GET', 'POST'])
def heatmap():

    roomdata = query(get_all_rooms)
    datedata = query(get_all_dates)

    # get values from form
    room = request.args.get('Room')
    datetime = request.args.get('Date')

    if room and datetime:
        plot = hotmap(datetime, room, weekly_occupancy_query)
        script, div = components(plot)
        # error = "Hi, I'm bokeh!"

        return render_template(
            'explore_heatmap.html',
            script=script,
            div=div,
            # error=error,
            rooms=roomdata,
            dates=datedata
            )
    else:
        return render_template("explore_heatmap.html",
                               title='Estimations',
                               rooms=roomdata,
                               dates=datedata)



# @WiFinderApp.route("/explore2")
# def explore2():
#
#     def true_count(a, b, c): return int(bool(a)) + int(bool(b)) + int(bool(c))
#
#     def select_time_value(day, date, hour):
#         if true_count(day, date, hour) != 1:
#             time_error = "Please choose exactly one time value."
#             print(time_error)
#
#
#         if true_count(day, date, hour) == 1:
#                 if bool(day) == 1:
#                     return 'AND strftime("%w", w.Datetime) = "{day}"'.format(day=day_dict[day])
#                 if bool(date) == 1:
#                     return 'AND w.Datetime = "{date}"'.format(date=date)
#                 if bool(hour) == 1:
#                     return 'AND  strftime("%H", w.Time) = "{hour}"'.format(hour=hour)
#
#     def select_filter_value(room, module):
#         if true_count(room, module, None) > 1:
#             filter_error = "Please choose exactly one filter value."
#             print(filter_error)
#             return 'ERROR IN FILTER FUNCTION' + str(true_count(room, module, None)) + str(room) + str(module)
#
#         if true_count(room, module, None) == 1:
#                 if bool(room) == 1:
#                     return 'AND r.RoomID = "{room}"'.format(room=room)
#                 if bool(module) == 1:
#                     return 'AND c.Module = "{module}"'.format(module=module)
#
#     def select_y_axis_value(occupancy_requested, count_requested, capacity_requested):
#
#         stem = ''
#         if bool(occupancy_requested) == 1:
#             stem += 'o.Occupancy' + ', '
#         if bool(count_requested) == 1:
#             stem += 'w.Log_Count' + ', '
#         if bool(capacity_requested) == 1:
#             stem += 'r.Capacity'
#
#         if stem.count(",") >= stem.count("."):
#             index = stem.rfind(",")
#             stem = stem[:index] + stem[index + 1:]
#
#         return stem
#
#
#     day_dict = {'Monday': 1,
#                 'Tuesday': 2,
#                 'Wednesday': 3,
#                 'Thursday': 4,
#                 'Friday': 5}
#
#     rooms_available = query("SELECT DISTINCT RoomID FROM ROOM;")
#     modules_available = query("SELECT DISTINCT Module FROM CLASS;")
#     dates_available = query("SELECT DISTINCT Datetime FROM CLASS;")
#     hours_available = query("SELECT DISTINCT Hour FROM CLASS")
#
#
#     room_value = request.args.get('Room')
#     date_value = request.args.get('Date')
#     day_value = request.args.get('Day')
#     hour_value = request.args.get('Hour')
#     module_value = request.args.get('Module')
#     occupancy_requested = request.args.get('Occupancy_check')
#     capacity_requested = request.args.get('Capacity_check')
#     count_requested = request.args.get('Count_check')
#
#     time_value = select_time_value(day_value, date_value, hour_value)
#     filter_value = select_filter_value(room_value, module_value)
#     yaxis_value = select_y_axis_value(occupancy_requested, count_requested, capacity_requested)
#
#     if true_count(time_value, filter_value, yaxis_value) == 3:
#         df = pd.read_sql_query("""SELECT {y_axis_selector}
#                             FROM WIFI_LOGS w JOIN OCCUPANCY o JOIN ROOM r JOIN CLASS c
#                             WHERE o.ClassID = w.ClassID
#                             AND c.ClassID = o.ClassID
#                             AND r.RoomID = o.Room
#                             {time_selector}
#                             {filter_selector}
#                             """.format(y_axis_selector=yaxis_value,
#                                        time_selector=time_value,
#                                        filter_selector=filter_value),
#                             connectDB())
#
#         query_string = ("""SELECT {y_axis_selector}
#                             FROM WIFI_LOGS w JOIN OCCUPANCY o JOIN ROOM r JOIN CLASS c
#                             WHERE o.ClassID = w.ClassID
#                             AND c.ClassID = o.ClassID
#                             AND r.RoomID = o.Room
#                             {time_selector}
#                             {filter_selector}
#                             """.format(y_axis_selector=yaxis_value,
#                                        time_selector=time_value,
#                                        filter_selector=filter_value))
#
#         # this is the bokeh: bokeh forever!
#
#         # p = Scatter(df, x='Occupancy', y='Log_Count')
#         # script, div = components(p)
#
#         return render_template("explore2.html",
#                                 rooms=rooms_available,
#                                 modules=modules_available,
#                                 dates=dates_available,
#                                 days=day_dict,
#                                 hours=hours_available,
#                                #  script=script,
#                                # div=div,
#                                error=query_string
#                                )
#
#     if 1 <= true_count(time_value, filter_value, yaxis_value) < 3 :
#         selection_error = 'Please select one value from each list.'
#
#         return render_template("explore2.html",
#                            rooms=rooms_available,
#                            modules=modules_available,
#                            dates=dates_available,
#                            days=day_dict,
#                            hours=hours_available,
#                             error = selection_error,
#                                which_path=true_count(time_value, filter_value, yaxis_value),
#                                values = ['room', room_value,
#                                      'module',
#                                      module_value,
#                                      'date', date_value,
#                                      'day', day_value,
#                                      'hour', hour_value,
#                                     'occupancy', occupancy_requested,
#                                      'capacity', capacity_requested,
#                                      'count', count_requested,
#                                     'time', time_value,
#                                      'filter', filter_value,
#                                      'yaxis', yaxis_value])
#
#
#     return render_template("explore2.html",
#                            rooms=rooms_available,
#                            modules=modules_available,
#                            dates=dates_available,
#                            days=day_dict,
#                            hours=hours_available,
#                            which_path = true_count(time_value, filter_value, yaxis_value),
#                            values = ['room', room_value,
#                                      'module',
#                                      module_value,
#                                      'date', date_value,
#                                      'day', day_value,
#                                      'hour', hour_value,
#                                     'occupancy', occupancy_requested,
#                                      'capacity', capacity_requested,
#                                      'count', count_requested,
#                                     'time', time_value,
#                                      'filter', filter_value,
#                                      'yaxis', yaxis_value])
#
# @WiFinderApp.route("/explore")
# @login_required
# def exploredemo():
#     '''search page for website'''
#     timedata = query("SELECT DISTINCT Hour FROM CLASS;")
#     roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
#     moduledata = query("SELECT DISTINCT Module FROM CLASS;")
#     datedata = query("SELECT DISTINCT Datetime FROM CLASS;")
#
#     # get values from form
#     room = request.args.get('Room')
#     datetime = request.args.get('Date')
#     time = request.args.get('Time')
#
#     df = pd.read_sql_query(
#         "SELECT W.Log_Count, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy, O.OccID FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON C.ClassID = O.ClassID WHERE R.RoomID = \'{}\' AND W.Datetime =\'{}\' GROUP BY W.LogID;".format(
#             room, datetime), connectDB())
#
#     df['Time'] = df['Time'].apply(pd.to_datetime)
#
#     if room and datetime:
#
#         # figure 1: all lines on one line
#
#         p = figure(width=900, height=500, x_axis_type="datetime", title='Occupancy, Count, Capacity & Students vs. Time')
#         p.extra_y_ranges = {"foo": Range1d(start=0, end=1)}
#
#         p.line(df['Time'], df['Log_Count'], color='red', legend='Log Count')
#         p.line(df['Time'], df['Reg_Students'], color='green', legend='Registered Students')
#         p.line(df['Time'], df['Capacity'], color='blue', legend='Capacity')
#         p.line(df['Time'], df['Occupancy'] * 100, color='orange', legend='Occupancy')
#
#         p.add_layout(LinearAxis(y_range_name="foo"), 'left')
#
#
#
#         script, div = components(p)
#
#         # figure 2: occupancy and count on separate figures
#         # linked panning
#         # color
#
#         plot_options = dict(width=500, plot_height=500, x_axis_type="datetime",\
#                             tools='pan, wheel_zoom, box_select,box_zoom,reset,save')
#
#         linked_occu = figure(**plot_options)
#         linked_occu.circle(x=df['Time'], y=df['Occupancy'], color="red")
#
#         linked_count = figure(x_range=linked_occu.x_range, **plot_options)
#         linked_count.circle(x=df['Time'], y=df['Log_Count'], color='orange')
#
#         linked_pan_gridplot = gridplot([[linked_occu, linked_count]])
#
#         # script2, div2 = components(linked_pan_gridplot)
#
#         # script, div = components(linked_pan_gridplot)
#
#         # figure 3 - sharing data between two graphs
#
#         x = df['Time']
#         y0 = df['Occupancy']
#         y1 = df['Log_Count']
#
#         source = ColumnDataSource(data=dict(x=x, y0=y0, y1=y1))
#
#         brush_occu = figure(**plot_options)
#         brush_occu.square('x', 'y0', source=source, color="blue")
#
#         brush_count = figure(**plot_options)
#         brush_count.square('x', 'y1', source=source, color="green", alpha=0.5)
#
#         brush_pan_gridplot = gridplot([[brush_occu, brush_count]])
#
#         # script3, div3 = components(brush_pan_gridplot)
#
#         # script, div = components(brush_pan_gridplot)
#
#         linked_occu.yaxis.axis_label = 'Occupancy'
#         linked_count.yaxis.axis_label = 'Count'
#         brush_occu.yaxis.axis_label = 'Occupancy'
#         brush_count.yaxis.axis_label = 'Count'
#
#         # hover tool example
#
#         # hover_fig = figure(**plot_options, title='Hover-hand')
#         # hover_fig.line(df['Time'], df['Log_Count'], color='black', legend='Log Count', line_dash="5 5",\
#         #                line_width=2)
#         #
#         # hoverer = hover_fig.circle(x, y1,\
#         #                            fill_color='grey', hover_fill_color='orange',\
#         #                            fill_alpha=0.05, hover_alpha=0.04,\
#         #                            line_color=None, hover_line_color="white")
#         #
#         # hover_fig.add_tools(HoverTool(tooltips=None, renderers=[hoverer], mode='hline'))
#
#         # (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
#
#         #inputs needed
#         # need to know what days there are: could be hardcoded?
#         # hours could be hardcoded
#         # occupancy: can take the tertiary prediction or headcount
#         # list comprehensions?
#         # so, return the count for each day, list comprehend that and show the predicted occupancy
#         # NEED: sqlquery which will return all data for the week surrounding a given date.
#
#         weekly_occupancy_query = """SELECT AVG(Log_Count) as count, Datetime as date
#                                     FROM WIFI_LOGS
#                                     WHERE strftime('%W', Datetime) =  strftime('%W', "{date}")
#                                     AND strftime('%H', Time) BETWEEN "09" and "17"
#                                     AND strftime('%w', Datetime) BETWEEN "1" and "5"
#                                     And Room = "{room}"
#                                     GROUP BY ClassID
#                                     ORDER BY date ASC"""
#         #IMPORTANT: this query returns M-F values
#
#         # get a df with date and count values, for a given room and date
#         week_counts = pd.read_sql_query(weekly_occupancy_query.format(date=datetime, room=room),
#                                            connectDB())
#
#         headcount = list(week_counts['count'])
#         headcount = [linear_predictor(x) for x in headcount] # predict on all supplied values
#
#         bins = list(week_counts['count'])
#         bins = [tertiary_classifier(x) for x in bins] # predict on all supplied values
#         tert_dictionary = {'Empty': 0, 'Medium': 0.5, 'High': 1} # map to int as only ints can go in heatmap
#         bins = [tert_dictionary[x] for x in bins] # map with listcomp
#
#         # 5 * 9 = 45, so all elements need to have 45 values. Days and hours are just multipled out.
#         data = {'days': ['fri']*9 + ['thu']*9 + ['wed']*9 + ['tue']*9 + ['mon']*9,
#                 'occupancy': headcount,
#                 'hours': ['9', '10', '11', '12', '13', '14', '15', '16', '17']*5}
#
#         colors = ['#1abc9c', '#ec583a', '#474e5d'] # set colors; currently not shading on continuous features
#
#         hm = HeatMap(data, x='hours', y='days', values='occupancy',
#                      title='Occupancy in {} over the week'.format(room), stat=None,
#                      color=colors, tools=None)
#
#
#         # all_plots = gridplot([[p], [linked_occu, linked_count], [brush_occu, brush_count]])
#         all_plots = gridplot([[hm]])
#
#         script, div = components(all_plots)
#
#         return render_template(
#             'explore.html',
#             script=script,
#             div=div,
#             error=bins,
#             rooms=roomdata,
#             times=timedata,
#             modules=moduledata,
#             dates=datedata
#         )
#
#     else:
#         return render_template("explore.html",
#                                title='Estimations',
#                                rooms=roomdata,
#                                times=timedata,
#                                modules=moduledata,
#                                dates=datedata)


# @WiFinderApp.route("/heatmapplot", methods=['GET', 'POST'])
# def heatmapper():
#
#     roomdata = query(get_all_rooms)
#     datedata = query(get_all_dates)
#
#     # get values from form
#     room = request.args.get('Room')
#     datetime = request.args.get('Date')
#
#     if room and datetime:
#         plot = hotmap(datetime, room, weekly_occupancy_query)
#         script, div = components(plot)
#         error = "Hi, I'm bokeh!"
#
#         return render_template(
#             'explore_heatmap.html',
#             script=script,
#             div=div,
#             error=error,
#             rooms=roomdata,
#             dates=datedata
#             )
#     else:
#         return render_template("explore_heatmap.html",
#                                title='Estimations',
#                                rooms=roomdata,
#                                dates=datedata)

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

# @WiFinderApp.route("/exploreold")
# @login_required
# def explore():
#     '''explore page for website'''
#     timedata = query("SELECT DISTINCT Hour FROM CLASS;")
#     roomdata = query("SELECT DISTINCT RoomID FROM ROOM;")
#     moduledata = query("SELECT DISTINCT Module FROM CLASS;")
#     datedata = query("SELECT DISTINCT Datetime FROM CLASS;")
#
#     # get values from form
#     room = request.args.get('Room')
#     datetime = request.args.get('Date')
#     time = request.args.get('Time')
#
#     df = pd.read_sql_query(
#         "SELECT W.Log_Count, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy, O.OccID FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON C.ClassID = O.ClassID WHERE R.RoomID = \'{}\' AND W.Datetime =\'{}\' GROUP BY W.LogID;".format(
#             room, datetime), connectDB())
#
#     df['Time'] = df['Time'].apply(pd.to_datetime)
#
#     if room and datetime:
#         p = figure(width=800, height=500, x_axis_type="datetime", )
#         p.extra_y_ranges = {"foo": Range1d(start=0, end=1)}
#
#         p.line(df['Time'], df['Log_Count'], color='red', legend='Log Count')
#         p.line(df['Time'], df['Reg_Students'], color='green', legend='Registered Students')
#         p.line(df['Time'], df['Capacity'], color='blue', legend='Capacity')
#         p.line(df['Time'], df['Occupancy'] * 100, color='orange', legend='Occupancy')
#
#         p.add_layout(LinearAxis(y_range_name="foo"), 'left')
#
#         print(df.head(5))
#
#         script, div = components(p)
#         return render_template(
#             'explore.html',
#             script=script,
#             div=div,
#             rooms=roomdata,
#             times=timedata,
#             modules=moduledata,
#             dates=datedata
#         )
#     # else:
#     #     df = pd.read_sql_query(
#     #         "SELECT W.Log_Count, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy, O.OccID FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON C.ClassID = O.ClassID WHERE R.RoomID = 'B002' AND W.Datetime = '2015-11-12' GROUP BY W.LogID;",
#     #         connectDB())
#
#
#     #     df['Time'] = df['Time'].apply(pd.to_datetime)
#     #     p = figure(width=800, height=250, x_axis_type="datetime", )
#     #     p.extra_y_ranges = {"foo": Range1d(start=0, end=1)}
#
#     #     p.line(df['Time'], df['Log_Count'], color='red', legend='Log Count')
#     #     p.line(df['Time'], df['Reg_Students'], color='green', legend='Registered Students')
#     #     p.line(df['Time'], df['Capacity'], color='blue', legend='Capacity')
#     #     p.line(df['Time'], df['Occupancy'] * 100, color='orange', legend='Occupancy')
#
#     #     p.add_layout(LinearAxis(y_range_name="foo"), 'left')
#
#     #     p2 = figure(width=800, height=250, x_axis_type="datetime", x_range=p.x_range, )
#     #     p2.line(df['Time'], df['Log_Count'], color='red', legend='Log Count')
#
#     #     r = gridplot([[p, p2]], toolbar_location=None)
#
#     #     script, div = components(r)
#     #     return render_template(
#     #         'explore.html',
#     #         script=script,
#     #         div=div,
#     #         rooms=roomdata,
#     #         times=timedata,
#     #         modules=moduledata,
#     #         dates=datedata
#     #     )
#     return render_template('explore.html',
#                           rooms=roomdata,
#                           times=timedata,
#                           dates=datedata)

# @WiFinderApp.route("/modelupdated", methods=['GET'])
# @login_required
# def model_updated():
#
#
#     import Linear_Regression_Creator
#     import Logistic_Regression_Creator
#
#     return render_template("model_updated.html")

if __name__ == "__main__":
    WiFinderApp.run()

