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

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

class DragDropWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up drag and drop
        self.setAcceptDrops(True)

    def invalid_file_dialog(self):
        """ pops a Message box with file loading error, without beep """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Invalid File")
        msg_box.setText("Only .in, .xy, and .dat files are supported.")
        
        # Setting icon to avoid beep
        msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # Only accept if exactly one file is dragged
            event.acceptProposedAction()
        else:
            # Reject if more than one file is dragged
            event.ignore()

    def dropEvent(self, event):
        # Get the file path from the drop
        file_path = event.mimeData().urls()[0].toLocalFile()

        if file_path.endswith(".in"):
            # Handle .in files, prompting user is manged by user preference.
            self.menu_file_open(file_path)

        elif file_path.endswith(".xy"):
            # Handle .xy files (no header, skiprows=0)
            self.overlay_dat(filename=file_path, skiprows=0)

        elif file_path.endswith(".dat"):
            # Handle .dat files (with one header line, skiprows=1)
            self.overlay_dat(filename=file_path, skiprows=1)

        else:
            # Handle invalid file extensions
            self.invalid_file_dialog()

        # Refocus the window after the drop
        self.activateWindow()