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

def search_wiki_execution(output_widget, entities, chat_prompt):
    """
    Executes the 'search_wiki' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.            
    """

    if "wiki_query" in entities:
        wiki_query = entities.get("wiki_query")
    else:
        # prompt the user for the wiki query entity
        wiki_query = request_additional_info(chat_prompt, "Enter the what you would like to search on Wikipedia:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if wiki_query is None:
            output_widget.append("Wiki search operation canceled.")
            return
    
    # Replace spaces with underscores for wiki page format
    wiki_page = wiki_query.replace(" ", "_")

    # Check if the Wikipedia page exists
    response = requests.get(f"https://en.wikipedia.org/wiki/{wiki_page}")
    if response.status_code == 200:
        # Open browser to the Wikipedia page
        webbrowser.open_new_tab(f"https://en.wikipedia.org/wiki/{wiki_page}")
    else:
        # Replace spaces with plus signs for wiki search format
        wiki_search = wiki_query.replace(" ", "+")
        
        # Open browser to Wikipedia search results for query
        webbrowser.open_new_tab(f"https://en.wikipedia.org/w/index.php?search={wiki_search}&title=Special:Search&profile=advanced&fulltext=1&ns0=1")

    # Display message in output widget
    output_widget.append(f"AI: Here are the Wikipedia search results for '{wiki_query}'")

