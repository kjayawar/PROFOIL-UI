import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)

        # Two lines on the same plot
        self.line1, = self.ax.plot([random.randint(1, 10) for _ in range(10)], 'r-', label='Line 1')
        self.line2, = self.ax.plot([random.randint(1, 10) for _ in range(10)], 'b--', label='Line 2')
        self.ax.set_title("Right-click to change line settings")
        self.ax.legend()

        self.selected_line = None  # To track the selected line
        self.setContextMenuPolicy(3)  # Enables custom context menus
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        # Select Line
        select_line_menu = context_menu.addMenu('Select Line')
        select_line_menu.addAction('Line 1', lambda: self.set_selected_line(self.line1))
        select_line_menu.addAction('Line 2', lambda: self.set_selected_line(self.line2))

        if self.selected_line is not None:
            change_color_menu = context_menu.addMenu('Change Color')
            change_color_menu.addAction('Red', lambda: self.change_line_color('r'))
            change_color_menu.addAction('Blue', lambda: self.change_line_color('b'))
            change_color_menu.addAction('Green', lambda: self.change_line_color('g'))

            change_style_menu = context_menu.addMenu('Change Style')
            change_style_menu.addAction('Solid', lambda: self.change_line_style('-'))
            change_style_menu.addAction('Dashed', lambda: self.change_line_style('--'))
            change_style_menu.addAction('Dotted', lambda: self.change_line_style(':'))

        context_menu.exec_(self.mapToGlobal(pos))

    def set_selected_line(self, line):
        self.selected_line = line
        print(f"Selected: {self.selected_line.get_label()}")

    def change_line_color(self, color):
        if self.selected_line:
            self.selected_line.set_color(color)
            self.draw()

    def change_line_style(self, style):
        if self.selected_line:
            self.selected_line.set_linestyle(style)
            self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plot Line Settings")

        self.plot_canvas = PlotCanvas(self)
        self.setCentralWidget(self.plot_canvas)

        self.resize(800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
