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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import key_press_handler

from GUIMainWindow import Ui_MainWindow
from profoil_canvas import ProfoilCanvas
from syntax_highligher import CommentHighlighter
from dragndrop import DragDropWindow
from preferences import *
from annotate import annotate_text

import profoil_interface as p_intf
from profoil_interface import WORKDIR, BINDIR
from pathlib import Path

from scipy.interpolate import interp1d
import numpy as np

class ProfoilUI(DragDropWindow, Ui_MainWindow, ProfoilCanvas):
    def __init__(self):
        DragDropWindow.__init__(self)
        ProfoilCanvas.__init__(self)

        # Store the original home method
        original_home = NavigationToolbar.home

        # Monkey patch the home button to fix the axis limit issue
        def patched_home(toolbar_instance, *args, **kwargs):
            # Call the original home function
            original_home(toolbar_instance, *args, **kwargs)
            # Then call the setup_axes_limits method on the ProfoilUI instance
            self.setup_axes_limits()

        # Replace the home method in the toolbar with the patched version
        NavigationToolbar.home = patched_home

        # Add a new parameter to store the last open path
        # this will be changed upon opening a file if KEEP_LAST_OPEN_PATH_AS_DEFAULT is set
        self.default_open_dir = '../runs'

#========================================== EVENT TRIGGERS ==========================================
    def connect_widget_events(self):
        """
        maps button/menu/combo_box and tab signals to functions
        """
        # ================================= START EDITS ==================================
        # -->  BUTTON ACTION
        self.btn_start_edits.clicked.connect(self.start_cursor_edits)
        # -->  FIRST SHORTCUT
        self.edit_shortcut = QShortcut(QKeySequence(SHORTCUT_EDIT), self)
        self.edit_shortcut.activated.connect(self.start_cursor_edits)
        # -->  SECOND SHORTCUT
        # Create the shortcut for Alpha* Cursor edits using the 'E' key, active only in "Design View"
        self.cursor_edit_design_view_shortcut = QShortcut(QKeySequence(SHORTCUT_CURSOR_EDIT_DESIGN_VIEW), self)
        self.cursor_edit_design_view_shortcut.activated.connect(self.start_cursor_edits_design_view)

        # ==================================== CANCEL ====================================
        # -->  BUTTON ACTION
        self.btn_cancel.clicked.connect(self.cancel_cursor_inputs)
        # ->  FIRST SHORTCUT : Create the additional shortcut for "Cancel" using "Ctrl+D"
        self.cancel_shortcut = QShortcut(QKeySequence(SHORTCUT_CANCEL), self)
        self.cancel_shortcut.activated.connect(self.cancel_cursor_inputs)
        #  -->  SECOND SHORTCUT: Create the shortcut for "Cancel" using the 'D' key, active only in "Design View"
        self.cancel_designview_shortcut = QShortcut(QKeySequence(SHORTCUT_CANCEL_DESIGN_VIEW), self)
        self.cancel_designview_shortcut.activated.connect(self.activate_cancel)

        # ================================= APPLY EDITS ==================================
        # -->  BUTTON ACTION
        self.btn_apply_edits.clicked.connect(self.apply_edits)

        # ===================================== UNDO =====================================
        # -->  BUTTON ACTION
        self.btn_undo.clicked.connect(self.undo_edits)
        # -->  FIRST SHORTCUT : Create the shortcut for "Undo" using the 'u' key, active only in "Design View"
        self.undo_shortcut = QShortcut(QKeySequence(SHORTCUT_UNDO), self)
        self.undo_shortcut.activated.connect(self.activate_undo)

        # ================================ PLOT FROM FILE ================================
        # -->  BUTTON ACTION
        self.btn_plot_from_file.clicked.connect(self.plot_from_file)

        # ================================= RUN PROFOIL ==================================
        # -->  BUTTON ACTION
        self.btn_run_profoil.clicked.connect(self.run_profoil)
        # -->  FIRST SHORTCUT : Create the shortcut to trigger "Run Profoil"
        self.run_profoil_shortcut = QShortcut(QKeySequence(SHORTCUT_EXEC), self)
        self.run_profoil_shortcut.activated.connect(self.run_profoil)
        # -->  SECOND SHORTCUT: Create the shortcut for "Run PROFOIL" using the 'R' key, active only in "Design View"
        self.run_profoil_design_view_shortcut = QShortcut(QKeySequence(SHORTCUT_RUN_DESIGN_VIEW), self)
        self.run_profoil_design_view_shortcut.activated.connect(self.run_profoil_design_view)

        # ==================================== REVERT ====================================
        # -->  BUTTON ACTION
        self.btn_revert.clicked.connect(self.revert)
        # -->  FIRST SHORTCUT : Create the shortcut for "Revert" using the 'r' key, active only in "Design View"
        self.revert_shortcut = QShortcut(QKeySequence(SHORTCUT_REVERT), self)
        self.revert_shortcut.activated.connect(self.activate_revert)

        # ============================= [MENU] FILE -> OPEN ==============================
        # -->  MENU ACTION
        self.actionOpen.triggered.connect(self.menu_file_open)
        # --> SHORTCUT BUTTON : New connection for the "File | Open" button /shortcut to trigger "File | Open"
        self.btn_file_open.clicked.connect(self.menu_file_open)
        # --> KEYBOARD SHORTCUT
        self.open_shortcut = QShortcut(QKeySequence(SHORTCUT_OPEN), self)
        self.open_shortcut.activated.connect(self.menu_file_open)

        # ============================= [MENU] FILE -> SAVE ==============================
        # -->  MENU ACTION
        self.actionSave.triggered.connect(self.menu_file_save_as)
        # --> SHORTCUT BUTTON : New connection for the "File | Save As" button
        self.btn_file_save.clicked.connect(self.menu_file_save_as)
        # --> KEYBOARD SHORTCUT
        self.save_as_shortcut = QShortcut(QKeySequence(SHORTCUT_SAVE_AS), self)
        self.save_as_shortcut.activated.connect(self.menu_file_save_as)


        # ============================[MENU] FILE -> SAVE DAT=============================
        # -->  MENU ACTION
        self.actionSave_DAT.triggered.connect(self.menu_file_save_dat)

        # ========================== [MENU] OVERLAY -> XY FILE ===========================
        # -->  MENU ACTION
        self.actionProfoil_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=0))
        # --> SHORTCUT BUTTON : New connections for the "Overlay" actions
        self.btn_overlay_xy.clicked.connect(lambda:self.overlay_file_open(skiprows=0))

        # ========================== [MENU] OVERLAY -> DAT FILE ==========================
        # -->  MENU ACTION
        self.actionXFoil_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=1))
        # --> SHORTCUT BUTTON : New connections for the "Overlay" actions
        self.btn_overlay_dat.clicked.connect(lambda:self.overlay_file_open(skiprows=1))

        # ======================= [MENU] OVERLAY -> CLEAR OVERLAY ========================
        # -->  MENU ACTION
        self.actionClear_Overlay.triggered.connect(self.clear_overlay)
        # --> SHORTCUT BUTTON : New connections for the "Clear Overlay"
        self.btn_overlay_clear.clicked.connect(self.clear_overlay)

        # ====================== [MENU] ABOUT -> PROFOIL/PROFOIL_UI ======================
        # -->  MENU ACTION
        self.actionPROFOIL.triggered.connect(self.menu_about_profoil)
        self.actionPROFOIL_UI.triggered.connect(self.menu_about_profoil_ui)

        # ============================ [FILE VIEW] SAVE EDITS ============================
        # -->  BUTTON ACTION
        self.btn_save_profoil_in.clicked.connect(self.save_planTextEdit_to_profoil)
        # --> KEYBOARD SHORTCUT : Create the shortcut to trigger "Profoil.in Save" in File View
        self.save_shortcut = QShortcut(QKeySequence(SHORTCUT_SAVE), self)
        self.save_shortcut.activated.connect(self.save_on_shortcut)

        # ============================= [FILE VIEW] ANNOTATE =============================
        # -->  BUTTON ACTION
        self.btn_annotate.clicked.connect(self.annotate_profoil_in)
        # --> KEYBOARD SHORTCUT : Create the shortcut for "Annotate"
        self.annotate_shortcut = QShortcut(QKeySequence(SHORTCUT_ANNOTATE), self)
        self.annotate_shortcut.activated.connect(self.annotate_profoil_in)

        # ========================= [FILE VIEW] TOGGLE COMMENTS ==========================
        # --> KEYBOARD SHORTCUT :Create the shortcut for "Toggle Comments"
        self.toggle_comment_shortcut = QShortcut(QKeySequence(SHORTCUT_TOGGLE_COMMENT), self)
        self.toggle_comment_shortcut.activated.connect(self.toggle_comment)

        # =============================== CHECKBOX ACTIONS ===============================
        # -->  TICKBOX ACTION : CheckBox Events (History and Grid)
        self.checkBox_grid.stateChanged.connect(self.toggle_grid_lines)
        self.checkBox_airfoil_grid.stateChanged.connect(self.toggle_airfoil_grid_lines)
        self.checkBox_history.stateChanged.connect(self.toggle_previous_plots)
        # --> KEYBOARD SHORTCUT : Create the shortcut for toggling "History" using the 'h' key, active only in "Design View"
        self.history_toggle_shortcut = QShortcut(QKeySequence(SHORTCUT_HISTORY_TOGGLE), self)
        self.history_toggle_shortcut.activated.connect(self.toggle_history)

        # ======================== RADIO BUTTONS [SELECT SURFACE] ========================
        # Radio button Events (Upper / Lower Surface Switch)
        self.radio_upper_surface.toggled.connect(lambda: self.select_surface("Upper"))
        self.radio_lower_surface.toggled.connect(lambda: self.select_surface("Lower"))
        # --> KEYBOARD SHORTCUT : Create the shortcut to toggle between Upper and Lower surfaces
        self.toggle_surface_shortcut = QShortcut(QKeySequence(SHORTCUT_SURFACE_TOGGLE), self)
        self.toggle_surface_shortcut.activated.connect(self.toggle_surface_if_design_view)

        # ========================= [TAB] SWITCH TO DESIGN VIEW ==========================
        # FIRST SHORTCUT : Create the shortcut to switch to "Design View"
        self.design_view_shortcut = QShortcut(QKeySequence(SHORTCUT_TAB1), self)
        self.design_view_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(0))
        # SECOND SHORTCUT : Create the shortcut for "Design View" using F1
        self.f1_design_view_shortcut = QShortcut(QKeySequence(SHORTCUT_F1_DESIGN_VIEW), self)
        self.f1_design_view_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(0))

        # ========================== [TAB] SWITCH TO FILE VIEW ===========================
        # FIRST SHORTCUT : Create the shortcut to switch to "File View"
        self.file_view_shortcut = QShortcut(QKeySequence(SHORTCUT_TAB2), self)
        self.file_view_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(1))
        # SECOND SHORTCUT : Create the shortcut for "File View" using F2
        self.f2_file_view_shortcut = QShortcut(QKeySequence(SHORTCUT_F2_FILE_VIEW), self)
        self.f2_file_view_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(1))

        # ======================== [TAB] SWITCH TO CONVERGED VIEW ========================
        # FIRST SHORTCUT : Create the shortcut to switch to "Converged Data"
        self.converged_data_shortcut = QShortcut(QKeySequence(SHORTCUT_TAB3), self)
        self.converged_data_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(2))
        # SECOND SHORTCUT : Create the shortcut for "Converged View" using F3
        self.f3_converged_view_shortcut = QShortcut(QKeySequence(SHORTCUT_F3_CONVERGED_VIEW), self)
        self.f3_converged_view_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(2))

        # =================== [MATPLOTLIB] NAVIGATION TOOLBAR ACTIONS ====================
        # Create the shortcut for "Pan" using the space bar, active only in "Design View"
        self.pan_shortcut = QShortcut(QKeySequence(SHORTCUT_PAN), self)
        self.pan_shortcut.activated.connect(self.activate_pan)
                
        # Create the shortcut for "Zoom" using the 'z' key, active only in "Design View"
        self.zoom_shortcut = QShortcut(QKeySequence(SHORTCUT_ZOOM), self)
        self.zoom_shortcut.activated.connect(self.activate_zoom)

        # Create the shortcut for "Home" (reset graphics) using the 'a' key, active only in "Design View"
        self.home_shortcut = QShortcut(QKeySequence(SHORTCUT_HOME), self)
        self.home_shortcut.activated.connect(self.activate_home)

        # Create the shortcut for "Save" using the 's' key, active only in "Design View"
        self.save_button_shortcut = QShortcut(QKeySequence(SHORTCUT_SAVE_BUTTON), self)
        self.save_button_shortcut.activated.connect(self.activate_save)

        # ======================== OTHER SIGNALLING EVENTS->SLOTS ========================

        # Apply the syntax highlighter to the profoil.in text editor
        self.highlighter = CommentHighlighter(self.plainTextEdit_profoil_in.document())

        # Connect textChanged signal to slot
        self.plainTextEdit_profoil_in.textChanged.connect(self.on_profoil_in_text_changed)

        # backup zoomed limits of an_ax so that upper-lower surface switching wont be affected
        self.an_ax.figure.canvas.mpl_connect('draw_event', self.bkp_an_ax_zoomed_limits)

