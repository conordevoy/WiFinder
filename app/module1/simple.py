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

app = flask.Flask(__name__)



@app.route("/")



def data_retrieval():


    conn = lite.connect('/Users/shanekenny/PycharmProjects/WiFinder/app/website/WiFinderDBv02.db')
    with conn:
        df = pd.read_sql_query("SELECT Log_Count, Room, Hour, Datetime, Time from WIFI_LOGS Where Room= 'B002' and Hour ='9' ORDER BY Datetime ASC, Time ASC", conn)

        line = Line(df, title="WIfi Logs", legend="top_left", ylabel='Count', xlabel='Time')

        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        script, div = components(line)
        return flask.render_template(
            'embed.html',
            script=script,
            div=div,
            js_resources=js_resources,
            css_resources=css_resources,)











if __name__ == "__main__":
    print(__doc__)
    app.run()