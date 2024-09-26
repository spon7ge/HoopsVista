import os
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog, boxscoreadvancedv2 
from nba_api.stats.static import players 
import time
from datetime import datetime

#grabs basic stats from gamelogs
def fetch_and_process_player_stats(season='2024-25'):
    # Fetch all player game logs
    game_logs = leaguegamelog.LeagueGameLog(
        season=season, 
        player_or_team_abbreviation='P'
    ).get_data_frames()[0]
    
    # Rename columns
    game_logs.rename(columns={'TEAM_ABBREVIATION': 'TEAM'}, inplace=True)
    # Process 'MATCHUP' to get 'OPPONENT'
    def extract_opponent(row):
        matchup = row['MATCHUP']
        team_abbr = row['TEAM']
        if ' vs. ' in matchup:
            opponent = matchup.split(' vs. ')[1]
        elif ' @ ' in matchup:
            opponent = matchup.split(' @ ')[1]
        else:
            opponent = None
        return opponent

    game_logs['OPPONENT'] = game_logs.apply(extract_opponent, axis=1)
    
    # Reorder columns
    game_logs = game_logs[['PLAYER_NAME','PLAYER_ID','MATCHUP', 'TEAM','TEAM_ID', 'OPPONENT','GAME_ID', 'GAME_DATE','WL', 'MIN', 'PTS', 'AST', 'REB', 'FGM',
       'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
       'OREB', 'DREB','STL', 'BLK', 'TOV', 'PF','PLUS_MINUS','FANTASY_PTS']]
    
    return game_logs

#grabs ADV stats
def fetch_advanced_stats_for_games(game_ids, sleep_time=0.6):
    all_advanced_stats = []
    total_games = len(game_ids)
    
    for idx, game_id in enumerate(game_ids):
        # Respect rate limits
        time.sleep(sleep_time)
        try:
            boxscore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
            advanced_stats = boxscore.get_data_frames()[0]
            all_advanced_stats.append(advanced_stats)
            print(f"Fetched advanced stats for game {idx + 1}/{total_games} (ID: {game_id})")
        except Exception as e:
            print(f"Error fetching advanced stats for game {game_id}: {e}")
    
    # Combine all advanced stats into a single DataFrame
    if all_advanced_stats:
        advanced_stats_df = pd.concat(all_advanced_stats, ignore_index=True)
        return advanced_stats_df
    else:
        print("No advanced stats were fetched.")
        return pd.DataFrame()

#Merge both basic and adv stats into one file
def merge_player_stats_with_advanced_data(player_data, advanced_stats):
    player_data['GAME_ID'] = player_data['GAME_ID'].astype(str)
    advanced_stats['GAME_ID'] = advanced_stats['GAME_ID'].astype(str)
    advanced_stats['PLAYER_ID'] = advanced_stats['PLAYER_ID'].astype(int)
    # Select relevant columns from advanced stats
    advanced_columns = [
        'GAME_ID','PLAYER_ID','OFF_RATING', 'PLAYER_DEF_RATING', 'NET_RATING',
        'AST_PCT', 'AST_TOV', 'USG_PCT', 'TS_PCT', 'E_PACE'
    ]
    advanced_stats_subset = advanced_stats[advanced_columns]
    
    # Merge on 'GAME_ID' and 'PLAYER_ID'
    merged_data = pd.merge(player_data, advanced_stats_subset, on=['GAME_ID', 'PLAYER_ID'], how='left')
    
    return merged_data


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
'''

Using these functions you can save the files into the Data folder/csv_file with its correct folder, then we append it to the combined_seasons_df.csv to use for my model

'''
def save_player_stats_to_csv(data, season='2025'):
    # Set the data directory directly to your desired path
    data_dir = 'C:/Users/alexg/OneDrive/Documents/player_predictor/HoopsVista/PrizePicks/Data/csv_file/2025' #windows
    # data_dir = '/Applications/Documents/PredictorProject/playerPredictor/PrizePicks/Data/csv_file/2025' #mac
    os.makedirs(data_dir, exist_ok=True)  # Creates the directory if it doesn't exist
    output_file = os.path.join(data_dir, f'player_df_{season}.csv')
    data.to_csv(output_file, index=False)  # Saves the data to the specified file
    print(f"Data saved to {output_file}")
    return output_file


def append_to_combined_csv(new_file, combined_file='data/csv_file/combined/combined_df.csv'):
    # Read new data
    new_data = pd.read_csv(new_file)
    # Read existing combined data
    if os.path.exists(combined_file):
        combined_data = pd.read_csv(combined_file)
        # Append new data
        combined_data = pd.concat([combined_data, new_data], ignore_index=True)
    else:
        combined_data = new_data
    # Save combined data
    combined_data.to_csv(combined_file, index=False)
    print(f"Data appended to {combined_file}")