#============================================= DIALOGS ==============================================
    def message_box_without_beep(self, title, text):
        """ pops a Message box with given title and text, without beep """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        
        # Setting icon to avoid beep
        msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def failure_error_dialog(self):
        """ pops a Message box with convergence failure warning, without beep """
        self.message_box_without_beep(title="Error...", text="Design Failed - Please check the .in File")

    def overlay_error_dialog(self):
        """ pops a Message box with file loading error, without beep """
        self.message_box_without_beep(title="File loading Error...", text="Please check the .dat File")

    def menu_about_profoil(self):
        """ pops a Message box with PROFOIL version info """
        try:
            text = open(WORKDIR/"version.txt").read()
        except:
            text = "Version info not available"
        self.message_box_without_beep(title="PROFOIL Version", text=text)

    def menu_about_profoil_ui(self):
        """ pops a Message box with PROFOIL_UI version info """
        self.message_box_without_beep(title="PROFOIL_UI Version", text="Version 1.4 September 2024 / MIT License")

    def loading_warning_dialog(self):
        """ pops a Message box with file loading error. """
        return QMessageBox.question(
            self, 
            "Active Session", 
            "Any unsaved data will be lost.\n          Continue?          ",
            QMessageBox.Yes | QMessageBox.Cancel) if AIRFOIL_CHANGE_WARNING else QMessageBox.Yes

