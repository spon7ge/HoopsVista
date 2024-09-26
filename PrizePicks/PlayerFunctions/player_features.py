import pandas as pd
import numpy as np

# adds the opposing teams defensive stats
# Function to merge player_data with team and opponent stats
def merge_player_with_team(player_data, team_data):    
    # Prepare opponent stats by renaming columns to avoid duplication
    teams_df_opp = team_data.copy()
    teams_df_opp.rename(columns={
        'TEAM_ID': 'OPP_TEAM_ID',
        'TEAM_PACE': 'OPP_TEAM_PACE',
        'TEAM_OFF_RATING': 'OPP_TEAM_OFF_RATING',
        'OPP_DEF_RATING': 'OPP_DEF_RATING',
        'TEAM_STL': 'OPP_STL',
        'TEAM_BLK': 'OPP_BLK',
        'TEAM_REB': 'OPP_REB'
    }, inplace=True)
    
    # Merge team_data with teams_df_opp on 'GAME_ID'
    teams_df_merged = pd.merge(
        team_data,
        teams_df_opp[['GAME_ID', 'OPP_TEAM_ID', 'OPP_TEAM_PACE', 'OPP_TEAM_OFF_RATING',
                    'OPP_DEF_RATING', 'OPP_STL', 'OPP_BLK', 'OPP_REB']],
        on='GAME_ID',
        how='inner'  # Use 'left' if you want to keep all team_data entries
    )
    
    # Step 4: Filter out rows where Team_ID == OPP_TEAM_ID
    teams_df_merged = teams_df_merged[teams_df_merged['TEAM_ID'] != teams_df_merged['OPP_TEAM_ID']]
    
    # Step 5: Drop the 'OPP_TEAM_ID' column as it's no longer needed
    teams_df_merged.drop(columns=['OPP_TEAM_ID'], inplace=True)
    
    # Step 6: Merge with player_data on ['GAME_ID', 'TEAM_ID']
    player_data = pd.merge(
        player_data,
        opponent_stats,
        left_on=['GAME_ID', 'OPP_TEAM_ID'],
        right_on=['GAME_ID', 'OPP_TEAM_ID'],
        how='left'
    )
    
    # Drop the temporary 'OPP_TEAM_ID' column
    merged_data.drop(columns=['OPP_TEAM_ID'], inplace=True)
    
    # Remove duplicates if any (optional, based on your data)
    merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]
    
    return merged_data

# Adds Player Efficiency Rating to each game they played in 
def player_PER(player_data):
    # Constants
    uPER_constants = {
        'FG': 85.910, 'FT': 53.897, '3P': 51.757, 'ORB': 39.190,
        'DRB': 39.190, 'AST': 34.677, 'STL': 53.897, 'BLK': 53.897,
        'TO': 17.174, 'PF': 20.091
    }
    
    # Calculate components
    player_data['uPER'] = (
        uPER_constants['FG'] * player_data['FGM'] +
        uPER_constants['FT'] * player_data['FTM'] +
        uPER_constants['3P'] * player_data['FG3M'] +
        uPER_constants['ORB'] * player_data['OREB'] +
        uPER_constants['DRB'] * player_data['DREB'] +
        uPER_constants['AST'] * player_data['AST'] +
        uPER_constants['STL'] * player_data['STL'] +
        uPER_constants['BLK'] * player_data['BLK'] -
        uPER_constants['TO'] * player_data['TOV'] -
        uPER_constants['PF'] * player_data['PF']
    )
    
    # Avoid division by zero
    player_data['MIN'] = player_data['MIN'].replace(0, np.nan)
    player_data['PER'] = player_data['uPER'] / player_data['MIN']
    player_data['PER'] = player_data['PER'].fillna(0)
    
    # Drop the intermediate 'uPER' column if not needed
    player_data.drop(columns=['uPER'], inplace=True)
    
    return player_data

def add_pace_to_player_data(player_data, teams_df):
    player_data['TEAM_PACE'] = None
    player_data['GAME_PACE'] = None
    player_data['OPP_PACE'] = None
    
    # Iterate through each row in the player_data
    for idx, player in player_data.iterrows():
        game_id = player['GAME_ID']  # Get the Game_ID from player_data
        team_id = player['TEAM_ID']  # Get the Team_ID from player_data
        
        # Get the game data from teams_df corresponding to this game
        game_data = teams_df[teams_df['GAME_ID'] == game_id]
        
        # Make sure there are exactly 2 teams in the game
        if len(game_data) != 2:
            continue  # Skip if the game data doesn't have exactly 2 teams
        
        # Find the player's team and opponent team in the game data
        if game_data.iloc[0]['TEAM_ID'] == team_id:
            team_row = game_data.iloc[0]  # This is the player's team
            opp_row = game_data.iloc[1]   # This is the opponent team
        else:
            team_row = game_data.iloc[1]  # This is the player's team
            opp_row = game_data.iloc[0]   # This is the opponent team
        
        # Assign the team's pace, game pace, and opponent's pace to the player
        player_data.loc[idx, 'TEAM_PACE'] = team_row['TEAM_PACE']  # Player's team's pace
        player_data.loc[idx, 'GAME_PACE'] = team_row['GAME_PACE']  # Overall game pace (same for both teams)
        player_data.loc[idx, 'OPP_PACE'] = opp_row['TEAM_PACE']    # Opponent's pace
    
    return player_data

