import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Define some emotional thresholds
def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    compound = scores["compound"]

    # New: detect tone using individual scores
    neg = scores['neg']
    neu = scores['neu']
    pos = scores['pos']

    # Emotion tagging logic
    if compound >= 0.5:
        emotion = "positive"
        tag = "grateful" if pos > 0.7 else "calm"
    elif compound <= -0.5:
        if neg > 0.6:
            tag = "angry"
        elif "tired" in text or "exhausted" in text:
            tag = "burned out"
        elif "anxious" in text or "worried" in text:
            tag = "anxious"
        else:
            tag = "sad"
        emotion = "negative"
    else:
        emotion = "neutral"
        tag = "uncertain" if neu > 0.8 else "mixed"

    return {
        "emotion": emotion,
        "tag": tag,
        "compound": compound,
        "raw_scores": scores  # optional: remove if not needed
    }