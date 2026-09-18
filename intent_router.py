import re

from command_router import route_command


def normalize(text):

    text = text.lower().strip()

    replacements = {
        "btao": "batao",
        "bta": "batao",
        "dikhao": "show",
        "dikha": "show",
        "bnao": "create",
        "bana": "create",
        "banao": "create",
        "padh": "read",
        "padho": "read"
    }

    words = text.split()

    words = [
        replacements.get(
            word,
            word
        )
        for word in words
    ]

    return " ".join(words)


def smart_route(user):

    original = user.strip()

    text = normalize(
        original
    )

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    if (
        re.search(
            r"\btime\b",
            text
        )
        or "kitne baje" in text
        or "baje hain" in text
    ):

        return route_command(
            "current time"
        )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    if (
        re.search(
            r"\bdate\b",
            text
        )
        or "tarikh" in text
        or "aaj ki date" in text
    ):

        return route_command(
            "current date"
        )

    # -----------------------------------------------------
    # SYSTEM INFO
    # -----------------------------------------------------

    if (
        "system info" in text
        or "computer info" in text
        or "pc info" in text
        or "computer ki information" in text
        or "pc ki information" in text
    ):

        return route_command(
            "system info"
        )

    # -----------------------------------------------------
    # LIST FILES
    # -----------------------------------------------------

    if (
        "list files" in text
        or "show files" in text
        or "files show" in text
        or "folder dikhao" in text
        or "folder show" in text
    ):

        return route_command(
            "list files"
        )

    # -----------------------------------------------------
    # CREATE FOLDER
    # -----------------------------------------------------

    match = re.search(
        r"(?:create|make|new)\s+folder\s+(.+)",
        text
    )

    if match:

        name = match.group(
            1
        ).strip()

        return route_command(
            f"create folder {name}"
        )

    match = re.search(
        r"folder\s+(?:create|banao)\s+(.+)",
        text
    )

    if match:

        name = match.group(
            1
        ).strip()

        return route_command(
            f"create folder {name}"
        )

    # -----------------------------------------------------
    # READ FILE
    # -----------------------------------------------------

    match = re.search(
        r"(?:read|open|show)\s+file\s+(.+)",
        text
    )

    if match:

        name = match.group(
            1
        ).strip()

        return route_command(
            f"read file {name}"
        )

    # -----------------------------------------------------
    # CHECK FILE
    # -----------------------------------------------------

    match = re.search(
        r"(?:check|does)\s+file\s+(.+)",
        text
    )

    if match:

        name = match.group(
            1
        ).strip()

        return route_command(
            f"check file {name}"
        )

    # -----------------------------------------------------
    # CALCULATOR
    # -----------------------------------------------------

    if re.fullmatch(
        r"[0-9+\-*/().% \t]+",
        original
    ):

        return route_command(
            f"calculate {original}"
        )

    return route_command(
        original
    )