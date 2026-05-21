import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from transformers import pipeline
from dotenv import load_dotenv

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# =========================================================
# LOAD EMOTION MODEL
# =========================================================

emotion_classifier = None

try:

    emotion_classifier = pipeline(
        task="text-classification",

        model="j-hartmann/emotion-english-distilroberta-base",

        top_k=1,

        token=HF_TOKEN
    )

    print("✅ Emotion classifier loaded")

except Exception as e:

    print(f"❌ Emotion model load error: {e}")

# =========================================================
# EMOTION LABEL MAPPING
# =========================================================

EMOTION_MAPPING = {

    "joy": "joy",

    "sadness": "sadness",

    "anger": "anger",

    "fear": "fear",

    "surprise": "surprise",

    "disgust": "disgust",

    "neutral": "neutral"
}

# =========================================================
# DETECT EMOTION
# =========================================================

def detect_emotion(text):

    try:

        if not text.strip():

            return {
                "emotion": "neutral",
                "confidence": 0.5
            }

        if emotion_classifier is None:

            return {
                "emotion": "neutral",
                "confidence": 0.5
            }

        result = emotion_classifier(text)

        # =================================================
        # SAFETY CHECK
        # =================================================

        if not result:

            return {
                "emotion": "neutral",
                "confidence": 0.5
            }

        top_result = result[0][0]

        raw_emotion = (
            top_result["label"]
            .lower()
            .strip()
        )

        confidence = float(
            top_result["score"]
        )

        normalized_emotion = EMOTION_MAPPING.get(
            raw_emotion,
            "neutral"
        )

        print(
            f"🧠 Emotion Detected: {normalized_emotion} ({confidence:.2f})"
        )

        return {

            "emotion": normalized_emotion,

            "confidence": confidence
        }

    except Exception as e:

        print(f"❌ Emotion Detection Error: {e}")

        return {

            "emotion": "neutral",

            "confidence": 0.5
        }

# =========================================================
# GET EMOTION COLOR
# =========================================================

def get_emotion_color(emotion):

    colors = {

        "joy": "#10B981",

        "sadness": "#3B82F6",

        "anger": "#EF4444",

        "fear": "#8B5CF6",

        "surprise": "#F59E0B",

        "disgust": "#F97316",

        "neutral": "#9CA3AF"
    }

    return colors.get(
        emotion,
        "#9CA3AF"
    )

# =========================================================
# GET EMOTION EMOJI
# =========================================================

def get_emotion_emoji(emotion):

    emojis = {

        "joy": "😊",

        "sadness": "😢",

        "anger": "😠",

        "fear": "😨",

        "surprise": "😲",

        "disgust": "🤢",

        "neutral": "😐"
    }

    return emojis.get(
        emotion,
        "😐"
    )