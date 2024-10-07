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
recent_logs = prepare_recent_player_logs()

