import os
import logging
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "your-gemini-api-key"))


def analyze_mood(mood_text: str) -> dict:
    """
    Analyze user mood and generate weather metaphor with forecast and activity
    """
    prompt = f"""Convert the following emotion journal into a realistic weather report format:

1. A metaphorical weather condition (one line, like "Partly Cloudy with Emotional Patches")

2. A poetic Markdown description (3–5 lines max)

3. A 3-day emotional weather forecast with realistic weather details including:
   - Temperature (in both °F and °C that reflects the emotional intensity)
   - Humidity percentage (representing emotional depth)
   - Weather emoji/icon
   - Brief emotional weather description

4. A healthy, mood-aligned activity recommendation

Please format your response as JSON with these exact keys:
- "weather_condition": string
- "poetic_description": string (use Markdown formatting)
- "forecast": object with "day1", "day2", "day3" each containing:
  - "day": string (like "Today", "Tomorrow", "Day 3")
  - "emoji": string (weather emoji like ☀️, ⛅, 🌧️, ⛈️, 🌤️, 🌫️, ❄️)
  - "temp_f": number (temperature in Fahrenheit, 32-100 range)
  - "temp_c": number (temperature in Celsius, 0-38 range)
  - "humidity": number (percentage 20-90)
  - "condition": string (brief emotional weather condition)
- "activity_suggestion": string

Make the temperatures and humidity reflect the emotional state - warmer for positive emotions, cooler for sadness, high humidity for overwhelming feelings, etc.

Input: "{mood_text}"
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )

        if response.text:
            data = json.loads(response.text)
            return {
                "weather_condition": data.get(
                    "weather_condition", "Partly cloudy with emotional patches"
                ),
                "poetic_description": data.get(
                    "poetic_description",
                    "*Clouds gather softly in the heart,*\n*Whispers of change dance on the wind.*",
                ),
                "forecast": data.get(
                    "forecast",
                    {
                        "day1": {
                            "day": "Today",
                            "emoji": "⛅",
                            "temp_f": 72,
                            "temp_c": 22,
                            "humidity": 65,
                            "condition": "Gentle clearing expected",
                        },
                        "day2": {
                            "day": "Tomorrow",
                            "emoji": "☀️",
                            "temp_f": 78,
                            "temp_c": 26,
                            "humidity": 45,
                            "condition": "Warm emotional sunshine",
                        },
                        "day3": {
                            "day": "Day 3",
                            "emoji": "🌤️",
                            "temp_f": 75,
                            "temp_c": 24,
                            "humidity": 55,
                            "condition": "Peaceful evening clearing",
                        },
                    },
                ),
                "activity_suggestion": data.get(
                    "activity_suggestion", "Take a mindful walk in nature"
                ),
            }
        else:
            raise ValueError("Empty response from Gemini")

    except Exception as e:
        logging.error(f"Error in mood analysis: {str(e)}")

        return {
            "weather_condition": "Misty with occasional emotional clearing",
            "poetic_description": "*The soul carries gentle storms today,*\n*Between the raindrops, hope glimmers softly,*\n*Tomorrow's sky holds promises untold.*",
            "forecast": {
                "day1": {
                    "day": "Today",
                    "emoji": "🌫️",
                    "temp_f": 68,
                    "temp_c": 20,
                    "humidity": 75,
                    "condition": "Emotional mist gradually lifting",
                },
                "day2": {
                    "day": "Tomorrow",
                    "emoji": "🌤️",
                    "temp_f": 74,
                    "temp_c": 23,
                    "humidity": 60,
                    "condition": "Brighter moments emerge",
                },
                "day3": {
                    "day": "Day 3",
                    "emoji": "☀️",
                    "temp_f": 80,
                    "temp_c": 27,
                    "humidity": 40,
                    "condition": "Inner sunshine breaking through",
                },
            },
            "activity_suggestion": "Practice gentle breathing exercises or write in a journal",
        }


def generate_poetic_response(user_message: str) -> str:
    """
    Generate a poetic response to user message in Markdown format
    """
    prompt = f"""You are a poetic and emotionally intelligent AI companion. Reply to this message in beautiful, poetic Markdown format. Use metaphors, gentle imagery, and emotional wisdom. Keep your response warm, supportive, and artistically formatted with Markdown.

User message: "{user_message}"
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
        )

        if response.text:
            return response.text
        else:
            raise ValueError("Empty response from Gemini")

    except Exception as e:
        logging.error(f"Error in poetic response generation: {str(e)}")

        return """*In this moment of connection,*  
*I hear the whispers of your heart,*  
*Though words may sometimes fail me,*  
*Know that you are never alone.*  

**The universe listens,**  
**And so do I.**"""
