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
from scipy.interpolate import interp1d

from preferences import *
import profoil_interface as p_intf
from profoil_interface import WORKDIR, BINDIR

import matplotlib
matplotlib.use('Qt5Agg', force=True)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class ProfoilCanvas:

    def __init__(self):
        plt.ion()

        self.GRID_ON                  = True  # Grid on the phi-alpha* plot
        self.SHOW_PREV_LINES          = True  # Show previous plots on the Velocity and x,y plots.
        
        self.active_surface = "Upper"

        self.upper_xlim =AN_PLOT_XLIMITS_UPPER
        self.upper_ylim =AN_PLOT_YLIMITS
        self.lower_xlim =AN_PLOT_XLIMITS_LOWER
        self.lower_ylim =tuple(reversed(AN_PLOT_YLIMITS)) if AN_FLIP_YAXIS_LOWER_SURFACE else AN_PLOT_YLIMITS

        self.gen_gui_fig()
        
        # Upper Surface Lines in the phi-alpha* distribution plot
        # during the program execution these lines will not be re-plotted.

        self.upper_nu_alfa_previous   = plt.Line2D([],[], linestyle=AN_PREV_LINE_LINESTYLE, marker=AN_PREV_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PREV_LINE_COLOR, markerfacecolor=AN_PREV_LINE_MARKERFACECOLOR, clip_on=False)
        self.upper_nu_alfa_current    = plt.Line2D([],[], linestyle=AN_CURR_LINE_LINESTYLE, marker=AN_CURR_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_CURR_LINE_COLOR, markerfacecolor=AN_CURR_LINE_MARKERFACECOLOR, clip_on=False)
        self.upper_nu_alfa_prescribed = plt.Line2D([],[], linestyle=AN_PRES_LINE_LINESTYLE, marker=AN_PRES_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PRES_LINE_COLOR, markerfacecolor=AN_PRES_LINE_MARKERFACECOLOR, clip_on=False)
        self.upper_nu_alfa_modi       = plt.Line2D([],[], linestyle=AN_MODI_LINE_LINESTYLE, marker=AN_MODI_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_MODI_LINE_COLOR, clip_on=False)

        # Lower Surface Lines in the phi-alpha* distribution plot
        # during the program execution these lines will not be re-plotted.

        self.lower_nu_alfa_previous   = plt.Line2D([],[], linestyle=AN_PREV_LINE_LINESTYLE, marker=AN_PREV_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PREV_LINE_COLOR, markerfacecolor=AN_PREV_LINE_MARKERFACECOLOR, clip_on=False)
        self.lower_nu_alfa_current    = plt.Line2D([],[], linestyle=AN_CURR_LINE_LINESTYLE, marker=AN_CURR_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_CURR_LINE_COLOR, markerfacecolor=AN_CURR_LINE_MARKERFACECOLOR, clip_on=False)
        self.lower_nu_alfa_prescribed = plt.Line2D([],[], linestyle=AN_PRES_LINE_LINESTYLE, marker=AN_PRES_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_PRES_LINE_COLOR, markerfacecolor=AN_PRES_LINE_MARKERFACECOLOR, clip_on=False)
        self.lower_nu_alfa_modi       = plt.Line2D([],[], linestyle=AN_MODI_LINE_LINESTYLE, marker=AN_MODI_LINE_MARKER, linewidth=AN_PLOT_LINEWIDTH, markersize=AN_PLOT_MARKERSIZE, color=AN_MODI_LINE_COLOR, clip_on=False)

        self.cursor_edit_line, = self.an_ax.plot([], [], AN_SPLN_LINE_LINESTYLE, picker=True, color=AN_SPLN_LINE_COLOR, linewidth=AN_PLOT_LINEWIDTH)

        # Flags
        # =====
        self.ready_to_interact = False               
        # holds a flag to signal if program is ready to run.
        # purpose is to stop errors from occurring by accidental key presses
        # prior to loading files.

        self.edit_mode = False

    def gen_gui_fig(self):

        # Setting up the main window/figure

        self.gui_fig = Figure(figsize=(12, 7))
        grid = plt.GridSpec(4,2, wspace=0.1, hspace=0.2)

        # Setting up the 3 main axes
        # ue_ax : velocity distribution axes
        # xy_ax : x,y airfoil contour axes
        # an_ax : alpha*-nu axes

        self.ue_ax = self.gui_fig.add_subplot(grid[:3, 0])
        self.xy_ax = self.gui_fig.add_subplot(grid[ 3, 0])
        self.an_ax = self.gui_fig.add_subplot(grid[:3, 1])

        self.setup_axes()

        self.gui_fig.subplots_adjust(left=0.05, right=0.98, top=0.96, bottom=0.08, hspace = 0.02, wspace=0.02)
        self.gui_fig.canvas.mpl_connect('button_press_event', self.on_click)

    def setup_axes(self):
        """
        initializes the axes
        """
        self.ue_ax.n_untouch = 0
        self.xy_ax.n_untouch = 0
        self.an_ax.n_untouch = 1 # spline will be untouched

        self.ue_ax.set_title(r'$Velocity\ Distribution$')
        self.ue_ax.set_ylabel(r'$V/V_{\infty}$')

        self.xy_ax.set_xlabel(r"$x/c$")
        self.xy_ax.set_ylabel(r"$y/c$")

        self.an_ax.set_title(r'$\alpha^*(\phi) - Upper$')
        self.an_ax.set_xlabel(r"$\phi$")
        self.an_ax.grid(True)

        self.xy_ax.axes.set_aspect('equal', 'datalim')
        # self.an_ax.axes.set_aspect('equal', 'datalim')

        self.setup_axes_limits()

    def setup_axes_limits(self):
        """
        initializes the axes limits
        """
        self.ue_ax.set_xlim(-0.08, 1.08)
        self.ue_ax.set_ylim(0, 2.5)

        self.xy_ax.set_xlim(-0.08, 1.08)

        if self.active_surface == "Lower":
            self.an_ax.set_xlim(*AN_PLOT_XLIMITS_LOWER)
            self.an_ax.set_ylim(*(tuple(reversed(AN_PLOT_YLIMITS)) if AN_FLIP_YAXIS_LOWER_SURFACE else AN_PLOT_YLIMITS))
        if self.active_surface == "Upper":
            self.an_ax.set_xlim(*AN_PLOT_XLIMITS_UPPER)
            self.an_ax.set_ylim(*AN_PLOT_YLIMITS)

    def clear_axes(self):
        """
        clears all axes data such that new session with new airfoil can be loaded.
        """
        self.ue_ax.clear()
        # self.ue_ax.collections=[]

        self.xy_ax.clear()
        # self.xy_ax.collections=[]

        self.clear_an_ax()

        self.upper_nu_alfa_previous.set_data([],[]) 
        self.upper_nu_alfa_current.set_data([],[]) 
        self.upper_nu_alfa_prescribed.set_data([],[])
        self.upper_nu_alfa_modi.set_data([],[])

        self.lower_nu_alfa_previous.set_data([],[]) 
        self.lower_nu_alfa_current.set_data([],[]) 
        self.lower_nu_alfa_prescribed.set_data([],[])
        self.lower_nu_alfa_modi.set_data([],[])

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

            
    def on_click(self, event):
        """
        All the mouse click events goes here
        """
        if not self.ready_to_interact: return
        if not self.edit_mode: return
        if event.inaxes!=self.an_ax: return

        # Left click
        if event.button == 1:
            self.cursor_edit_line_points.append([event.xdata,event.ydata])
            self.cursor_edit_line_points.sort()
            self.cursor_edit_line.set_data(*list(zip(*self.cursor_edit_line_points)))
            self.gui_fig.canvas.draw()

        # Right Click and spline is actually built
        if event.button == 3:
            self.apply_edits(event)
            self.gui_fig.canvas.draw()

    def backup_zoomed_limits(self, surface):
        """
        save zoomed limits so that switching between upper and lower surfaces cause resetting limits
        """
        if surface == self.active_surface: return
        if surface == "Upper":
            self.lower_xlim = self.an_ax.get_xlim()
            self.lower_ylim = self.an_ax.get_ylim()
        if surface == "Lower":
            self.upper_xlim = self.an_ax.get_xlim()
            self.upper_ylim = self.an_ax.get_ylim()

    def select_surface(self, surface, first_time=False):
        """
        Callback function that switches the upper and lower surfaces
        through the radio buttons.
        Depending on the preferences:
            y-axis is inverted upon switching.
        """
        self.reset_toolbar()
        self.clear_an_ax()
        if surface =="Upper":
            # backup zoomed limits if applicable.
            if not first_time:
                self.backup_zoomed_limits(surface)
            self.active_surface = "Upper"

            self.an_ax.set_xlim(*self.upper_xlim)
            self.an_ax.set_ylim(*self.upper_ylim)

            self.an_ax.set_title(r'$\alpha^*(\phi) - Upper$')

            # axes transformation between ax limits and pixels are handled
            # automatically by ax.add_line(...)
            # ax.lines = [..] wouldn't work the same way

            self.an_ax.add_line(self.upper_nu_alfa_previous)
            self.an_ax.add_line(self.upper_nu_alfa_current)
            self.an_ax.add_line(self.upper_nu_alfa_prescribed)
            self.an_ax.add_line(self.upper_nu_alfa_modi)

            # load_line makes the Line2D object which is passed active
            # in the interactive plot.

            self.load_line(self.upper_nu_alfa_modi)

        if surface =="Lower":
            # backup zoomed limits if applicable.
            if not first_time:
                self.backup_zoomed_limits(surface)
            self.active_surface = "Lower"

            self.an_ax.set_xlim(*self.lower_xlim)
            self.an_ax.set_ylim(*self.lower_ylim)

            self.an_ax.set_title(r'$\alpha^*(\phi) - Lower$')

            # axes transformation between pixel and ax limits are handled
            # automatically by ax.add_line(...)
            # ax.lines = [..] wouldn't work the same way

            self.an_ax.add_line(self.lower_nu_alfa_previous)
            self.an_ax.add_line(self.lower_nu_alfa_current)
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

    def toggle_previous_plots(self, event):
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
        self.gui_fig.canvas.draw()

    def toggle_grid_lines(self, event):
        """
        Toggles the grid lines on the an_ax.
        Will make effect immediately
        """
        self.GRID_ON = bool(event)
        self.an_ax.grid(self.GRID_ON)
        self.gui_fig.canvas.draw()

    def set_edit_mode_off(self):
        self.edit_mode = False
        self.btn_start_edits.setStyleSheet('QPushButton {color: black;}')

    def start_cursor_edits(self, event):
        self.reset_toolbar()
        self.edit_mode = not self.edit_mode
        self.btn_start_edits.setStyleSheet('QPushButton {color: red;}' if self.edit_mode else 'QPushButton {color: black;}')
        if not self.edit_mode: self.cancel_cursor_inputs()

    def cancel_cursor_inputs(self, event=None):
        """
        Resets the cursor edit line in to an empty line.
        Simple means to start over with a new cursor edit line.
        """
        self.reset_toolbar()
        if not self.ready_to_interact: return
        self.cursor_edit_line.set_data([],[])
        self.cursor_edit_line_points = self.cursor_edit_line.get_xydata().tolist()
        self.set_edit_mode_off()
        self.gui_fig.canvas.draw()

    def apply_edits(self, event):
        """
        Cursor edits are applied to the green line from the red line
        """
        self.reset_toolbar()
        # Better protection than if self.cursor_edit_line_points because one point cannot make spline 
        if len(self.cursor_edit_line_points)>1: 
            self.set_edit_mode_off()
            x_data, y_data = self.nu_alfa.get_data()
            spline = interp1d(*np.array(self.cursor_edit_line_points).T, 
                               kind='linear', 
                               bounds_error=False)
            new_y = spline(x_data)
            self.nu_alfa.set_ydata(np.where(np.isnan(new_y), y_data, new_y))
        self.save_edits_to_file()
        self.cancel_cursor_inputs()

    def save_edits_to_file(self):
        """
        Saves green line data in to the profoil.in file
        """
        nu_upper, alfa_upper = self.upper_nu_alfa_modi.get_data()
        nu_lower, alfa_lower = self.lower_nu_alfa_modi.get_data()
        nu_list = list(nu_upper) + list(nu_lower)
        alfa_list = list(alfa_upper) + list(alfa_lower)
        p_intf.gen_buffer()
        p_intf.gen_input_file(nu_list, alfa_list, len(nu_upper))

    def undo_edits(self, event):
        """
        This callback function resets the modifiable phi-alpha* distribution
        back to the current converged data from the most recent run. 
        Typically used when the line edits
        has to be reverted.
        """
        self.reset_toolbar()
        if not self.ready_to_interact: return
        self.cancel_cursor_inputs()
        self.upper_nu_alfa_modi.set_data(*self.upper_nu_alfa_current.get_data())
        self.lower_nu_alfa_modi.set_data(*self.lower_nu_alfa_current.get_data())
        self.save_edits_to_file()
        self.gui_fig.canvas.draw()

    def plot_from_file(self, event):
        """
        Reads profoil.in file in the work directory and updates the green line
        This action confirms any manual modifications if applicable
        """
        self.reset_toolbar()
        nu, alfa, ile, phis = p_intf.extract_dmp("profoil.in")

        nu_upper = nu[:ile]
        alfa_upper = alfa[:ile]

        nu_lower = nu[ile:]
        alfa_lower = alfa[ile:]

        self.upper_nu_alfa_modi.set_data(nu_upper,alfa_upper)
        self.lower_nu_alfa_modi.set_data(nu_lower,alfa_lower)
        self.gui_fig.canvas.draw()

    def run_profoil(self, event=None):
        """
        Executes PROFOIL with the following steps.
        1. Backup the previous line.    # For reloading as required
        2. Resets the cursor edit line. # Because after the run cursor edit line should not be there.
        3. Creates buffer.in from the existing profoil.in file.
        4. Creates a new profoil.in file by replacing the FOIL lines with the data in the graph.
        5. Prints out the profoil.log file.
        """
        self.reset_toolbar()
        if not self.ready_to_interact: return
        self.set_edit_mode_off()
        self.bkp_previous_line()
        self.cancel_cursor_inputs()
        self.run_from_profoil_in()
        self.gui_fig.canvas.draw()

    def revert(self, event):
        """
        This callback function loads the converged data from the previous run
        typically used when something goes wrong with the current run.
        Equivalent to loading buffer.in instead of profoil.in in the work dir.
        """
        self.reset_toolbar()
        if not self.ready_to_interact: return
        if not self.upper_nu_alfa_previous.get_data()[0]: return
        self.set_edit_mode_off()
        self.cancel_cursor_inputs()
        p_intf.swap_buffer()
        self.run_profoil()
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

    def proc_make_line_untouchable(self, ax, plot_index=-1):
        """
        plot list is divided into 2 main sections.
        untouchable plots ; these hold fixed REF lines
        touchable plots   ; these hold variable plots.
        untouchable plots were pushed towards the beginning of the
        plot list such that the remaining plots can be modified with
        slicing with ease
        """
        plots = ax.lines
        reserve_plot = plots[plot_index]
        del plots[plot_index]
        plots.insert(ax.n_untouch, reserve_plot)
        ax.n_untouch += 1

    def remove_last_untouchable(self, ax):
        """
        Pops the last object from the "untouchable plots" section of ax.lines list
        """
        plots = ax.lines
        del plots[ax.n_untouch -1]
        ax.n_untouch -= 1

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
        n_cols = len(self.ue_lines.keys())
        n_ue_preserve = n_cols * n_prev_plots # alphas give the number of lines

        # make the previous plots "old" [greyed out and dashed etc]
        self.proc_make_ax_old(self.ue_ax, n_ue_preserve)
    
        # plots the velocity distribution
        # color of the original plot is extracted back to make the upper and lower markers.
        for alpha in sorted(self.ue_lines.keys(), key=float):
            p = self.ue_ax.plot(self.ue_lines[alpha]['x'], self.ue_lines[alpha]['v_vinf'], label = "{:5.2f}".format(alpha), lw=UE_PLOT_LINEWIDTH, color=UE_PLOT_COLOR, clip_on=False)
            self.ue_ax.scatter(self.upper_vel_markers[alpha]['x'], self.upper_vel_markers[alpha]['v_vinf'], color=p[-1].get_color(), marker=UPPER_SURFACE_PHI_MARKER, s=UPPER_SURFACE_PHI_MARKER_SIZE, clip_on=False)
            self.ue_ax.scatter(self.lower_vel_markers[alpha]['x'], self.lower_vel_markers[alpha]['v_vinf'], color=p[-1].get_color(), marker=LOWER_SURFACE_PHI_MARKER, s=LOWER_SURFACE_PHI_MARKER_SIZE, clip_on=False)

        # legend is not used in the current implementation because Alphas are just dummy variables.
        # can modify easily in the future if Alphas to be read from the .in file.
        # self.ue_ax.legend(fontsize ='small', frameon = False, loc="upper right")

        self.gui_fig.canvas.draw()

    def bkp_previous_line(self):
        """
        data from "current" plot sets data on "previous" plot
        """
        self.upper_nu_alfa_previous.set_data(*self.upper_nu_alfa_current.get_data())
        self.lower_nu_alfa_previous.set_data(*self.lower_nu_alfa_current.get_data())

    def clear_an_ax(self):
        """
        Removes all lines except the "untouchable plots" section
        ax.clear(...) wouldn't work here because it resets all the limits and
        de-reference the axes from the cursor editor.
        """
        for line in self.an_ax.lines[self.an_ax.n_untouch:]: 
            line.remove()

    def plot_nu_alfa(self):
        """
        As per the overall description on the top, plotting of phi-alpha* distribution
        does not generate new plot lines (Line2D objects) using ax.plot(...)
        The state of these 8 lines will be maintained with the same ID by changing 
        the data these lines hold. This method vastly eases off the surface switching.
        """
        self.upper_nu_alfa_prescribed.set_data(*self.upper_nu_alfa_modi.get_data())
        self.upper_nu_alfa_modi.set_data(self.nu_upper, self.alfa_upper)
        self.upper_nu_alfa_current.set_data(self.nu_upper, self.alfa_upper)

        self.lower_nu_alfa_prescribed.set_data(*self.lower_nu_alfa_modi.get_data())
        self.lower_nu_alfa_modi.set_data(self.nu_lower, self.alfa_lower)
        self.lower_nu_alfa_current.set_data(self.nu_lower, self.alfa_lower)

    def overlay_dat(self, datfile, skiprows):
        """
        This function overlays a given dat file contour in the xy plot.
        File formats with different number of header are supported
        """
        try:
            x,y = np.loadtxt(Path(datfile), skiprows=skiprows).T
        except:
            self.overlay_error_dialog()
            return

        self.xy_ax.plot(x, y, OVERLAY_LINESTYLE, lw=OVERLAY_LINEWIDTH, color=OVERLAY_LINECOLOR, markersize=OVERLAY_MARKERSIZE, clip_on=False)
        self.proc_make_line_untouchable(self.xy_ax)
        self.gui_fig.canvas.draw()

    def clear_overlay(self):
        """ 
        This function removes the the overlay in LIFO order
        If more than one overlay being added the last one
        will be cleared off first
        """
        self.remove_last_untouchable(self.xy_ax)
        self.gui_fig.canvas.draw()

    def update_file_view(self):
        """
        Updates the text boxes in the File View tab
        """
        self.plainTextEdit_profoil_log.setPlainText(p_intf.catfile(BINDIR/"profoil.log", tail=0))
        self.plainTextEdit_profoil_in.setPlainText(p_intf.catfile(BINDIR/"profoil.in", tail=0))

    def update_summary_text(self):
        """
        updates the summary label in the design view
        """
        self.lbl_summary.setText(p_intf.catfile(BINDIR/"profoil.log", tail=14))

    def extract_all_profoil_data(self):
        """
        Once the PROFOIL is finished running, the data will be in the BINDIR.
        This functions updates all the relevant fields in the UI
        from the PROFOIL output files in one go
        """
        self.x,                \
        self.y,                \
        self.xy_marker_upper,  \
        self.xy_marker_lower,  \
        self.ue_lines,         \
        self.upper_vel_markers,\
        self.lower_vel_markers,\
        self.nu_upper,         \
        self.alfa_upper,       \
        self.nu_lower,         \
        self.alfa_lower,       \
        self.ile = p_intf.extract_all_data()
       
    def run_from_profoil_in(self):
        """
        Executes PROFOIL when the profoil.in file is ready in the WORKDIR
        """

        # copy profoil.in file from work_directory in to bin directory
        # execute profoil
        # bring all the output files back in to work_directory
        # last step is for conceptual isolation between bin and work
        # because the airfoil designer is supposed to work on work_directory

        p_intf.work2bin()
        p_intf.exec_profoil()
        p_intf.bin2work()

        # profoil run may or may not have been successful.
        # either way, file view has to be updated.
        # conditional logic follows

        self.update_file_view()
        
        if p_intf.is_design_converged():
            p_intf.bin2work()
            self.extract_all_profoil_data()
            self.update_summary_text()
            self.plot_ue()
            self.plot_xy()
            self.plot_nu_alfa()

        else:
            self.failure_error_dialog()

    def initial_plot(self):
        """
        Initial plot is called once at the initial setup. 
        Before calling initial_plot its required to have run_from_profoil_in(...) called.
        """     
        self.select_surface("Upper", first_time =True)
        self.gui_fig.canvas.draw()

    def load_in_file(self, in_file=None):
        """
        Loads a *.in file in to the program. Keeps on calling until a valid file is provided.
        1. Sets the ready_to_interact flag to make sure no errors will occur by pressing a random button. 
        2. copies *.in file in to WORKDIR as profoil.in
        3. Runs PROFOIL
        """
        in_file = Path(in_file) if in_file else Path(input("Please specify the input file: "))
        self.ready_to_interact = True
        p_intf.save2profoil_in(in_file.open().read())
        self.run_from_profoil_in()
        self.initial_plot() 

    def save_airfoil(self, out_file):
        """
        Saves the profoil.in file from the WORKDIR in to a specified location with a given name.
        For the ease of use, if the given path does not exist, the program creates the path for you. 
        """
        file_path = Path(out_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w") as f:
            f.write(Path(WORKDIR/"profoil.in").open().read())
