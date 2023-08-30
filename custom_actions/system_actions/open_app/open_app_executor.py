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

def open_app_execution(output_widget, entities, chat_prompt, os_name):
    """
    Opens of an application.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
        os_name (str): The name of the operating system.
    """

    if "open_app_id" in entities:
        open_app_id = entities.get("open_app_id")
    else:
        # prompt the user for the open_app_id entity
        open_app_id = request_additional_info(chat_prompt, "Enter the application that you wish to open:")
        
        # Check if the user would like to cancel the operation when prompted for additional information
        if open_app_id is None:
            output_widget.append("Open application operation canceled.")
            return

    def get_all_apps_win(max_depth=3):
        apps = []

        # List of directories where browsers and other applications might be installed
        directories = [
            'C:\\Program Files\\',
            'C:\\Program Files (x86)\\',
            os.path.expanduser('~\\AppData\\Local\\'),
            'C:\\Windows\\System32\\',
            'C:\\Windows\\SysWOW64\\'
        ]

        def dfs(directory, depth=0):
            if depth > max_depth:
                return

            try:
                for entry in os.scandir(directory):
                    if entry.is_dir(follow_symlinks=False):
                        dfs(entry.path, depth + 1)
                    elif entry.is_file(follow_symlinks=False) and entry.name.endswith('.exe'):
                        apps.append({
                            'type': 'normal',
                            'name': os.path.splitext(entry.name)[0],
                            'full_info': entry.path
                        })
            except (FileNotFoundError, PermissionError):
                pass

        for directory in directories:
            dfs(directory)

        # Remove duplicates based on full_info
        apps = list({app['full_info']:app for app in apps}.values())

        return apps

    def get_all_apps_linux():
        apps = []
        
        # Get the list of commands in the $PATH
        for directory in os.environ['PATH'].split(os.pathsep):
            try:
                apps.extend([{'type': 'native', 'name': os.path.splitext(app)[0], 'full_info': os.path.join(directory, app)} for app in os.listdir(directory) if os.access(os.path.join(directory, app), os.X_OK)])
            except FileNotFoundError:
                pass
        try:
            cmd_output = subprocess.Popen('flatpak list --app', stdout=subprocess.PIPE, shell=True)
            cmd_output = cmd_output.communicate()[0].decode('utf-8')

            flatpak_apps = [{'type': 'flatpak', 'name': line.split('\t')[1], 'full_info': line} for line in cmd_output.split('\n') if line]
            apps.extend(flatpak_apps)
        except subprocess.CalledProcessError:
            pass

        try:
            cmd_output = subprocess.Popen('snap list', stdout=subprocess.PIPE, shell=True)
            cmd_output = cmd_output.communicate()[0].decode('utf-8')

            snap_apps = [{'type': 'snap', 'name': line.split()[0], 'full_info': line} for line in cmd_output.split('\n') if line]
            apps.extend(snap_apps)
        except subprocess.CalledProcessError:
            pass

        # Remove duplicates based on name
        apps = list({app['name']:app for app in apps}.values())

        return apps

    def open_app_linux(app):
        if app['type'] == 'native':
            subprocess.Popen(app['full_info'])
        elif app['type'] == 'flatpak':
            subprocess.Popen(['flatpak', 'run', app['name']])
        elif app['type'] == 'snap':
            subprocess.Popen(['snap', 'run', app['name']])


    def open_app_win(app):
        try:
            subprocess.Popen(app['name'])
        except FileNotFoundError:
            subprocess.Popen(app['full_info'])

    if os_name == 'Windows':
        apps = get_all_apps_win()
        open_app = open_app_win
    elif os_name == 'Linux':
        apps = get_all_apps_linux()
        open_app = open_app_linux
    else:
        output_widget.append('Unsupported OS')
        return

    matches = [app for app in apps if open_app_id.lower() in app['name'].lower()]
    print("matchy")
    print(matches)

    if len(matches) == 0:
        output_widget.append('No applications found')
        return

    output_widget.append('Did you mean one of these?')

    if os_name == 'Windows':
        dir_to_exact_matches = {}
        for match in matches:
            directory = os.path.dirname(match["full_info"])
            is_exact_match = match['name'].lower() == open_app_id.lower()

            if directory not in dir_to_exact_matches:
                dir_to_exact_matches[directory] = {
                    'exact_matches': [],
                    'other_matches': []
                }

            if is_exact_match:
                dir_to_exact_matches[directory]['exact_matches'].append(match)
            else:
                dir_to_exact_matches[directory]['other_matches'].append(match)

        matches = []
        for matches_in_dir in dir_to_exact_matches.values():
            if matches_in_dir['exact_matches']:
                matches.extend(matches_in_dir['exact_matches'])
                if len(matches_in_dir['exact_matches']) > 1:
                    matches.extend(matches_in_dir['other_matches'])
            else:
                matches.extend(matches_in_dir['other_matches'])

    for i, match in enumerate(matches):
        output_widget.append(f'{i+1}: {match["name"]}')
        output_widget.append(f'   path: {match["full_info"]}')

    chat_prompt.expecting_additional_info = True
    chat_prompt.request_input('Enter the number of the correct application: ')
    app_num = int(chat_prompt.wait_for_input().strip().lower())

    chat_prompt.expecting_additional_info = True
    chat_prompt.request_input(f'Do you want to open {matches[app_num-1]["name"]}? (yes/no): ')
    confirm = chat_prompt.wait_for_input().strip().lower()


    if confirm.lower() == 'yes':
        thread = threading.Thread(target=open_app, args=(matches[app_num-1],))
        thread.start()

    if os_name == 'Windows':
        software_name, _ = os.path.splitext(os.path.basename(matches[app_num-1]["full_info"].split('\t')[0]))
    elif os_name == 'Linux':
        if matches[app_num-1]["type"] == "flatpak":
            print("snap/native loop")
            software_name = matches[app_num-1]["full_info"].split('\t')[0]
        elif matches[app_num-1]["type"] == "snap" or matches[app_num-1]["type"]== "native":
            software_name = matches[app_num-1]["name"]
    
    output_widget.append(f"AI: I have opened {software_name} software")

