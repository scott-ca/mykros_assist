from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import subprocess
import os
import json
from urllib.parse import urlparse
import webbrowser
import sqlite3
import requests
import platform
import threading
import sys
import re
import platform
import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info

def open_browser_execution(output_widget, entities, chat_prompt, os_name):
    """
    Executes the 'open_browser' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.            
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
        os_name (str): The name of the operating system.

    """

    if "url" in entities:
        url = entities.get("url")
    else:
        # prompt the user for the url entity query
        url = request_additional_info(chat_prompt, "Enter the URL you want to open:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if url is None:
            output_widget.append("Open browser operation canceled.")
            return

    if not urlparse(url).scheme:
        url = 'https://' + url

    logging.debug(f"Opening a new browser tab to {url}")

    if os_name == "Linux":

        subprocess.run(["xdg-open", url])
        logging.debug("Opened a new browser tab.")

    if os_name == "Windows":
        subprocess.run(["cmd.exe", "/c","start", url])

    else:
        logging.debug("Unsupported OS")

