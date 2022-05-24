# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:06:10 2022

@author: flori
"""

import os
import plotly.graph_objects as go
from plotly.graph_objs import Layout
import numpy as np
import plotly.io as pio
pio.renderers.default='browser'

import pandas as pd

df = pd.read_csv('demo.csv')  

COLOR_BLUE = "#80DEEA"
COLOR_GRAY = "#BEBEBE"
COLOR_TEXT = "#FFFFFF"
  
fs = 44100
x = (df["w"] / np.pi) * (fs / 2)
y = 20 * np.log10(df["H"])
  

layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=COLOR_TEXT,
)
fig = go.Figure(layout=layout)
  
fig.add_trace(go.Scatter(x=x, y=y, line = dict(color=COLOR_BLUE, width=4, dash='solid')))


fig.update_yaxes(ticks="outside", tickwidth=1, tickcolor=COLOR_GRAY, ticklen=5,
                 linewidth=1, linecolor=COLOR_GRAY, gridwidth=1, gridcolor=COLOR_GRAY,
                 tickfont=dict(size=15))
fig.update_xaxes(ticks="outside", tickwidth=1, tickcolor=COLOR_GRAY, ticklen=5,
                 linewidth=1, linecolor=COLOR_GRAY, gridwidth=1, gridcolor=COLOR_GRAY,
                 tickfont=dict(size=15))

fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [20, 50, 200, 1000, 5000, 20000],
        ticktext = ['20', '50', '200', '1k', '5k', '20k']
    ),
    yaxis = dict(
        tickmode = 'array',
        tickvals = [10, 0, -10, -20, -30, -40, -50],
        ticktext = ['10', '0', '-10', '-20', '-30', '-40', '-50']
    )
)

fig['layout']['xaxis'].update(zeroline=False, range=[np.log10(20), np.log10(fs / 2)])
fig['layout']['yaxis'].update(zeroline=False, range=[-50, 10])
  
fig.update_layout(xaxis_type="log")
fig.update_layout(autosize=False, width=300, height=200,
                  margin=dict(l=0, r=15, b=0, t=0, pad=0),
                  template="plotly_white", showlegend=False)

#fig.show()


if not os.path.exists("images"):
    os.mkdir("images")
fig.write_image("images/fig1.png")