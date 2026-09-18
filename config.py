import os

from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("RUDRA_MODEL", "phi4-mini")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
)

MEMORY_FILE = os.getenv(
    "MEMORY_FILE",
    "memory.json"
)

SETTINGS_FILE = os.getenv(
    "SETTINGS_FILE",
    "settings.json"
)

OWNER_NAME = os.getenv(
    "OWNER_NAME",
    "Gaurav"
)

OWNER_KEY = os.getenv(
    "OWNER_KEY",
    ""
)

MAX_CONTEXT_MESSAGES = int(
    os.getenv("MAX_CONTEXT_MESSAGES", "12")
)