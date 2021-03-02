import numpy as np 
from flask import Flask, request, render_template, abort, Response
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go
import json
import pandas as pd
from bokeh.embed import components 
from bokeh.models import HoverTool
import geopandas as gpd
import os 
import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.plotting import figure, curdoc
import requests
import statistics 
from datetime import date, datetime
from pytz import timezone
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer, Category20, Turbo256
from bokeh.plotting import figure
from bokeh.models import FixedTicker
from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs
from bokeh.sampledata.autompg import autompg as df

app = Flask(__name__)

@app.route('/')
def index():
    tz = timezone('US/Central')
    tz1 = timezone('US/Mountain')
    time = datetime.now(tz)
    time1 = datetime.now(tz1)
    t = time.strftime("%Y-%m-%d")
    t1 = time.strftime("%H:%M:%S")
    t2 = time1.strftime("%Y-%m-%d")
    t3 = time1.strftime("%H:%M:%S")
    comma = ' '
    S1 = 'https://rwis.tulsa.ou.edu/rwis/api/weatherAll/data?station='
    P1= '&datetime_from='
    P2 = '&datetime_to='
    st = ['35ST213','35ST199','35ST187','35ST165','35ST154','35ST141','35ST235','35ST107','35ST092','35ST074','35ST058','35ST051','35ST032',
          '35ST015','35ST001']
    st_n = ['213 - Road','213 - Bridge','199 - Road','199 - Bridge','187 - Road','187 - Bridge','165 - Road','165 - Bridge','154 - Road','154 - Bridge'
            ,'141 - Road','141 - Bridge','235 - Road','235 - Bridge','107 - Road','107 - Bridge','92 - Road','92 - Bridge',
            '74 - Road','74 - Bridge','58 - Road','58 - Bridge','51 - Road','51 - Bridge','32 - Road','32 - Bridge',
            '15 - Road','15 - Bridge','1 - Road','1 - Bridge']
    temp1 = []
    
    for x in range(len(st)):
        
        #print(x)
        temp1_surface_temperature = []
        time_now = []
        temp2_surface_temperature = []
        total_msg = ("".join([S1,st[x],P1,t2,comma,t3,P2,t,comma,t1]))
        data = requests.get(total_msg).json()
       
        
        if not data: 
            temp = temp1[-1]
            tempp = temp1[-2]
            temp1.append(tempp)
            temp1.append(temp)
        else:
            time_now.append(data[0]['date_time'])
            n= len(data)
            for i in range(n):
                temp1_surface_temperature.append(data[i]['temp1_surface_temperature'])
                Not_none_values = filter(None.__ne__, temp1_surface_temperature)
                temp1_surface_temperature = list(Not_none_values)
                #print(temp1_surface_temperature)
            if not temp1_surface_temperature: 
                temp = temp1[-1]
                temp1.append(temp)
            else:
                temp1.append(statistics.mean(temp1_surface_temperature))
                #print(temp1)
            for i in range(n):
                temp2_surface_temperature.append(data[i]['temp2_surface_temperature'])
                Not_none_values = filter(None.__ne__, temp2_surface_temperature)
                temp2_surface_temperature = list(Not_none_values)
                #print(temp1_surface_temperature)
            if not temp2_surface_temperature: 
                temp = temp1[-1]
                temp1.append(temp)
            else:
                temp1.append(statistics.mean(temp2_surface_temperature))
                #print(temp1)
                #print(temp1)
            del data
            del temp1_surface_temperature
            del temp2_surface_temperature
            time_st = time_now*30
                                       
    
    df = pd.DataFrame(
        {'Time': time_st,
         'codes': st_n,
         'temp': temp1
         })
    
    
    
    #os.chdir(r"C:\Users\afif0000\Documents\Heatmap_temp-main\Heatmap_temp-main\myapp") 
    # set the filepath and load in a shapefile
    fp = 'stationsI35_Merge2.shp'
    map_df = gpd.read_file(fp)
    # check data type so we can see that this is not a normal dataframe, but a GEOdataframe
    merged = map_df.set_index('Name').join(df.set_index('codes'))
    merged.reset_index(level=0, inplace=True)
    
    
    
    merged1 = merged.loc[~merged['NAME_0'].isin(['United States'])]
        
        
        #merged.fillna('No data', inplace = True)
    
    # Input GeoJSON source that contains features for plotting
    geosource = GeoJSONDataSource(geojson = merged.to_json())
    geosource1 = GeoJSONDataSource(geojson = merged1.to_json())
        
        
        # Define color palettes
    palette = Turbo256 
    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    mx = df['temp'].max()
    mn = df['temp'].min()
    color_mapper = LinearColorMapper(palette = palette, low = mn, high = mx, nan_color = None)
        
    mx = merged['temp'].max()
    mn = merged['temp'].min()
    n_ticks = 5
    ticks = np.linspace(mn, mx, n_ticks).round(1)  # round to desired precision 
    #color_ticks = FixedTicker(ticks=ticks)

  #create first plot
    p1 = figure(plot_width=950, plot_height=600)
    p1.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)
    
    
    p3 = figure(plot_width=950, plot_height=600)
    p3.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)
    


    data = np.random.normal(0, 0.5, 1000)
    hist, edges = np.histogram(data, density=True, bins=50)

    p2 = figure(plot_width=950, plot_height=600)
    p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white")  
    
    # Create color bar.
    color_bar = ColorBar(color_mapper = color_mapper, 
                         label_standoff = 8,
                         width = 500, height = 20,
                         border_line_color = None,
                         location = (0,0), 
                         orientation = 'horizontal')
    # Create figure object.
    title = f'Surface Temperature of I-35 from {t3} to {t1} at {t2}'
    p = figure(title = title, 
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
    #html = file_html(p, CDN, "my plot")
    p.axis.visible = False
    # Create tab1 from plot p1: tab1
    tab1 = Panel(child=p, title='Surface Temperature HM')
 
    # Create tab2 from plot p2: tab2
    tab2 = Panel(child=p1, title='Temp last 12 hours')
 
    # Create tab3 from plot p3: tab3
    tab3 = Panel(child=p2, title='Precipitation Events')
 
    # Create tab4 from plot p4: tab4
    tab4 = Panel(child=p3, title='Predicted Temp')    
    #kwargs['title'] = 'bokeh-with-flask'    
    # Create a Tabs layout: layout
    layout = Tabs(tabs=[tab1, tab2, tab3, tab4])
    script, div = components(layout)
    return render_template('index.html',div=div, script=script)   

if __name__ == '__main__':
    app.run(debug=True)
