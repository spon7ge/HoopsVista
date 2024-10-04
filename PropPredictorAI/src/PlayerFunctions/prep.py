from fetch_player_data import *
from fetch_team_data import *
import pandas as pd
import os

def prepare_latest_player_and_team_logs(season='2024-25'):
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
    combined_logs = merge_player_with_team(player_logs, team_logs)

    return combined_logs

# Example usage:
latest_logs = prepare_latest_player_and_team_logs()

def append_to_combined_data(combined_file='Data/csv_file/combined_data/combined_clean_df_.csv', season='2024-25'):
    # Prepare the latest player and team logs
    latest_logs = prepare_latest_player_and_team_logs(season=season)

    # Check if the combined data file exists
    if os.path.exists(combined_file):
        # Load the existing combined data
        combined_data = pd.read_csv(combined_file)
        # Append the latest logs
        combined_data = pd.concat([combined_data, latest_logs], ignore_index=True)
    else:
        # If the file does not exist, use the latest logs as the combined data
        combined_data = latest_logs

    # Save the updated combined data back to the file
    combined_data.to_csv(combined_file, index=False)
    print(f"Data appended to {combined_file}")

# Example usage:
append_to_combined_data()

