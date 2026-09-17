import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Add more legitimate websites to balance the dataset
X_train = np.array([
    [18, 1, 3, 0, 0],  # Example phishing site
    [20, 0, 2, 1, 1],  # Example legitimate site
    [10, 1, 3, 0, 0],  # Google (legitimate)
    [12, 1, 2, 0, 0],  # Amazon (legitimate)
    [25, 0, 5, 1, 1],  # Phishing example
    [22, 1, 3, 0, 0],  # Facebook (legitimate)
])

y_train = [1, 0, 0, 0, 1, 0]  # 1 = Phishing, 0 = Legitimate

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save new model
with open("phishing_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("New model trained and saved!")
