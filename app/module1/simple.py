'''This example demonstrates embedding a standalone Bokeh document
into a simple Flask application, with a basic HTML web form.
To view the example, run:
    python simple.py
in this directory, and navigate to:
    http://localhost:5000
'''
from __future__ import print_function

import flask
import sqlite3 as lite
from bokeh.charts import Line
import pandas as pd
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure,output_file,show
from bokeh.models import LinearAxis, Range1d
from bokeh.layouts import WidgetBox, column
from bokeh.models.widgets.inputs import DatePicker
from bokeh.layouts import layout, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.layouts import gridplot

from bokeh.io import output_file, show, vform


app = flask.Flask(__name__)
@app.route("/")



def data_retrieval():


    conn = lite.connect('/Users/shanekenny/PycharmProjects/WiFinder/app/website/WiFinderDBv02.db')
    with conn:
        datetime = "2015-11-12"
        df = pd.read_sql_query("SELECT W.Log_Count, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy, O.OccID FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON C.ClassID = O.ClassID WHERE R.RoomID = 'B002' AND W.Datetime =\'{}\' GROUP BY W.LogID;".format(datetime), conn)
        # p = figure(width=800, height=250, x_axis_type="datetime")
        # p.line = Line(df, title="WIfi Logs", ylabel='Count', xlabel='Time',index='W.Datetime', legend=True)

        df['Time'] = df['Time'].apply(pd.to_datetime)
        p = figure(width=800, height=250, x_axis_type="datetime", )
        p.extra_y_ranges = {"foo": Range1d(start=0, end=1)}

        p.line(df['Time'], df['Log_Count'],  color='red',legend='Log Count')
        p.line(df['Time'], df['Reg_Students'], color='green',legend='Registered Students')
        p.line(df['Time'], df['Capacity'], color='blue', legend='Capacity')
        p.line(df['Time'], df['Occupancy']*100, color='orange', legend='Occupancy')

        p.add_layout(LinearAxis(y_range_name="foo"), 'left')

        # picker_start = "2015-11-03"
        # picker_end = '2015-11-13'
        # slider = DatePicker(title="Date:", min_date=picker_start, max_date=picker_end, value=picker_start)
        slider = Slider(start=0, end=10, value=1, step=.1, title="Stuff")

        controls = [slider]


        sizing_mode = 'fixed'
        inputs = widgetbox(*controls, sizing_mode=sizing_mode)

        layoutss = widgetbox(slider)

        r = layout([[p, layoutss]], sizing_mode='stretch_both')


        script, div = components(r)

        return flask.render_template('explore.html', script=script,
                                     div=div,
                                     )











if __name__ == "__main__":
    print(__doc__)
    app.run()