#==================================== CALLBACK FUNCTIONS [MENU] =====================================
    def menu_file_open(self, filename=None):
        """
        opens profoil.in file, if a session is current, warning will be shown.
        """
        if self.ready_to_interact:
            if self.loading_warning_dialog() != QMessageBox.Yes:
                return
            if KEEP_OLD_AIRFOIL_UPON_LOADING:
                self.bkp_previous_line()    

        filename = filename or QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,self.default_open_dir, "Input File (*.in)")[0]
        if filename:
            self.load_in_file(filename)
            self.current_file_basename = Path(filename).stem
            # Store the path to be used for Save As
            if KEEP_LAST_OPEN_PATH_AS_DEFAULT:
                self.default_open_dir = str(Path(filename).parent)

    def menu_file_save_as(self):
        """
        saves profoil.in file
        """
        if not self.ready_to_interact: return
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', self.default_open_dir, "Input File (*.in)")[0]
        if filename:
            self.save_airfoil(filename)
            self.current_file_basename = Path(filename).stem
            # Store the path to be used for Save As
            if KEEP_LAST_OPEN_PATH_AS_DEFAULT:
                self.default_open_dir = str(Path(filename).parent)

    def menu_file_save_dat(self):
        """
        saves resulting airfoil coordinates in XFoil format
        """
        if not self.ready_to_interact: return
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save DAT', self.default_open_dir, "Dat File (*.dat)")[0]
        if filename:
            self.save_as_dat(self.current_file_basename, filename)

    def overlay_file_open(self, skiprows):
        """
        Overlays *.xy or *.dat file based on skiprows (0 for .xy, 1 for .dat)
        """
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,'.', "All Files (*.*)")[0]
        if filename:
            self.overlay_dat(filename, skiprows)

