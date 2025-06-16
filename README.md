# mental-health-checkin-assistant

Note: If the assistant is to be deployed on heroku, use the `Procfile`
- this contains:
`web: python -m app.webhook`

This is the folder structure for this project:
    mental-health-checkin-assistant/
    │
    ├── app/
    │   ├── __init__.py             # blank file to generate the python environment
    │   ├── webhook.py              # Flask app (webhook logic)
    │   ├── sentiment.py            # Sentiment analysis utilities (VADER setup, analysis)
    │   └── db.py                   # SQLite logging and summary functions
    │
    ├── data/
    │   └── mood_logs.db            # (Optional) Pre-filled example DB (if not .gitignored)
    │
    ├── requirements.txt            # Python dependencies
    ├── runtime.txt                 # Optional (e.g., python-3.10 for Heroku)
    ├── Procfile                    # For deployment (e.g., on Heroku)
    ├── README.md                   # Project overview and usage instructions
    └── .gitignore                  # Ignore DB files, virtual env, etc.

To run locally
`pip install -r requirements.txt`
`python3 -m app.webhook`

and run (IN ANOTHER TERMINAL)`ngrok http PORT_NUMBER`

Test the functionality of the mental-health AI assistant by typing in the Dialogflow Simulator (located in the right hand side of the dialogflow console)
You can type:
Today is a good day. I feel encouraged!

I feel stressed.

I am pretty downhearted.

*Note that every time the interface runs, you have to re-copy the fullfillment url in dialog flow