"""
RUDRA AI - Main Application
ChatGPT-style local AI assistant
"""

import os
import time
from datetime import datetime

from brain import ask, MODEL_NAME
from memory import (
    load as load_memory,
    save as save_memory,
    remember_conversation,
    context as memory_context,
    clear as clear_memory,
    profile as memory_profile,
    facts as memory_facts,
)
from session import RudraSession
from security import (
    security_status,
    verify_owner,
    logout_owner,
)
from settings_manager import (
    load_settings,
    save_settings,
    reset_settings,
)


# ============================================================
# STARTUP
# ============================================================

def startup():
    print()
    print("=" * 70)
    print("                         RUDRA AI")
    print("=" * 70)
    print()
    print("Hey! 👋 I'm RUDRA — your personal AI assistant.")
    print()
    print("Built & engineered by Gaurav.")
    print()
    print("System status: ONLINE 🟢")
    print(f"AI model: {MODEL_NAME}")
    print("=" * 70)
    print()


# ============================================================
# HELP
# ============================================================

def show_help():
    print()
    print("RUDRA COMMANDS")
    print("-" * 50)
    print()
    print("/help          Show available commands")
    print("/status        Show RUDRA system status")
    print("/session       Show current session")
    print("/memory        Show saved memory")
    print("/clear memory  Clear all saved memory")
    print("/settings      Show current settings")
    print("/reset         Reset settings")
    print("/web on        Enable web intelligence")
    print("/web off       Disable web intelligence")
    print("/security      Show security status")
    print("/owner         Authenticate owner")
    print("/logout        Lock owner session")
    print("/time          Show current time")
    print("/clear         Clear terminal screen")
    print("/exit          Exit RUDRA")
    print()


# ============================================================
# STATUS
# ============================================================

def show_status(session, settings):
    print()
    print("=" * 60)
    print("                    RUDRA STATUS")
    print("=" * 60)
    print()
    print("System          : ONLINE")
    print(f"AI Model        : {MODEL_NAME}")
    print("Brain           : ACTIVE")
    print("Memory          : ACTIVE")
    print("Context         : ACTIVE")
    print(
        "Web Intelligence: "
        + ("ON" if settings.get("web_intelligence") else "OFF")
    )
    print(
        "Session         : "
        + ("ACTIVE" if session.active else "CLOSED")
    )
    print(f"Messages        : {session.message_count}")
    print(f"Session ID      : {session.session_id}")
    print()
    print("=" * 60)
    print()


# ============================================================
# SESSION
# ============================================================

def show_session(session):
    data = session.status()

    print()
    print("=" * 60)
    print("                   SESSION")
    print("=" * 60)
    print()
    print(f"Session ID : {data['session_id']}")
    print(f"Started    : {data['started_at']}")
    print(f"Messages   : {data['messages']}")
    print(f"Status     : {data['status']}")
    print()
    print("=" * 60)
    print()


# ============================================================
# MEMORY
# ============================================================

def show_memory(memory):
    profile = memory_profile(memory)
    facts = memory_facts(memory)

    print()
    print("=" * 60)
    print("                    RUDRA MEMORY")
    print("=" * 60)
    print()

    if profile:
        print("PROFILE")
        print("-" * 30)

        for key, value in profile.items():
            print(f"{key}: {value}")

        print()

    if facts:
        print("FACTS")
        print("-" * 30)

        for fact in facts[-20:]:
            print(f"- {fact}")

        print()

    if not profile and not facts:
        print("No saved memory yet.")
        print()

    print("=" * 60)
    print()


# ============================================================
# SETTINGS
# ============================================================

def show_settings(settings):
    print()
    print("=" * 60)
    print("                   SETTINGS")
    print("=" * 60)
    print()
    print(f"Personality      : {settings.get('personality')}")
    print(f"Response style   : {settings.get('response_style')}")
    print(
        "Web intelligence : "
        + ("ON" if settings.get("web_intelligence") else "OFF")
    )
    print()
    print("=" * 60)
    print()


# ============================================================
# COMMAND HANDLER
# ============================================================

