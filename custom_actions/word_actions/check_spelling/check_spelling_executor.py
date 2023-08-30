from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
from spellchecker import SpellChecker
import os
import platform
import subprocess

import logging

from util.misc import request_additional_info

def check_spelling_execution(output_widget, entities, chat_prompt):
    """
    Preforms spell checking on a word.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "misspelled_word" in entities:
        misspelled_word = entities.get("misspelled_word")
    else:
        # prompt the user for the misspelled word
        misspelled_word = request_additional_info(chat_prompt, "What word would you like to check the spelling of:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if misspelled_word is None:
            output_widget.append("Running spell check command operation canceled.")
            return

    spell = SpellChecker()

    # Find those words that may be misspelled
    misspelled = spell.unknown([misspelled_word])

    if len(misspelled) == 0:
        output_widget.append(f"The word {misspelled_word} is spelled correctly.")
    else:
        output_widget.append(f"The misspelled word is '{misspelled_word}'")
        for word in misspelled:
            # Get the one `most likely` answer
            most_likely_correction = spell.correction(word)

            # Get a list of `likely` options
            alternative_suggestions = spell.candidates(word)

            # Format and print the output
            output_widget.append(f"Most likely correction is '{most_likely_correction}'.")
            output_widget.append(f"Alternative suggestions are {', '.join(alternative_suggestions)}")          