#=================================== CALLBACK FUNCTIONS [BUTTONS] ===================================
    def save_planTextEdit_to_profoil(self):
        """
        saves the profoil.in file view, in to the profoil.in file.
        """
        p_intf.gen_buffer()
        p_intf.save2profoil_in(self.plainTextEdit_profoil_in.toPlainText())

        # upon saving change the save button color back to black
        self.btn_save_profoil_in.setStyleSheet('QPushButton {color: black; font-style: normal;}')

    def start_cursor_edits(self, event=None):
        self.reset_toolbar()
        self.edit_mode = not self.edit_mode
        self.btn_start_edits.setStyleSheet('QPushButton {color: red;}' if self.edit_mode else 'QPushButton {color: black;}')
        if self.edit_mode:
            self.canvas.setCursor(QtCore.Qt.CrossCursor)  # Keep crosshair during edit mode
        else:
            self.canvas.setCursor(QtCore.Qt.ArrowCursor)  # Reset to default cursor when exiting edit mode
            self.cancel_cursor_inputs()

    def set_edit_mode_off(self):
        self.edit_mode = False
        self.btn_start_edits.setStyleSheet('QPushButton {color: black;}')

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
        self.canvas.setCursor(QtCore.Qt.ArrowCursor)  # Reset to default cursor on the canvas
        self.gui_fig.canvas.draw()

    def apply_edits(self, event=None):
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
        self.canvas.setCursor(QtCore.Qt.ArrowCursor) # Reset to default cursor on the canvas

    def undo_edits(self, event=None):
        """
        This callback function resets the modifiable phi-alpha* distribution
        back to the current converged data from the most recent run. 
        Typically used when the line edits
        has to be reverted.
        """
        self.reset_toolbar()
        if not self.ready_to_interact: return
        self.cancel_cursor_inputs()
        self.upper_nu_alfa_modi.set_data(*self.upper_nu_alfa_prescribed.get_data())
        self.lower_nu_alfa_modi.set_data(*self.lower_nu_alfa_prescribed.get_data())
        self.save_edits_to_file()
        self.gui_fig.canvas.draw()

    def plot_from_file(self, event=None):
        """
        Reads profoil.in file in the work directory and updates the green line
        This action confirms any manual modifications if applicable
        """
        self.reset_toolbar()
        nu, alfa, ile, phis = p_intf.extract_dmp(WORKDIR/"profoil.in")

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
        if not self.ready_to_interact: return
        self.reset_toolbar()
        self.set_edit_mode_off()
        self.bkp_previous_line()
        self.cancel_cursor_inputs()
        self.run_from_profoil_in()
        self.gui_fig.canvas.draw()

    def revert(self, event=None):
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

