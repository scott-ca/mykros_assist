from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import os
import platform
import subprocess

import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info

def create_file_execution(output_widget, entities, shared_data, chat_prompt):
    """
    Executes the 'create_file' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.            
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "create_file_import" in entities:
        create_file_import = entities.get("create_file_import")
        create_file_data = shared_data.pop(0)
        print("creating of the stuff import")
        print(create_file_import)
    else:
        create_file_data = ""

    create_file_path = None

    if "create_file_path" in entities:
        create_file_path = entities.get("create_file_path")
    elif create_file_path is not None:
        print(create_file_path)
    else:
        # Prompt the user for the file_path
        create_file_path = request_additional_info(chat_prompt, "Enter the file path including the file name of the file you want to create:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if create_file_path is None:
            output_widget.append("File creation operation canceled.")
            return

    logging.debug(f"Creating file: {create_file_path}")
    try:
        with open(create_file_path, "w") as file:
            file.write(create_file_data)
        output_widget.append(f"Created a file called {create_file_path} in the current directory.")
    except Exception as e:
        output_widget.append(f"An error occurred while creating the file: {e}")

    if "create_file_export" in entities:
        create_file_export = entities.get("create_file_export")
        if create_file_export == "export" or create_file_export == "exported":
            # if "create_file_export" in entities:
            print("made it this far")
            shared_data.append(create_file_path)
            print("pre-return")
            print(shared_data)
            return shared_data

