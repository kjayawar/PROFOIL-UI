# Copyright (c) 2022 Kanishka Jayawardane [kanishkagj@yahoo.com]
# Copyright (c) 2022 Michael Selig

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

AN_PREV_LINE_COLOR              = "lightgrey"       # previous profoil.in after first run
AN_CURR_LINE_COLOR              = "mediumorchid"    # converged alpha* solution from profoil.dmp after run
AN_PRES_LINE_COLOR              = "yellowgreen"     # prescribed alfa* in the profoil.in file
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

AN_PLOT_YLIMITS                 = (-20, 20)         # From -20 deg to ~ +20 deg
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

# ==================================== CONFIG RELATED TO OVERLAY =====================================

OVERLAY_LINEWIDTH               = 0.7               # Overlay Plot line width                   
OVERLAY_LINESTYLE               = '-'               # Overlay Plot line style
OVERLAY_LINE_MARKER             = ""                # Overlay Plot line marker
OVERLAY_LINE_COLOR              = 'green'           # Overlay Plot line color
OVERLAY_MARKERSIZE              = None              # Overlay Plot marker size
OVERLAY_MARKERFACECOLOR         = None              # Overlay Plot marker color

#================================= CONFIG RELATED TO UE & XY PLOTS ==================================

UPPER_SURFACE_PHI_MARKER        = "^"               # Upward facing Triangular Phi Marks
LOWER_SURFACE_PHI_MARKER        = "v"               # Downward facing Triangular Phi Marks
UPPER_SURFACE_PHI_MARKER_SIZE   = 8                 # Phi marker size - upper Surface
LOWER_SURFACE_PHI_MARKER_SIZE   = 8                 # Phi marker size - lower Surface

#================================= CONFIG RELATED TO MAIN WINDOW ====================================

MAIN_WINDOW_WIDTH               = 1250              # Main window width
MAIN_WINDOW_HEIGHT              =  870              # Main window height

#================================ CONFIG RELATED TO AIRFOIL LOADING =================================

AIRFOIL_CHANGE_WARNING          = False             # A warning dialog upon changing active session
KEEP_OLD_AIRFOIL_UPON_LOADING   = True              # Old airfoil data is preserved upon switching
                                                    # when set to True

#======================================== KEYBOARD SHORTCUTS ========================================
# Main shortcuts
SHORTCUT_OPEN                   = "Ctrl+O"          # Shortcut for File | Open Dialog     
SHORTCUT_SAVE                   = "Ctrl+S"          # Shortcut for profoil.in file save in "File View"
SHORTCUT_SAVE_AS                = "Ctrl+Shift+S"    # Shortcut for File | 'Save As' in "Design View"
SHORTCUT_EDIT                   = "Ctrl+E"          # Shortcut for Start Edits
SHORTCUT_CANCEL                 = "Ctrl+D"          # Shortcut for Cancel Edits
SHORTCUT_EXEC                   = "Ctrl+R"          # Shortcut for Run PROFOIL
SHORTCUT_REVERT                 = "T"               # Shortcut for Revert action in Design View
SHORTCUT_UNDO                   = "U"               # Shortcut for Undo action in Design View
SHORTCUT_HISTORY_TOGGLE         = "H"               # Shortcut for toggling History in Design View
SHORTCUT_SURFACE_TOGGLE         = "Q"               # Shortcut to toggle between Upper and Lower surface alpha* selection
SHORTCUT_TOGGLE_COMMENT         = "Ctrl+/"          # Shortcut for toggling comment lines
SHORTCUT_ANNOTATE               = "Ctrl+W"          # Shortcut for annotating profoil.in file

# Shortcuts for matplotlib toolbar in "Design View" tab:
SHORTCUT_HOME                   = "A"               # Shortcut for Home action (reset graphics) in Design View
SHORTCUT_PAN                    = "Space"           # Shortcut for Pan action in Design View
SHORTCUT_ZOOM                   = "Z"               # Shortcut for Zoom action in Design View
SHORTCUT_SAVE_BUTTON            = "S"               # Shortcut for Save action in Design View

# Tab switching shortcuts
SHORTCUT_TAB1                   = "Ctrl+1"          # Shortcut for switching tab to "Design View"
SHORTCUT_TAB2                   = "Ctrl+2"          # Shortcut for switching tab to "File View"
SHORTCUT_TAB3                   = "Ctrl+3"          # Shortcut for switching tab to "Converged View"

# Even shorter [Alternative] Shortcuts when in Design View
SHORTCUT_RUN_DESIGN_VIEW        = "R"               # Shortcut for Run PROFOIL in Design View
SHORTCUT_CURSOR_EDIT_DESIGN_VIEW= "E"               # Shortcut for Alpha* Cursor edits in Design View
SHORTCUT_CANCEL_DESIGN_VIEW     = "D"               # Shortcut for Cancel in Design View

SHORTCUT_F1_DESIGN_VIEW         = "F1"              # Alternative Shortcut for Design View
SHORTCUT_F2_FILE_VIEW           = "F2"              # Alternative Shortcut for File View
SHORTCUT_F3_CONVERGED_VIEW      = "F3"              # Alternative Shortcut for Converged View

#========================================== COMMENT STYLE ===========================================

COMMENT_MARKER                  = "#"               # PROFOIL supports # or ! as comment markers
COMMENT_COLOR                   = "green"           # Choose comment color

#========================================== MISCELLANEOUS ===========================================
SHOW_SHORTCUTS_ON_BUTTONS       = "FULL"            # Buttons show shortcuts strings - 3 possible options
                                                    #   "NONE" -- No shortcuts strings shown on the buttons
                                                    #   "FULL" -- All shortcuts are shown - ex Cancel (C, Ctrl+C)
                                                    #   "HALF" -- only one shortcut is shown - ex Cancel (C)
KEEP_LAST_OPEN_PATH_AS_DEFAULT  = True              # Set to True to keep the last open/Save As path as default; 
                                                    # False to use ~/runs as the default folder