def handle_command(command, memory, settings, session):
    cmd = command.strip().lower()

    # ---------------- HELP ----------------

    if cmd == "/help":
        show_help()
        return True, False

    # ---------------- STATUS ----------------

    if cmd == "/status":
        show_status(session, settings)
        return True, False

    # ---------------- SESSION ----------------

    if cmd == "/session":
        show_session(session)
        return True, False

    # ---------------- MEMORY ----------------

    if cmd == "/memory":
        show_memory(memory)
        return True, False

    # ---------------- CLEAR MEMORY ----------------

    if cmd in ("/clear memory", "/memory clear"):
        confirm = input(
            "This will delete saved memory. Type YES to confirm: "
        ).strip()

        if confirm.upper() == "YES":
            clear_memory(memory)
            save_memory(memory)
            print()
            print("[OK] RUDRA memory cleared.")
            print()
        else:
            print()
            print("Memory was not cleared.")
            print()

        return True, False

    # ---------------- SETTINGS ----------------

    if cmd == "/settings":
        show_settings(settings)
        return True, False

    # ---------------- RESET SETTINGS ----------------

    if cmd in ("/reset", "/reset settings"):
        new_settings = reset_settings()

        settings.clear()
        settings.update(new_settings)

        print()
        print("[OK] Settings reset to default.")
        print()

        return True, False

    # ---------------- WEB ----------------

    if cmd == "/web on":
        settings["web_intelligence"] = True
        save_settings(settings)

        print()
        print("[OK] Web intelligence enabled.")
        print()

        return True, False

    if cmd == "/web off":
        settings["web_intelligence"] = False
        save_settings(settings)

        print()
        print("[OK] Web intelligence disabled.")
        print()

        return True, False

    # ---------------- SECURITY ----------------

    if cmd == "/security":
        status = security_status()

        print()
        print("=" * 60)
        print("                  SECURITY STATUS")
        print("=" * 60)
        print()
        print(f"Owner          : {status['owner']}")
        print(
            "Authentication : "
            + ("ACTIVE" if status["authenticated"] else "LOCKED")
        )
        print(f"Status         : {status['status']}")
        print()
        print("=" * 60)
        print()

        return True, False

    # ---------------- OWNER ----------------

    if cmd == "/owner":
        verify_owner()
        return True, False

    # ---------------- LOGOUT ----------------

    if cmd == "/logout":
        logout_owner()
        return True, False

    # ---------------- TIME ----------------

    if cmd == "/time":
        now = datetime.now()

        print()
        print(
            "RUDRA TIME > "
            + now.strftime("%d %B %Y, %I:%M:%S %p")
        )
        print()

        return True, False

    # ---------------- CLEAR SCREEN ----------------

    if cmd == "/clear":
        os.system("cls")
        startup()
        return True, False

    # ---------------- EXIT ----------------

    if cmd in ("/exit", "/quit", "/bye"):
        return True, True

    # ---------------- UNKNOWN COMMAND ----------------

    if cmd.startswith("/"):
        print()
        print(
            "Unknown command. Type /help to see available commands."
        )
        print()

        return True, False

    return False, False


# ============================================================
# MAIN LOOP
# ============================================================

def main():
    memory = load_memory()
    settings = load_settings()
    session = RudraSession()

    startup()

    print("Type /help for commands.")
    print()

    try:
        while session.active:

            try:
                user_input = input("YOU > ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                print("RUDRA > Session closed.")
                break

            if not user_input:
                continue

            # Commands are handled BEFORE AI.
            handled, should_exit = handle_command(
                user_input,
                memory,
                settings,
                session
            )

            if handled:
                if should_exit:
                    break
                continue

            # Normal AI conversation
            session.register_message()

            print()
            print("RUDRA > ", end="", flush=True)

            start_time = time.time()

            answer = ask(
                user_input,
                memory=memory,
                settings=settings
            )

            elapsed = time.time() - start_time

            print(answer)

            # Save conversation
            try:
                remember_conversation(
                    memory,
                    user_input,
                    answer
                )
                save_memory(memory)
            except Exception as error:
                print()
                print(
                    f"[Memory warning] Could not save memory: {error}"
                )

            print()

    finally:
        session.close()

        try:
            save_memory(memory)
            save_settings(settings)
        except Exception:
            pass

        print()
        print("=" * 60)
        print("              RUDRA SESSION CLOSED")
        print("=" * 60)
        print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()