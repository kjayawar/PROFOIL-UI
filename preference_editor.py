from PyQt5 import QtWidgets, QtGui

class PreferenceEditor(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Fixed file path
        self.preference_file = 'test.txt'

        # Set window properties
        self.setWindowTitle('~/preference.py')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(100, 100, 600, 800)  # Set window size (width=600, height=800)

        # Set up the main widget (QTextEdit)
        self.editor = QtWidgets.QTextEdit(self)
        self.editor.textChanged.connect(self.on_text_changed)  # Connect textChanged signal

        # Set up the Save button
        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_file)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()

        # Add QTextEdit with a vertical stretch to ensure it expands with the window
        main_layout.addWidget(self.editor)

        # Button layout with horizontal spacer to keep the Save button on the bottom-right
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()  # Horizontal spacer
        button_layout.addWidget(self.save_button)

        # Add button layout
        main_layout.addLayout(button_layout)

        # Set the layout to a container widget
        container = QtWidgets.QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load the content from the file into the editor
        self.load_file()

    def load_file(self):
        """Load the content of the file into the QTextEdit widget."""
        self.editor.setPlainText(open(self.preference_file, 'r').read())
        # Reset the button's style after saving
        self.save_button.setStyleSheet('')
        
    def save_file(self):
        """Save the content from the QTextEdit widget back to the file."""
        with open(self.preference_file, 'w') as file:
            file.write(self.editor.toPlainText())
        # Reset the button's style after saving
        self.save_button.setStyleSheet('')

    def on_text_changed(self):
        """Change the style of the Save button when the text is modified."""
        self.save_button.setStyleSheet('QPushButton {color: red; font-style: italic;}')

def open_preference_editor():
    """Function to open the PreferenceEditor as a separate window."""
    editor = PreferenceEditor()
    editor.show()
    return editor


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Calling the editor function, useful in a larger system
    window = open_preference_editor()

    # Keep the application running
    app.exec_()
