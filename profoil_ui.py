# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PROFOIL-UI.ui'
# Created by: PyQt5 UI code generator 5.9.2
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import key_press_handler

from profoil_canvas import ProfoilCanvas
from preferences import *
import profoil_interface as p_intf

from pathlib import Path
WORKDIR = Path(WORKDIR)
BINDIR 	= Path(BINDIR)
UI_DIR  = Path.cwd()

"""
Below is a monkey patch to handle a possible bug in matplotlib. 
regardless of the back-end, matplotlib tool-bar home-button, doesn't appear to redraw even when the frameon=True. 
This results in messed up axis limits on zoom-> home.
Upon multiple failed attempts to fix this issue in a pragmatic way, below decorator is introduced
to wrap the home button with an additional axis limit change. 
"""

home = NavigationToolbar.home
def patched_home(self, *args, **kwargs):
	home(self, *args, **kwargs)
	ui.setup_axes_limits()
NavigationToolbar.home = patched_home


class Ui_MainWindow(QtWidgets.QMainWindow, ProfoilCanvas):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		ProfoilCanvas.__init__(self)

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		# MainWindow.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
		MainWindow.setMinimumSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
		font = QtGui.QFont()
		font.setPointSize(8)
		# font.setFamily("Courier")
		self.tabWidget.setFont(font)
		self.tabWidget.setObjectName("tabWidget")
		self.widget = QtWidgets.QWidget()
		self.widget.setObjectName("widget")
		self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget)
		self.horizontalLayout_10.setObjectName("horizontalLayout_10")
		self.verticalLayout_canvas = QtWidgets.QVBoxLayout()
		self.verticalLayout_canvas.setObjectName("verticalLayout_canvas")
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.verticalLayout_canvas.addItem(spacerItem)
		self.horizontalLayout_10.addLayout(self.verticalLayout_canvas)
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.checkBox_grid = QtWidgets.QCheckBox(self.widget)
		self.checkBox_grid.setChecked(True)
		self.checkBox_grid.setObjectName("checkBox_grid")
		self.horizontalLayout_3.addWidget(self.checkBox_grid)
		self.checkBox_history = QtWidgets.QCheckBox(self.widget)
		self.checkBox_history.setChecked(True)
		self.checkBox_history.setObjectName("checkBox_history")
		self.horizontalLayout_3.addWidget(self.checkBox_history)
		self.verticalLayout.addLayout(self.horizontalLayout_3)
		self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_9.setObjectName("horizontalLayout_9")
		self.label_4 = QtWidgets.QLabel(self.widget)
		self.label_4.setObjectName("label_4")
		self.horizontalLayout_9.addWidget(self.label_4)
		self.combo_switch_surface = QtWidgets.QComboBox(self.widget)
		self.combo_switch_surface.setObjectName("combo_switch_surface")
		self.combo_switch_surface.addItem("")
		self.combo_switch_surface.addItem("")
		self.horizontalLayout_9.addWidget(self.combo_switch_surface)
		self.horizontalLayout_9.setStretch(0, 1)
		self.horizontalLayout_9.setStretch(1, 3)
		self.verticalLayout.addLayout(self.horizontalLayout_9)
		self.btn_start_edits = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.btn_start_edits.setFont(font)
		self.btn_start_edits.setObjectName("btn_start_edits")
		self.verticalLayout.addWidget(self.btn_start_edits)
		self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_8.setObjectName("horizontalLayout_8")
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_8.addItem(spacerItem1)
		self.btn_cancel = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.btn_cancel.setFont(font)
		self.btn_cancel.setObjectName("btn_cancel")
		self.horizontalLayout_8.addWidget(self.btn_cancel)
		self.verticalLayout.addLayout(self.horizontalLayout_8)
		self.btn_apply_edits = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.btn_apply_edits.setFont(font)
		self.btn_apply_edits.setObjectName("btn_apply_edits")
		self.verticalLayout.addWidget(self.btn_apply_edits)
		self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_6.setObjectName("horizontalLayout_6")
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_6.addItem(spacerItem2)
		self.btn_undo = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.btn_undo.setFont(font)
		self.btn_undo.setObjectName("btn_undo")
		self.horizontalLayout_6.addWidget(self.btn_undo)
		self.verticalLayout.addLayout(self.horizontalLayout_6)
		self.btn_plot_from_file = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.btn_plot_from_file.setFont(font)
		self.btn_plot_from_file.setObjectName("btn_plot_from_file")
		self.verticalLayout.addWidget(self.btn_plot_from_file)
		self.btn_run_profoil = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.btn_run_profoil.setFont(font)
		self.btn_run_profoil.setStyleSheet("background-color:yellowgreen;")
		self.btn_run_profoil.setObjectName("btn_run_profoil")
		self.verticalLayout.addWidget(self.btn_run_profoil)
		self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_7.setObjectName("horizontalLayout_7")
		spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_7.addItem(spacerItem3)
		self.btn_revert = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.btn_revert.setFont(font)
		self.btn_revert.setObjectName("btn_revert")
		self.horizontalLayout_7.addWidget(self.btn_revert)
		self.verticalLayout.addLayout(self.horizontalLayout_7)
		self.lbl_summary = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setFamily("Courier")
		self.lbl_summary.setFont(font)
		self.lbl_summary.setWordWrap(True)
		self.lbl_summary.setObjectName("lbl_summary")
		self.verticalLayout.addWidget(self.lbl_summary)
		spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem4)
		self.horizontalLayout_10.addLayout(self.verticalLayout)
		self.horizontalLayout_10.setStretch(0, 6)
		self.horizontalLayout_10.setStretch(1, 1)
		self.tabWidget.addTab(self.widget, "")
		self.widget1 = QtWidgets.QWidget()
		self.widget1.setObjectName("widget1")
		self.gridLayout = QtWidgets.QGridLayout(self.widget1)
		self.gridLayout.setObjectName("gridLayout")
		self.plainTextEdit_profoil_log = QtWidgets.QPlainTextEdit(self.widget1)
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setFamily("Courier")
		self.plainTextEdit_profoil_log.setFont(font)
		self.plainTextEdit_profoil_log.setReadOnly(True)
		self.plainTextEdit_profoil_log.setPlainText("")
		self.plainTextEdit_profoil_log.setObjectName("plainTextEdit_profoil_log")
		self.gridLayout.addWidget(self.plainTextEdit_profoil_log, 1, 1, 1, 1)
		self.plainTextEdit_profoil_in = QtWidgets.QPlainTextEdit(self.widget1)
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setFamily("Courier")
		self.plainTextEdit_profoil_in.setFont(font)
		self.plainTextEdit_profoil_in.setPlainText("")
		self.plainTextEdit_profoil_in.setObjectName("plainTextEdit_profoil_in")
		self.gridLayout.addWidget(self.plainTextEdit_profoil_in, 1, 0, 1, 1)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem5)
		self.btn_save_profoil_in = QtWidgets.QPushButton(self.widget1)
		self.btn_save_profoil_in.setObjectName("btn_save_profoil_in")
		self.horizontalLayout_2.addWidget(self.btn_save_profoil_in)
		self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.widget1)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.widget1)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
		self.tabWidget.addTab(self.widget1, "")
		self.horizontalLayout.addWidget(self.tabWidget)
		self.horizontalLayout.setStretch(0, 4)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1313, 21))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		self.menuOverlay = QtWidgets.QMenu(self.menubar)
		self.menuOverlay.setObjectName("menuOverlay")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.actionOpen = QtWidgets.QAction(MainWindow)
		self.actionOpen.setObjectName("actionOpen")
		self.actionSave = QtWidgets.QAction(MainWindow)
		self.actionSave.setObjectName("actionSave")
		self.action_dat_File = QtWidgets.QAction(MainWindow)
		self.action_dat_File.setObjectName("action_dat_File")
		self.actionClear_Overlay = QtWidgets.QAction(MainWindow)
		self.actionClear_Overlay.setObjectName("actionClear_Overlay")		
		self.menuFile.addAction(self.actionOpen)
		self.menuFile.addAction(self.actionSave)
		self.menuOverlay.addAction(self.action_dat_File)
		self.menuOverlay.addAction(self.actionClear_Overlay)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuOverlay.menuAction())

		self.load_canvas()
		self.connect_buttons()

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "PROFOIL-UI"))
		self.checkBox_grid.setText(_translate("MainWindow", "Grid"))
		self.checkBox_history.setText(_translate("MainWindow", "History"))
		self.label_4.setText(_translate("MainWindow", "Surface"))
		self.combo_switch_surface.setItemText(0, _translate("MainWindow", "Upper"))
		self.combo_switch_surface.setItemText(1, _translate("MainWindow", "Lower"))
		self.btn_start_edits.setText(_translate("MainWindow", "Start Edits"))
		self.btn_cancel.setText(_translate("MainWindow", "Cancel"))
		self.btn_apply_edits.setText(_translate("MainWindow", "Apply Edits"))
		self.btn_undo.setText(_translate("MainWindow", "Undo"))
		self.btn_plot_from_file.setText(_translate("MainWindow", "Plot From File"))
		self.btn_run_profoil.setText(_translate("MainWindow", "Run Profoil"))
		self.btn_revert.setText(_translate("MainWindow", "Revert"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "Design View"))
		self.btn_save_profoil_in.setText(_translate("MainWindow", "Save"))
		self.label.setText(_translate("MainWindow", "Profoil.in"))
		self.label_2.setText(_translate("MainWindow", "Profoil.log"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget1), _translate("MainWindow", "File View"))
		self.menuFile.setTitle(_translate("MainWindow", "File"))
		self.menuOverlay.setTitle(_translate("MainWindow", "Overlay"))
		self.actionOpen.setText(_translate("MainWindow", "Open"))
		self.actionSave.setText(_translate("MainWindow", "Save"))
		self.action_dat_File.setText(_translate("MainWindow", "*.dat File"))
		self.actionClear_Overlay.setText(_translate("MainWindow", "Clear Overlay"))

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

	def connect_buttons(self):
		"""
		maps button click signals to functions
		"""
		self.btn_start_edits.clicked.connect(self.start_cursor_edits)
		self.btn_cancel.clicked.connect(self.cancel_cursor_inputs)
		self.btn_apply_edits.clicked.connect(self.apply_edits)
		self.btn_undo.clicked.connect(self.undo_edits)
		self.btn_plot_from_file.clicked.connect(self.plot_from_file)
		self.btn_run_profoil.clicked.connect(self.run_profoil)
		self.btn_revert.clicked.connect(self.revert)

		self.btn_save_profoil_in.clicked.connect(self.save_planTextEdit_to_profoil)

		self.actionOpen.triggered.connect(self.menu_file_open)
		self.actionSave.triggered.connect(self.menu_file_save)
		self.action_dat_File.triggered.connect(self.overlay_file_open)
		self.actionClear_Overlay.triggered.connect(self.clear_overlay)

		self.checkBox_grid.stateChanged.connect(self.toggle_grid_lines)
		self.checkBox_history.stateChanged.connect(self.toggle_previous_plots)
		self.combo_switch_surface.currentIndexChanged.connect(self.switch_surface)

		self.combo_switch_surface.currentIndexChanged.connect(self.switch_surface)

		self.tabWidget.currentChanged.connect(self.load_file_view)

	def load_file_view(self, event):
		"""
		In file view, profoil.in is updated when the tab is selected so that the most up to date file
		"""
		if self.tabWidget.tabText(event) == "File View":
			self.plainTextEdit_profoil_in.setPlainText(p_intf.catfile(WORKDIR/"profoil.in", tail=0))

	def switch_surface(self, event):
		"""
		Switching the surface through the combo box.
		"""
		self.select_surface(self.combo_switch_surface.itemText(event))

	def failure_error_dialog(self):
		"""	pops a Message box with convergence failure warning """
		QMessageBox.critical(self, "Error...", "Design Failed - Please check the .in File")

	def overlay_error_dialog(self):
		""" pops a Message box with file loading error. """
		QMessageBox.information(self, "File loading Error...", "Please check the .dat File")

	def loading_warning_dialog(self):
		""" pops a Message box with file loading error. """
		return QMessageBox.warning(self, 
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

		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,'.', "Input File (*.in)")[0]
		if filename:
			self.load(filename)

	def menu_file_save(self):
		"""
		saves profoil.in file
		"""
		if not self.ready_to_interact: return
		filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File' ,'.', "Input File (*.in)")[0]
		if filename:
			self.save_airfoil(filename)

	def overlay_file_open(self):
		"""
		overlays *.dat file
		"""
		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file' ,'.', "All Files (*.*)")[0]
		if filename:
			self.overlay_dat(filename)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	app.exec_()