from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import wordhoard
import os
import sys
import platform
import logging
from spellchecker import SpellChecker

from util.misc import request_additional_info

def word_operation_execution(output_widget, entities, chat_prompt, working_action):
    """
    Preforms various word oprtions on a word. 
    Included are definitions, antonyms, synonyms, hyponyms, hypernyms, homophones.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
        working_action (str): The name of the intent so it can call the correct function.
    """

    entity_mapping = {
        "define_word": {
            "entity": "define_query",
            "class": wordhoard.Definitions,
            "method": "find_definitions"
        },
        "antonymize_word": {
            "entity": "antonymize_query",
            "class": wordhoard.Antonyms,
            "method": "find_antonyms"
        },
        "synonymize_word": {
            "entity": "synonymize_query",
            "class": wordhoard.Synonyms,
            "method": "find_synonyms"
        },
        "hyponymize_word": {
            "entity": "hyponymize_query",
            "class": wordhoard.Hyponyms,
            "method": "find_hyponyms"
        },
        "hypernymize_word": {
            "entity": "hypernymize_query",
            "class": wordhoard.Hypernyms,
            "method": "find_hypernyms"
        },
        "homophonize_word": {
            "entity": "homophonize_query",
            "class": wordhoard.Homophones,
            "method": "find_homophones"
        }
    }

    logging.debug("mapping")
    logging.debug(entity_mapping)
    if working_action in entity_mapping:
        entity_name = entity_mapping[working_action]["entity"]
        operation_class = entity_mapping[working_action]["class"]
        method_name = entity_mapping[working_action]["method"]

        if entity_name in entities:
            word = entities.get(entity_name)
        else:
            word = request_additional_info(chat_prompt, f"What word would you like to {working_action.split('_')[0]}:")

            if word is None:
                output_widget.append(f"{working_action.split('_')[0]} word operation canceled.")
                return

        operation = operation_class(word)
        operation_method = getattr(operation, method_name)
        operation_results = operation_method()

        output_widget.append(f"{working_action} for {word}: {operation_results}")

        # privacy_cleanup = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'wordhoard_error.yaml')



        error_path = os.path.abspath(__file__)  # Get the absolute path of the current file

        # Navigate up three directories
        for _ in range(4):
            error_path = os.path.dirname(error_path)

        # Construct the path to wordhoard_error.yaml
        privacy_cleanup = os.path.join(error_path, 'wordhoard_error.yaml')


        print("privacy cleanup")
        print(privacy_cleanup)

        logging.debug(privacy_cleanup)
        if os.path.exists(privacy_cleanup):
            os.remove(privacy_cleanup)
            logging.debug("file deleted")
        else:
            logging.debug("file not found")
    else:
        output_widget.append("AI: Unknown word operation.")

