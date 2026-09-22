# inference_model.py

import re
import joblib
import pandas as pd
import tldextract

from collections import Counter
from scipy.stats import entropy


# ============================================================
# 1. Load trained model
# ============================================================

artifact = joblib.load("phishing_model.pkl")

model = artifact["model"]
FEATURE_COLUMNS = artifact["feature_columns"]


# ============================================================
# 2. Feature-engineering configuration
# ============================================================

# Use the SAME lists that were used during training.
dangerous_chars = [
    '\\',
    ';',
    '|',
    '@',
    "'",
    '-',
    '&',
    '>',
    '<',
    '='
]

# IMPORTANT:
# Replace these with the exact dangerous_TLDs list
# you used while training your original model.
dangerous_TLDs = [
    # Example:
    # "xyz",
    # "top",
    # "click",
]


sus_words = [
    "secure",
    "account",
    "update",
    "login",
    "verify",
    "signin",
    "bank",
    "notify",
    "click",
    "inconvenient"
]


ip_pattern = r"[0-9]+(?:\.[0-9]+){3}"


# ============================================================
# 3. Entropy
# ============================================================

def urlentropy(url):

    frequencies = Counter(url)

    probabilities = [
        frequencies[char] / len(url)
        for char in url
    ]

    return entropy(probabilities, base=2)


# ============================================================
# 4. Feature extraction
# ============================================================

def extract_features(url):

    features = {}

    # 1. URL length
    features["URL length"] = len(url)

    # 2. Number of dots
    features["Number of dots"] = url.count(".")

    # 3. Number of slashes
    features["Number of slashes"] = url.count("/")

    # 4. Percentage of numerical characters
    features["Percentage of numerical characters"] = (
        sum(c.isdigit() for c in url) / len(url)
        if len(url) > 0 else 0
    )

    # 5. Dangerous characters
    features["Dangerous characters"] = int(
        any(char in url for char in dangerous_chars)
    )

    # 6. Dangerous TLD
    extracted = tldextract.extract(url)

    features["Dangerous TLD"] = int(
        extracted.suffix in dangerous_TLDs
    )

    # 7. Entropy
    features["Entropy"] = urlentropy(url)

    # 8. IP Address
    features["IP Address"] = int(
        bool(re.search(ip_pattern, url))
    )

    # 9. Domain name length
    features["Domain name length"] = len(
        extracted.domain
    )

    # 10. Suspicious keywords
    features["Suspicious keywords"] = int(
        any(word in url for word in sus_words)
    )

    # 11. Repetitions
    features["Repetitions"] = int(
        bool(
            re.search(
                r"(.)\1{2,}",
                extracted.domain
            )
        )
    )

    # 12. Redirections
    pos = url.rfind("//")

    features["Redirections"] = int(pos > 7)


    # ========================================================
    # VERY IMPORTANT:
    # Force exactly the training feature order
    # ========================================================

    feature_vector = pd.DataFrame(
        [[features[column] for column in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    return feature_vector


# ============================================================
# 5. Prediction function
# ============================================================

def predict_url(url):

    features = extract_features(url)

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0][1]

    if prediction == 1:
        label = "Phishing"
    else:
        label = "Legitimate"

    return {
        "url": url,
        "prediction": label,
        "phishing_probability": round(float(probability), 4),
        "features": features
    }


# ============================================================
# 6. Test
# ============================================================

if __name__ == "__main__":

    url = input("Enter URL: ").strip()

    result = predict_url(url)

    print("\nPrediction")
    print("=" * 40)

    print("URL:", result["url"])
    print("Prediction:", result["prediction"])
    print(
        "Phishing Probability:",
        result["phishing_probability"]
    )

    print("\nExtracted Features:")
    print(result["features"].to_string(index=False))