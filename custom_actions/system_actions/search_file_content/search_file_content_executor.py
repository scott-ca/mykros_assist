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

from util.misc import request_additional_info

def search_file_content_execution(output_widget, entities, chat_prompt, os_name):
    """
    Executes the 'search_file_content' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
        os_name (str): The name of the operating system.
    """

    if "file_query" in entities:
        file_query = entities.get("file_query")
    else:
        # prompt the user for the file_query entity
        file_query = request_additional_info(chat_prompt, "Enter the word(s) that you would like to search for in the contents of the file:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if file_query is None:
            output_widget.append("File search operation canceled.")
            return

    if "folder_query" in entities:
        folder_query = entities.get("folder_query")
    else:
        # prompt the user for the folder_path entity
        folder_query = request_additional_info(chat_prompt, "Enter the folder you would like to search in:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if folder_query is None:
            output_widget.append("File search operation canceled.")
            return
        
    # Check if the folder path exists
    if not os.path.isdir(folder_query):
        output_widget.append(f"AI: Sorry, the folder path '{folder_query}' does not exist.")
        return
        
    if os_name == "Linux":
        logging.debug("Linux Specific")

        # Use find and grep commands to search for files containing query in their contents within folder
        command = f"find {folder_query} -type f -exec grep -l '{file_query}' {{}} +"
        result = subprocess.check_output(command, shell=True, text=True)

        # Display search results in output widget
        output_widget.append(f"AI: Here are the files containing '{file_query}' in '{folder_query}':\n{result}")


    elif os_name == "Windows":
        logging.debug("Windows Specific")
        # Use findstr command to locate files with the specified content
        file_paths = subprocess.run(f'cmd /c findstr /s /m /i /c:"{file_query}" "{folder_query}\\*.*"', capture_output=True, text=True, shell=True).stdout.strip().split("\r\n")       
        # Display file paths in output widget
        print(file_paths)
        output_widget.append(f"AI: Here are the file paths for files containing the text '{file_query}':")
        for path in file_paths:
            output_widget.append(path)
    else:
        logging.debug("Unsupported OS")

