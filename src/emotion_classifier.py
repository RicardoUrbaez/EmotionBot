from transformers import pipeline

# ✅ Load 27-emotion GoEmotions model
emotion_pipeline = pipeline(
    "text-classification",
    model="monologg/bert-base-cased-goemotions-original",
    return_all_scores=True,
    top_k=None  # important: return ALL emotions
)

def classify_emotion(text):
    results = emotion_pipeline(text)[0]  # Get list of 27+1 emotions with scores
    sorted_result = sorted(results, key=lambda x: x['score'], reverse=True)
    return sorted_result