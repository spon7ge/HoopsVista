import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,r2_score

# Load the data 
csv_file_path = os.path.join('..', 'Data', 'csv_file','2024', 'players_df_2024.csv')
data = pd.read_csv(csv_file_path) 



target_pts = 'PTS' 


# Split the dataset for each target
X = data[features]
y_pts = data[target_pts]


# Split into train and test sets (same split for all three models)
X_train, X_test, y_pts_train, y_pts_test = train_test_split(X, y_pts, test_size=0.2, random_state=42)

# Function to train Random Forest and XGBoost models
def train_and_evaluate(X_train, X_test, y_train, y_test, target_name):
    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    rf_rmse = mean_squared_error(y_test, rf_preds, squared=False)
    print(f"Random Forest RMSE for {target_name}: {rf_rmse}")

# Train and evaluate models for Points,Assits, and Rebounds
train_and_evaluate(X_train, X_test, y_pts_train, y_pts_test, "Points")

# Function to make predictions for a specific player against a specific team
def predict_for_player_team(model, player_id, team_id, other_features):
    input_data = [player_id, team_id] + other_features  # Combine player_id, team_id, and other features
    input_df = pd.DataFrame([input_data], columns=features)
    prediction = model.predict(input_df)
    return prediction

# Example: Predict points for a specific player and team
player_id = 123 
team_id = 456   
other_features = ['PLAYER_ID','MIN', 'FGA', 'FG3A', 'FTA', 'TOV', 'PLUS_MINUS', 'USG_PCT', 'TS_PCT', 'EFG_PCT',
                'OFF_RATING', 'PTS_LAST_5', 'HomeGame', 'DAYS_OF_REST', 'TEAM_PACE', 'GAME_PACE',
                'OPP_PACE', 'OPP_DRTG', 'OPP_STL', 'OPP_BLK', 'OPP_REB', 'PER', 'BACK_TO_BACK',
                'PLAYER_HOME_AVG_PTS', 'PLAYER_AWAY_AVG_PTS', 'USG_PCT_LAST_5', 'USG_DRTG_INTERACTION'
]

# Use the Random Forest model for prediction (you can also use XGBoost model)
points_prediction = predict_for_player_team(rf_model, player_id, team_id, other_features)
print(f"Predicted points: {points_prediction[0]}")
