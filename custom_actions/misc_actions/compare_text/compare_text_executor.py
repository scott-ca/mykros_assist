from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QTextEdit, QTableWidget, QTableWidgetItem
from PySide2.QtCore import QTimer
import difflib

import re
import platform
import logging

if platform.system() == "Windows":
    import winreg

class CompareTextWindow(QDialog):
    """
    Dialog window for comparing text differences.
    """

    def __init__(self):
        """
        Initializes the CompareTextWindow dialog.
        """
        super().__init__()

        self.setWindowTitle('Text Difference Finder')
        self.setLayout(QVBoxLayout())

        # Create a horizontal layout for the text boxes
        hbox_layout = QHBoxLayout()
        self.text_edit1 = QTextEdit()
        self.text_edit2 = QTextEdit()
        hbox_layout.addWidget(self.text_edit1)
        hbox_layout.addWidget(self.text_edit2)
        self.layout().addLayout(hbox_layout)

        self.button = QPushButton('Find differences')
        self.layout().addWidget(self.button)
        self.table = QTableWidget()        
        self.layout().addWidget(self.table)
        self.button.clicked.connect(self.on_button_clicked)

    def diff_highlight(self, text1, text2):
        d = difflib.Differ()
        diff = list(d.compare(text1, text2))
        highlighted = ''
        for i in diff:
            if i[0] == '+':
                highlighted += f'<span style="background-color: #00FF00">{i[2:]}</span> '
            elif i[0] == '-':
                highlighted += f'<span style="background-color: #FF0000">{i[2:]}</span> '
            else:
                highlighted += i[2:] + ' '
        return highlighted

    def on_button_clicked(self):
        text1 = self.text_edit1.toPlainText().split('\n')
        text2 = self.text_edit2.toPlainText().split('\n')

        # First pass: Determine where to insert blank lines
        blank_lines_to_insert1 = []
        blank_lines_to_insert2 = []
        text1_modified = text1.copy()
        text2_modified = text2.copy()
        i = 0
        j = 0
        while i < len(text1_modified) or j < len(text2_modified):
            line1 = text1_modified[i] if i < len(text1_modified) else ''
            line2 = text2_modified[j] if j < len(text2_modified) else ''

            if line1 == line2:
                i += 1
                j += 1
                continue

            found_match = False
            for k in range(j + 1, len(text2_modified)):
                if line1 == text2_modified[k]:
                    found_match = True
                    blank_lines_to_insert1.append(i)
                    text1_modified.insert(i, '')
                    break

            if not found_match:
                for k in range(i + 1, len(text1_modified)):
                    if line2 == text1_modified[k]:
                        blank_lines_to_insert2.append(i)
                        text2_modified.insert(i, '')
                        break

            i += 1
            j += 1

        # Second pass: Highlight differences and create table
        self.table.clearContents()
        self.table.setRowCount(max(len(text1_modified), len(text2_modified)))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([' ', 'Text 1', ' ', 'Text 2'])
        for i in range(max(len(text1_modified), len(text2_modified))):
            line1 = text1_modified[i] if i < len(text1_modified) else ''
            line2 = text2_modified[i] if i < len(text2_modified) else ''
            diff1 = self.diff_highlight(line1.split(), line2.split())
            diff2 = self.diff_highlight(line2.split(), line1.split())

            text_edit_widget1 = QTextEdit()
            text_edit_widget1.setHtml(diff1)
            text_edit_widget1.setReadOnly(True)

            text_edit_widget2 = QTextEdit()
            text_edit_widget2.setHtml(diff2)
            text_edit_widget2.setReadOnly(True)

            self.table.setCellWidget(i, 1, text_edit_widget1)
            self.table.setCellWidget(i, 3, text_edit_widget2)

            if i in blank_lines_to_insert1:
                self.table.setItem(i, 0, QTableWidgetItem('-'))
            elif i in blank_lines_to_insert2:
                self.table.setItem(i, 2, QTableWidgetItem('+'))

        self.table.resizeColumnsToContents()

def compare_text_execution(output_widget, entities, chat_prompt):
    """
    Executes the 'compare_text' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    text_difference_window = CompareTextWindow()
    text_difference_window.exec_()

