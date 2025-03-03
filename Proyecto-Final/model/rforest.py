from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import pandas as pd

df = pd.read_csv("Proyecto-Final/data/raw/matches.csv")

X = df[['WhiteRatingDiff', 'Opening', 'TimeControl', 'Result', 'Moves']] 
y = df['WhiteElo']  # Target variable is 'WhiteElo'

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the trained model
with open('../model/chess_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

# Predict on the test set
y_pred = rf_model.predict(X_test)

# Print the predicted vs actual values
print("Predicted WhiteElo vs Actual WhiteElo:")
for i in range(10):
    print(f"Predicted: {y_pred[i]}, Actual: {y_test.iloc[i]}")
