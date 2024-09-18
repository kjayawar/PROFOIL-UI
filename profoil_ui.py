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
        self.btn_annotate.clicked.connect(self.annotate_profoil_in)

        # Menu Events
        self.actionOpen.triggered.connect(self.menu_file_open)
        self.actionSave.triggered.connect(self.menu_file_save)
        self.actionProfoil_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=0))
        self.actionXFoil_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=1))
        # self.actionMSES_dat_File.triggered.connect(lambda:self.overlay_file_open(skiprows=2))
        self.actionClear_Overlay.triggered.connect(self.clear_overlay)

        # CheckBox Events (History and Grid)
        self.checkBox_grid.stateChanged.connect(self.toggle_grid_lines)
        self.checkBox_airfoil_grid.stateChanged.connect(self.toggle_airfoil_grid_lines)
        self.checkBox_history.stateChanged.connect(self.toggle_previous_plots)

        # Dropdown Events (Upper / Lower Surface Switch)
        self.combo_switch_surface.currentIndexChanged.connect(self.switch_surface)

        # Apply the syntax highlighter to the profoil.in text editor
        self.highlighter = CommentHighlighter(self.plainTextEdit_profoil_in.document())

        # Connect textChanged signal to slot
        self.plainTextEdit_profoil_in.textChanged.connect(self.on_profoil_in_text_changed)

        # New connection for the "File | Save" button
        self.btn_file_save.clicked.connect(self.menu_file_save)

        # New connection for the "File | Open" button
        self.btn_file_open.clicked.connect(self.menu_file_open)

        # New connections for the "Overlay" buttons
        self.btn_overlay_xy.clicked.connect(lambda:self.overlay_file_open(skiprows=0))
        self.btn_overlay_dat.clicked.connect(lambda:self.overlay_file_open(skiprows=1))
        self.btn_overlay_clear.clicked.connect(self.clear_overlay)

        # Create the shortcut to trigger "File | Open"
        self.open_shortcut = QShortcut(QKeySequence(SHORTCUT_OPEN), self)
        self.open_shortcut.activated.connect(self.menu_file_open)

        # Create the shortcut to trigger "Profoil.in Save"
        self.save_shortcut = QShortcut(QKeySequence(SHORTCUT_SAVE), self)
        self.save_shortcut.activated.connect(self.save_on_shortcut)

        # Create the shortcut to trigger "Start Edits"
        self.edit_shortcut = QShortcut(QKeySequence(SHORTCUT_EDIT), self)
        self.edit_shortcut.activated.connect(self.start_cursor_edits)

        # Create the shortcut to trigger "Run Profoil"
        self.run_profoil_shortcut = QShortcut(QKeySequence(SHORTCUT_EXEC), self)
        self.run_profoil_shortcut.activated.connect(self.run_profoil)

        # Create the shortcut to switch to "Design View"
        self.design_view_shortcut = QShortcut(QKeySequence(SHORTCUT_TAB1), self)
        self.design_view_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(0))
        
        # Create the shortcut to switch to "File View"
        self.file_view_shortcut = QShortcut(QKeySequence(SHORTCUT_TAB2), self)
        self.file_view_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(1))
        
        # Create the shortcut to switch to "Converged Data"
        self.converged_data_shortcut = QShortcut(QKeySequence(SHORTCUT_TAB3), self)
        self.converged_data_shortcut.activated.connect(lambda: self.tabWidget.setCurrentIndex(2))

        # Create the shortcut to switch to "Toggle Comments"
        self.toggle_comment_shortcut = QShortcut(QKeySequence(SHORTCUT_TOGGLE_COMMENT), self)
        self.toggle_comment_shortcut.activated.connect(self.toggle_comment)

    def on_profoil_in_text_changed(self):
        """
        Indicates there are some unsaved changes in the profoil.in file
        by changing the color of the "Save" button
        """
        self.btn_save_profoil_in.setStyleSheet('QPushButton {color: red; font-style: italic;}')

    def switch_surface(self, event):
        """
        Switching the surface through the combo box.
        """
        self.select_surface(self.combo_switch_surface.itemText(event))

    def failure_error_dialog(self):
        """ pops a Message box with convergence failure warning, without beep """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Error...")
        msg_box.setText("Design Failed - Please check the .in File")
        
        # Setting icon to avoid beep
        msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def overlay_error_dialog(self):
        """ pops a Message box with file loading error, without beep """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("File loading Error...")
        msg_box.setText("Please check the .dat File")
        
        # Setting icon to avoid beep
        msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def loading_warning_dialog(self):
        """ pops a Message box with file loading error. """
        return QMessageBox.question(
            self, 
            "Active Session", 
            "Any unsaved data will be lost.\n          Continue?          ",
            QMessageBox.Yes | QMessageBox.Cancel) if AIRFOIL_CHANGE_WARNING else QMessageBox.Yes

    def save_planTextEdit_to_profoil(self):
        """
        saves the profoil.in file view, in to the profoil.in file.
        """
        p_intf.gen_buffer()
        p_intf.save2profoil_in(self.plainTextEdit_profoil_in.toPlainText())

        # upon saving change the save button color back to black
        self.btn_save_profoil_in.setStyleSheet('QPushButton {color: black; font-style: normal;}')

    def menu_file_open(self, filename=None):
        """
        opens profoil.in file, if a session is current, warning will be shown.
        """
        if self.ready_to_interact:
            if self.loading_warning_dialog() != QMessageBox.Yes:
                return
            self.active_surface = "Upper"
            if not KEEP_OLD_AIRFOIL_UPON_LOADING:
                self.setup_axes()
                self.clear_axes()

        filename = filename or QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,'../runs', "Input File (*.in)")[0]
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
        Overlays *.xy or *.dat file based on skiprows (0 for .xy, 1 for .dat)
        """
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,'.', "All Files (*.*)")[0]
        if filename:
            self.overlay_dat(filename, skiprows)

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

            modified_lines = [line.replace(COMMENT_MARKER, "", 1) if line.startswith(("#","!")) else f"{COMMENT_MARKER}{line}" for line in selected_lines]
            cursor.insertText("\n".join(modified_lines))

    def annotate_profoil_in(self):
        """
        note: setting text with setPlainText() just wont work here
        because it wipes out the Qtextedit undo() stack
        hence the cursor.intertText() is used here
        """
        annotated_text = annotate_text(self.plainTextEdit_profoil_in.toPlainText())
        cursor = self.plainTextEdit_profoil_in.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.insertText(annotated_text)

        # users should be able to undo the annotation straight away if not happy with the outcome
        # hence the focus is set on the plainTextEdit_profoil_in
        self.plainTextEdit_profoil_in.setFocus()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Set the icon
    app.setWindowIcon(QtGui.QIcon("icon.ico"))
    
    ui = ProfoilUI()
    ui.setupUi(ui)
    ui.load_canvas()
    ui.connect_widget_events()
    ui.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
    ui.show()
    app.exec_()
