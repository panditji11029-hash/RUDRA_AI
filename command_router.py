import ast
import re

from tool_manager import tool_manager


def extract_calculation(text):

    expression = text.strip()

    prefixes = [
        "calculate ",
        "calc ",
        "what is "
    ]

    lower = expression.lower()

    for prefix in prefixes:

        if lower.startswith(prefix):

            expression = expression[
                len(prefix):
            ].strip()

            break

    if not expression:
        return None

    if not re.fullmatch(
        r"[0-9+\-*/().% \t]+",
        expression
    ):
        return None

    return expression


def route_command(user):

    text = user.strip()

    low = text.lower()

    # -----------------------------------------------------
    # SYSTEM INFO
    # -----------------------------------------------------

    if low in {
        "system info",
        "system information",
        "computer info",
        "pc info"
    }:

        return tool_manager.execute(
            "system_info"
        )

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    if low in {
        "time",
        "current time",
        "what time is it",
        "time batao"
    }:

        return tool_manager.execute(
            "current_time"
        )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    if low in {
        "date",
        "current date",
        "today's date",
        "what is today's date",
        "date batao"
    }:

        return tool_manager.execute(
            "current_date"
        )

    # -----------------------------------------------------
    # LIST FILES
    # -----------------------------------------------------

    if low in {
        "list files",
        "show files",
        "list folder",
        "show folder"
    }:

        return tool_manager.execute(
            "list_files"
        )

    # -----------------------------------------------------
    # CREATE FOLDER
    # -----------------------------------------------------

    for prefix in [
        "create folder ",
        "make folder ",
        "new folder "
    ]:

        if low.startswith(prefix):

            name = text[
                len(prefix):
            ].strip()

            return tool_manager.execute(
                "create_folder",
                name
            )

    # -----------------------------------------------------
    # READ FILE
    # -----------------------------------------------------

    for prefix in [
        "read file ",
        "open file ",
        "show file "
    ]:

        if low.startswith(prefix):

            name = text[
                len(prefix):
            ].strip()

            return tool_manager.execute(
                "read_file",
                name
            )

    # -----------------------------------------------------
    # CHECK FILE
    # -----------------------------------------------------

    for prefix in [
        "check file ",
        "does file exist "
    ]:

        if low.startswith(prefix):

            name = text[
                len(prefix):
            ].strip()

            return tool_manager.execute(
                "check_file",
                name
            )

    # -----------------------------------------------------
    # CREATE FILE
    # -----------------------------------------------------

    if low.startswith(
        "create file "
    ):

        remainder = text[
            len("create file "):
        ].strip()

        if not remainder:

            return (
                "Please provide "
                "a file name."
            )

        parts = remainder.split(
            " ",
            1
        )

        filename = parts[0]

        content = (
            parts[1]
            if len(parts) > 1
            else ""
        )

        return tool_manager.execute(
            "create_file",
            filename,
            content
        )

    # -----------------------------------------------------
    # CALCULATOR
    # -----------------------------------------------------

    expression = extract_calculation(
        text
    )

    if expression:

        return tool_manager.execute(
            "calculate",
            expression
        )

    return None