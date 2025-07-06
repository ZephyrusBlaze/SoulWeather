import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from gemini_service import analyze_mood, generate_poetic_response
from models import db

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "soulweather-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///soulweather.db"
)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

with app.app_context():
    from models import MoodEntry, ChatMessage

    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mood_text = request.form.get("mood_text", "").strip()

        if not mood_text:
            flash("Please share your current emotional state.", "error")
            return render_template("index.html")

        try:
            weather_data = analyze_mood(mood_text)

            from models import MoodEntry
            import json

            mood_entry = MoodEntry(
                mood_text=mood_text,
                weather_condition=weather_data["weather_condition"],
                poetic_description=weather_data["poetic_description"],
                forecast=(
                    json.dumps(weather_data["forecast"])
                    if isinstance(weather_data["forecast"], dict)
                    else weather_data["forecast"]
                ),
                activity_suggestion=weather_data["activity_suggestion"],
                timestamp=datetime.utcnow(),
            )
            db.session.add(mood_entry)
            db.session.commit()

            return render_template(
                "index.html", weather_data=weather_data, mood_text=mood_text
            )

        except Exception as e:
            logging.error(f"Error analyzing mood: {str(e)}")
            flash(
                "Unable to process your emotions right now. Please try again later.",
                "error",
            )
            return render_template("index.html")

    return render_template("index.html")


@app.route("/journal")
def journal():
    try:
        from models import MoodEntry

        mood_entries = MoodEntry.query.order_by(MoodEntry.timestamp.desc()).all()

        import json

        for entry in mood_entries:
            try:
                if isinstance(entry.forecast, str):
                    entry.forecast = json.loads(entry.forecast)
            except (json.JSONDecodeError, TypeError):
                pass

        chart_data = []
        for entry in reversed(mood_entries[-30:]):
            chart_data.append(
                {
                    "date": entry.timestamp.strftime("%Y-%m-%d"),
                    "mood_length": len(entry.mood_text),
                    "description_length": len(entry.poetic_description),
                }
            )

        return render_template(
            "journal.html", mood_entries=mood_entries, chart_data=chart_data
        )
    except Exception as e:
        logging.error(f"Error loading journal: {str(e)}")
        flash("Unable to load your journal right now.", "error")
        return render_template("journal.html", mood_entries=[], chart_data=[])


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if not user_message:
            flash("Please enter a message.", "error")
            return redirect(url_for("chat"))
        try:
            ai_response = generate_poetic_response(user_message)

            from models import ChatMessage

            user_chat = ChatMessage(
                message=user_message, is_user=True, timestamp=datetime.utcnow()
            )
            ai_chat = ChatMessage(
                message=ai_response, is_user=False, timestamp=datetime.utcnow()
            )

            db.session.add(user_chat)
            db.session.add(ai_chat)
            db.session.commit()
        except Exception as e:
            logging.error(f"Error generating chat response: {str(e)}")
            flash("The poetic spirit is temporarily quiet. Please try again.", "error")
    try:
        from models import ChatMessage

        chat_messages = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
        return render_template("chat.html", chat_messages=chat_messages)
    except Exception as e:
        logging.error(f"Error loading chat history: {str(e)}")
        return render_template("chat.html", chat_messages=[])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
