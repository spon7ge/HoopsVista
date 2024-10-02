from nba_api.stats.static import players,teams
import requests
import pandas as pd
import json

 
#looks for name using players ID
def find_player_name_by_id(player_id):
    player_data = players.find_player_by_id(player_id=player_id)
    return player_data['full_name']

#looks for ID using name
def find_player_id_by_name(player_name):
    player_data = players.find_player_by_full_name(player_name)
    return player_data['id']

# Function to get upcoming NBA games
def get_upcoming_games():
    # NBA stats endpoint for today's scoreboard
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    response = requests.get(url) #import request
    data = response.json()
    
    games = []

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

