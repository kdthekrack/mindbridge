import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

# =========================================================
# DATABASE LOCATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_DIR = BASE_DIR / "instance"

DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "mindbridge.db"

# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn

# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            # =================================================
            # MOODS TABLE
            # =================================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS moods (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    username TEXT NOT NULL,

                    message TEXT NOT NULL,

                    ai_reply TEXT,

                    emotion TEXT,

                    confidence REAL,

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # =================================================
            # USERS TABLE
            # =================================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    username TEXT NOT NULL UNIQUE,

                    password_hash TEXT NOT NULL,

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # =================================================
            # INDEXES
            # =================================================

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_username
                ON moods(username)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_emotion
                ON moods(emotion)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at
                ON moods(created_at)
            """)

            conn.commit()

            print("✅ Database initialized successfully")

    except Exception as e:

        print(f"❌ Database Initialization Error: {e}")

# =========================================================
# USER MANAGEMENT


def create_user(
    username,
    password
):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            password_hash = (
                generate_password_hash(
                    password
                )
            )

            cursor.execute("""
                INSERT INTO users (
                    username,
                    password_hash
                )
                VALUES (?, ?)
            """, (

                username,
                password_hash
            ))

            conn.commit()

            return True

    except sqlite3.IntegrityError:

        return False

    except Exception as e:

        print(f"❌ Create User Error: {e}")

        return False


def get_user_by_username(
    username
):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id,
                       username,
                       password_hash,
                       created_at
                FROM users
                WHERE username = ?
            """, (username,))

            row = cursor.fetchone()

            if not row:

                return None

            return {
                "id": row["id"],
                "username": row["username"],
                "password_hash": row["password_hash"],
                "created_at": row["created_at"]
            }

    except Exception as e:

        print(f"❌ Get User Error: {e}")

        return None


def verify_user_credentials(
    username,
    password
):

    user = get_user_by_username(
        username
    )

    if not user:

        return False

    return check_password_hash(
        user["password_hash"],
        password
    )

# =========================================================
# SAVE CONVERSATION
# =========================================================

def save_conversation(
    username,
    message,
    ai_reply,
    emotion,
    confidence
):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO moods (

                    username,
                    message,
                    ai_reply,
                    emotion,
                    confidence

                )
                VALUES (?, ?, ?, ?, ?)
            """, (

                username,
                message,
                ai_reply,
                emotion,
                confidence
            ))

            conn.commit()

            print("✅ Conversation stored")

            return True

    except Exception as e:

        print(f"❌ Save Conversation Error: {e}")

        return False

# =========================================================
# GET USER HISTORY
# =========================================================

def get_user_history(
    username,
    limit=20
):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    message,
                    ai_reply,
                    emotion,
                    confidence,
                    created_at

                FROM moods

                WHERE username = ?

                ORDER BY created_at DESC

                LIMIT ?
            """, (

                username,
                limit
            ))

            rows = cursor.fetchall()

            history = []

            for row in rows:

                history.append({

                    "message": row["message"],

                    "ai_reply": row["ai_reply"],

                    "emotion": row["emotion"],

                    "confidence": row["confidence"],

                    "created_at": row["created_at"]
                })

            return history

    except Exception as e:

        print(f"❌ History Fetch Error: {e}")

        return []

# =========================================================
# GET DASHBOARD DATA
# =========================================================

def get_dashboard_data(
    username,
    days=30
):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            start_date = (
                datetime.now() - timedelta(days=days)
            )

            cursor.execute("""
                SELECT
                    emotion,
                    confidence,
                    created_at

                FROM moods

                WHERE username = ?
                AND created_at >= ?

                ORDER BY created_at ASC
            """, (

                username,
                start_date.isoformat()
            ))

            rows = cursor.fetchall()

            result = []

            for row in rows:

                result.append({

                    "emotion": row["emotion"],

                    "confidence": row["confidence"],

                    "created_at": row["created_at"]
                })

            return result

    except Exception as e:

        print(f"❌ Dashboard Fetch Error: {e}")

        return []

# =========================================================
# GET EMOTION STATS
# =========================================================

def get_emotion_stats(username):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    emotion,
                    COUNT(*) as total

                FROM moods

                WHERE username = ?

                GROUP BY emotion
            """, (username,))

            rows = cursor.fetchall()

            stats = {}

            for row in rows:

                stats[row["emotion"]] = row["total"]

            return stats

    except Exception as e:

        print(f"❌ Emotion Stats Error: {e}")

        return {}

# =========================================================
# DELETE USER DATA
# =========================================================

def clear_user_history(username):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM moods
                WHERE username = ?
            """, (username,))

            conn.commit()

            print("✅ User history cleared")

            return True

    except Exception as e:

        print(f"❌ Clear History Error: {e}")

        return False