#================================== CALLBACK FUNCTIONS [SHORTCUTS] ==================================
    def save_on_shortcut(self):
        # Check if the current tab is "File View" (index 1)
        if self.tabWidget.currentIndex() == 1:
            self.save_planTextEdit_to_profoil()

    def toggle_comment(self):
        cursor = self.plainTextEdit_profoil_in.textCursor()
        # Check if the current tab is "File View" (index 1) and part of text is being selected
        if (self.tabWidget.currentIndex() == 1 and cursor.hasSelection()):
            selection = cursor.selection().toPlainText()
            selected_lines = selection.split("\n")

            modified_lines = [line[1:] if line.startswith(("#","!")) else COMMENT_MARKER+line for line in selected_lines]
            cursor.insertText("\n".join(modified_lines))

    def activate_pan (self): self.activate_tool_bar_action("Pan" )
    def activate_zoom(self): self.activate_tool_bar_action("Zoom")
    def activate_home(self): self.activate_tool_bar_action("Home")
    def activate_save(self): self.activate_tool_bar_action("Save")

    def activate_revert(self): self.activate_function_in_design_view(self.btn_revert)
    def activate_cancel(self): self.activate_function_in_design_view(self.btn_cancel)
    def activate_undo  (self): self.activate_function_in_design_view(self.btn_undo  )

    def cancel_design_view(self)            : self.activate_function_in_design_view(self.cancel_cursor_inputs)
    def run_profoil_design_view(self)       : self.activate_function_in_design_view(self.run_profoil)
    def toggle_surface_if_design_view(self) : self.activate_function_in_design_view(self.toggle_surface_selection)
    def start_cursor_edits_design_view(self): self.activate_function_in_design_view(self.start_cursor_edits)
    
    def toggle_history(self):
        # Ensure the "Design View" tab is active
        if self.tabWidget.currentIndex() == 0:
            # Toggle the check state of the "History" checkbox
            current_state = self.checkBox_history.isChecked()
            self.checkBox_history.setChecked(not current_state)
            # Call the function to toggle the visibility of the history
            self.toggle_previous_plots(not current_state)

