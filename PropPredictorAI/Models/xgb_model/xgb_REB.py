import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib  # For saving the model

csv_file_path = os.path.join('..', 'Data', 'csv_file', 'combined_data', 'train_data.csv')
train_data = pd.read_csv(csv_file_path)

features = [
    'MIN', 'OREB', 'DREB', 'REB_LAST_3', 'REB_LAST_5', 'REB_LAST_7',
    'USG_PCT', 'TS_PCT', 'PLAYER_HOME_AVG_REB', 'PLAYER_AWAY_AVG_REB',
    'TEAM_REB', 'TEAM_OREB', 'TEAM_DREB', 'TEAM_PACE',
    'OPP_DEF_RATING', 'OPP_REB', 'OPP_BLK', 'OPP_PACE','HOME_GAME'
]

X_train = train_data[features]
y_train = train_data['REB']

# Initialize and train the XGBRegressor
xgb_model_ast = XGBRegressor()
xgb_model_ast.fit(X_train, y_train)

# Evaluate the model using cross-validation on the training data
cv_scores = cross_val_score(xgb_model_ast, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-cv_scores)
print(f"Cross-validated RMSE: {rmse_scores.mean():.4f} ± {rmse_scores.std():.4f}")

# Load the test data (2024)
test_csv_file_path = os.path.join('..', 'Data', 'csv_file', '2024', 'players_df_2024.csv')
test_data = pd.read_csv(test_csv_file_path)

# Ensure the test data has the same features
X_test = test_data[features]
y_test = test_data['REB']

# Make predictions on the 2024 data
predictions_2024 = xgb_model_ast.predict(X_test)

# Evaluate the model's performance on the 2024 data
rmse_2024 = np.sqrt(mean_squared_error(y_test, predictions_2024))
r2_2024 = r2_score(y_test, predictions_2024)
print(f"2024 Season RMSE: {rmse_2024:.4f}, R²: {r2_2024:.4f}")

# Add predictions to the 2024 data for comparison
test_data['actual'] = y_test
test_data['predicted'] = predictions_2024
test_data['error'] = abs(y_test-predictions_2024)



