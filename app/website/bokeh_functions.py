from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure,output_file,show
from bokeh.charts import Scatter, HeatMap, Bar, Histogram
from bokeh.models import LinearAxis, Range1d, ColumnDataSource, HoverTool, Legend
import pandas as pd
from bokeh.layouts import gridplot
import sqlite3
from bokeh.palettes import Oranges9 as palette
from hardwire_models import *
from SQL_queries import *


db = "WiFinderDBv03test.db"

def connectDB():
    '''Connects to an Sqlite3 database'''
    return sqlite3.connect(db, timeout=10)

weekly_occupancy_query = """SELECT AVG(Log_Count) as count, Datetime as date
                                    FROM WIFI_LOGS
                                    WHERE strftime('%W', Datetime) =  strftime('%W', "{date}")
                                    AND strftime('%H', Time) BETWEEN "09" and "17"
                                    AND strftime('%w', Datetime) BETWEEN "1" and "5"
                                    And Room = "{room}"
                                    GROUP BY ClassID
                                    ORDER BY date ASC"""


def hotmap(datetime, room, query):
    """Generates a heatmap bokeh model"""

    #IMPORTANT: this query returns M-F values

    # get a df with date and count values, for a given room and date
    week_counts = pd.read_sql_query(query.format(date=datetime, room=room),
                                       connectDB())

    headcount = list(week_counts['count'])
    headcount = [linear_predictor(x) for x in headcount] # predict on all supplied values

    bins = list(week_counts['count'])
    # bins = [tertiary_classifier(x) for x in bins] # predict on all supplied values
    tert_dictionary = {'Empty': 0, 'Medium': 0.5, 'High': 1} # map to int as only ints can go in heatmap
    # bins = [tert_dictionary[x] for x in bins] # map with listcomp

    # 5 * 9 = 45, so all elements need to have 45 values. Days and hours are just multipled out.
    data = {'days': ['fri']*9 + ['thu']*9 + ['wed']*9 + ['tue']*9 + ['mon']*9,
            'occupancy': headcount,
            'hours': ['9', '10', '11', '12', '13', '14', '15', '16', '17']*5}

    week_counts['headcount'] = week_counts['count'].apply(linear_predictor)
    week_counts['bins'] = week_counts['count'].apply(tertiary_classifier)

    source = ColumnDataSource(ColumnDataSource.from_df(week_counts))


    # hover = HoverTool()
    #
    # tooltips = [("headcount", "@headcount")]
    #
    # tools = [hover]

    # colors = ['#1abc9c', '#ec583a', '#474e5d'] # set colors; currently not shading on continuous features

    hm = HeatMap(data, x='hours', y='days', values='occupancy',
                 title='Occupancy in room over the week'.format(room), stat=None,
                 palette=palette, tools=None,
                 hover_tool=True)

    legend = Legend(location=(0, -30))

    hm.add_layout(legend, 'right')

    all_plots = gridplot([[hm]])

    return all_plots

def simplePlotter(room, datetime, chartpick):

    df_day_counts = pd.read_sql_query(day_count_query.format(date=datetime, room=room),
                                            connectDB())

        # df_day_survey_counts = pd.read_sql_query(day_count_and_survey_query.format(date=datetime, room=room),
        #                                     connectDB())

    if chartpick == 'Histogram':
            plot = Histogram(df_day_counts['count'], title="Counts", bins=10)
    if chartpick == 'Bar':
            plot = Bar(df_day_counts['count'], title="Counts")

    all_plots = gridplot([[plot]])

    return all_plots


def correlatorPlot(datetime, room):

    plot_options = dict(x_axis_type="datetime",\
                            tools='pan, wheel_zoom, box_select,box_zoom,reset,save')

    df_day_survey_counts = pd.read_sql_query(day_count_and_survey_query.format(date=datetime, room=room),
                                        connectDB())

    x = df_day_survey_counts['hour']
    y0 = df_day_survey_counts['count']
    y1 = df_day_survey_counts['survey']

    source = ColumnDataSource(data=dict(x=x, y0=y0, y1=y1))

    brush_occu = figure(**plot_options)
    brush_occu.square('x', 'y0', source=source, color="blue")

    brush_count = figure(**plot_options)
    brush_count.square('x', 'y1', source=source, color="green", alpha=0.5)

    plot = gridplot([[brush_occu, brush_count]])

    return plot