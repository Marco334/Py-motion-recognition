
from bokeh.plotting import figure, output_file, show
#from bokeh.io import output_file, show
#import pandas
from MOTION_DETECTION_2 import df
'''
-------------------------------
py -3 Video_Data_Ploting.py
------------------------------
'''
#def V_D_P (DF):

p = figure(height=100,width=500,  x_axis_type="datetime",responsive=True,title="Video_mouvements")
#plot_width=250,
p.title.text_color                  = "Gray"
p.title.text                        = "Cool Data"
p.title.text_font                   = "times"
p.title.text_font_style             = "bold"
#p.xaxis.minor_tick_line_color       = None
p.yaxis.minor_tick_line_color       = None
p.xaxis.axis_label                  = "Date"
p.yaxis.axis_label                  = "Intensity"
p.ygrid[0].ticker.desired_num_ticks = 1

q=p.quad(left=df["Start" ], right=df["End"], top=1, bottom=0, color="Orange")

#p.line(df["date"],df["Close"],color="Orange", alpha=0.5)
output_file("Vido_mouvment_graph.html")
show(p)
