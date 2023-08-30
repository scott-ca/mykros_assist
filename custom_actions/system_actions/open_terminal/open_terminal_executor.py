from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import subprocess
import os
import platform
import threading
import sys
import psutil
import platform
from pynput import keyboard
import logging

def open_terminal_execution(output_widget, os_name):
    """
    Executes the 'open_terminal' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        os_name (str): The name of the operating system.
    """

    if os_name == "Linux":

        subprocess.Popen(["gnome-terminal"])
        logging.debug("Opened the terminal.")

    elif os_name == "Windows":
        subprocess.run(["cmd.exe", "/c","start cmd /k"])
        output_widget.append("Open the command prompt")
            
    else:
        logging.debug("Unsupported OS")

