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

def run_terminal_execution(output_widget, entities, chat_prompt, os_name):
    """
    Executes the 'run_terminal' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
        os_name (str): The name of the operating system.            
    """


    if "terminal_command" in entities:
        terminal_command = entities.get("terminal_command")
    else:
        # prompt the user for the terminal_command entity
        terminal_command = request_additional_info(chat_prompt,"What command would you like to run in the terminal:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if terminal_command is None:
            output_widget.append("Running terminal command operation canceled.")
            return
        
    if os_name == "Windows":
        terminal_command == '\"cmd.exe\", ' + terminal_command

    try:

        if os_name == "Linux":

            cmd_path = subprocess.check_output(["which", terminal_command.split()[0]]).decode().strip()

            try:
                output = subprocess.check_output(['ldd', cmd_path])
                output = output.decode("utf-8")
                curses_detected = "libncurses" in output
            except subprocess.CalledProcessError:
                curses_detected = False

            if curses_detected:

                # Launch command in a new terminal window
                new_terminal_cmd = f"x-terminal-emulator -e 'bash -i -c \"{terminal_command}; exec bash\"'"
                output_widget.append(f"testing")
                subprocess.Popen(new_terminal_cmd, shell=True)
                output_widget.append(f"AI: Terminal command '{terminal_command}' launched in a new terminal window.")
            else:
                logging.debug(f"No curses: {cmd_path}")

        
        if os_name == "Linux" or os_name == "Windows":
        
            # Run terminal command and capture output
            result = subprocess.run(terminal_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Display output in output widget
            if result.returncode == 0:
                output_widget.append(f"AI: Terminal command '{terminal_command}' executed successfully.")
                output_widget.append(f"Output:\n{result.stdout}")
            else:
                output_widget.append(f"AI: Error executing terminal command '{terminal_command}':")
                output_widget.append(f"Error message:\n{result.stderr}")


    except subprocess.CalledProcessError:
        cmd_path = terminal_command.split()[0]

        if os_name == "Linux":
            terminal_command = f"bash -i -c '{terminal_command}'"
            logging.debug(f" Except curses: {cmd_path}")

        if os_name == "Windows":
            terminal_command = f"cmd /k '{terminal_command}'"
        
        # Run terminal command and capture output
        result = subprocess.run(terminal_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


        # Display output in output widget
        if result.returncode == 0:
            output_widget.append(f"AI: Terminal command '{terminal_command}' executed successfully.")
            output_widget.append(f"Output:\n{result.stdout}")
        else:
            output_widget.append(f"AI: Error executing terminal command '{terminal_command}':")
            output_widget.append(f"Error message:\n{result.stderr}")

