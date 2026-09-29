import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("data/messages.csv")

# Input and output
X = data["text"]
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create NLP + ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("================================")
print("SafeText AI Model")
print("================================")
print(f"Accuracy: {accuracy * 100:.2f}%")

# Create model folder if it doesn't exist
os.makedirs("model", exist_ok=True)

# Save trained model
with open("model/scam_detector.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")
print("File: model/scam_detector.pkl")