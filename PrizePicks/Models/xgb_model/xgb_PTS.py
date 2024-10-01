import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib  # For saving the model

csv_file_path = os.path.join('..', 'Data', 'csv_file', 'combined_data', 'train_data.csv')
train_data = pd.read_csv(csv_file_path)

# Define features and target
features = [
    'MIN', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'PTS_LAST_3', 'PTS_LAST_5', 'PTS_LAST_7',
    'PLAYER_HOME_AVG_PTS', 'PLAYER_AWAY_AVG_PTS', 'USG_PCT', 'PER', 'TS_PCT',
    'USG_PCT_LAST_5', 'USG_DRTG_INTERACTION', 'NET_RATING', 'OFF_RATING', 'PF',
    'TEAM_OFF_RATING', 'TEAM_PACE', 'TEAM_PTS', 'TEAM_AST', 'TEAM_FGA',
    'OPP_DEF_RATING', 'OPP_PACE', 'GAME_PACE', 'HOME_GAME'
]

X_train = train_data[features]
y_train = train_data['PTS']

# Initialize and train the XGBRegressor
xgb_model_pts = XGBRegressor()
xgb_model_pts.fit(X_train, y_train)

# Evaluate the model using cross-validation on the training data
cv_scores = cross_val_score(xgb_model_pts, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-cv_scores)
print(f"Cross-validated RMSE: {rmse_scores.mean():.4f} ± {rmse_scores.std():.4f}")

# Load the test data (2024)
test_csv_file_path = os.path.join('..', 'Data', 'csv_file', '2024', 'players_df_2024.csv')
test_data = pd.read_csv(test_csv_file_path)

# Ensure the test data has the same features
X_test = test_data[features]
y_test = test_data['PTS']

# Make predictions on the 2024 data
predictions_2024 = xgb_model_pts.predict(X_test)

# Evaluate the model's performance on the 2024 data
rmse_2024 = np.sqrt(mean_squared_error(y_test, predictions_2024))
r2_2024 = r2_score(y_test, predictions_2024)
print(f"2024 Season RMSE: {rmse_2024:.4f}, R²: {r2_2024:.4f}")

# Add predictions to the 2024 data for comparison
test_data['actual'] = y_test
test_data['predicted'] = predictions_2024
test_data['error'] = abs(y_test-predictions_2024)

# Optionally, save the results or further analyze them
# test_data.to_csv('predictions_2024.csv', index=False)



