from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import os
import platform
import subprocess

import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info
    
def open_file_execution(output_widget, entities, shared_data, chat_prompt, os_name):
    """
    Executes the 'open_file' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.            
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "open_file_import" in entities:
        open_file_import = entities.get("open_file_import")
        file_path = shared_data.pop(0)
        print(open_file_import)
    else:
        file_path = None

    if "file_path" in entities:
        file_path = entities.get("file_path")
    elif file_path is not None:
        print(file_path)
    else:
        # Prompt the user for the file path
        file_path = request_additional_info(chat_prompt, "Enter the location and name of the file you want to open:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if file_path is None:
            output_widget.append("File open operation canceled.")
            return

    # Check if the file exists
    if not os.path.isfile(file_path):
        output_widget.append(f"AI: Sorry, the file '{file_path}' does not exist.")
        return

    if os_name == "Linux":
        try:
            subprocess.run(["xdg-open", file_path])
            output_widget.append(f"AI: Opened file '{file_path}'.")
        except Exception as e:
            output_widget.append(f"AI: Error opening file: {str(e)}")
    elif os_name == "Windows":
        try:
            os.startfile(file_path)
            output_widget.append(f"AI: Opened file '{file_path}'.")
        except Exception as e:
            output_widget.append(f"AI: Error opening file: {str(e)}")
    else:
        output_widget.append("AI: Unsupported OS.")

