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

def unmute_computer_execution(output_widget):
    """
    Executes the 'unmute_computer' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
    """

    # Create a keyboard controller
    keyboard_controller = keyboard.Controller()

    # Simulate pressing and releasing the mute key
    with keyboard_controller.pressed(keyboard.Key.media_volume_mute):
        pass

