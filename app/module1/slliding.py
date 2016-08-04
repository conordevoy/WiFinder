from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show

output_file("callback.html")


start = "2015-11-03"
end = '2015-11-17'
reviews = DatePicker(title="Period:", min_date=start, max_date = end, value=start)


source=  ColumnDataSource(data(dict(
    Log_Count=df[],
    y=df[y_name],
    color=df["color"],
    title=df["Title"],
    year=df["Year"],
    revenue=df["revenue"],
    alpha=df["alpha"],
)




plot = Figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

callback = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var f = cb_obj.get('value')
        x = data['x']
        y = data['y']
        for (i = 0; i < x.length; i++) {
            y[i] = Math.pow(x[i], f)
        }
        source.trigger('change');
    """)

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power", callback=callback)

layout = column(slider, plot)

show(layout)