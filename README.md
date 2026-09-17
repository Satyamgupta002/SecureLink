# 🛡️ SecureLink
A machine learning-based web application that detects and classifies websites as **legitimate** or **phishing** in real time. The model leverages advanced feature engineering techniques, ensemble learning algorithms, and Flask for deployment.

## 🎯 Key Features
-  **Automated Feature Extraction**: Based on URL characteristics, RegEx patterns, TLD structure, and entropy scores.
-  **Machine Learning Models**: XGBoost and Random Forest Classifier.
-  **Model Optimization**: RandomizedSearchCV for hyperparameter tuning, PCA for dimensionality reduction.
-  **Model Evaluation**: Accuracy, Precision, Recall, and F1-score used for assessment.
-  **Deployment**: Flask-powered web app with real-time predictions.
-  **Interactive UI**: Clean HTML frontend for URL input and instant results. 

## 🧩 How It Works
1. Input: User enters a URL into the web form.
2. Preprocessing: URL is cleaned and transformed via regular expressions, length-based features, and domain parsing.
3. Feature Engineering: Entropy calculation, TLD analysis, special character detection, and PCA-based dimensionality reduction.
4. Model Prediction: Pretrained ML model classifies the input as phishing or legitimate.
5. Output: Classification result is shown on the web UI.

## 📊 Future Enhancements
- Add support for browser extension integration.
- Cloud deployment with HTTPS and load balancing.
- Use LSTM or transformers for sequence-based phishing detection.
- Integrate phishing database cross-check for more accuracy.

## 📈 Interactive Dashboard
- Tableau - https://public.tableau.com/app/profile/tanisha.gangrade/vizzes
