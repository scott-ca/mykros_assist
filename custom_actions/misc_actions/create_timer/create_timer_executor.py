from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QTextEdit, QTableWidget, QTableWidgetItem
from PySide2.QtCore import QTimer
import difflib

import re
import platform
import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info

class CountdownTimer(QDialog):
    """
    Dialog window for a countdown timer.
    """

    def __init__(self, hours=0, minutes=0, seconds=0):
        """
        Initializes the CountdownTimer dialog with the specified hours, minutes, and seconds.

        Args:
            hours (int): The number of hours for the countdown timer. Defaults to 0.
            minutes (int): The number of minutes for the countdown timer. Defaults to 0.
            seconds (int): The number of seconds for the countdown timer. Defaults to 0.
        """
        super().__init__()
        self.total_time_remaining = hours * 3600 + minutes * 60 + seconds
        self.time_remaining = self.total_time_remaining
        self.paused = False
        self.timer_label = QLabel(self.format_time(self.time_remaining))
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.pause_button)
        self.setLayout(layout)
        # Start the timer
        self.update_timer()
        
    def update_timer(self):
        """
        Updates the timer label and time remaining for the countdown timer.
        """

        if not self.paused and self.time_remaining > 0:
            self.timer_label.setText(self.format_time(self.time_remaining))
            self.time_remaining -= 1
            # Update the timer every second
            QTimer.singleShot(1000, self.update_timer)
        elif self.time_remaining == 0:
            self.timer_label.setText("Time's up!")
        
    def toggle_pause(self):
        """
        Toggles the pause state of the countdown timer.
        """

        if self.paused:
            self.paused = False
            self.pause_button.setText("Pause")
            self.update_timer()
        else:
            self.paused = True
            self.pause_button.setText("Resume")
        
    def format_time(self, seconds):
        """
        Formats the given number of seconds into a time string.

        Args:
            seconds (int): The number of seconds to format.

        Returns:
            str: The formatted time string.
        """

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d}"
    
def create_timer_execution(output_widget, entities, chat_prompt):
    """
    Executes the 'create_timer' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "timer" in entities:
        timer = entities.get("timer")
    else:
        # prompt the user for the timer entity
        timer = request_additional_info(chat_prompt, "Enter the duration for the timer you want to start:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if timer is None:
            output_widget.append("Timer operation canceled.")
            return

    # Parse time string to get hours, minutes, and seconds
    hours, minutes, seconds = 0, 0, 0
    match = re.search(r"(\d+)\s*hour", timer)
    if match:
        hours = int(match.group(1))
    match = re.search(r"(\d+)\s*minute", timer)
    if match:
        minutes = int(match.group(1))
    match = re.search(r"(\d+)\s*second", timer)
    if match:
        seconds = int(match.group(1))

    # Create and show countdown timer dialog
    timer_dialog = CountdownTimer(hours=hours, minutes=minutes, seconds=seconds)
    timer_dialog.exec_()

