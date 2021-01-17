#Load the packages
import pandas as pd
from bokeh.embed import components 
from bokeh.models import HoverTool
import os 
import geopandas as gpd
import os 
import geopandas as gpd
import pandas as pd
import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer, Category20, Turbo256
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.plotting import figure, curdoc


#os.chdir(r"C:\Users\Afify\Downloads\Heatmap_App") 
df = pd.read_csv('myapp/data/stations.csv')
fp = 'myapp/data/stationsI35_Merge2.shp'
map_df = gpd.read_file(fp)
merged = map_df.set_index('Name').join(df.set_index('codes'))
merged.reset_index(level=0, inplace=True)
merged1 = merged.loc[~merged['NAME_0'].isin(['United States'])]
geosource = GeoJSONDataSource(geojson = merged.to_json())
geosource1 = GeoJSONDataSource(geojson = merged1.to_json())


# Define color palettes
palette = Turbo256 
# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40, nan_color = 'dimgray')
# Define custom tick labels for color bar.
tick_labels = {'10': '15', '15':'20','20':'25','30':'30+'}
# Create color bar.
color_bar = ColorBar(color_mapper = color_mapper, 
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal',
                     major_label_overrides = tick_labels)
# Create figure object.
p = figure(title = 'Surface Temperature of I-35 on Dec 14 at 6 AM', 
           plot_height = 600, plot_width = 950, 
           toolbar_location = 'below',
           tools = 'pan, wheel_zoom, box_zoom, reset')
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
# Add patch renderer to figure.
states = p.patches('xs','ys', source = geosource,
                   fill_color = {'field' :'temp',
                                 'transform' : color_mapper},
                   line_color = 'grey', 
                   line_width = 0.8, 
                   fill_alpha = 0.5)
states1 = p.patches('xs','ys', source = geosource1,
                    fill_color = {'field' :'temp',
                                  'transform' : color_mapper},
                    line_color = 'grey', 
                    line_width = 0.8, 
                    fill_alpha = 0.5)
# Create hover tool
p.add_tools(HoverTool(renderers = [states1],
                      tooltips = [('station','@index'),
                                  ('temp','@temp')]))
# Specify layout
p.add_layout(color_bar, 'below')
p.axis.visible = False


# This final command is required to launch the plot in the browser
curdoc().add_root(column(p))
