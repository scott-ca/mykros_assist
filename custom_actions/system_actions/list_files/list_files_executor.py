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

def list_files_execution(output_widget, entities, shared_data, os_name):
    """
    Executes the 'list_files' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
    """

    if "folder_query" in entities:
        folder_query = entities.get("folder_query")
    else:
        # List the files in the directory the chatbot was opened from.
        folder_query = "."    

    # Check if the folder path exists
    if not os.path.isdir(folder_query):
        output_widget.append(f"AI: Sorry, the folder path '{folder_query}' does not exist.")
        return
    
    if os_name == "Linux":

        result = subprocess.run(["ls", folder_query], stdout=subprocess.PIPE, text=True)
        output_widget.append(f"AI: Listed files in the current directory:\n{result.stdout}")
        
    elif os_name == "Windows":

        result = subprocess.run(["cmd.exe", "/c", "dir", folder_query], stdout=subprocess.PIPE, text=True)
        output_widget.append(f"AI: Listed files in the current directory:\n{result.stdout}")
            
    else:
        logging.debug("Unsupported OS")


    if "list_files_export" in entities:
        list_files_export = entities.get("list_files_export")
        if list_files_export == "export" or list_files_export == "exported":
            print("made it this far")
            print(result.stdout)
            shared_data.append(result.stdout)
            print("pre-return")
            print(shared_data)
            return shared_data
