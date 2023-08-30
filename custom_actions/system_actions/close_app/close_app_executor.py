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

def close_app_execution(output_widget, entities, chat_prompt, os_name):
    """
    Closes all instances of an application.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
        os_name (str): The name of the operating system.
    """

    if "close_app_id" in entities:
        close_app_id = entities.get("close_app_id")
    else:
        # Prompt the user for the close_app_id entity
        close_app_id = request_additional_info(chat_prompt, "Please enter the name of the application you would like to close:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if close_app_id is None:
            output_widget.append("Closing application operation canceled.")
            return

    def check_process(close_app_id):
        # Get the list of running processes
        processes = psutil.process_iter()

        # Filter processes by name (case-insensitive)
        matching_processes = [p for p in processes if close_app_id.lower() in p.name().lower()]

        # Check if any matching processes were found
        if len(matching_processes) == 0:
            output_widget.append(f"No process matching the name '{close_app_id}' is currently running.")
            return []

        # Print the matching processes
        output_widget.append("Matching processes:")
        for process in matching_processes:
            output_widget.append(f"PID: {process.pid}, Name: {process.name()}")

        return matching_processes
        
    while True:
        # Check the process and prompt for confirmation
        matching_processes = check_process(close_app_id)
        if matching_processes:
            chat_prompt.expecting_additional_info = True
            chat_prompt.request_input("Are you sure you want to end the process? (yes/no/edit): ")
            user_input = chat_prompt.wait_for_input().strip().lower()

            if user_input == "yes":
                # Terminate each matching process based on the platform
                for process in matching_processes:
                    if os_name == "Windows":
                        os.system(f"taskkill /F /PID {process.pid}")
                    elif os_name == "Linux":
                        process.terminate()
                output_widget.append("Process terminated successfully.")
                # Display message in output widget
                output_widget.append(f"AI: I have closed '{close_app_id} software'")
                break
            elif user_input == "no":
                output_widget.append("Process termination cancelled.")
                break
            elif user_input == "edit":
                close_app_id = request_additional_info(chat_prompt, "Please enter the new process name:")
                if close_app_id is None:
                    output_widget.append("Editing process terminated.")
                    break
            else:
                output_widget.append("Invalid input. Please type 'yes', 'no', or 'edit'.")
            
        elif matching_processes == []:
            break

