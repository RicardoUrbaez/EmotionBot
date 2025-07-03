from src.emotion_classifier import classify_emotion

def main():
    print("🤖 EmotionBot is running! Type a sentence and I’ll tell you how you’re feeling.")
    print("Type 'quit' to exit.\n")

    while True:
        text = input("You: ")
        if text.lower() == 'quit':
            break

        emotions = classify_emotion(text)
        top_emotion = emotions[0]

        print(f"\n🎯 Top Emotion: {top_emotion['label']} ({top_emotion['score']:.2f})")
        print("📊 Full breakdown:")
        for e in emotions:  # 🔥 This will now print all 27 emotions
            print(f" - {e['label']}: {e['score']:.2f}")
        print("\n")

if __name__ == "__main__":
    main()

    