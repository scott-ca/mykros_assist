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

def search_google_execution(output_widget, entities, chat_prompt):
    """
    Executes the 'search_wiki' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.            
    """

    if "google_query" in entities:
        google_query = entities.get("google_query")
    else:
        # prompt the user for the google query entity
        google_query = request_additional_info(chat_prompt, "Enter the what you would like to search on Google:")
        
        # Check if the user would like to cancel the operation when prompted for additional information
        if google_query is None:
            output_widget.append("Google search operation canceled.")
            return

    # Open browser to Google search results for query
    webbrowser.open_new_tab(f"https://www.google.com/search?q={google_query}")

    # Display message in output widget
    output_widget.append(f"AI: Here are the Google search results for '{google_query}'")

