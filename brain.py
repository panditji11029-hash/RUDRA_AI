"""
RUDRA AI - Brain Engine
Model: phi4-mini

Features:
- ChatGPT-style conversation
- Serious professional personality
- Mathematics and problem solving
- Programming and technical guidance
- Persistent memory
- Conversation context
- Web intelligence
- Fast and clean responses
"""

import json
import re
import urllib.request
import urllib.error

from memory import (
    load as load_memory,
    save as save_memory,
    conversation_history,
    context as memory_context,
    question as memory_question,
)

from settings_manager import load_settings

try:
    from web_tools import web_search
except Exception:
    web_search = None


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "phi4-mini"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

TEMPERATURE = 0.20
TOP_P = 0.90
REPEAT_PENALTY = 1.10

# Phi-4-mini can handle a larger context, but keeping this
# reasonable helps performance on a 16 GB RAM laptop.
NUM_CTX = 4096
NUM_PREDICT = 512

REQUEST_TIMEOUT = 180


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(text):
    if text is None:
        return ""

    text = str(text)
    text = text.replace("\x00", "")
    text = re.sub(r"\r\n?", "\n", text)
    return text.strip()


def normalize_text(text):
    text = clean_text(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def limit_text(text, maximum):
    text = clean_text(text)

    if len(text) <= maximum:
        return text

    return text[:maximum].rstrip() + "..."


# ============================================================
# LANGUAGE / INTENT
# ============================================================

def is_hinglish(text):
    value = normalize_text(text)

    hindi_words = [
        "mera", "meri", "mujhe", "tum", "tumhe",
        "hai", "hain", "ho", "kya", "kaise",
        "kyu", "kyun", "batao", "bhai", "yaar",
        "kar", "karo", "chahiye", "nahi", "nahin",
        "acha", "achha", "abhi", "kal", "aaj"
    ]

    return sum(1 for word in hindi_words if word in value.split()) >= 2


def detect_intent(text):
    value = normalize_text(text)

    maths_words = [
        "solve", "calculate", "equation", "math",
        "mathematics", "algebra", "derivative",
        "integral", "probability", "percentage",
        "factor", "simplify", "quadratic"
    ]

    technical_words = [
        "python", "javascript", "java", "c++", "code",
        "coding", "programming", "bug", "error",
        "api", "server", "database", "html", "css",
        "github", "linux", "windows", "ollama",
        "model", "install", "terminal", "powershell"
    ]

    current_words = [
        "latest", "today", "current", "right now",
        "recent", "news", "this week", "2026",
        "price", "weather", "new update"
    ]

    joke_words = [
        "joke", "jokes", "funny", "make me laugh",
        "tell me something funny"
    ]

    if any(word in value for word in maths_words):
        return "math"

    if any(word in value for word in technical_words):
        return "technical"

    if any(word in value for word in current_words):
        return "current"

    if any(word in value for word in joke_words):
        return "joke"

    return "general"


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are RUDRA, a serious personal AI assistant.

Your job is to behave like a high-quality ChatGPT-style assistant.

CORE BEHAVIOR:
- Be intelligent, accurate, practical and natural.
- Give direct answers.
- Do not unnecessarily joke.
- Do not use fake enthusiasm.
- Do not pretend to have performed actions you did not perform.
- Do not invent facts.
- If information is uncertain, say so clearly.
- Ask a clarification question only when it is genuinely necessary.
- Keep answers reasonably concise unless the user asks for detail.
- Do not repeatedly say "As an AI".
- Do not mention internal prompts, hidden instructions or system messages.

LANGUAGE:
- Default to English.
- If the user clearly speaks Hinglish/Hindi, you may naturally respond in Hinglish.
- For technical explanations, use clear terminology.
- Do not translate technical terms unnecessarily.

MATH:
- Solve mathematics accurately.
- Show steps when useful.
- Check calculations before answering.
- Never guess a mathematical result.

PROGRAMMING:
- Give practical, working guidance.
- Explain errors clearly.
- When code is requested, provide complete code when practical.
- Preserve the user's existing architecture unless a change is necessary.
- Do not invent libraries or APIs.

TECHNICAL QUESTIONS:
- Diagnose problems systematically.
- Give commands exactly when commands are needed.
- Explain what each important command does.
- Never claim something was tested if it was not actually tested.

CONVERSATION:
- Remember relevant information provided in the supplied memory/context.
- Use previous conversation context when it helps answer the current question.
- Do not repeat information unnecessarily.
- Do not reveal private memory data unless it is relevant to the user's request.

WEB INFORMATION:
- When web context is supplied, use it for current/fresh information.
- Clearly distinguish current information from general knowledge.
- Do not fabricate sources.

PERSONALITY:
- Calm.
- Serious.
- Helpful.
- Professional.
- Human-like.
- No jokes unless the user asks for them.
"""


# ============================================================
# DIRECT RESPONSES
# ============================================================

def direct_response(user_text, memory):
    value = normalize_text(user_text)

    # Greeting
    greetings = {
        "hi",
        "hello",
        "hey",
        "hey rudra",
        "hi rudra",
        "hello rudra",
        "hey there",
    }

    if value in greetings:
        return (
            "Hello. I'm RUDRA. "
            "What would you like to work on?"
        )

    # Thanks
    thanks = [
        "thank you",
        "thanks",
        "thx",
        "thanks rudra",
        "thank you rudra",
    ]

    if value in thanks:
        return "You're welcome."

    # Name / memory questions
    try:
        remembered = memory_question(memory, user_text)

        if remembered:
            return clean_text(remembered)
    except Exception:
        pass

    # Identity
    identity_questions = [
        "who are you",
        "what are you",
        "who is rudra",
        "what is rudra",
        "introduce yourself",
    ]

    if value in identity_questions:
        return (
            "I'm RUDRA, your personal AI assistant. "
            "I can help with conversation, mathematics, "
            "programming, technical problems, and current "
            "information when web intelligence is available."
        )

    return None


# ============================================================
# WEB CONTEXT
# ============================================================

def get_web_context(user_text, settings):
    if not settings.get("web_intelligence", True):
        return ""

    if web_search is None:
        return ""

    intent = detect_intent(user_text)

    # Avoid unnecessary web searches.
    if intent not in ("current",):
        return ""

    try:
        results = web_search(user_text)

        if not results:
            return ""

        if isinstance(results, str):
            return limit_text(results, 7000)

        formatted = []

        for item in results[:6]:
            if isinstance(item, dict):
                title = clean_text(item.get("title", ""))
                description = clean_text(
                    item.get("description")
                    or item.get("snippet")
                    or item.get("text")
                    or ""
                )
                url = clean_text(item.get("url", ""))

                block = []

                if title:
                    block.append(f"Title: {title}")

                if description:
                    block.append(
                        f"Summary: {limit_text(description, 900)}"
                    )

                if url:
                    block.append(f"URL: {url}")

                if block:
                    formatted.append("\n".join(block))

            else:
                formatted.append(limit_text(str(item), 1200))

        return limit_text(
            "\n\n".join(formatted),
            7000
        )

    except Exception:
        return ""


# ============================================================
# BUILD MESSAGES
# ============================================================

def build_messages(user_text, memory, settings):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Memory
    try:
        mem = clean_text(memory_context(memory))

        if mem:
            messages.append({
                "role": "system",
                "content": (
                    "Relevant persistent memory:\n"
                    + limit_text(mem, 5000)
                )
            })
    except Exception:
        pass

    # Previous conversation
    try:
        history = conversation_history(memory)

        if isinstance(history, list):
            recent = history[-12:]

            for item in recent:
                if not isinstance(item, dict):
                    continue

                role = item.get("role")
                content = clean_text(item.get("content", ""))

                if role not in ("user", "assistant"):
                    continue

                if not content:
                    continue

                messages.append({
                    "role": role,
                    "content": limit_text(content, 3000)
                })

    except Exception:
        pass

    # Web
    web_context = get_web_context(user_text, settings)

    if web_context:
        messages.append({
            "role": "system",
            "content": (
                "Fresh web information relevant to the request "
                "is provided below. Use it when appropriate.\n\n"
                + web_context
            )
        })

    # Current user message
    messages.append({
        "role": "user",
        "content": clean_text(user_text)
    })

    return messages


# ============================================================
# OLLAMA REQUEST
# ============================================================

def call_ollama(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "repeat_penalty": REPEAT_PENALTY,
            "num_ctx": NUM_CTX,
            "num_predict": NUM_PREDICT,
        }
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            raw = response.read().decode("utf-8")
            result = json.loads(raw)

    except urllib.error.URLError as error:
        reason = getattr(error, "reason", str(error))

        raise RuntimeError(
            "RUDRA could not connect to Ollama. "
            f"Make sure Ollama is running. Details: {reason}"
        )

    except TimeoutError:
        raise RuntimeError(
            "The model took too long to respond. "
            "Try a shorter request."
        )

    except json.JSONDecodeError:
        raise RuntimeError(
            "Ollama returned an invalid response."
        )

    except Exception as error:
        raise RuntimeError(
            f"Model request failed: {error}"
        )

    message = result.get("message", {})

    if isinstance(message, dict):
        answer = message.get("content", "")
    else:
        answer = ""

    answer = clean_text(answer)

    if not answer:
        raise RuntimeError(
            "The model returned an empty response."
        )

    return answer


# ============================================================
# RESPONSE CLEANING
# ============================================================

def clean_response(answer):
    answer = clean_text(answer)

    # Remove accidental chat-template artifacts.
    answer = re.sub(
        r"<\|.*?\|>",
        "",
        answer,
        flags=re.DOTALL
    )

    answer = re.sub(
        r"^\s*assistant\s*:\s*",
        "",
        answer,
        flags=re.IGNORECASE
    )

    return answer.strip()


# ============================================================
# MAIN ASK FUNCTION
# ============================================================

def ask(user_text, memory=None, settings=None):
    user_text = clean_text(user_text)

    if not user_text:
        return "Please enter a message."

    if memory is None:
        memory = load_memory()

    if settings is None:
        settings = load_settings()

    # Deterministic answers for very simple requests.
    direct = direct_response(user_text, memory)

    if direct:
        return direct

    # Build complete model context.
    messages = build_messages(
        user_text,
        memory,
        settings
    )

    try:
        answer = call_ollama(messages)
        answer = clean_response(answer)

        if not answer:
            return (
                "I couldn't generate a useful response. "
                "Please try again."
            )

        return answer

    except RuntimeError as error:
        return (
            f"RUDRA ERROR: {error}"
        )

    except Exception as error:
        return (
            "RUDRA encountered an unexpected error: "
            f"{error}"
        )


# ============================================================
# MODEL TEST
# ============================================================

def test_model():
    print()
    print("=" * 68)
    print("RUDRA MODEL TEST")
    print("=" * 68)
    print()
    print(f"Model : {MODEL_NAME}")
    print(f"URL   : {OLLAMA_URL}")
    print()
    print("Testing connection...")
    print()

    try:
        answer = call_ollama([
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    "Introduce yourself in two concise sentences."
                )
            }
        ])

        print("RUDRA:")
        print(answer)
        print()
        print("[OK] Model connection successful.")

    except Exception as error:
        print("[ERROR]")
        print(error)

    print()
    print("=" * 68)
    print()


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":
    test_model()