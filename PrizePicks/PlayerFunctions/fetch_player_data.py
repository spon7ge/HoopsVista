import os
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog, boxscoreadvancedv2 
from nba_api.stats.static import players 
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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

def fetch_advanced_stats_for_game(game_id, sleep_time=1):
   try:
       time.sleep(sleep_time)  # Sleep to respect rate limits
       boxscore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
       advanced_stats = boxscore.get_data_frames()[0]  # Adjust index if necessary
       return advanced_stats
   except Exception as e:
       print(f"Error fetching advanced stats for game {game_id}: {e}")
       return pd.DataFrame()


# Function to fetch advanced stats for all games in player_data using parallel processing
def add_advanced_stats_for_player_games(player_data, sleep_time=1, max_workers=4):
   # Extract unique game IDs from player data
   game_ids = player_data['GAME_ID'].unique()  # Assuming 'game_id' is the column containing game IDs
   total_games = len(game_ids)
   all_advanced_stats = []


   # Use ThreadPoolExecutor to fetch stats in parallel
   with ThreadPoolExecutor(max_workers=max_workers) as executor:
       futures = {executor.submit(fetch_advanced_stats_for_game, game_id, sleep_time): game_id for game_id in game_ids}
      
       for idx, future in enumerate(as_completed(futures)):
           game_id = futures[future]
           try:
               advanced_stats = future.result()
               if not advanced_stats.empty:
                   all_advanced_stats.append(advanced_stats)
               print(f"Fetched advanced stats for game {idx + 1}/{total_games} (ID: {game_id})")
           except Exception as e:
               print(f"Error processing game {game_id}: {e}")


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
        'GAME_ID','PLAYER_ID','OFF_RATING', 'DEF_RATING', 'NET_RATING',
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
def save_player_stats_to_csv(data, season='2025',type='team'):
    # Set the data directory directly to your desired path
    data_dir = 'C:/Users/alexg/OneDrive/Documents/player_predictor/HoopsVista/PrizePicks/Data/csv_file/2025' #windows
    # data_dir = '/Applications/Documents/PredictorProject/playerPredictor/PrizePicks/Data/csv_file/2023' #mac
    os.makedirs(data_dir, exist_ok=True)  # Creates the directory if it doesn't exist
    output_file = os.path.join(data_dir, f'{type}_df_{season}.csv')
    data.to_csv(output_file, index=False)  # Saves the data to the specified file
    print(f"Data saved to {output_file}")
    return output_file


def append_to_combined_csv(new_file, combined_file='Data/csv_file/combined_data/train_data.csv'):
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