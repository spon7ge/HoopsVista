from fetch_player_data import *
from fetch_team_data import *
from features import *
import pandas as pd
import os

def prepare_recent_player_logs(season='2024-25'):
    # Fetch team logs and enhance with opponent stats, offensive ratings, and pace
    team_logs = get_teams_gamelogs(season=season)
    team_logs = add_opponent_stats(team_logs)
    team_logs = add_team_off_rating(team_logs)
    team_logs = add_pace_stats(team_logs)

    # Fetch player logs and add advanced stats
    player_logs = fetch_and_process_player_stats(season=season)
    advanced_stats = add_advanced_stats_for_player_games(player_logs)
    player_logs = merge_player_stats_with_advanced_data(player_logs, advanced_stats)

    # Merge player logs with team logs
    recent_logs = merge_player_with_team(player_logs, team_logs)

    return recent_logs

# Example usage:
player_recent_logs = prepare_recent_player_logs()


# def prepare_recent_player_logs(season='2024-25', update_only=True):
#     # File to store the last update information
#     update_info_file = f'update_info_{season}.json'
    
#     if update_only and os.path.exists(update_info_file):
#         with open(update_info_file, 'r') as f:
#             update_info = json.load(f)
#         last_update = pd.to_datetime(update_info['last_update'])
#         last_game_count = update_info['game_count']
#     else:
#         last_update = pd.to_datetime('1900-01-01')
#         last_game_count = 0

#     # Fetch team logs and enhance with opponent stats, offensive ratings, and pace
#     team_logs = get_teams_gamelogs(season=season)
#     new_game_count = len(team_logs)

#     if new_game_count > last_game_count:
#         team_logs = add_opponent_stats(team_logs)
#         team_logs = add_team_off_rating(team_logs)
#         team_logs = add_pace_stats(team_logs)

#         # Fetch player logs and add advanced stats
#         player_logs = fetch_and_process_player_stats(season=season)
#         advanced_stats = add_advanced_stats_for_player_games(player_logs)
#         player_logs = merge_player_stats_with_advanced_data(player_logs, advanced_stats)

#         # Merge player logs with team logs
#         recent_logs = merge_player_with_team(player_logs, team_logs)

#         # If updating, only keep new games
#         if update_only:
#             recent_logs = recent_logs[recent_logs['GAME_DATE'] > last_update]

#         # Update the existing data file if it exists, otherwise create a new one
#         existing_data_file = f'player_logs_{season}.csv'
#         if os.path.exists(existing_data_file) and update_only:
#             existing_data = pd.read_csv(existing_data_file)
#             updated_data = pd.concat([existing_data, recent_logs]).drop_duplicates().reset_index(drop=True)
#         else:
#             updated_data = recent_logs

#         # Save the updated data
#         updated_data.to_csv(existing_data_file, index=False)

#         # Update the update info file
#         with open(update_info_file, 'w') as f:
#             json.dump({
#                 'last_update': pd.Timestamp.now().isoformat(),
#                 'game_count': new_game_count
#             }, f)

#         return updated_data
#     else:
#         print("No new games to update.")
#         return pd.read_csv(f'player_logs_{season}.csv')