#===================================== CALLBACK HELPERS OR MISC =====================================
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

    def save_airfoil(self, out_file):
        """
        Saves the profoil.in file from the WORKDIR in to a specified location with a given name.
        For the ease of use, if the given path does not exist, the program creates the path for you. 
        """
        file_path = Path(out_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w") as f:
            f.write(Path(WORKDIR/"profoil.in").open().read())

    def save_as_dat(self, header, out_file):
        """
        Saves the profoil.xy file from the WORKDIR in to a specified location with a given name in XFoil format.
        For the ease of use, if the given path does not exist, the program creates the path for you. 
        """
        file_path = Path(out_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w") as f:
            f.write(f"{header}\n"+Path(WORKDIR/"profoil.xy").open().read())

    def on_profoil_in_text_changed(self):
        """
        Indicates there are some unsaved changes in the profoil.in file
        by changing the color of the "Save" button
        """
        self.btn_save_profoil_in.setStyleSheet('QPushButton {color: red; font-style: italic;}')

    def activate_tool_bar_action(self, action_name):
        # Ensure the "Design View" tab is active
        if self.tabWidget.currentIndex() == 0:
            # Find the Pan action in the toolbar and trigger it
            for action in self.tool_bar.actions():
                if action.text() == action_name:
                    action.trigger()
                    break

    def activate_function_in_design_view(self, func):
        # Ensure the "Design View" tab is active
        if self.tabWidget.currentIndex() == 0:
            # Trigger the revert button action or execute the function
            try:
                func.click()
            except:
                func()

    def toggle_surface_selection(self):
        # Toggle between Upper and Lower surface selection
        if self.radio_upper_surface.isChecked():
            self.radio_lower_surface.setChecked(True)
        else:
            self.radio_upper_surface.setChecked(True)  

#======================================== UTILITY FUNCTIONS =========================================
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
        tool_bar = NavigationToolbar(self.canvas, self)
        selected_buttons = ['Home', 'Pan','Zoom','Save']
        for x in tool_bar.actions():
            if x.text() not in selected_buttons:
                tool_bar.removeAction(x)
        return tool_bar

    def load_in_file(self, in_file=None):
        """
        Loads a *.in file in to the program.
        1. Sets the ready_to_interact flag to make sure no errors will occur by pressing a random button. 
        2. copies *.in file in to WORKDIR as profoil.in
        3. Runs PROFOIL
        """
        self.ready_to_interact = True
        if not KEEP_OLD_AIRFOIL_UPON_LOADING:
            self.setup_axes_limits()
            self.clear_axes()

        p_intf.save2profoil_in(Path(in_file).open().read())
        self.run_from_profoil_in()

        # Keep the current state of the surface selection
        if self.radio_upper_surface.isChecked():
            self.select_surface("Upper")
        else:
            self.select_surface("Lower")

        self.gui_fig.canvas.draw()

    def run_from_profoil_in(self):
        """
        Executes PROFOIL when the profoil.in file is ready in the WORKDIR
        """
        # execute profoil
        p_intf.exec_profoil()

        # profoil run may or may not have been successful.
        # either way, file view has to be updated.
        # conditional logic follows for the graphics

        self.update_file_view()
        self.update_converged_view()
        
        if p_intf.is_design_converged():
            self.extract_all_profoil_data()
            self.update_summary_text()
            self.plot_ue()
            self.plot_xy()
            self.plot_nu_alfa()
        else:
            self.failure_error_dialog()

    def extract_all_profoil_data(self):
        """
        Once the PROFOIL is finished running, the data will be in the WORKDIR.
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
        self.ile,              \
        self.nu_conv_upper,    \
        self.alfa_conv_upper,  \
        self.nu_conv_lower,    \
        self.alfa_conv_lower = p_intf.extract_all_data()

    def update_file_view(self):
        """
        Updates the text boxes in the File View tab
        """
        self.plainTextEdit_profoil_log.setPlainText(p_intf.catfile(WORKDIR/"profoil.log", tail=0))
        self.plainTextEdit_profoil_in.setPlainText(p_intf.catfile(WORKDIR/"profoil.in", tail=0))

        # upon updating  plainTextEdit_profoil_in change the save button color back to black
        self.btn_save_profoil_in.setStyleSheet('QPushButton {color: black;}')

    def update_converged_view(self):
        """
        Updates the text boxes in the File View tab
        """
        self.plainTextEdit_profoil_dmp.setPlainText(p_intf.catfile(WORKDIR/"profoil.dmp", tail=0))
        self.plainTextEdit_profoil_xy.setPlainText(p_intf.catfile(WORKDIR/"profoil.xy", tail=0))

    def update_summary_text(self):
        """
        updates the summary label in the design view
        """
        self.lbl_summary.setText(p_intf.extract_summary(WORKDIR/"profoil.log"))

    def annotate_profoil_in(self):
        """
        note: setting text with setPlainText() just wont work here
        because it wipes out the Qtextedit undo() stack
        hence the cursor.intertText() is used
        """
        cursor = self.plainTextEdit_profoil_in.textCursor()
        if cursor.hasSelection():
            annotated_text = annotate_text(cursor.selection().toPlainText())
        else:
            annotated_text = annotate_text(self.plainTextEdit_profoil_in.toPlainText())
            cursor.select(QtGui.QTextCursor.Document)
        
        cursor.insertText(annotated_text)
        
        # users should be able to undo the annotation straight away if the outcome is not satisfactory
        # hence the focus is set on the plainTextEdit_profoil_in
        self.plainTextEdit_profoil_in.setFocus()

    def amend_shortcut_names(self):
        """
        Append menu items and button names with the shortcuts given in the preferences.py
        menu action text has to be fixed length for better visual appeal
        """
        if SHOW_SHORTCUTS_ON_BUTTONS == "NONE": return
        # Menu Actions
        MENU_TEXT_LENGTH = 24
        self.actionOpen.setText(f"{self.actionOpen.text().ljust(MENU_TEXT_LENGTH-len(SHORTCUT_OPEN))}({SHORTCUT_OPEN})")
        self.actionSave.setText(f"{self.actionSave.text().ljust(MENU_TEXT_LENGTH-len(SHORTCUT_SAVE_AS))}({SHORTCUT_SAVE_AS})")

        # Design View buttons        
        self.btn_start_edits.setText(
             self.btn_start_edits.text()+
             f" ({SHORTCUT_CURSOR_EDIT_DESIGN_VIEW}"+
             f"{', '+SHORTCUT_EDIT   if SHOW_SHORTCUTS_ON_BUTTONS =='FULL' else ''})")
        self.btn_cancel.setText(
             self.btn_cancel.text()+
             f" ({SHORTCUT_CANCEL_DESIGN_VIEW}"+
             f"{', '+SHORTCUT_CANCEL if SHOW_SHORTCUTS_ON_BUTTONS =='FULL' else ''})")
        self.btn_run_profoil.setText(
             self.btn_run_profoil.text()+
             f" ({SHORTCUT_RUN_DESIGN_VIEW}"+
             f"{', '+SHORTCUT_EXEC   if SHOW_SHORTCUTS_ON_BUTTONS =='FULL' else ''})")
        self.btn_undo.setText(f"{self.btn_undo.text()} ({SHORTCUT_UNDO})")
        self.btn_revert.setText(f"{self.btn_revert.text()} ({SHORTCUT_REVERT})")
        
        # Design View labels/checkbox
        self.checkBox_history.setText(f"{self.checkBox_history.text()} ({SHORTCUT_HISTORY_TOGGLE})")
        self.lbl_surface_sel.setText(f"{self.lbl_surface_sel.text()} ({SHORTCUT_SURFACE_TOGGLE})")

        # FileView Buttons
        self.btn_save_profoil_in.setText(f"{self.btn_save_profoil_in.text()} ({SHORTCUT_SAVE})")
        self.btn_annotate.setText(f"{self.btn_annotate.text()} ({SHORTCUT_ANNOTATE})")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Set the icon
    app.setWindowIcon(QtGui.QIcon("icon.ico"))
    
    ui = ProfoilUI()
    ui.setupUi(ui)
    ui.load_canvas()
    ui.connect_widget_events()
    ui.amend_shortcut_names()
    ui.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
    ui.show()
    app.exec_()
