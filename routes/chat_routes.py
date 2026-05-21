from flask import (

    Blueprint,
    request,
    jsonify,
    session
)

# =========================================================
# DATABASE
# =========================================================

from database.db import (

    save_conversation,
    get_user_history
)

# =========================================================
# SERVICES
# =========================================================

from services.emotion_service import (

    detect_emotion
)

from services.cbt_service import (

    get_support_package
)

from services.crisis_service import (

    get_crisis_payload
)

# =========================================================
# AI ENGINE
# =========================================================

from models.ai_engine import (

    generate_reply
)

# =========================================================
# BLUEPRINT
# =========================================================

chat_bp = Blueprint(

    "chat",

    __name__
)

# =========================================================
# CHAT API
# =========================================================

@chat_bp.route(
    "/chat",
    methods=["POST"]
)

def chat():

    try:

        data = request.get_json()

        # =================================================
        # VALIDATION
        # =================================================

        if not data:

            return jsonify({

                "success": False,

                "error": "No request data"
            }), 400

        message = (
            data.get("message", "")
            .strip()
        )

        username = (
            data.get("username", "")
            .strip()
        )

        if not message:

            return jsonify({

                "success": False,

                "error": "Message is required"
            }), 400

        if not username:

            return jsonify({

                "success": False,

                "error": "Username missing"
            }), 400

        print("\\n================================================")
        print(f"👤 USER: {username}")
        print(f"💬 MESSAGE: {message}")
        print("================================================")

        # =================================================
        # CRISIS DETECTION
        # =================================================

        crisis_payload = get_crisis_payload(
            message
        )

        if crisis_payload["is_crisis"]:

            print(
                "🚨 Crisis detected"
            )

            return jsonify({

                "success": True,

                "crisis": True,

                "reply": crisis_payload[
                    "response"
                ],

                "safety_level": crisis_payload[
                    "safety_level"
                ]
            })

        # =================================================
        # EMOTION DETECTION
        # =================================================

        emotion_data = detect_emotion(
            message
        )

        emotion = emotion_data[
            "emotion"
        ]

        confidence = emotion_data[
            "confidence"
        ]

        print(
            f"🧠 Emotion: {emotion}"
        )

        print(
            f"📊 Confidence: "
            f"{confidence:.2f}"
        )

        # =================================================
        # CBT SUPPORT
        # =================================================

        support_package = (
            get_support_package(
                emotion
            )
        )

        # =================================================
        # CONVERSATION MEMORY
        # =================================================

        conversation_history = session.get(
            "conversation_history",
            []
        )

        # =================================================
        # AI REPLY
        # =================================================

        ai_reply = generate_reply(

            message=message,

            emotion=emotion,

            conversation_history=
            conversation_history
        )

        print(
            f"🤖 AI Reply: {ai_reply}"
        )

        # =================================================
        # SAVE MEMORY
        # =================================================

        conversation_history.append({

            "role": "user",

            "text": message
        })

        conversation_history.append({

            "role": "model",

            "text": ai_reply
        })

        # =================================================
        # LIMIT MEMORY
        # =================================================

        if len(conversation_history) > 20:

            conversation_history = (
                conversation_history[-20:]
            )

        session[
            "conversation_history"
        ] = conversation_history

        # =================================================
        # DATABASE STORAGE
        # =================================================

        save_conversation(

            username=username,

            message=message,

            ai_reply=ai_reply,

            emotion=emotion,

            confidence=confidence
        )

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "crisis": False,

            "reply": ai_reply,

            "emotion": emotion,

            "confidence": round(
                confidence,
                2
            ),

            "support": support_package
        })

    except Exception as e:

        print(
            f"❌ Chat Route Error: {e}"
        )

        return jsonify({

            "success": False,

            "error": (
                "Something went wrong."
            )
        }), 500

# =========================================================
# GET HISTORY
# =========================================================

@chat_bp.route(
    "/history/<username>",
    methods=["GET"]
)

def history(username):

    try:

        history_data = get_user_history(
            username=username
        )

        return jsonify({

            "success": True,

            "history": history_data
        })

    except Exception as e:

        print(
            f"❌ History Route Error: {e}"
        )

        return jsonify({

            "success": False,

            "error": (
                "Failed to fetch history."
            )
        }), 500