import numpy as np
import pandas as pd
import datetime
import urllib
from bokeh.plotting import figure, output_file, show
import numpy as np

query = ("https://data.lacity.org/resource/mgue-vbsx.json?"
    "$group=date"
    "&call_type_code=507P"
    "&$select=date_trunc_ymd(dispatch_date)%20AS%20date%2C%20count(*)"
    "&$order=date")
raw_data = pd.read_json(query)




TOOLS="crosshair,pan,wheel_zoom,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select"



p = figure(tools=TOOLS)

output_file("test.html", title="color_scatter.py example")