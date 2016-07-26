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
from bokeh.charts import Line, output_file, show
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = flask.Flask(__name__)

colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route("/")



def data_retrieval():
    """
        Fucntion that queries database

    :return:
    """

    # Grab the inputs arguments from the URL
    # This is automated by the button
#  args = flask.request.args         for when we want arguments input from url

    # Connect to database

    conn = lite.connect('/Users/shanekenny/PycharmProjects/WiFinder/app/website/WiFinderDBv02.db')
    with conn:
        df = pd.read_sql_query("SELECT Log_Count, Room, Hour, Datetime, Time from WIFI_LOGS Where Room= 'B002' and Hour ='9' ORDER BY Datetime ASC, Time ASC", conn)

        # verify that result of SQL query is stored in the dataframe
        print(df.head())
        line = Line(df, title="WIfi Logs", legend="top_left", ylabel='Count', xlabel='Time')
        output_file("line.html")

        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()

        # For more details see:
        #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
        script, div = components(line, INLINE)
        html = flask.render_template(
            'embed.html',
            plot_script=script,
            plot_div=div,
            js_resources=js_resources,
            css_resources=css_resources,

        )
        return encode_utf8(html)









if __name__ == "__main__":
    print(__doc__)
    app.run()