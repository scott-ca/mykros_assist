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

def translate_webpage_execution(output_widget, entities, chat_prompt):
    """
    Tranlates a webpage using Google Translate.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "webpage_translate_query" in entities:
        webpage_translate_query = entities.get("webpage_translate_query")
    else:
        # prompt the user for the webpage_translate_query
        webpage_translate_query = request_additional_info(chat_prompt, "Enter the url that you would like to translate to English:")
        
        # Check if the user would like to cancel the operation when prompted for additional information
        if webpage_translate_query is None:
            output_widget.append("webpage translate operation canceled.")
            return
        
    if not urlparse(webpage_translate_query).scheme:
        webpage_translate_query = 'https://' + webpage_translate_query


    # Open browser to Google search results for query
    webbrowser.open_new_tab(f"https://translate.google.com/translate?sl=auto&tl=en&hl=en&u={webpage_translate_query}&client=webapp")

    # Display message in output widget
    output_widget.append(f"AI: I have opened your browser to the translated webpage of '{webpage_translate_query}'")

