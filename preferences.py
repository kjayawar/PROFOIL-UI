# Copyright (c) 2022 Kanishka Jayawardane [kanishkagj@yahoo.com]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This file list out all the preferences
# The options listed down here has to be compatible with matplotlib.
# Documentation can be found at 

# https://matplotlib.org/stable/api/markers_api.html
# https://matplotlib.org/3.5.0/gallery/lines_bars_and_markers/linestyles.html

#=========================================== DIRECTORIES ============================================

WORK_DIR                        = "../work"
BIN_DIR                         = "../bin"

#===================================== CONFIG OF PHI-ALPHA PLOT =====================================

AN_PREV_LINE_LINESTYLE          = '--'              # dotted lines for previous plot
AN_CURR_LINE_LINESTYLE          = '--'              # dotted lines for current plot
AN_PRES_LINE_LINESTYLE          = '--'              # dotted lines for prescribed plot
AN_MODI_LINE_LINESTYLE          = '-'               # continuous lines for main modifiable line

AN_PREV_LINE_COLOR              = "black"           # color of previous plot
AN_CURR_LINE_COLOR              = "darkviolet"      # color of current plot
AN_PRES_LINE_COLOR              = "blue"            # color of prescribed plot
AN_MODI_LINE_COLOR              = "green"           # color of modifiable line

AN_SPLN_LINE_LINESTYLE          = '--+'             # dotted lines with + marks for spline
AN_SPLN_LINE_COLOR              = 'red'             # dotted lines with + marks for spline

AN_PREV_LINE_MARKER             = "o"               # markers on the alfa_nu plot
AN_CURR_LINE_MARKER             = "o"               # markers on the alfa_nu plot
AN_PRES_LINE_MARKER             = "o"               # markers on the alfa_nu plot
AN_MODI_LINE_MARKER             = "o"               # markers on the alfa_nu plot

AN_PREV_LINE_MARKERFACECOLOR    = "None"            # markers face color on ref plots
AN_CURR_LINE_MARKERFACECOLOR    = "None"            # markers face color on ref plots
AN_PRES_LINE_MARKERFACECOLOR    = "None"            # markers face color on ref plots

AN_PLOT_MARKERSIZE              = 3                 # All markers share the same size.
AN_PLOT_LINEWIDTH               = 1                 # All lines share the same width.

AN_PLOT_YLIMITS                 = (-20, 20)         # From -20 deg to +20 deg
AN_PLOT_XLIMITS_UPPER           = ( 37,  0)         # From -20 deg to +20 deg
AN_PLOT_XLIMITS_LOWER           = ( 23, 60)         # From -20 deg to +20 deg
AN_FLIP_YAXIS_LOWER_SURFACE     = True              # With this set, y-axis limits will be reversed
                                                    # for lower surface

#============================ CONFIG OF VELOCITY DISTRIBUTION (UE) PLOT =============================

UE_PLOT_OLD_LINE_COLOR          = "darkgrey"        # UE Plot , previous reference plot colors
UE_PLOT_OLD_LINE_STYLE          = "--"              # UE Plot , previous reference plot line-style
UE_PLOT_OLD_MARKER_COLOR        = "darkgrey"        # UE Plot , previous reference plot marker color

UE_PLOT_LINEWIDTH               = 1                 # UE Plot , line width of the plots
UE_PLOT_COLOR                   = None              # UE Plot , line color of the plots

# ======================================== CONFIG OF XY PLOT =========================================

XY_PLOT_LINEWIDTH               = 1                 # XY Plot line width
XY_PLOT_COLOR                   = "black"           # XY Plot line color

OVERLAY_LINEWIDTH               = 1                 # Overlay Plot line width                   
OVERLAY_LINESTYLE               = '--'              # Overlay Plot line style
OVERLAY_LINE_MARKER             = "."               # Overlay Plot line marker
OVERLAY_LINE_COLOR              = 'red'             # Overlay Plot line color
OVERLAY_MARKERSIZE              = 5                 # Overlay Plot marker size
OVERLAY_MARKERFACECOLOR         = 'red'             # Overlay Plot marker color

#================================= CONFIG RELATED TO UE & XY PLOTS ==================================


UPPER_SURFACE_PHI_MARKER        = "^"               # Upward facing Triangular Phi Marks
LOWER_SURFACE_PHI_MARKER        = "v"               # Downward facing Triangular Phi Marks
UPPER_SURFACE_PHI_MARKER_SIZE   = 8                 # Phi marker size - upper Surface
LOWER_SURFACE_PHI_MARKER_SIZE   = 8                 # Phi marker size - lower Surface