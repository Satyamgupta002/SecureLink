from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import tldextract
from feature_extraction import extract_features  # Import feature extraction

# Load trained model
with open("phishing_model.pkl", "rb") as file:
    model = pickle.load(file)

app = Flask(__name__)

# Home Route (Frontend)
@app.route("/")
def home():
    return render_template("index.html")

# API Route for Phishing Detection
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        url = data.get("url")

        # Extract features
        features = extract_features(url)
        print("Extracted Features for", url, ":", features)  # Debugging

        if features is None:
            return jsonify({"error": "Feature extraction failed"})

        features_array = np.array(features).reshape(1, -1)
        print("Feature Array Shape:", features_array.shape)  # Debugging

        # Predict
        prediction = model.predict(features_array)[0]
        result = "Phishing" if prediction == 1 else "Legitimate"

        print("Prediction for", url, ":", result)  # Debugging

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)