from flask import (

    Blueprint,
    jsonify,
    session
)

# =========================================================
# DATABASE
# =========================================================

from database.db import (

    get_dashboard_data,
    get_emotion_stats
)

# =========================================================
# BLUEPRINT
# =========================================================

dashboard_bp = Blueprint(

    "dashboard",

    __name__
)

# =========================================================
# DASHBOARD ANALYTICS
# =========================================================

@dashboard_bp.route(
    "/api/dashboard",
    methods=["GET"]
)

def dashboard_analytics():

    try:

        # =================================================
        # AUTH CHECK
        # =================================================

        username = session.get(
            "username"
        )

        if not username:

            return jsonify({

                "success": False,

                "error": "Unauthorized"
            }), 401

        print(
            f"📊 Loading dashboard for "
            f"{username}"
        )

        # =================================================
        # FETCH DATA
        # =================================================

        dashboard_data = (
            get_dashboard_data(
                username=username
            )
        )

        emotion_stats = (
            get_emotion_stats(
                username=username
            )
        )

        # =================================================
        # TOTAL MESSAGES
        # =================================================

        total_messages = len(
            dashboard_data
        )

        # =================================================
        # AVG CONFIDENCE
        # =================================================

        if total_messages > 0:

            avg_confidence = (

                sum(
                    item["confidence"]
                    for item in dashboard_data
                )

                / total_messages
            )

        else:

            avg_confidence = 0

        # =================================================
        # DOMINANT EMOTION
        # =================================================

        dominant_emotion = "neutral"

        if emotion_stats:

            dominant_emotion = max(

                emotion_stats,

                key=emotion_stats.get
            )

        # =================================================
        # EMOTIONAL DIVERSITY
        # =================================================

        emotional_diversity = len(
            emotion_stats
        )

        # =================================================
        # RECENT ACTIVITY
        # =================================================

        recent_activity = (
            dashboard_data[-5:]
        )

        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "analytics": {

                "total_messages":
                total_messages,

                "avg_confidence":
                round(avg_confidence, 2),

                "dominant_emotion":
                dominant_emotion,

                "emotional_diversity":
                emotional_diversity,

                "emotion_distribution":
                emotion_stats,

                "recent_activity":
                recent_activity,

                "timeline":
                dashboard_data
            }
        })

    except Exception as e:

        print(
            f"❌ Dashboard API Error: {e}"
        )

        return jsonify({

            "success": False,

            "error": (
                "Failed to load analytics."
            )
        }), 500

# =========================================================
# QUICK STATS
# =========================================================

@dashboard_bp.route(
    "/api/stats",
    methods=["GET"]
)

def quick_stats():

    try:

        username = session.get(
            "username"
        )

        if not username:

            return jsonify({

                "success": False,

                "error": "Unauthorized"
            }), 401

        emotion_stats = (
            get_emotion_stats(
                username
            )
        )

        total_entries = sum(
            emotion_stats.values()
        )

        return jsonify({

            "success": True,

            "stats": {

                "total_entries":
                total_entries,

                "emotion_stats":
                emotion_stats
            }
        })

    except Exception as e:

        print(
            f"❌ Quick Stats Error: {e}"
        )

        return jsonify({

            "success": False,

            "error": (
                "Failed to fetch stats."
            )
        }), 500