from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QTextEdit, QTableWidget, QTableWidgetItem
from PySide2.QtCore import QTimer
import difflib

import re
import platform
import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info


def do_math_execution(output_widget, entities, chat_prompt):
    """
    Executes the 'create_file' action.

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "math_expression" in entities:
        math_expression = entities.get("math_expression")
    else:
        # prompt the user for the math_expression
        math_expression = request_additional_info(chat_prompt, "Please enter the math expression you would like me to complete:")

        # Check if the user would like to cancel the operation when prompted for additional information
        if math_expression is None:
            output_widget.append("Math calculation operation canceled.")
            return


    # Convert math operations to standard operators
    operators = {
        "plus": "add",
        "add": "add",
        "subtract": "subtract",
        "minus": "subtract",
        "multiply": "multiply",
        "times": "multiply",
        "divide": "divide",
        "percent of": "percent_of",
        "what percent": "what_percent"
    }
       
    # Pre-process the math_expression to handle the "%" symbol
    math_expression = math_expression.replace('%', ' percent')

    # Find brackets in user input and calculate their value first
    brackets = re.findall(r'\((.*?)\)', math_expression)
    results_dict = {}  # dictionary to store the results of each parenthesis
    for idx, bracket in enumerate(brackets):
        bracket_numbers = re.findall(r'\d+', bracket)
        bracket_operations = re.findall(r'plus|add|subtract|minus|multiply|times|divide|percent of|what percent', bracket)
        bracket_operations = [operators[op] for op in bracket_operations]

        result = 0
        if bracket_numbers:
            result = int(bracket_numbers[0])
            for i in range(1, len(bracket_numbers)):
                operation = bracket_operations[i - 1]
                operand = int(bracket_numbers[i])
                
                if operation == "add":
                    result += operand
                elif operation == "subtract":
                    result -= operand
                elif operation == "multiply":
                    result *= operand
                elif operation == "divide":
                    result /= operand
                elif operation == "percent_of":
                    result = (result * operand) / 100
                elif operation == "what_percent":
                    result = (result / operand) * 100
        
        # replace the parentheses with unique identifiers
        math_expression = math_expression.replace(f'({bracket})', f'result{idx}', 1)
        results_dict[f'result{idx}'] = str(result)

    # replace the identifiers with their respective results
    for key, value in results_dict.items():
        math_expression = math_expression.replace(key, value)

    # Extract entities from user input after calculating brackets
    numbers = re.findall(r'\d+', math_expression)
    math_operations = re.findall(r'plus|add|subtract|minus|multiply|times|divide|percent of|what percent', math_expression)
    math_operations = [operators[op] for op in math_operations]

    result = 0
    if numbers:
        result = int(numbers[0])
        for i in range(1, len(numbers)):
            operation = math_operations[i - 1]
            operand = int(numbers[i])
            
            if operation == "add":
                result += operand
            elif operation == "subtract":
                result -= operand
            elif operation == "multiply":
                result *= operand
            elif operation == "divide":
                result /= operand
            elif operation == "percent_of":
                result = (result * operand) / 100
            elif operation == "what_percent":
                result = (result / operand) * 100

    output_widget.append(f"Result: {result}")

