import time
import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo,playergamelog,boxscoreadvancedv2, leaguegamelog
from nba_api.stats.static import *

def get_player_ids_for_season(season='2022-23', output_csv='players_season.csv'):
    # Use leaguegamelog to get all player game logs for the specified season
    game_log = leaguegamelog.LeagueGameLog(season=season, player_or_team_abbreviation='P')
    player_games_df = game_log.get_data_frames()[0]

    # Extract unique player IDs and names
    player_ids_df = player_games_df[['PLAYER_ID', 'PLAYER_NAME']].drop_duplicates()

    # Sort the DataFrame by the last name
    player_ids_df = player_ids_df.sort_values(by='PLAYER_NAME', key=lambda x: x.str.split().str[-1])

    # Reset the index after sorting
    player_ids_df.reset_index(drop=True, inplace=True)

    # Save the DataFrame to a CSV file
    player_ids_df.to_csv(output_csv, index=False)
    print(f"Data successfully saved to '{output_csv}'")
    
    return player_ids_df

import time

#Get players game logs
def fetch_all_player_game_logs(player_ids, season='2022-23', sleep_time=0.6):
    all_game_logs = []
    player_info_dict = {}

    for idx, player_id in enumerate(player_ids['PLAYER_ID']):
        # Sleep to respect rate limits
        time.sleep(sleep_time)

        # Fetch player information (name and team) using commonplayerinfo
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
            player_name = player_info['DISPLAY_FIRST_LAST'][0]
            player_team_id = player_info['TEAM_ID'][0]
            player_info_dict[player_id] = {'Name': player_name, 'Team': player_team_id}
        except Exception as e:
            print(f"Error fetching info for player {player_id}: {e}")
            player_info_dict[player_id] = {'Name': 'Unknown', 'Team': 'Unknown'}

        try:
            # Fetch player game logs
            player_log = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
            
            # Add player name and team to each game log entry
            player_log['NAME'] = player_info_dict[player_id]['Name']
            player_log['Team_ID'] = player_info_dict[player_id]['Team']
            
            all_game_logs.append(player_log)
            print(f"Fetched game logs for player {idx + 1}/{len(player_ids)} (ID: {player_id})")
        except Exception as e:
            print(f"Error fetching game logs for player {player_id}: {e}")

    # Combine all player game logs
    all_game_logs_df = pd.concat(all_game_logs, ignore_index=True)
    return all_game_logs_df

#make sure we only get the unique gameIDs
def get_unique_game_ids(game_logs_df):
    game_ids = game_logs_df['Game_ID'].unique()
    return game_ids

#gather all adv stats
def fetch_all_advanced_stats(game_ids, sleep_time=0.6, retries=3):
    all_advanced_stats = []

    for idx, game_id in enumerate(game_ids):
        # Sleep to respect rate limits
        time.sleep(sleep_time)
        for attempt in range(retries):
            try:
                boxscore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id, timeout=60)
                advanced_stats = boxscore.get_data_frames()[0]
                all_advanced_stats.append(advanced_stats)
                print(f"Fetched advanced stats for game {idx + 1}/{len(game_ids)} (ID: {game_id})")
                break  # Break out of retry loop if successful
            except Exception as e:
                if attempt < retries - 1:
                    sleep_duration = 2 ** attempt
                    print(f"Error fetching advanced stats for game {game_id}, attempt {attempt + 1}/{retries}: {e}")
                    print(f"Retrying in {sleep_duration} seconds...")
                    time.sleep(sleep_duration)
                else:
                    print(f"Failed to fetch advanced stats for game {game_id} after {retries} attempts.")
        else:
            continue  # Move to the next game ID if failed

    # Combine all advanced stats
    all_advanced_stats_df = pd.concat(all_advanced_stats, ignore_index=True)
    return all_advanced_stats_df

#merge both adv and basic stats for each player
def merge_game_logs_and_advanced_stats(game_logs_df, advanced_stats_df,output_csv='merged_gamelogs_adv.csv'):
    #rename game_id and player_id
    game_logs_df.rename(columns={'Game_ID': 'GAME_ID', 'Player_ID': 'PLAYER_ID'}, inplace=True)
    # Select relevant columns from advanced stats
    columns_to_keep = ['GAME_ID', 'PLAYER_ID', 'USG_PCT', 'TS_PCT', 'EFG_PCT',
                       'OFF_RATING', 'DEF_RATING', 'NET_RATING']
    advanced_stats_df = advanced_stats_df[columns_to_keep]
    # Merge DataFrames
    merged_df = pd.merge(game_logs_df, advanced_stats_df, on=['GAME_ID', 'PLAYER_ID'], how='left')
    
    merged_df['GAME_DATE'] = pd.to_datetime(merged_df['GAME_DATE'])
    merged_df.to_csv(output_csv, index=False)
    print(f"Data successfully saved to '{output_csv}'")
    
    return merged_df

# game_logs_df = fetch_all_player_game_logs(player_ids, season='2022-23', sleep_time=0.5)

# # Get unique game IDs
# game_ids = get_unique_game_ids(game_logs_df)

