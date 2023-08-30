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


def open_file_explorer_execution(output_widget, entities, os_name):
    """
    Executes the 'open_file_explorer' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        os_name (str): The name of the operating system.
        
    """

    if "folder_query" in entities:
        folder_query = entities.get("folder_query")
    else:
        # Opens the file explorer in the folder the chatbot was opened from.
        folder_query = "."

    # Check if the folder path exists
    if not os.path.isdir(folder_query):
        output_widget.append(f"AI: Sorry, the folder path '{folder_query}' does not exist.")
        return

    if os_name == "Linux":

        subprocess.run(["xdg-open", folder_query])
        output_widget.append("Opened the file explorer.")

    elif os_name == "Windows":

        subprocess.run(["cmd.exe", "/c","start explorer", folder_query])
        output_widget.append("Opened the file explorer.")
            
    else:
        logging.debug("Unsupported OS")


