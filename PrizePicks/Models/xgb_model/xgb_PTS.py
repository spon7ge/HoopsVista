import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib  # For saving the model

# Load the data
csv_file_path = os.path.join('..', 'Data', 'csv_file', '2024', 'players_df_2024.csv')
data = pd.read_csv(csv_file_path)

# Define the feature columns and the target variable
features = ['MIN', 'FTA', 'PTS_LAST_5', 'PLAYER_HOME_AVG_PTS', 'PLAYER_AWAY_AVG_PTS', 'USG_PCT', 'PER', 
            'PTS+REB_LAST_5', 'PTS+AST_LAST_5', 'TS_PCT', 'USG_PCT_LAST_5', 'USG_DRTG_INTERACTION', 'OFF_RATING', 
            'NET_RATING', 'TEAM_OFF_RATING', 'TEAM_PACE', 'TEAM_PTS', 'TEAM_AST', 'TEAM_FGA', 'TEAM_FG_PCT', 
            'OPP_DEF_RATING', 'OPP_PACE', 'OPP_REB', 'OPP_BLK', 'OPP_STL', 'HOME_GAME', 'GAME_PACE']

# Prepare feature matrix X and target variable y
X = data[features]
y = data['PTS']

# Split the data into training and validation sets (80% train, 20% validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining XGBoost model for PTS")

# Define the XGBoost model
xgb_model = XGBRegressor(random_state=42)

# Set up the hyperparameter grid for XGBoost
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Set up GridSearchCV
grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=param_grid,
    cv=5,
    n_jobs=-1,
    scoring='neg_mean_squared_error'
)

# Train the model using grid search
grid_search.fit(X_train, y_train)

# Get the best model from the grid search
best_xgb_model = grid_search.best_estimator_

# Predict on the validation set
y_pred = best_xgb_model.predict(X_val)

# Calculate performance metrics
rmse = np.sqrt(mean_squared_error(y_val, y_pred))
r2 = r2_score(y_val, y_pred)

print(f"PTS - RMSE: {rmse:.4f}, R²: {r2:.4f}")

# Save the best model
joblib.dump(best_xgb_model, f'best_xgb_model_PTS.joblib')
print(f"Best XGBoost model for PTS saved as best_xgb_model_PTS.joblib")

# Function to make predictions for a specific player against a specific team
def predict_for_player_team(model, input_features):
    input_df = pd.DataFrame([input_features], columns=features)
    prediction = model.predict(input_df)
    return prediction

# Function to find a player's stats by their name and make a prediction
def predict_points_by_player_name(player_name, model, data):
    # Search for the player in the dataset
    player_data = data[data['PLAYER_NAME'] == player_name]
    
    if player_data.empty:
        print(f"No data found for player: {player_name}")
        return None
    
    # Extract the relevant features (exclude 'PLAYER_NAME' and 'PTS')
    player_features = player_data[features].iloc[0]
    
    # Convert the features into a DataFrame (as the model expects)
    input_df = pd.DataFrame([player_features])
    
    # Predict the points for the player
    predicted_points = model.predict(input_df)
    
    print(f"Predicted points for {player_name}: {predicted_points[0]:.2f}")
    return predicted_points[0]

# Example: Predict points for a specific player by name
# player_name = 'LeBron James' 
# predict_points_by_player_name(player_name, best_xgb_model, data)
