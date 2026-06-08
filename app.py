import os

from flask import (

    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request
)

from dotenv import load_dotenv

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

# =========================================================
# DATABASE
# =========================================================

from database.db import (

    init_db,
    create_user,
    get_user_by_username,
    verify_user_credentials
)

# =========================================================
# ROUTES
# =========================================================

from routes.chat_routes import (

    chat_bp
)

from routes.dashboard_routes import (

    dashboard_bp
)

# =========================================================
# FLASK APP
# =========================================================

app = Flask(

    __name__,

    template_folder="templates",

    static_folder="static"
)

# =========================================================
# SECRET KEY
# =========================================================

app.secret_key = os.getenv(

    "FLASK_SECRET_KEY",

    "fallback_secret"
)

# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(

    chat_bp
)

app.register_blueprint(

    dashboard_bp
)

# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_db()

print("✅ Database initialized")

# =========================================================
# HOME
# =========================================================

@app.route("/")

def home():

    if "username" in session:

        return redirect(

            url_for("chat_page")
        )

    return redirect(

        url_for("login")
    )

# =========================================================
# LOGIN PAGE
# =========================================================

@app.route(
    "/login",

    methods=["GET", "POST"]
)

def login():

    if "username" in session:

        return redirect(

            url_for("chat_page")
        )

    error = request.args.get(
        "message",
        ""
    )

    if request.method == "POST":

        username = (

            request.form.get(
                "username",
                ""
            )
            .strip()
        )

        password = (

            request.form.get(
                "password",
                ""
            )
        )

        if not username or not password:

            error = (
                "Username and password are required."
            )

        elif verify_user_credentials(
            username,
            password
        ):

            session["username"] = username

            session[
                "conversation_history"
            ] = []

            print(
                f"✅ User logged in: "
                f"{username}"
            )

            return redirect(

                url_for("chat_page")
            )

        else:

            error = (
                "Invalid username or password."
            )

    return render_template(

        "login.html",

        error=error
    )

# =========================================================
# SIGNUP PAGE

@app.route(
    "/signup",

    methods=["GET", "POST"]
)

def signup():

    if "username" in session:

        return redirect(

            url_for("chat_page")
        )

    error = ""

    if request.method == "POST":

        username = (

            request.form.get(
                "username",
                ""
            )
            .strip()
        )

        password = (

            request.form.get(
                "password",
                ""
            )
        )

        if not username or not password:

            error = (
                "Username and password are required."
            )

        elif get_user_by_username(
            username
        ):

            return redirect(

                url_for(
                    "login",
                    message=(
                        "Account already exists. "
                        "Please sign in."
                    )
                )
            )

        elif create_user(
            username,
            password
        ):

            session["username"] = username

            session[
                "conversation_history"
            ] = []

            print(
                f"✅ New user signed up: "
                f"{username}"
            )

            return redirect(

                url_for("chat_page")
            )

        else:

            error = (
                "Unable to create account. "
                "Please try again."
            )

    return render_template(

        "signup.html",

        error=error
    )

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")

def logout():

    username = session.get(
        "username"
    )

    session.clear()

    print(
        f"👋 User logged out: "
        f"{username}"
    )

    return redirect(

        url_for("login")
    )

# =========================================================
# CHAT PAGE
# =========================================================

@app.route("/chat")

def chat_page():

    username = session.get(
        "username"
    )

    if not username:

        return redirect(

            url_for("login")
        )

    return render_template(

        "index.html",

        username=username
    )

# =========================================================
# DASHBOARD PAGE
# =========================================================

@app.route("/dashboard")

def dashboard_page():

    username = session.get(
        "username"
    )

    if not username:

        return redirect(

            url_for("login")
        )

    return render_template(

        "dashboard.html",

        username=username
    )

# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")

def health():

    return {

        "status": "healthy",

        "app": "MindBridge",

        "version": "1.0.0"
    }

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("\\n🚀 Starting MindBridge Server...")

    print(
        "🌐 Running on: "
        "http://127.0.0.1:5000"
    )

    print(
        "=" * 48
    )

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000
    )