from flask import Flask, request, jsonify
import pickle
import numpy as np
from feature_extraction import extract_features  # Import your feature extraction function

# Initialize Flask app
app = Flask(__name__)

# Load trained model
with open("phishing_model.pkl", "rb") as file:
    model = pickle.load(file)

@app.route("/")
def home():
    return "Phishing Detection API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"})

        # Extract features
        features = extract_features(url)
        print(f"Extracted Features for {url}: {features}")  # Debugging

        if features is None or len(features) == 0:
            return jsonify({"error": "Feature extraction failed"})

        # Convert to numpy array and reshape
        features_array = np.array(features).reshape(1, -1)
        print(f"Feature Array Shape: {features_array.shape}")  # Debugging

        # Ensure feature count matches model expectation
        if features_array.shape[1] != model.n_features_in_:
            return jsonify({
                "error": f"Feature count mismatch. Expected {model.n_features_in_}, got {features_array.shape[1]}"
            })

        # Make prediction
        prediction = model.predict(features_array)[0]
        result = "Phishing" if prediction == 1 else "Legitimate"

        print(f"Prediction for {url}: {result}")  # Debugging

        return jsonify({"prediction": result})

    except Exception as e:
        print(f"Error processing request: {str(e)}")  # Debugging
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
