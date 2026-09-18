import json
import os


SETTINGS_FILE = "rudra_settings.json"


DEFAULT_SETTINGS = {
    "personality": "intelligent, natural, concise, professional",
    "response_style": "balanced",
    "web_intelligence": True
}


def _safe_settings(data):
    settings = DEFAULT_SETTINGS.copy()

    if not isinstance(data, dict):
        return settings

    personality = data.get("personality")

    if isinstance(personality, str) and personality.strip():
        settings["personality"] = personality.strip()

    response_style = data.get("response_style")

    if isinstance(response_style, str) and response_style.strip():
        settings["response_style"] = response_style.strip()

    web_intelligence = data.get("web_intelligence")

    if isinstance(web_intelligence, bool):
        settings["web_intelligence"] = web_intelligence

    return settings


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        return _safe_settings(data)

    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    safe = _safe_settings(settings)

    temporary_file = SETTINGS_FILE + ".tmp"

    try:
        with open(
            temporary_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                safe,
                file,
                indent=4,
                ensure_ascii=False
            )

        os.replace(
            temporary_file,
            SETTINGS_FILE
        )

        return True

    except Exception:
        try:
            if os.path.exists(temporary_file):
                os.remove(temporary_file)
        except Exception:
            pass

        return False


def reset_settings():
    settings = DEFAULT_SETTINGS.copy()
    save_settings(settings)
    return settings


def update_setting(settings, key, value):
    if key not in DEFAULT_SETTINGS:
        return False

    if key == "web_intelligence":
        if isinstance(value, bool):
            settings[key] = value
            return True

        return False

    if value is None:
        return False

    value = str(value).strip()

    if not value:
        return False

    settings[key] = value

    return True