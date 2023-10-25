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

from util.translator import translate_custom

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info

def translate_words_execution(output_widget, entities, chat_prompt):
    """
    Tranlates a webpage using Google Translate.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "word_translate_query" in entities:
        word_translate_query = entities.get("word_translate_query")
    else:
        # prompt the user for the word_translate_query
        word_translate_query = request_additional_info(chat_prompt, "Enter the word or phrase that you would like to translated:")
        
        # Check if the user would like to cancel the operation when prompted for additional information
        if word_translate_query is None:
            output_widget.append("translate words operation canceled.")
            return

    if "custom_from_language" in entities:
        custom_from_language = entities.get("custom_from_language")
    else:
        # prompt the user for the custom_from_language
        custom_from_language = request_additional_info(chat_prompt, "Enter the language you would like to have translated to:")
        
        # Check if the user would like to cancel the operation when prompted for additional information
        if custom_from_language is None:
            output_widget.append("translate words operation canceled.")
            return


    if "custom_to_language" in entities:
        custom_to_language = entities.get("custom_to_language")
    else:
        # prompt the user for the custom_from_language
        custom_to_language = request_additional_info(chat_prompt, "Enter the language you would like have translated from:")
        
        # Check if the user would like to cancel the operation when prompted for additional information
        if custom_to_language is None:
            output_widget.append("translate words operation canceled.")
            return

    language_codes = {
    "arabic": "ar",
    "azerbaijani": "az",
    "catalan": "ca",
    "chinese": "zh",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "finnish": "fi",
    "french": "fr",
    "german": "de",
    "greek": "el",
    "hebrew": "he",
    "hindi": "hi",
    "hungarian": "hu",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "porean": "ko",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "russian": "ru",
    "slovak": "sk",
    "spanish": "es",
    "swedish": "sv",
    "turkish": "tr",
    "ukrainian": "uk"
    }

    custom_from_code = language_codes.get(custom_from_language.lower())
    custom_to_code = language_codes.get(custom_to_language.lower())

    translated_text = translate_custom(word_translate_query, custom_from_code, custom_to_code)

    output_widget.append(f"AI: The original {custom_from_language.lower()} text of |{word_translate_query}| translates to |{translated_text}| in {custom_to_language.lower()}")