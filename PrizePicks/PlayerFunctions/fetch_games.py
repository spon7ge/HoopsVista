import requests

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

    return games # Fetch and print upcoming games
# upcoming_games = get_upcoming_games()