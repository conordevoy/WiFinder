from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.plotting import figure
import flask
import sqlite3 as lite
from bokeh.charts import Line
import pandas as pd
from bokeh.embed import components
from bokeh.resources import INLINE

output_file("panning.html")




def data_retrieval():
    conn = lite.connect('/Users/shanekenny/PycharmProjects/WiFinder/app/website/WiFinderDBv02.db')

    with conn:
        # create a new plot

        s1= pd.read_sql_query("SELECT Log_Count, Room, Hour, Datetime, Time from WIFI_LOGS Where Room= 'B002' and Hour ='9' ORDER BY Datetime ASC, Time ASC", conn)
        line1 = Line(s1, title="WIfi Logs", legend="top_left", ylabel='Count', xlabel='Time')

        s2 = pd.read_sql_query(
            "SELECT Log_Count, Room, Hour, Datetime, Time from WIFI_LOGS Where Room= 'B002' and Hour ='9' ORDER BY Datetime ASC, Time ASC",
            conn)
        line2 = Line(s2, title="WIfi Logs", legend="top_left", ylabel='Count', xlabel='Time')

        s3 = pd.read_sql_query(
            "SELECT Log_Count, Room, Hour, Datetime, Time from WIFI_LOGS Where Room= 'B002' and Hour ='9' ORDER BY Datetime ASC, Time ASC",
            conn)
        line3 = Line(s3, title="WIfi Logs", legend="top_left", ylabel='Count', xlabel='Time')





        script, div = components(line1,line2, line3)


        return flask.render_template(
            'embed.html',
            script=script,
            div=div,
            js_resources=js_resources,
            css_resources=css_resources,)


data_retrieval()