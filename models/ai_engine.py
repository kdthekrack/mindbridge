import os
import sys
from typing import Any

from dotenv import load_dotenv
import google.generativeai as genai
import google.generativeai.client as genai_client
from transformers import pipeline

# =====================================================
# ENSURE UTF-8 OUTPUT
# =====================================================

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-flash-latest").strip()

if not GEMINI_API_KEY:
    raise RuntimeError(
        "Missing GEMINI_API_KEY in .env. Add GEMINI_API_KEY=your_key and restart."
    )

# =====================================================
# GEMINI CLIENT
# =====================================================

try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_client = genai_client.get_default_generative_client()
    print("✅ Gemini client initialized")
    print(f"ℹ️ Gemini model configured: {GEMINI_MODEL}")
except Exception as e:
    print(f"❌ Gemini initialization error: {e}")
    gemini_client = None

# =====================================================
# EMOTION MODEL
# =====================================================

try:
    emotion_model = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=1,
        token=HF_TOKEN or None,
    )
    print("✅ Emotion model loaded")
except Exception as e:
    print(f"❌ Emotion model initialization error: {e}")
    emotion_model = None

# =====================================================
# SYSTEM PROMPT
# =====================================================

SYSTEM_PROMPT = """
You are MindBridge,
an emotionally supportive AI companion.

Your tone is:
- warm
- calm
- human
- emotionally intelligent

Rules:
- Never sound robotic
- Keep responses concise
- Be emotionally validating
- Encourage reflection
- Avoid generic repetition
- Respond naturally
"""

# =====================================================
# GEMINI CHAT
# =====================================================

def get_chat_reply(prompt: str) -> str:
    if gemini_client is None:
        print("⚠️ Gemini client unavailable, falling back to safe reply")
        return fallback_reply()

    try:
        response = gemini_client.generate_content(
            model=GEMINI_MODEL,
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
        )

        print("✅ Gemini generation successful")

        candidates = getattr(response, "candidates", None)
        if candidates:
            candidate = candidates[0]
            content = getattr(candidate, "content", None)
            if content and getattr(content, "parts", None):
                text = "".join(
                    getattr(part, "text", "")
                    for part in content.parts
                    if getattr(part, "text", None)
                ).strip()
                if text:
                    return text

        print("⚠️ Gemini response missing generated text, using fallback reply")
        return fallback_reply()

    except Exception as e:
        print(f"❌ Gemini generation error: {e}")
        return fallback_reply()

# =====================================================
# AI REPLY
# =====================================================


def generate_reply(
    message: str,
    emotion: str,
    conversation_history: list[dict[str, str]],
) -> str:
    try:
        prompt = build_gemini_prompt(
            message=message,
            emotion=emotion,
            conversation_history=conversation_history,
        )

        print("🧠 Generating Gemini reply")
        print(f"🧠 Emotion context: {emotion}")
        print(f"🧠 Prompt preview: {prompt[:1000]}")

        reply = get_chat_reply(prompt)
        print(f"🤖 AI reply length: {len(reply)}")

        return reply
    except Exception as e:
        print(f"❌ Generate reply error: {e}")
        return fallback_reply()

# =====================================================
# FALLBACK
# =====================================================

def fallback_reply() -> str:
    return (
        "I’m here with you. "
        "Tell me a little more "
        "about what’s on your mind."
    )

# =====================================================
# PROMPT BUILDING
# =====================================================

def build_gemini_prompt(
    message: str,
    emotion: str,
    conversation_history: list[dict[str, str]],
) -> str:
    history_lines = []
    for entry in conversation_history[-10:]:
        role = entry.get("role", "user").capitalize()
        text = entry.get("text", "").strip()
        if text:
            history_lines.append(f"{role}: {text}")

    history_block = "\n".join(history_lines) or "No prior conversation history."

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"CONTEXT:\n"
        f"- Detected emotion: {emotion}\n"
        f"- Recent conversation:\n{history_block}\n\n"
        f"USER:\n{message}\n\n"
        "Please reply with empathy, avoid repetition, validate feelings, "
        "and gently encourage reflection while keeping the reply natural and concise."
    )

# =====================================================
# EMOTION DETECTION
# =====================================================

def get_emotion(message):

    try:

        result = emotion_model(message)

        top = result[0][0]

        return {

            "emotion":
                top["label"].lower(),

            "confidence":
                float(top["score"])
        }

    except Exception as e:

        print(
            f"Emotion Error: {e}"
        )

        return {

            "emotion": "neutral",

            "confidence": 0.5
        }