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


# This is the main module of PROFOIL-UI. 

# From the beginning It was conceptualized as a minimalistic program which allows users to do any modifications as they wish relatively easily. 
# So as a result, only the commonly available libraries with minimal overhead was chosen for this application. 
# Matplotlib is the core library in use which provides all the functionalities related to graphing and callbacks.

# Concept inventory
# =================

# +------------------------------------+--------------------------+
# |              Concept               |      Implementation      |
# +------------------------------------+--------------------------+
# | GUI-Window                         | matplotlib figure        |
# | Graphs                             | matplotlib axes          |
# | Plots                              | matplotlib Line2D object |
# | Previous plots                     | matplotlib Line2D object |
# | All plots in an axis               | list                     |
# | Previous phi-alpha* distribution   | matplotlib Line2D object |
# | Current phi-alpha* distribution    | matplotlib Line2D object |
# | Prescribed phi-alpha* distribution | matplotlib Line2D object |
# | Modifiable phi-alpha* distribution | matplotlib Line2D object |
# +------------------------------------+--------------------------+

# Initial development started with the spline_editor module which allows users to prescribe phi-alpha* distribution using mouse clicks
# and cursor edits. The main functionalities related to interactive graph were implemented through this module and 
# profoil_ui module with extends the above as the main class Profoil_UI(...).

# For velocity and x,y graphs, axes.plot(...) function is used to plot lines, just as in any other matplotlib based program. 
# axes.lines which holds a list of all plots are represented in the below manner for ease of changing their appearance 
# when new plots being added in.

# +-------------------+----------------+-----------+
# | untouchable plots | previous plots | new plots |
# +-------------------+----------------+-----------+

# Untouchable section of plots is used to carry the plots, which should not be purged off as new plots being added in. 
# Depending on a pre-set number of previous plots to hold "previous plots" section keeps the data of the n-previous runs. 
# "new plots" are the section newly being added in, on each plotting action. 
# When plotting starts, "previous plots" section will be purged off and "new plots" will be turned in to "previous plots" 
# with the pre-set markers and colors etc. Then only a new set of plots will be added into "new plots" 
# As an additional note, overlayed dat file plot and cursor edit line for example sit on "untouchable plots" section.  

# Last 4 items listed on the concept inventory is constructed directly from the matplotlib.pyplot Line2D objects instead of using 
# axes.plot(..) because for surface switching, these lines already been constructed and updated in place is important. 
# These line will always be there with the same ids which was created at the startup. 
# Only the data which these lines represent, is altered in subsequent plotting actions. 

# More in-depth implementation details follows in each functions doc-strings. 

import numpy as np
from pathlib import Path

from preferences import *
import profoil_interface as p_intf
from profoil_interface import WORKDIR, BINDIR

import matplotlib
matplotlib.use('Qt5Agg', force=True)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from PyQt5 import QtCore

class ProfoilCanvas:

    def __init__(self):
        plt.ion()

        self.GRID_ON                  = True  # Grid on the phi-alpha* plot
        self.SHOW_PREV_LINES          = True  # Show previous plots on the Velocity and x,y plots.
        
        self.active_surface = "Upper"
        self.n_held_history_lines = 0

        self.upper_xlim =AN_PLOT_XLIMITS_UPPER
        self.upper_ylim =AN_PLOT_YLIMITS
        self.lower_xlim =AN_PLOT_XLIMITS_LOWER
        self.lower_ylim =tuple(reversed(AN_PLOT_YLIMITS)) if AN_FLIP_YAXIS_LOWER_SURFACE else AN_PLOT_YLIMITS

        # Creating the matplotlib figure containing all 3 plots.
        self.gen_gui_fig()
        
        # Upper Surface Lines in the phi-alpha* distribution plot
        # during the program execution these lines will not be re-plotted.

        self.upper_nu_alfa_previous   = plt.Line2D([],[], linestyle=AN_PREV_LINE_LINESTYLE, marker=AN_PREV_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PREV_LINE_COLOR, markerfacecolor=AN_PREV_LINE_MARKERFACECOLOR, clip_on=False)
        self.upper_nu_alfa_converged  = plt.Line2D([],[], linestyle=AN_CURR_LINE_LINESTYLE, marker=AN_CURR_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_CURR_LINE_COLOR, markerfacecolor=AN_CURR_LINE_MARKERFACECOLOR, clip_on=False)
        self.upper_nu_alfa_prescribed = plt.Line2D([],[], linestyle=AN_PRES_LINE_LINESTYLE, marker=AN_PRES_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PRES_LINE_COLOR, markerfacecolor=AN_PRES_LINE_MARKERFACECOLOR, clip_on=False)
        self.upper_nu_alfa_modi       = plt.Line2D([],[], linestyle=AN_MODI_LINE_LINESTYLE, marker=AN_MODI_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_MODI_LINE_COLOR, clip_on=False)

        # Lower Surface Lines in the phi-alpha* distribution plot
        # during the program execution these lines will not be re-plotted.

        self.lower_nu_alfa_previous   = plt.Line2D([],[], linestyle=AN_PREV_LINE_LINESTYLE, marker=AN_PREV_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PREV_LINE_COLOR, markerfacecolor=AN_PREV_LINE_MARKERFACECOLOR, clip_on=False)
        self.lower_nu_alfa_converged  = plt.Line2D([],[], linestyle=AN_CURR_LINE_LINESTYLE, marker=AN_CURR_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_CURR_LINE_COLOR, markerfacecolor=AN_CURR_LINE_MARKERFACECOLOR, clip_on=False)
        self.lower_nu_alfa_prescribed = plt.Line2D([],[], linestyle=AN_PRES_LINE_LINESTYLE, marker=AN_PRES_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PRES_LINE_COLOR, markerfacecolor=AN_PRES_LINE_MARKERFACECOLOR, clip_on=False)
        self.lower_nu_alfa_modi       = plt.Line2D([],[], linestyle=AN_MODI_LINE_LINESTYLE, marker=AN_MODI_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_MODI_LINE_COLOR, clip_on=False)

        # cursor edit line
        self.cursor_edit_line, = self.an_ax.plot([], [], AN_SPLN_LINE_LINESTYLE, picker=True, color=AN_SPLN_LINE_COLOR, linewidth=AN_PLOT_LINEWIDTH)

        # DAT Overlay line. Matplotlib versions >3.5 has ArtistList class in-place of generic list
        # which does not support alterations matplotlib previously supported. so a Line2D object is added to the xy_ax
        # axis which will be updated when a DAT file is loaded. Initially this line is set to be not visible.

        self.overlay_line = plt.Line2D([],[], linestyle=OVERLAY_LINESTYLE, marker=OVERLAY_LINE_MARKER, linewidth=OVERLAY_LINEWIDTH, markersize=OVERLAY_MARKERSIZE, color=OVERLAY_LINE_COLOR, markerfacecolor=OVERLAY_MARKERFACECOLOR, clip_on=False)
        self.overlay_line.set_visible(False)
        self.xy_ax.add_line(self.overlay_line)

        # Flags
        # =====
        self.ready_to_interact = False               
        # holds a flag to signal if program is ready to run.
        # purpose is to stop errors from occurring by accidental key presses
        # prior to loading files.

        self.edit_mode = False

    def gen_gui_fig(self):

        # Setting up the main window/figure

        self.gui_fig = Figure()
        grid = plt.GridSpec(4,2, wspace=0.1, hspace=0.2)

        # Setting up the 3 main axes
        # ue_ax : velocity distribution axes
        # xy_ax : x,y airfoil contour axes
        # an_ax : alpha*-nu axes

        self.ue_ax = self.gui_fig.add_subplot(grid[:3, 0])
        self.xy_ax = self.gui_fig.add_subplot(grid[ 3, 0])
        self.an_ax = self.gui_fig.add_subplot(grid[:3, 1])

        # Set zorder for each axis.
        # Airfoil xy is on top (3), then alpha* (2), then ue (1).
        self.xy_ax.set_zorder(3)
        self.an_ax.set_zorder(2)
        self.ue_ax.set_zorder(1)
        
        self.gui_fig.subplots_adjust(left=0.05, right=0.98, top=0.96, bottom=0.08, hspace = 0.02, wspace=0.02)
        self.gui_fig.canvas.mpl_connect('button_press_event', self.on_click)

        self.setup_axes()

    def setup_axes(self):
        """
        initializes the axes
        """
        self.ue_ax.n_untouch = 0
        self.xy_ax.n_untouch = 1 # DAT overlay line has to be untouchable to not to get overwritten in each run.
        self.an_ax.n_untouch = 1 # cursor edit spline has to be untouchable

        self.ue_ax.set_title(r'$Velocity\ Distribution$')
        self.ue_ax.set_ylabel(r'$V/V_{\infty}$')

        self.xy_ax.set_xlabel(r"$x/c$")
        self.xy_ax.set_ylabel(r"$y/c$")

        self.an_ax.set_title(r'$\alpha^*(\phi) - Upper$')
        self.an_ax.set_xlabel(r"$\phi$")
        self.an_ax.grid(True)

        # Setting the aspect ratios.
        # For alpha*-nu axis and x-y axis aspect ratio should be 1
        # For velocity aspect ratio of 0.5, ie: 2 units of y -> 1 unit of x being used
        self.xy_ax.axes.set_aspect('equal', 'datalim')
        self.an_ax.axes.set_aspect('equal', 'datalim')
        self.ue_ax.axes.set_aspect(0.5, 'datalim')

        self.setup_axes_limits()

    def update_ylim(self, ax, y_lower):
        """
        Given a bounded x-range set y-range of an axis keeping the AR and bbox size intact
        https://github.com/matplotlib/matplotlib/issues/28673
        """
        bbox = ax.get_window_extent().transformed(ax.get_figure().dpi_scale_trans.inverted())
        pixel_AR = bbox.height/bbox.width
        x_lim = ax.get_xlim()
        x_range = abs(x_lim[0]-x_lim[1])
        y_range = (x_range/ax.get_aspect()) * pixel_AR
        ax.set_ylim(y_lower, y_lower+y_range)

    def setup_ax_limit(self, ax, x_lower, x_upper, y_lower):
        """
        setup single subplot ax limits
        """
        ax.set_xlim(x_lower, x_upper)
        self.update_ylim(ax, y_lower)

    def setup_axes_limits(self):
        """
        initializes the axes limits
        """
        self.setup_ax_limit(self.ue_ax, -0.08, 1.08, y_lower=0)
        self.setup_ax_limit(self.xy_ax, -0.08, 1.08, y_lower=-0.15)

        if self.active_surface == "Lower":
            self.setup_ax_limit(self.an_ax, *AN_PLOT_XLIMITS_LOWER, y_lower=AN_PLOT_YLIMITS[0])
            if AN_FLIP_YAXIS_LOWER_SURFACE : 
                self.an_ax.invert_yaxis()

        if self.active_surface == "Upper":
            self.setup_ax_limit(self.an_ax, *AN_PLOT_XLIMITS_UPPER, y_lower=AN_PLOT_YLIMITS[0])

    def clear_axes(self):
        """
        clears all axes data such that new session with new airfoil can be loaded.
        """
        self.clear_ax(self.ue_ax)
        self.clear_ax(self.xy_ax)
        self.clear_ax(self.an_ax)

        self.upper_nu_alfa_converged.set_data([],[]) 
        self.upper_nu_alfa_prescribed.set_data([],[])
        self.upper_nu_alfa_modi.set_data([],[])
        self.upper_nu_alfa_previous.set_data([],[])

        self.lower_nu_alfa_converged.set_data([],[]) 
        self.lower_nu_alfa_prescribed.set_data([],[])
        self.lower_nu_alfa_modi.set_data([],[])
        self.lower_nu_alfa_previous.set_data([],[])

        self.cursor_edit_line.set_data([],[])

    def reset_toolbar(self):
        """
        This function resets the toolbar such that all tool bar items are set to not-checked
        """
        try:
            for x in self.tool_bar.actions():
                if x.isChecked():
                    x.trigger()
        except:
            pass

    def load_line(self, line):
        """
        This function "loads a line" in to the cursor editor.
        In summary it references a line object from the child class to be modified
        """
        self.cancel_cursor_inputs()
        self.nu_alfa = line
        self.nu_alfa_points = self.nu_alfa.get_xydata().tolist()
        self.gui_fig.canvas.draw()

    def on_click(self, event=None):
        """
        All the mouse click events go here
        """
        if not self.ready_to_interact: return
        if not self.edit_mode: return
        if event.inaxes!=self.an_ax: return

        # Left click : Add a point to the edit line
        if event.button == 1:
            self.cursor_edit_line_points.append([event.xdata,event.ydata])
            self.cursor_edit_line_points.sort()
            self.cursor_edit_line.set_data(*list(zip(*self.cursor_edit_line_points)))

            self.gui_fig.canvas.draw()
            # Ensure cursor remains a crosshair during the edit process
            self.canvas.setCursor(QtCore.Qt.CrossCursor)

        # Right Click and spline is actually built
        if event.button == 3:
            self.apply_edits(event)
            # Reset to default cursor after applying edits
            self.setCursor(QtCore.Qt.ArrowCursor)

            self.gui_fig.canvas.draw()

    def bkp_an_ax_zoomed_limits(self, event):
        """
        save zoomed limits so that switching between upper and lower surfaces wont reset limits
        """
        if self.active_surface == "Lower":
            self.lower_xlim = self.an_ax.get_xlim()
            self.lower_ylim = self.an_ax.get_ylim()
        if self.active_surface == "Upper":
            self.upper_xlim = self.an_ax.get_xlim()
            self.upper_ylim = self.an_ax.get_ylim()

    def select_surface(self, surface):
        """
        Callback function that switches the upper and lower surfaces
        through the radio buttons.
        Depending on the preferences:
            y-axis is inverted upon switching.
        """
        self.reset_toolbar()
        self.clear_ax(self.an_ax)
        if surface =="Upper":
            self.active_surface = "Upper"

            self.an_ax.set_xlim(*self.upper_xlim)
            self.an_ax.set_ylim(*self.upper_ylim)

            self.an_ax.set_title(r'$\alpha^*(\phi) - Upper$')

            # axes transformation between ax limits and pixels are handled
            # automatically by ax.add_line(...)
            # ax.lines = [..] wouldn't work the same way

            self.an_ax.add_line(self.upper_nu_alfa_previous)
            self.an_ax.add_line(self.upper_nu_alfa_converged)
            self.an_ax.add_line(self.upper_nu_alfa_prescribed)
            self.an_ax.add_line(self.upper_nu_alfa_modi)

            # load_line makes the Line2D object which is passed active
            # in the interactive plot.

            self.load_line(self.upper_nu_alfa_modi)

        if surface =="Lower":
            self.active_surface = "Lower"

            self.an_ax.set_xlim(*self.lower_xlim)
            self.an_ax.set_ylim(*self.lower_ylim)

            self.an_ax.set_title(r'$\alpha^*(\phi) - Lower$')

            # axes transformation between pixel and ax limits are handled
            # automatically by ax.add_line(...)
            # ax.lines = [..] wouldn't work the same way

            self.an_ax.add_line(self.lower_nu_alfa_previous)
            self.an_ax.add_line(self.lower_nu_alfa_converged)
            self.an_ax.add_line(self.lower_nu_alfa_prescribed)
            self.an_ax.add_line(self.lower_nu_alfa_modi)

            # load_line makes the Line2D object which is passed active
            # in the interactive plot.

            self.load_line(self.lower_nu_alfa_modi)
        self.gui_fig.canvas.draw()

    def checkbox_toggle(self, label):
        self.reset_toolbar()
        if label=="Grid":
            self.toggle_grid_lines()
        else:
            self.toggle_previous_plots()

    def toggle_airfoil_grid_lines(self, event=None):
        """
        Toggles the grid lines on the xy_ax (airfoil plot).
        Will make effect immediately
        """
        grid_on = bool(event)
        self.xy_ax.grid(grid_on)
        self.gui_fig.canvas.draw()
        
    def toggle_previous_plots(self, event=None):
        """
        Toggles the visibility of previous lines.
        Will make effect from the next plot - not on the current plot
        """
        self.SHOW_PREV_LINES = bool(event)

        # Goes through each axis and sets the visibility
        # of the preserved lines. 
        # each ax class will hold a list of preserved lines.
        for ax in [self.ue_ax, self.xy_ax]:
            for line in ax.preserved_plots:
                line.set_visible(self.SHOW_PREV_LINES)
            for marker in ax.preserved_markers:
                marker.set_visible(self.SHOW_PREV_LINES)

        self.upper_nu_alfa_previous.set_visible(self.SHOW_PREV_LINES)
        self.lower_nu_alfa_previous.set_visible(self.SHOW_PREV_LINES)

        self.gui_fig.canvas.draw()

    def toggle_grid_lines(self, event=None):
        """
        Toggles the grid lines on the an_ax.
        Will make effect immediately
        """
        self.GRID_ON = bool(event)
        self.an_ax.grid(self.GRID_ON)
        self.gui_fig.canvas.draw()

    def proc_make_ax_old(self, ax, preserve_lines=1):
        """
        This function accepts an axes object and applies the settings for previous plot.
        1. Keep only last few lines on the axes given by preserve_lines and purges away the rest
        2. Greys/blacks out the lines/markers
        3. Make the lines dashed
        4. Removes the legend
        5. Sets visibility
        6. Makes a list of preserved lines and collections to set the visibility later on through "History" check-box
        """
        plots = ax.lines

        ax.preserved_plots   = []  # list of references for preserved plots will be stored for clearing history
        ax.preserved_markers = []  # list of references for preserved plots will be stored for clearing history

        untouch_plots  = plots[:ax.n_untouch]
        preserved_plots = plots[ax.n_untouch:][-preserve_lines:]
        
        for plot in untouch_plots:
            plot.set_label('_nolegend_')

        for plot in preserved_plots:
            plot.set_color(UE_PLOT_OLD_LINE_COLOR)
            plot.set_linestyle(UE_PLOT_OLD_LINE_STYLE)
            plot.set_label('_nolegend_')
            plot.set_visible(self.SHOW_PREV_LINES)

        markers = ax.collections[-2* preserve_lines:]
        for marker in markers:
            marker.set_color(UE_PLOT_OLD_MARKER_COLOR)
            marker.set_visible(self.SHOW_PREV_LINES)

        ax.preserved_plots = preserved_plots.copy() # list of references for clearing history
        ax.preserved_markers = markers.copy()       # list of references for clearing history

        # remove old plots except the untouchable and the ones from last run
        for line in ax.lines[ax.n_untouch:-preserve_lines]: 
            line.remove()

        # remove markers except the markers of last run
        for marker in ax.collections[:-2* preserve_lines]:
            marker.remove()

        ax.set_prop_cycle(None)

    def plot_xy(self, n_prev_plots =1):
        """ 
        Plots airfoil contour
        """
        n_xy_preserve = n_prev_plots

        # make the previous plots "old" [greyed out and dashed etc]
        self.proc_make_ax_old(self.xy_ax, n_xy_preserve)

        # plots the airfoil contour
        # color of the original plot is extracted back to make the upper and lower markers.

        p = self.xy_ax.plot(self.x, self.y, lw=XY_PLOT_LINEWIDTH, color=XY_PLOT_COLOR, clip_on=False)
        self.xy_ax.scatter(self.xy_marker_upper['x'], self.xy_marker_upper['y'], color=p[-1].get_color(), marker=UPPER_SURFACE_PHI_MARKER, s=UPPER_SURFACE_PHI_MARKER_SIZE, clip_on=False)
        self.xy_ax.scatter(self.xy_marker_lower['x'], self.xy_marker_lower['y'], color=p[-1].get_color(), marker=LOWER_SURFACE_PHI_MARKER, s=LOWER_SURFACE_PHI_MARKER_SIZE, clip_on=False)

        self.gui_fig.canvas.draw()


    def plot_ue(self, n_prev_plots =1):
        """ 
        Plots velocity distribution data
        """
        n_ue_preserve = self.n_held_history_lines * n_prev_plots # alphas give the number of lines

        # make the previous plots "old" [greyed out and dashed etc]
        self.proc_make_ax_old(self.ue_ax, n_ue_preserve)
    
        # plots the velocity distribution
        # color of the original plot is extracted back to make the upper and lower markers.
        for alpha in sorted(self.ue_lines.keys(), key=float):
            p = self.ue_ax.plot(self.ue_lines[alpha]['x'], self.ue_lines[alpha]['v_vinf'], label = "{:5.2f}".format(alpha), lw=UE_PLOT_LINEWIDTH, color=UE_PLOT_COLOR, clip_on=False)
            self.ue_ax.scatter(self.upper_vel_markers[alpha]['x'], self.upper_vel_markers[alpha]['v_vinf'], color=p[-1].get_color(), marker=UPPER_SURFACE_PHI_MARKER, s=UPPER_SURFACE_PHI_MARKER_SIZE, clip_on=False)
            self.ue_ax.scatter(self.lower_vel_markers[alpha]['x'], self.lower_vel_markers[alpha]['v_vinf'], color=p[-1].get_color(), marker=LOWER_SURFACE_PHI_MARKER, s=LOWER_SURFACE_PHI_MARKER_SIZE, clip_on=False)

        self.n_held_history_lines = len(self.ue_lines.keys())

        # legend is not used in the current implementation because Alphas are just dummy variables.
        # can modify easily in the future if Alphas to be read from the .in file.
        # self.ue_ax.legend(fontsize ='small', frameon = False, loc="upper right")

        self.gui_fig.canvas.draw()

    def bkp_previous_line(self):
        """
        data from "current" plot sets data on "previous" plot
        """
        self.upper_nu_alfa_previous.set_data(*self.upper_nu_alfa_prescribed.get_data())
        self.lower_nu_alfa_previous.set_data(*self.lower_nu_alfa_prescribed.get_data())

    def clear_ax(self, ax):
        """
        Removes all lines except the "untouchable plots" section
        ax.clear(...) wouldn't work here because it resets all the limits and
        de-reference the axes from the cursor editor.
        n_untouch is not applicable for collections because the only 2 lines that are untouchable
        are the cursor edit line and overlay line- none of them have associated collection
        """
        for line in ax.lines[ax.n_untouch:]: 
            line.remove()
        for c in ax.collections: 
            c.remove()

    def plot_nu_alfa(self):
        """
        As per the overall description on the top, plotting of phi-alpha* distribution
        does not generate new plot lines (Line2D objects) using ax.plot(...)
        The state of these 8 lines will be maintained with the same ID by changing 
        the data these lines hold. This method vastly eases off the surface switching.
        """
        self.upper_nu_alfa_prescribed.set_data(self.nu_upper, self.alfa_upper)
        self.upper_nu_alfa_modi.set_data(self.nu_upper, self.alfa_upper)
        self.upper_nu_alfa_converged.set_data(self.nu_conv_upper, self.alfa_conv_upper)

        self.lower_nu_alfa_prescribed.set_data(self.nu_lower, self.alfa_lower)
        self.lower_nu_alfa_modi.set_data(self.nu_lower, self.alfa_lower)
        self.lower_nu_alfa_converged.set_data(self.nu_conv_lower, self.alfa_conv_lower)

    def overlay_dat(self, filename, skiprows):
        """
        This function overlays a given DAT file contour in the xy plot.
        File formats with different number of header are supported
        """
        try:
            x,y = np.loadtxt(Path(filename), skiprows=skiprows).T
        except:
            self.overlay_error_dialog()
            return

        self.overlay_line.set_data(x,y)
        self.overlay_line.set_visible(True)
        self.gui_fig.canvas.draw()

    def clear_overlay(self):
        """ 
        This function removes the the overlay in LIFO order
        If more than one overlay being added the last one
        will be cleared off first
        """
        self.overlay_line.set_data([],[])
        self.overlay_line.set_visible(False)
        self.gui_fig.canvas.draw()
