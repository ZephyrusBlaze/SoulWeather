from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class MoodEntry(db.Model):
    """Model for storing mood entries and their weather metaphors"""

    id = db.Column(db.Integer, primary_key=True)
    mood_text = db.Column(db.Text, nullable=False)
    weather_condition = db.Column(db.String(200), nullable=False)
    poetic_description = db.Column(db.Text, nullable=False)
    forecast = db.Column(db.Text, nullable=False)
    activity_suggestion = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<MoodEntry {self.id}: {self.weather_condition}>"


class ChatMessage(db.Model):
    """Model for storing chat messages with the poetic AI"""

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        sender = "User" if self.is_user else "AI"
        return f"<ChatMessage {self.id}: {sender}>"