def last_5_avg(player_data, player_id_col='PLAYER_ID', props=['PTS'], games=5, date_col='GAME_DATE'):
    # If a single stat is passed, convert it to a list to keep the logic consistent
    if isinstance(props, str):
        props = [props]
    
    # Create a new column name based on the combined stats (e.g., PTS+AST)
    combined_name = '+'.join(props)
    rolling_col_name = f"{combined_name}_LAST_{games}"
    
    # Sort by player and date to ensure rolling works correctly
    player_data = player_data.sort_values([player_id_col, date_col])
    
    # Calculate the rolling mean for the combined stat without adding the intermediate column
    player_data[rolling_col_name] = (
        player_data[props]
        .sum(axis=1)  # Sum the selected properties
        .groupby(player_data[player_id_col])  # Group by player ID
        .rolling(window=games, min_periods=1)  # Apply rolling window
        .mean()
        .reset_index(level=0, drop=True)  # Reset index after rolling
    )
    
    return player_data


def add_home_away_indicator(player_data, matchup_col='MATCHUP'):
    player_data['HOME_GAME'] = player_data[matchup_col].apply(lambda x: 1 if 'vs.' in x else 0)
    return player_data

#Get days of rest in between games
def calculate_days_of_rest(df, player_id_col='PLAYER_ID', game_date_col='GAME_DATE'):
    df[game_date_col] = pd.to_datetime(df[game_date_col], format='%Y-%m-%d')
    df = df.sort_values(by=[player_id_col, game_date_col])
    df['DAYS_OF_REST'] = df.groupby(player_id_col)[game_date_col].diff().dt.days
    return df


#looks for back-to-back games
def add_back_to_back(player_data):
    """
    Adds a 'BACK_TO_BACK' column to the DataFrame. 
    The value is 1 if the 'DAYS_OF_REST' is equal to 1, otherwise 0.
    """
    player_data['BACK_TO_BACK'] = player_data['DAYS_OF_REST'].apply(lambda x: 1 if x == 1 else 0)
    return player_data


def add_player_home_avg(player_data,prop):
    avg_column_name = f'PLAYER_HOME_AVG_{prop}'
    player_data[avg_column_name] = player_data.groupby('PLAYER_ID').apply(
    lambda group: group[prop].where(group['HomeGame'] == 1).expanding().mean()
    ).reset_index(level=0, drop=True)
    return player_data

def add_player_away_avg(player_data,prop):
    avg_column_name = f'PLAYER_AWAY_AVG_{prop}'
    player_data[avg_column_name] = player_data.groupby('PLAYER_ID').apply(
    lambda group: group[prop].where(group['HomeGame'] == 0).expanding().mean()
    ).reset_index(level=0, drop=True)
    return player_data

def add_usg_pct_last_5(player_data):
    player_data['USG_PCT_LAST_5'] = player_data.groupby('PLAYER_ID')['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    return player_data

def add_usg_drtg_interaction(player_data):
    player_data['USG_DRTG_INTERACTION'] = player_data['USG_PCT'] * player_data['OPP_DRTG']
    return player_data

# teams_data['TEAM_AVG_OFF_RATING_LAST_5'] = teams_data.groupby('Team_ID')['OFF_RATING'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
"""
HELPER FUNCTIONS USED IN MERGE BETWEEN PLAYER AND TEAM
"""
def remove_duplicate_columns(df, keep='first'):
    """
    Removes duplicate columns from a DataFrame.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame to process.
    - keep (str): Which duplicates to keep. Options are:
        - 'first': Keep the first occurrence.
        - 'last': Keep the last occurrence.
        - False: Drop all duplicates.
    
    Returns:
    - pd.DataFrame: DataFrame with duplicate columns removed.
    """
    if keep not in ['first', 'last', False]:
        raise ValueError("Parameter 'keep' must be 'first', 'last', or False.")
    
    # Identify duplicate columns
    duplicate_columns = df.columns[df.columns.duplicated()].unique().tolist()
    if duplicate_columns:
        print(f"Duplicate columns found: {duplicate_columns}")
    else:
        print("No duplicate columns found.")
    
    # Remove duplicates
    df_cleaned = df.loc[:, ~df.columns.duplicated(keep=keep)]
    
    if duplicate_columns:
        print(f"Removed duplicate columns. Remaining columns: {df_cleaned.columns.tolist()}")
    else:
        print("No columns were removed.")
    
    return df_cleaned

def remove_suffixes(df):
    new_columns = []
    for col in df.columns:
        if col.endswith('_x') or col.endswith('_y'):
            new_columns.append(col[:-2])  # Remove the last two characters
        else:
            new_columns.append(col)
    df.columns = new_columns
    return df




