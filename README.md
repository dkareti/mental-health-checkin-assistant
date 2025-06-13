# mental-health-checkin-assistant

Note: If the assistant is to be deployed on heroku, use the `Procfile`
- this contains:
`web: python -m app.webhook`

This is the folder structure for this project:
    mental-health-checkin-assistant/
    │
    ├── app/
    │   ├── __init__.py
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
`pip install -r requirements.txt
python3 -m app.webhook