# # Fetch all advanced stats
# advanced_stats_df = fetch_all_advanced_stats(game_ids, sleep_time=0.5, retries=3)

# # Merge game logs and advanced stats
# merged_23_df = merge_game_logs_and_advanced_stats(game_logs_df, advanced_stats_df)


def get_all_teams_gamelogs(season='2022-23'):
    team_ids = [team['id'] for team in teams.get_teams()]
    team_names = [team['full_name'] for team in teams.get_teams()] 
    team_gamelogs_all = []

    # Progress bar to track the downloading process
    for i, team_id in tqdm(enumerate(team_ids), total=len(team_ids), desc="Downloading Team Game Logs"):
        try:
            team_gamelogs = teamgamelog.TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
            team_gamelogs_all.append(team_gamelogs)
        except Exception as e:
            print(f"Error downloading data for {team_names[i]}: {e}")

    # Concatenate 
    team_gamelogs_all_df = pd.concat(team_gamelogs_all, ignore_index=True)

    return team_gamelogs_all_df

# Adds opponents DRTG, STL, BLK, and REB to each team for every game they played
def add_opponent_stats(teams_df):
    game_ids = teams_df['Game_ID'].unique()
    
    for i in game_ids:
        # Filter data for the current game
        game_data = teams_df[teams_df['Game_ID'] == i]

        if len(game_data) != 2:
            continue 

        # Split into two teams based on the matchup
        team_one = game_data.iloc[0]  # First team in the matchup
        team_two = game_data.iloc[1]  # Second team in the matchup

        # Calculate team one's DRTG (based on team two's offensive stats)
        team_one_DRTG = (team_two['PTS'] / (team_two['FGA'] + 0.44 * team_two['FTA'] - team_two['OREB'] + team_two['TOV'])) * 100

        # Calculate team two's DRTG (based on team one's offensive stats)
        team_two_DRTG = (team_one['PTS'] / (team_one['FGA'] + 0.44 * team_one['FTA'] - team_one['OREB'] + team_one['TOV'])) * 100

        # Update teams_df with the calculated DRTG values for both teams
        teams_df.loc[game_data.index[0], 'OPP_DRTG'] = team_two_DRTG  # Update team one with team two's DRTG
        teams_df.loc[game_data.index[1], 'OPP_DRTG'] = team_one_DRTG  # Update team two with team one's DRTG

        # Update team one's OPP stats based on team two's stats
        teams_df.loc[game_data.index[0], 'OPP_STL'] = team_two['STL']  # Team one's opponent steals
        teams_df.loc[game_data.index[0], 'OPP_BLK'] = team_two['BLK']  # Team one's opponent blocks
        teams_df.loc[game_data.index[0], 'OPP_REB'] = team_two['OREB'] + team_two['DREB']  # Team one's opponent total rebounds

        # Update team two's OPP stats based on team one's stats
        teams_df.loc[game_data.index[1], 'OPP_STL'] = team_one['STL']  # Team two's opponent steals
        teams_df.loc[game_data.index[1], 'OPP_BLK'] = team_one['BLK']  # Team two's opponent blocks
        teams_df.loc[game_data.index[1], 'OPP_REB'] = team_one['OREB'] + team_one['DREB']  # Team two's opponent total rebounds
    
    return teams_df

def add_pace_stats(teams_df):
    game_ids = teams_df['Game_ID'].unique()
    
    for i in game_ids:
        # Filter data for the current game
        game_data = teams_df[teams_df['Game_ID'] == i]

        if len(game_data) != 2:
            continue  # Ensure there are exactly two teams in the game

        # Split into two teams based on the matchup
        team_one = game_data.iloc[0]  # First team in the matchup
        team_two = game_data.iloc[1]  # Second team in the matchup

        # Calculate possessions for each team
        team_one_possessions = team_one['FGA'] + 0.44 * team_one['FTA'] - team_one['OREB'] + team_one['TOV']
        team_two_possessions = team_two['FGA'] + 0.44 * team_two['FTA'] - team_two['OREB'] + team_two['TOV']

        # Total possessions for the game (average of both teams)
        total_possessions = (team_one_possessions + team_two_possessions) / 2

        # Assume total game time is 48 minutes for NBA (could be adjusted for other leagues)
        game_pace = 48 * total_possessions / 48  # Total minutes is 48 for NBA regulation time

        # Update the DataFrame with team-specific pace values
        team_one_pace = 48 * team_one_possessions / 48
        team_two_pace = 48 * team_two_possessions / 48

        # Update teams_df with the calculated pace values
        teams_df.loc[game_data.index[0], 'TEAM_PACE'] = team_one_pace  # Update team one's pace
        teams_df.loc[game_data.index[1], 'TEAM_PACE'] = team_two_pace  # Update team two's pace

        # Update the overall game pace for both teams
        teams_df.loc[game_data.index[0], 'GAME_PACE'] = game_pace  # Game pace (same for both teams)
        teams_df.loc[game_data.index[1], 'GAME_PACE'] = game_pace  # Game pace (same for both teams)
    
    return teams_df


