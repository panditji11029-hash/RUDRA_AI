import json
import os
import re
from datetime import datetime


MEMORY_FILE = "rudra_memory.json"
MAX_HISTORY = 40
MAX_FACTS = 150


DEFAULT_MEMORY = {
    "profile": {},
    "facts": [],
    "history": []
}


def _new_memory():
    return {
        "profile": {},
        "facts": [],
        "history": []
    }


def load():
    if not os.path.exists(MEMORY_FILE):
        return _new_memory()

    try:
        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return _new_memory()

        data.setdefault("profile", {})
        data.setdefault("facts", [])
        data.setdefault("history", [])

        if not isinstance(data["profile"], dict):
            data["profile"] = {}

        if not isinstance(data["facts"], list):
            data["facts"] = []

        if not isinstance(data["history"], list):
            data["history"] = []

        return data

    except Exception:
        return _new_memory()


def save(memory):
    try:
        temporary_file = MEMORY_FILE + ".tmp"

        with open(
            temporary_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

        os.replace(
            temporary_file,
            MEMORY_FILE
        )

        return True

    except Exception:
        try:
            if os.path.exists(temporary_file):
                os.remove(temporary_file)
        except Exception:
            pass

        return False


def normalize_text(text):
    return re.sub(
        r"\s+",
        " ",
        str(text).strip()
    )


def add_fact(memory, fact):
    fact = normalize_text(fact)

    if not fact:
        return False

    facts = memory.setdefault("facts", [])

    existing_lower = {
        str(item).strip().lower()
        for item in facts
    }

    if fact.lower() not in existing_lower:
        facts.append(fact)

    if len(facts) > MAX_FACTS:
        del facts[:-MAX_FACTS]

    return True


def set_profile(memory, key, value):
    key = normalize_text(key).lower()
    value = normalize_text(value)

    if not key or not value:
        return False

    memory.setdefault("profile", {})[key] = value

    return True


def _clean_name(name):
    name = name.strip()

    name = re.sub(
        r"[.!?,;:]+$",
        "",
        name
    )

    return name.strip()


def extract_personal_information(text, memory):
    """
    Extract obvious user-provided personal information.

    This is intentionally conservative.
    We only save clear statements instead of guessing.
    """

    original = normalize_text(text)

    if not original:
        return False

    lowered = original.lower()

    changed = False

    # -------------------------------------------------
    # NAME
    # -------------------------------------------------

    name_patterns = [
        r"\bmera naam\s+(?:hai\s+)?(.+)$",
        r"\bmy name is\s+(.+)$",
        r"\bi am\s+([A-Za-z][A-Za-z .'-]{1,40})$",
        r"\bi'm\s+([A-Za-z][A-Za-z .'-]{1,40})$",
        r"\bmain\s+([A-Za-z][A-Za-z .'-]{1,40})\s+hoon$"
    ]

    for pattern in name_patterns:
        match = re.search(
            pattern,
            original,
            re.IGNORECASE
        )

        if match:
            candidate = _clean_name(
                match.group(1)
            )

            # Avoid saving obvious non-name sentences.
            blocked = {
                "fine",
                "good",
                "okay",
                "ok",
                "busy",
                "happy",
                "sad",
                "tired",
                "ready",
                "here",
                "back"
            }

            if (
                candidate
                and candidate.lower() not in blocked
                and len(candidate) <= 50
            ):
                set_profile(
                    memory,
                    "name",
                    candidate
                )

                add_fact(
                    memory,
                    f"User's name is {candidate}."
                )

                changed = True

                break

    # -------------------------------------------------
    # LIKES
    # -------------------------------------------------

    like_patterns = [
        r"\bmujhe\s+(.+?)\s+pasand\s+hai\b",
        r"\bi\s+like\s+(.+)$",
        r"\bi\s+love\s+(.+)$"
    ]

    for pattern in like_patterns:
        match = re.search(
            pattern,
            original,
            re.IGNORECASE
        )

        if match:
            thing = normalize_text(
                match.group(1)
            )

            if thing and len(thing) <= 100:
                add_fact(
                    memory,
                    f"User likes {thing}."
                )

                changed = True

                break

    # -------------------------------------------------
    # DISLIKES
    # -------------------------------------------------

    dislike_patterns = [
        r"\bmujhe\s+(.+?)\s+pasand\s+nahi\s+hai\b",
        r"\bi\s+don't\s+like\s+(.+)$",
        r"\bi\s+hate\s+(.+)$"
    ]

    for pattern in dislike_patterns:
        match = re.search(
            pattern,
            original,
            re.IGNORECASE
        )

        if match:
            thing = normalize_text(
                match.group(1)
            )

            if thing and len(thing) <= 100:
                add_fact(
                    memory,
                    f"User does not like {thing}."
                )

                changed = True

                break

    return changed


def remember_conversation(
    memory,
    user_message,
    assistant_message
):
    user_message = normalize_text(user_message)
    assistant_message = normalize_text(assistant_message)

    # Extract clear personal facts before saving conversation.
    extract_personal_information(
        user_message,
        memory
    )

    history = memory.setdefault(
        "history",
        []
    )

    history.append({
        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "user": user_message,
        "assistant": assistant_message
    })

    if len(history) > MAX_HISTORY:
        del history[:-MAX_HISTORY]


def conversation_history(memory):
    return memory.get(
        "history",
        []
    )


def context(memory, limit=16):
    history = memory.get(
        "history",
        []
    )

    if not history:
        return ""

    recent = history[-limit:]

    lines = []

    for item in recent:
        if not isinstance(item, dict):
            continue

        user = normalize_text(
            item.get("user", "")
        )

        assistant = normalize_text(
            item.get("assistant", "")
        )

        if user:
            lines.append(
                f"User: {user}"
            )

        if assistant:
            lines.append(
                f"RUDRA: {assistant}"
            )

    return "\n".join(lines)


def facts(memory):
    return memory.get(
        "facts",
        []
    )


def profile(memory):
    return memory.get(
        "profile",
        {}
    )


def get_profile_value(memory, key):
    return memory.get(
        "profile",
        {}
    ).get(key)


def question(text, memory):
    """
    Handles direct memory questions.
    """

    text = normalize_text(text).lower()

    if not text:
        return None

    name_questions = [
        "mera naam kya hai",
        "mera name kya hai",
        "what is my name",
        "what's my name",
        "do you know my name",
        "tumhe mera naam pata hai"
    ]

    if any(
        phrase in text
        for phrase in name_questions
    ):
        name = get_profile_value(
            memory,
            "name"
        )

        if name:
            return name

    return None


def detect(text, memory):
    text = normalize_text(text).lower()

    if not text:
        return None

    remember_words = [
        "remember",
        "yaad rakh",
        "yaad rakhna",
        "don't forget",
        "mat bhoolna"
    ]

    if any(
        word in text
        for word in remember_words
    ):
        return "remember"

    return None


def clear(memory):
    memory.clear()

    memory.update(
        _new_memory()
    )

    return memory