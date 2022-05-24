###############################################################################
# file    Plotter.py
###############################################################################
# brief   This module creates sveral plots for GUI with plotly
###############################################################################
# author  Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-23
###############################################################################
# MIT License
#
# Copyright (c) 2022 ICAI Interdisciplinary Center for Artificial Intelligence
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

import os
import plotly.graph_objects as go
from plotly.graph_objs import Layout
import numpy as np

class EqualizerPlotter:
    def __init__(self, width, height, fs):
        self._width = width
        self._height = height
        self._fs = fs
        
        self._COLOR_BLUE = "#80DEEA"
        self._COLOR_GRAY = "#BEBEBE"
        self._COLOR_TEXT = "#FFFFFF"
        
    def generatePlot(self, w, H, path):
        w = (w / np.pi) * (self._fs / 2)
        H = 20 * np.log10(H)
        
        layout = Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color=self._COLOR_TEXT,
        )
        fig = go.Figure(layout=layout)      
        fig.add_trace(go.Scatter(x=w, y=H, line = dict(color=self._COLOR_BLUE,
                                                       width=4, dash='solid')))
        
        
        fig.update_yaxes(ticks="outside", tickwidth=1,
                         tickcolor=self._COLOR_GRAY, ticklen=5,
                         linewidth=1, linecolor=self._COLOR_GRAY,
                         gridwidth=1, gridcolor=self._COLOR_GRAY,
                         tickfont=dict(size=15))
        fig.update_xaxes(ticks="outside", tickwidth=1,
                         tickcolor=self._COLOR_GRAY, ticklen=5,
                         linewidth=1, linecolor=self._COLOR_GRAY,
                         gridwidth=1, gridcolor=self._COLOR_GRAY,
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
        
        xRange = [np.log10(20), np.log10(self._fs / 2)]
        fig['layout']['xaxis'].update(zeroline=False, range=xRange)
        fig['layout']['yaxis'].update(zeroline=False, range=[-50, 10])
          
        fig.update_layout(xaxis_type="log")
        fig.update_layout(width=self._width, height=self._height,
                          margin=dict(l=0, r=15, b=0, t=0, pad=0),
                          template="plotly_white", showlegend=False,
                          autosize=False)
        
        fig.write_image(path)
        
        
if __name__ == '__main__':
    import pandas as pd
    
    df = pd.read_csv('Files/demo.csv')
    w = df["w"]
    H = df["H"]
    
    plotter = EqualizerPlotter(250, 100, 44100)
    plotter.generatePlot(w, H, "demo.svg")