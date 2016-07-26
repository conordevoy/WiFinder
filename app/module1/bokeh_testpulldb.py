import numpy as np
import pandas as pd
import datetime
import urllib
from bokeh.plotting import figure, output_file, show
import numpy as np
import sqlite3 as lite
from bokeh.charts import Line, output_file, show


def data_retrieval():
    """
        Fucntion that queries database

    :return:
    """
    # Connect to database

    conn = lite.connect('/Users/shanekenny/PycharmProjects/WiFinder/app/website/WiFinderDBv02.db')
    with conn:
        df = pd.read_sql_query("SELECT Log_Count, Room, Hour, Datetime, Time from WIFI_LOGS Where Room= 'B002' and Hour ='9' ORDER BY Datetime ASC, Time ASC", conn)

        # verify that result of SQL query is stored in the dataframe
        print(df.head())
        return df




classdata = data_retrieval() # in this iteration
classdata.dtypes


line = Line(classdata, title="WIfi Logs", legend="top_left", ylabel='Count', xlabel='Time')
output_file("line.html")

show (line)