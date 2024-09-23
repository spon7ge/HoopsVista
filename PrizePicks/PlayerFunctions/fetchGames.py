
# Function to get upcoming NBA games
def get_upcoming_games():
    # NBA stats endpoint for today's scoreboard
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    
    # Fetch the data
    response = requests.get(url) #import request
    data = response.json()
    
    # List to store upcoming games
    games = []

    # Loop through each game and extract relevant information
    for game in data['scoreboard']['games']:
        game_info = {
            'home_team': game['homeTeam']['teamName'],
            'away_team': game['awayTeam']['teamName'],
            'game_time': game['gameEt']
        }
        games.append(game_info)

    return games
# Fetch and print upcoming games
# upcoming_games = get_upcoming_games()

#read JSON file
def read_json(json_file):
    # Load the JSON file
    file_path = json_file
    with open(file_path, 'r') as file:
        data = json.load(file)

    df = pd.json_normalize(data['data'])
    return df

# def fetch_players_for_games(games_df):
#     # Code to fetch player IDs for today's games
#     return player_ids

# def fetch_player_data(player_id):
#     # Code to fetch historical data for a player
#     df_player = playergamelog.PlayerGameLog(player_id=player_id,season='2024-25').get_data_frames()[0]
#     return df_player

# def preprocess_player_data(df_player):
#     # Code for feature engineering
#     return df_preprocessed

# def predict_player_stat(df_preprocessed, model):
#     # Code to make predictions
#     return predicted_stat

# def compile_predictions(predictions):
#     # Code to compile all predictions into a DataFrame
#     return predictions_df

# def compare_with_lines(predictions_df):
#     # Code to compare predictions with over/under lines
#     return final_df

# def main():
#     games_df = fetch_today_games()
#     player_ids = fetch_players_for_games(games_df)
#     predictions = {}
#     for player_id in player_ids:
#         df_player = fetch_player_data(player_id)
#         df_preprocessed = preprocess_player_data(df_player)
#         predicted_stat = predict_player_stat(df_preprocessed, model)
#         predictions[player_id] = predicted_stat
#     predictions_df = compile_predictions(predictions)
#     final_df = compare_with_lines(predictions_df)
#     # Output or upload final_df as needed

# if __name__ == "__main__":
#     main()
