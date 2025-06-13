from flask import Flask, request, jsonify
import os
from app.sentiment import analyze_sentiment
from app.db import init_db, log_mood, get_weekly_summary

app = Flask(__name__)
init_db()

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    user_input = req.get("queryResult", {}).get("queryText", "")

    if intent == "DailyMoodCheckIn":
        sentiment, score = analyze_sentiment(user_input)
        log_mood(user_input, sentiment, score)

        if sentiment == "positive":
            response_text = "I'm glad to hear you're feeling good today! 😊"
        elif sentiment == "negative":
            response_text = "I'm sorry to hear that. Want to talk more about it or try a breathing exercise?"
        else:
            response_text = "Thanks for checking in. I hope the rest of your day goes well."

        return jsonify({"fulfillmentText": response_text})

    elif intent == "WeeklySummary":
        summary = get_weekly_summary()
        return jsonify({"fulfillmentText": summary})

    return jsonify({"fulfillmentText": "I'm here whenever you're ready to check in."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=port)