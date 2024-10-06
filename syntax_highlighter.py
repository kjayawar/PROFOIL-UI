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

from PyQt5 import QtGui
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtCore import QRegExp

from preferences import COMMENT_COLOR

class CommentHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(CommentHighlighter, self).__init__(parent)
        # Define the format for comment lines
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(COMMENT_COLOR))
        self.comment_format.setFontWeight(QtGui.QFont.Bold)

    def highlightBlock(self, text):
        # Regular expression to match lines starting with #
        # comment_pattern = QRegExp(r"^#.*")

        # Regular expression to match lines starting with # or ! with optional leading whitespace
        comment_pattern = QRegExp(r'^\s*[#!].*')

        index = comment_pattern.indexIn(text)

        while index >= 0:
            length = comment_pattern.matchedLength()
            # Apply the comment format to the matched text
            self.setFormat(index, length, self.comment_format)
            index = comment_pattern.indexIn(text, index + length)
