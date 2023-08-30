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

def open_bookmark_execution(output_widget, entities, chat_prompt, os_name):
    """
    Executes the 'open_bookmark' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
        os_name (str): The name of the operating system.
    """

    if "bookmark_query" in entities:
        bookmark_query = entities.get("bookmark_query")
    else:
        # prompt the user for the bookmark_query entity
        bookmark_query = request_additional_info(chat_prompt, "What bookmark would you like to open from your browser:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if bookmark_query is None:
            output_widget.append("Opening bookmark operation canceled.")
            return

    bookmark_browser = entities.get("browser")
    

    if os_name == "Linux":
    
        logging.debug(f"Browser bookmark: {bookmark_browser}")
        browser = subprocess.run(['xdg-settings', 'get', 'default-web-browser'], stdout=subprocess.PIPE)
        logging.debug("Browser: {browser}")
        default_browser = browser.stdout.decode('utf-8').strip()
        logging.debug("Default browser: {default_browser}")

        if 'firefox' in default_browser:
            default_browser = 'Firefox'
        elif 'com.brave.Browser' in default_browser:
            default_browser = 'Brave.Flatpak'

        if default_browser is not None:
            logging.debug(f"Default browser: {default_browser}")

            # Find the profile path and search for bookmarks
            if (default_browser == "Firefox" and bookmark_browser == "bookmark") or bookmark_browser == "firefox bookmark":
                firefox_profile_dir = None
                firefox_profile_paths = os.listdir(os.path.expanduser("~/.mozilla/firefox"))
                for path in firefox_profile_paths:
                    logging.debug(f"Profile path: {path}")
                    if "default-release" in path:
                        firefox_profile_dir = path
                        break

                if firefox_profile_dir is not None:
                    firefox_profile_path = os.path.join(os.path.expanduser("~/.mozilla/firefox"), firefox_profile_dir)
                    db_path = os.path.join(firefox_profile_path, "places.sqlite")
                    logging.debug(f"Firefox profile path: {firefox_profile_path}")
                    logging.debug(f"Database path: {db_path}")
                else:
                    logging.debug("Unable to locate the Firefox profile directory.")

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                query = """
                SELECT moz_bookmarks.title, moz_places.url
                FROM moz_bookmarks
                INNER JOIN moz_places ON moz_bookmarks.fk = moz_places.id
                WHERE moz_bookmarks.title LIKE ?
                """

                cursor.execute(query, (f"%{bookmark_query}%",))
                results = cursor.fetchall()

                conn.close()

            elif (default_browser == "Brave.Flatpak" and bookmark_browser == "bookmark") or bookmark_browser == "brave bookmark":
                paths = [
                    os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks"),
                    os.path.expanduser("~/.var/app/com.brave.Browser/config/BraveSoftware/Brave-Browser/Default/Bookmarks")
                ]

                for path in paths:
                    if os.path.exists(path):
                        brave_profile_path = path
                        break

                if brave_profile_path is not None:
                    with open(brave_profile_path, 'r') as f:
                        bookmarks_data = json.load(f)

                    def search_bookmarks(node, bookmark_query):
                        results = []

                        if 'name' in node and bookmark_query.lower() in node['name'].lower():
                            results.append((node['name'], node['url']))

                        if 'children' in node:
                            for child in node['children']:
                                results.extend(search_bookmarks(child, bookmark_query))

                        return results

                    results = search_bookmarks(bookmarks_data['roots']['bookmark_bar'], bookmark_query)
                    results.extend(search_bookmarks(bookmarks_data['roots']['other'], bookmark_query))

                else:
                    logging.debug("Unable to locate the Brave bookmarks file.")

            if results:
                logging.debug(f"Launching bookmark: {results[0][0]} ({results[0][1]})")
                if default_browser == 'Firefox':
                    subprocess.Popen(['firefox', results[0][1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                elif default_browser == 'Brave.Flatpak':
                    subprocess.Popen(['flatpak', 'run', 'com.brave.Browser', results[0][1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                output_widget.append("No bookmarks found with the specified search term.")
        else:
            logging.debug("Unsupported browser.")

    elif os_name == "Windows":

        # Open the registry key for the default browser
        regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")

        # Get the ProgId value which contains the default browser name
        prog_id, _ = winreg.QueryValueEx(regkey, "Progid")

        # Extract the browser name from the ProgId value
        default_browser = prog_id.split('.')[-1]

        print(f"Default browser: {default_browser}")

        if "firefox" in default_browser.lower():
            default_browser = "Firefox"
        elif "brave" in default_browser.lower():
            default_browser = "Brave"

        elif "edge" in default_browser.lower():
            default_browser = "Edge"

        if default_browser is not None:
            logging.debug(f"Default browser: {default_browser}")
            

        # Find the profile path and search for bookmarks
        if (default_browser == "Firefox" and bookmark_browser == "bookmark") or bookmark_browser == "firefox bookmark":
            logging.debug("firefox loop")
            # Firefox bookmarks location in Windows
            firefox_profile_path = os.path.join(os.path.expanduser("~"), "AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
            firefox_profile_dir = None
            for folder in os.listdir(firefox_profile_path):
                if folder.endswith(".default-release"):
                    firefox_profile_dir = folder
                    break

            if firefox_profile_dir is not None:
                firefox_profile_path = os.path.join(firefox_profile_path, firefox_profile_dir)
                db_path = os.path.join(firefox_profile_path, "places.sqlite")
                logging.debug(f"Firefox profile path: {firefox_profile_path}")
                logging.debug(f"Database path: {db_path}")
            else:
                logging.debug("Unable to locate the Firefox profile directory.")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = """
            SELECT moz_bookmarks.title, moz_places.url
            FROM moz_bookmarks
            INNER JOIN moz_places ON moz_bookmarks.fk = moz_places.id
            WHERE moz_bookmarks.title LIKE ?
            """

            cursor.execute(query, (f"%{bookmark_query}%",))
            results = cursor.fetchall()

            logging.debug(results)

            conn.close()

        elif (default_browser == "Brave" and bookmark_browser == "bookmark") or bookmark_browser == "brave bookmark":
            logging.debug("brave loop")
            # Brave bookmarks location in Windows
            brave_profile_path = os.path.join(os.path.expanduser("~"), "AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Bookmarks")
            if os.path.exists(brave_profile_path):
                with open(brave_profile_path, 'r') as f:
                    bookmarks_data = json.load(f)

                def search_bookmarks(node, bookmark_query):
                    results = []

                    if 'name' in node and bookmark_query.lower() in node['name'].lower():
                        results.append((node['name'], node['url']))

                    if 'children' in node:
                        for child in node['children']:
                            results.extend(search_bookmarks(child, bookmark_query))

                    return results

                results = search_bookmarks(bookmarks_data['roots']['bookmark_bar'], bookmark_query)
                results.extend(search_bookmarks(bookmarks_data['roots']['other'], bookmark_query))
                logging.debug(results)

            else:
                logging.debug("Unable to locate the Brave bookmarks file.")


        elif (default_browser == "Edge" and bookmark_browser == "bookmark") or bookmark_browser == "edge bookmark":
            logging.debug("edge loop")
            # Edge bookmarks location in Windows
            edge_profile_path = os.path.join(os.path.expanduser("~"), "AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Bookmarks")

            if os.path.exists(edge_profile_path):
                with open(edge_profile_path, 'r') as f:
                    bookmarks_data = json.load(f)
                    print(bookmarks_data)

                def search_bookmarks(node, bookmark_query):
                    results = []

                    if 'name' in node and bookmark_query.lower() in node['name'].lower():
                        results.append((node['name'], node['url']))

                    if 'children' in node:
                        for child in node['children']:
                            results.extend(search_bookmarks(child, bookmark_query))

                    return results

                results = search_bookmarks(bookmarks_data['roots']['bookmark_bar'], bookmark_query)
                results.extend(search_bookmarks(bookmarks_data['roots']['other'], bookmark_query))
                logging.debug(results)

            else:
                logging.debug("Unable to locate the Edge bookmarks file.")



        if results:
            logging.debug(f"Launching bookmark: {results[0][0]} ({results[0][1]})")

            if default_browser == 'Firefox':
                logging.debug("launching firefox")
                firefox_executable = None
                firefox_path1 = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
                firefox_path2 = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
                if os.path.exists(firefox_path1):
                    firefox_executable = firefox_path1
                elif os.path.exists(firefox_path2):
                    firefox_executable = firefox_path2
                if firefox_executable is not None:
                    subprocess.Popen([firefox_executable, results[0][1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    logging.debug("Firefox executable not found.")

            elif default_browser == 'Brave':
                logging.debug("launching brave")
                brave_executable = None
                brave_path1 = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                brave_path2 = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                if os.path.exists(brave_path1):
                    brave_executable = brave_path1
                elif os.path.exists(brave_path2):
                    brave_executable = brave_path2
                if brave_executable is not None:
                    subprocess.Popen([brave_executable, results[0][1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    logging.debug("Brave executable not found.")

            elif default_browser == 'Edge':
                logging.debug("launching edge")
                edge_executable = None
                edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
                if os.path.exists(edge_path):
                    edge_executable = edge_path
                if edge_executable is not None:
                    subprocess.Popen([edge_executable, results[0][1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    logging.debug("Edge executable not found.")
        else:
                output_widget.append("No bookmarks found with the specified search term.")            
    else:
        logging.debug("Unsupported OS")

