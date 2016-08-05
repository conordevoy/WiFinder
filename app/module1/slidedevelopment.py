from __future__ import print_function

import flask
import sqlite3 as sql
import pandas as pd
from bokeh.plotting import figure,output_server,show
from bokeh.models import LinearAxis, Range1d
from bokeh.io import curdoc
from bokeh.layouts import layout, widgetbox
import pandas.io.sql as psql
from bokeh.models.widgets.inputs import DatePicker
from bokeh.models import ColumnDataSource, HoverTool, Div

db = '/Users/shanekenny/PycharmProjects/WiFinder/app/website/WiFinderDBv02.db'
conn = sql.connect(db)
query = "SELECT W.Log_Count, W.Time, W.Hour, W.Datetime, R.RoomID, R.Capacity, C.ClassID, C.Module, C.Reg_Students, O.Occupancy, O.OccID FROM WIFI_LOGS W JOIN CLASS C ON W.ClassID = C.ClassID JOIN ROOM R ON C.Room = R.RoomID JOIN OCCUPANCY O ON C.ClassID = O.ClassID WHERE R.RoomID = 'B002'  GROUP BY W.LogID;"
movies = psql.read_sql(query, conn)

start = "2015-11-04"
end = '2015-11-17'
reviews = DatePicker(title="Date:", min_date=start, max_date = end, value=start)



source = ColumnDataSource(data=dict(Log_Count=[], Time=[], Hour=[], Datetime=[], RoomID=[], Capacity=[], ClassID=[], Module=[], Reg_Students=[], Occupancy=[], OccID=[]))


p = figure(width=800, height=250, x_axis_type="datetime")
p.line("Time", "Log_Count",source=source, color='red', legend='Log Count')
print(source)

output_server("hover")

def select_day():

    movies['Time'] = movies['Time'].apply(pd.to_datetime)
    movies['Datetime'] = movies['Datetime'].apply(pd.to_datetime)






    selected=movies[movies.Datetime==reviews.value]


    return selected



def update():
    df = select_day()


    p.title.text = "%d movies selected" % len(df)
    source.data = dict(Log_Count=df['Log_Count'],
                       Time=df['Time'],
                       Hour=df['Hour'],
                       Datetime=df['Datetime'],
                       RoomID=df['RoomID'],
                       Capacity=df['Capacity'],
                       ClassID=df['ClassID'],
                       Module=df['Module'],
                       Reg_Students=df['Reg_Students'],
                       Occupancy=df['Occupancy'],
                       OccID=df['OccID']

                       )




# Controller Listeners
controls = [reviews]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([

    [inputs, p],
], sizing_mode=sizing_mode)

update()

# Output
curdoc().add_root(l)
curdoc().title = "trends"

