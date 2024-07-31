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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import key_press_handler

from GUIMainWindow import Ui_MainWindow
from profoil_canvas import ProfoilCanvas
from preferences import *
import profoil_interface as p_intf

"""
Below is a monkey patch to handle a possible bug in matplotlib. 
regardless of the back-end, matplotlib tool-bar home-button, doesn't appear to redraw even when the frameon=True. 
This results in messed up axis limits on zoom-> home.
Upon multiple failed attempts to fix this issue in a pragmatic way, below decorator is introduced
to wrap the home button with an additional axis limit change. 
"""

# home = NavigationToolbar.home
# def patched_home(self, *args, **kwargs):
#     home(self, *args, **kwargs)
#     ui.setup_axes_limits()
# NavigationToolbar.home = patched_home


class ProfoilUI(QtWidgets.QMainWindow, Ui_MainWindow, ProfoilCanvas):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ProfoilCanvas.__init__(self)

    def load_canvas(self):
        """
        creates FigureCanvas from matplotlib Figure and loads into PyQt Widget space
        """
        self.canvas = FigureCanvas(self.gui_fig)
        self.verticalLayout_canvas.addWidget(self.canvas)

        self.tool_bar = self.gen_toolbar()
        self.verticalLayout_canvas.addWidget(self.tool_bar)

    def gen_toolbar(self):
        """
        creates a custom tool bar without unnecessary buttons to minimize confusion
        """
        tool_bar = NavigationToolbar(self.canvas, None)
        selected_buttons = ['Home', 'Pan','Zoom','Save']
        for x in tool_bar.actions():
            if x.text() not in selected_buttons:
                tool_bar.removeAction(x)
        return tool_bar

    def connect_widget_events(self):
        """
        maps button/menu/combo_box and tab signals to functions
        """
        # Button Events
        self.btn_start_edits.clicked.connect(self.start_cursor_edits)
        self.btn_cancel.clicked.connect(self.cancel_cursor_inputs)
        self.btn_apply_edits.clicked.connect(self.apply_edits)
        self.btn_undo.clicked.connect(self.undo_edits)
        self.btn_plot_from_file.clicked.connect(self.plot_from_file)
        self.btn_run_profoil.clicked.connect(self.run_profoil)
        self.btn_revert.clicked.connect(self.revert)
        self.btn_save_profoil_in.clicked.connect(self.save_planTextEdit_to_profoil)

        # Menu Events
        self.actionOpen.triggered.connect(self.menu_file_open)
        self.actionSave.triggered.connect(self.menu_file_save)
        self.actionProfoil_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=0))
        self.actionXFoil_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=1))
        # self.actionMSES_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=2))
        self.actionClear_Overlay.triggered.connect(self.clear_overlay)

        # CheckBox Events (History and Grid)
        self.checkBox_grid.stateChanged.connect(self.toggle_grid_lines)
        self.checkBox_history.stateChanged.connect(self.toggle_previous_plots)

        # Dropdown Events (Upper / Lower Surface Switch)
        self.combo_switch_surface.currentIndexChanged.connect(self.switch_surface)
        self.combo_switch_surface.currentIndexChanged.connect(self.switch_surface)

    def switch_surface(self, event):
        """
        Switching the surface through the combo box.
        """
        self.select_surface(self.combo_switch_surface.itemText(event))

    def failure_error_dialog(self):
        """ pops a Message box with convergence failure warning """
        QMessageBox.critical(
            self, 
            "Error...", 
            "Design Failed - Please check the .in File")

    def overlay_error_dialog(self):
        """ pops a Message box with file loading error. """
        QMessageBox.information(
            self, 
            "File loading Error...", 
            "Please check the .dat File")

    def loading_warning_dialog(self):
        """ pops a Message box with file loading error. """
        return QMessageBox.warning(
            self, 
            "Active Session", 
            "Current design session is active and all data will be lost - Please confirm",
            QMessageBox.Yes | QMessageBox.Cancel)

    def save_planTextEdit_to_profoil(self):
        """
        saves the profoil.in file view, in to the profoil.in file.
        """
        p_intf.gen_buffer()
        p_intf.save2profoil_in(self.plainTextEdit_profoil_in.toPlainText())

    def menu_file_open(self):
        """
        opens profoil.in file, if a session is current, warning will be shown.
        """
        if self.ready_to_interact:
            if self.loading_warning_dialog() == QMessageBox.Yes:
                self.active_surface = "Upper"
                self.setup_axes()
                self.clear_axes()
            else:
                return

        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,'../runs', "Input File (*.in)")[0]
        if filename:
            self.load_in_file(filename)

    def menu_file_save(self):
        """
        saves profoil.in file
        """
        if not self.ready_to_interact: return
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File' ,'.', "Input File (*.in)")[0]
        if filename:
            self.save_airfoil(filename)

    def overlay_file_open(self, skiprows):
        """
        overlays *.dat file
        """
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,'.', "All Files (*.*)")[0]
        if filename:
            self.overlay_dat(filename, skiprows)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Set the icon
    app.setWindowIcon(QtGui.QIcon("../ui/profoil_ui.ico"))
    
    MainWindow = QtWidgets.QMainWindow()
    ui = ProfoilUI()
    ui.setupUi(MainWindow)
    ui.load_canvas()
    ui.connect_widget_events()
    MainWindow.show()
    app.exec_()
