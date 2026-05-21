# =========================================================
# CRISIS KEYWORDS
# =========================================================

CRISIS_KEYWORDS = [

    "suicide",

    "kill myself",

    "want to die",

    "end my life",

    "self harm",

    "hurt myself",

    "cut myself",

    "end it all",

    "can't go on",

    "no reason to live",

    "i want to disappear",

    "life is pointless",

    "i hate myself",

    "i give up",

    "i am hopeless"
]

# =========================================================
# CRISIS RESPONSE
# =========================================================

CRISIS_RESPONSE = """
I'm really concerned about what you're sharing right now.

You do not have to go through this alone.

Please consider reaching out to someone you trust or contacting a professional support service immediately.

📞 iCall India: 9152987821
📞 Vandrevala Foundation: 1860-2662-345

If you are in immediate danger, please contact local emergency services or a nearby trusted person.

You matter, and support is available.
"""

# =========================================================
# CLEAN TEXT
# =========================================================

def normalize_text(text):

    return (
        text
        .lower()
        .strip()
    )

# =========================================================
# DETECT CRISIS
# =========================================================

def detect_crisis(message):

    try:

        cleaned_message = normalize_text(message)

        for keyword in CRISIS_KEYWORDS:

            if keyword in cleaned_message:

                print(
                    f"🚨 Crisis keyword detected: {keyword}"
                )

                return True

        return False

    except Exception as e:

        print(f"❌ Crisis Detection Error: {e}")

        return False

# =========================================================
# GET CRISIS RESPONSE
# =========================================================

def get_crisis_response():

    return CRISIS_RESPONSE.strip()

# =========================================================
# GET SAFETY LEVEL
# =========================================================

def get_safety_level(message):

    message = normalize_text(message)

    high_risk_words = [

        "suicide",

        "kill myself",

        "end my life",

        "want to die"
    ]

    medium_risk_words = [

        "hopeless",

        "self harm",

        "hurt myself",

        "can't go on"
    ]

    # =====================================================
    # HIGH RISK
    # =====================================================

    for word in high_risk_words:

        if word in message:

            return "high"

    # =====================================================
    # MEDIUM RISK
    # =====================================================

    for word in medium_risk_words:

        if word in message:

            return "medium"

    # =====================================================
    # LOW RISK
    # =====================================================

    return "low"

# =========================================================
# SAFETY PAYLOAD
# =========================================================

def get_crisis_payload(message):

    return {

        "is_crisis": detect_crisis(message),

        "safety_level": get_safety_level(message),

        "response": get_crisis_response()
    }