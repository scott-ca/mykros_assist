from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QTextEdit, QTableWidget, QTableWidgetItem
from PySide2.QtCore import QTimer
import difflib

import re
import pint
import platform
import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info


def convert_units_execution(output_widget, entities, chat_prompt):

    """
    Executes the 'convert_units' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """


    if "unit_amount" in entities:
        unit_amount = entities.get("unit_amount")
    else:
        # prompt the user for the unit_amount
        unit_amount = request_additional_info(chat_prompt, "Please enter the amount you would like to convert:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if unit_amount is None:
            output_widget.append("Convert units operation canceled.")
            return

    if "from_unit" in entities:
        from_unit = entities.get("from_unit").lower()
    else:
        # prompt the user for the from_unit
        from_unit = request_additional_info(chat_prompt, "Please enter the source unit(IE. feet or inches) that you would to convert from:").lower()
 
        # Check if the user would like to cancel the operation when prompted for additional information
        if from_unit is None:
            output_widget.append("Convert units operation canceled.")

    if "to_unit" in entities:
        to_unit = entities.get("to_unit").lower()
    else:
        # prompt the user for the to_unit
        to_unit = request_additional_info(chat_prompt, "Please enter the destination unit(IE. feet or inches) that you would to convert from:").lower()
 
        # Check if the user would like to cancel the operation when prompted for additional information
        if to_unit is None:
            output_widget.append("Convert units operation canceled.")

    # Converts unit amount to a float from a string
    unit_amount = float(unit_amount)

    # Initialize the Pint UnitRegistry
    ureg = pint.UnitRegistry()
    

    if from_unit in ("c", "celsius"):
        from_unit = "degC"
    elif from_unit in ("f", "fahrenheit"):
        from_unit = "degF"
  
    if to_unit in ("c", "Celsius", "C","Celsius"):
        to_unit = "degC"
    elif to_unit in ("f", "fahrenheit", "F", "Fahrenheit"):
        to_unit = "degF"


    # Perform other unit conversions without specifying temperature scales
    source_quantity = ureg.Quantity(unit_amount, ureg.parse_expression(from_unit))
    target_quantity = source_quantity.to(ureg.parse_expression(to_unit))
    
    if from_unit == "degC":
        from_unit = "Celsius"
    if from_unit == "degF":
        from_unit = "Fahrenheit"
    
    if to_unit == "degC":
        to_unit = "Celsius"
    if to_unit == "degF":
        to_unit = "Fahrenheit"

    output_widget.append(f"{unit_amount} {from_unit} is equal to {target_quantity.magnitude:.2f} {to_unit}")
