from flask import Flask, request, jsonify

from brain import ask
from memory import load as load_memory, save as save_memory
from settings_manager import load_settings

app = Flask(__name__)

memory = load_memory()
settings = load_settings()


@app.get("/")
def home():
    return jsonify({
        "name": "RUDRA AI",
        "status": "ONLINE",
        "model": "phi4-mini"
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "RUDRA AI"
    })


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    if not isinstance(message, str):
        return jsonify({
            "error": "message must be text"
        }), 400

    message = message.strip()

    if not message:
        return jsonify({
            "error": "message is required"
        }), 400

    answer = ask(
        message,
        memory=memory,
        settings=settings
    )

    try:
        from memory import remember_conversation

        remember_conversation(
            memory,
            message,
            answer
        )

        save_memory(memory)

    except Exception:
        pass

    return jsonify({
        "reply": answer
    })


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("                 RUDRA API SERVER")
    print("=" * 60)
    print()
    print("Status : ONLINE")
    print("Model  : phi4-mini")
    print("URL    : http://127.0.0.1:5000")
    print()
    print("=" * 60)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )