from flask import Flask, request, jsonify, render_template
import os
from app.sentiment import analyze_sentiment
from app.db import init_db, log_mood, get_weekly_summary
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from pathlib import Path

#### ++++++++++++++++++++++++++++++++++++++
#### Start the Flask App and initialize the database
#### --------------------------------------
app = Flask(__name__)
init_db()

#### ++++++++++++
####  Define path to outer .env file
####
#### Find the .env file in the parent directory
#### Then the environment is loaded
####
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

#### ++++++++++++++++++++++++++++++++++++++++++++++++
#### Get DIALOGFLOW auth details
key_path = os.getenv("DIALOGFLOW_KEY_PATH")
project_id = os.getenv("PROJECT_MHA_ID")

if not key_path or not project_id:
    raise RuntimeError("Missing environment variables: check DIALOGFLOW_KEY_PATH and PROJECT_MHA_ID in your .env file")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
PROJECT_ID = project_id
#### ---------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    user_input = req.get("queryResult", {}).get("queryText", "")

    if intent == "DailyMoodCheckIn":
        result = analyze_sentiment(user_input)
        emotion = result["emotion"]
        tag = result["tag"]

        #log the data into the database
        log_mood(user_input, emotion, result["compound"])

        if emotion == "positive":
            response_text = f"I'm really glad to hear you're feeling {tag} today."
        elif emotion == "negative":
            if tag == "anxious":
                response_text = "It sounds like you're feeling anxious. Would a calming exercise help?"
            elif tag == "burned out":
                response_text = "Feeling burned out is tough. Want to talk about what's draining you?"
            else:
                response_text = "I'm here for you. Would it help to talk more or try a reflection activity?"
        else:
            response_text = "Thanks for sharing that. Sometimes it\’s hard to describe how we feel, and that\’s okay."

        return jsonify({"fulfillmentText": response_text})

    elif intent == "WeeklySummary":
        summary = get_weekly_summary()
        return jsonify({"fulfillmentText": summary})

    return jsonify({"fulfillmentText": "I'm here whenever you're ready to check in."})



@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(PROJECT_ID, "user-session-id")

        text_input = dialogflow.TextInput(text=user_message, language_code="en-US")
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        bot_reply = response.query_result.fulfillment_text

        return jsonify({"reply": bot_reply})
    except Exception as error_msg:
        return jsonify({"error": str(error_msg)}), 500




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=port)