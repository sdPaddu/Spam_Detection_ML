import joblib
import re

# Load model and vectorizer
model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]','',text)
    return text


def predict_spam(msg):

    clean = clean_text(msg)

    vec = vectorizer.transform([clean])

    result = model.predict(vec)

    return "Spam" if result[0] == 1 else "Ham"


while True:

    message = input("\nEnter message (type 'exit' to quit): ")

    if message.lower() == "exit":
        break

    prediction = predict_spam(message)

    print("Prediction:", prediction)