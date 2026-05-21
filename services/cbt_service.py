# =========================================================
# CBT STRATEGIES DATABASE
# =========================================================

CBT_STRATEGIES = {

    "sadness": {

        "title": "Gentle Reflection",

        "tip": (
            "Try writing down three small things "
            "you are grateful for today."
        ),

        "exercise": (
            "Take 5 slow breaths and reflect on "
            "one thing that brought you comfort recently."
        )
    },

    "fear": {

        "title": "Breathing Reset",

        "tip": (
            "Try the 4-7-8 breathing technique "
            "to calm your nervous system."
        ),

        "exercise": (
            "Inhale for 4 seconds, "
            "hold for 7 seconds, "
            "exhale for 8 seconds."
        )
    },

    "anger": {

        "title": "Grounding Exercise",

        "tip": (
            "Reconnect with your surroundings "
            "using the 5-4-3-2-1 method."
        ),

        "exercise": (
            "Identify:\n"
            "5 things you can see\n"
            "4 things you can touch\n"
            "3 things you can hear\n"
            "2 things you can smell\n"
            "1 thing you can taste"
        )
    },

    "fearful": {

        "title": "Safety Awareness",

        "tip": (
            "Focus on what is within your control "
            "right now."
        ),

        "exercise": (
            "Write down:\n"
            "- what you can control\n"
            "- what you cannot control"
        )
    },

    "disgust": {

        "title": "Mental Reset",

        "tip": (
            "A short walk or change of environment "
            "can help reset overwhelming emotions."
        ),

        "exercise": (
            "Step away from screens for 5 minutes "
            "and focus on your breathing."
        )
    },

    "surprise": {

        "title": "Emotional Processing",

        "tip": (
            "Unexpected situations can feel intense. "
            "Give yourself time to process."
        ),

        "exercise": (
            "Journal briefly about what surprised you "
            "and how it made you feel."
        )
    },

    "joy": {

        "title": "Positive Reinforcement",

        "tip": (
            "Celebrate and acknowledge "
            "positive emotional moments."
        ),

        "exercise": (
            "Share something positive with someone "
            "you trust."
        )
    },

    "neutral": {

        "title": "Mindfulness Check-In",

        "tip": (
            "Pause for a moment and check in "
            "with your thoughts and body."
        ),

        "exercise": (
            "Take 3 deep breaths and observe "
            "how you feel right now."
        )
    }
}

# =========================================================
# GET CBT SUPPORT
# =========================================================

def get_cbt_support(emotion):

    emotion = (
        emotion
        .lower()
        .strip()
    )

    return CBT_STRATEGIES.get(

        emotion,

        CBT_STRATEGIES["neutral"]
    )

# =========================================================
# GET QUICK TIP
# =========================================================

def get_quick_tip(emotion):

    support = get_cbt_support(emotion)

    return support["tip"]

# =========================================================
# GET EXERCISE
# =========================================================

def get_exercise(emotion):

    support = get_cbt_support(emotion)

    return support["exercise"]

# =========================================================
# GET FULL SUPPORT PACKAGE
# =========================================================

def get_support_package(emotion):

    support = get_cbt_support(emotion)

    return {

        "emotion": emotion,

        "title": support["title"],

        "tip": support["tip"],

        "exercise": support["exercise"]
    }