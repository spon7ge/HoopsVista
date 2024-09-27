import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import joblib  # For saving the model

# Load the data
csv_file_path = os.path.join('..', 'Data', 'csv_file', '2024', 'players_df_2024.csv')
data = pd.read_csv(csv_file_path)

features = ['MIN', 'FTA', 'PTS_LAST_5', 'PLAYER_HOME_AVG_PTS', 'PLAYER_AWAY_AVG_PTS', 'USG_PCT', 'PER', 'PTS+REB_LAST_5', 'PTS+AST_LAST_5', 
    'TS_PCT', 'USG_PCT_LAST_5', 'USG_DRTG_INTERACTION', 'OFF_RATING', 'NET_RATING', 'TEAM_OFF_RATING', 'TEAM_PACE', 'TEAM_PTS', 'TEAM_AST', 'TEAM_FGA', 'TEAM_FG_PCT', 
    'OPP_TEAM_ID', 'OPP_DEF_RATING', 'OPP_PACE', 'OPP_REB', 'OPP_BLK', 'OPP_STL', 'HOME_GAME', 'GAME_PACE'
]

# Prepare feature matrix X and target variables y
X = data[features]
y = data['PTS']

# Split the data into training and validation sets (same split for all targets)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# For each target stat, train a model with cross-validation and hyperparameter tuning

print("\nTraining model for PTS")

# Define the model
model = RandomForestRegressor(random_state=42)

# Set up hyperparameter grid for GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

# Set up GridSearchCV
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,
    n_jobs=-1,
    scoring='neg_mean_squared_error'
)

# Train the model
grid_search.fit(X_train, y_train['PTS'])

# Get the best model
best_model = grid_search.best_estimator_

# Predict on the validation set
y_pred = best_model.predict(X_val)

# Calculate performance metrics
rmse = np.sqrt(mean_squared_error(y_val['PTS'], y_pred))
r2 = r2_score(y_val['PTS'], y_pred)
print(f"PTS - RMSE: {rmse:.4f}, R²: {r2:.4f}")

# Save the best model
joblib.dump(best_model, f'best_model_PTS.joblib')
print(f"Best model for PTS saved as best_model_PTS.joblib")

# Function to make predictions for a specific player against a specific team
def predict_for_player_team(model, input_features):
    input_df = pd.DataFrame([input_features], columns=features)
    prediction = model.predict(input_df)
    return prediction

# Example: Predict points for a specific player and team
# Prepare input features for the player and team
player_features = ['MIN', 'FTA', 'PTS_LAST_5', 'PLAYER_HOME_AVG_PTS', 'PLAYER_AWAY_AVG_PTS', 'USG_PCT', 'PER', 'PTS+REB_LAST_5', 'PTS+AST_LAST_5', 
    'TS_PCT', 'USG_PCT_LAST_5', 'USG_DRTG_INTERACTION', 'OFF_RATING', 'NET_RATING', 'TEAM_OFF_RATING', 'TEAM_PACE', 'TEAM_PTS', 'TEAM_AST', 'TEAM_FGA', 'TEAM_FG_PCT', 
    'OPP_TEAM_ID', 'OPP_DEF_RATING', 'OPP_PACE', 'OPP_REB', 'OPP_BLK', 'OPP_STL', 'HOME_GAME', 'GAME_PACE'
]
# Load the saved model for 'PTS'
best_model_pts = joblib.load('best_model_PTS.joblib')

# Function to find a player's stats by their name and make a prediction
def predict_points_by_player_name(player_name, model, data):
    # Search for the player in the dataset
    player_data = data[data['PLAYER_NAME'] == player_name]
    
    if player_data.empty:
        print(f"No data found for player: {player_name}")
        return None
    
    # Extract the relevant features (exclude 'PLAYER_NAME' and 'PTS')
    features = ['MIN', 'FTA', 'PTS_LAST_5', 'PLAYER_HOME_AVG_PTS', 'PLAYER_AWAY_AVG_PTS', 'USG_PCT', 'PER', 'PTS+REB_LAST_5', 
                'PTS+AST_LAST_5', 'TS_PCT', 'USG_PCT_LAST_5', 'USG_DRTG_INTERACTION', 'OFF_RATING', 'NET_RATING', 
                'TEAM_OFF_RATING', 'TEAM_PACE', 'TEAM_PTS', 'TEAM_AST', 'TEAM_FGA', 'TEAM_FG_PCT', 'OPP_DEF_RATING', 
                'OPP_PACE', 'OPP_REB', 'OPP_BLK', 'OPP_STL', 'HOME_GAME', 'GAME_PACE']
    
    # Select only the relevant features for the player
    player_features = player_data[features].iloc[0]
    
    # Convert the features into a DataFrame (as the model expects)
    input_df = pd.DataFrame([player_features])
    
    # Predict the points for the player
    predicted_points = model.predict(input_df)
    
    print(f"Predicted points for {player_name}: {predicted_points[0]:.2f}")
    return predicted_points[0]

# Example: Predict points for a specific player by name
# player_name = 'LeBron James' 
# predict_points_by_player_name(player_name, best_model_pts, data)

