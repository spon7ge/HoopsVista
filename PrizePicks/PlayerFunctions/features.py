import pandas as pd
import numpy as np

# adds the opposing teams defensive stats
# Function to merge player_data with team and opponent stats
def merge_player_with_team(player_data, team_data):
    """
    Merges player_data with team_data to add team and opponent details.
    
    Parameters:
    - player_data (pd.DataFrame): DataFrame containing player game logs.
    - team_data (pd.DataFrame): DataFrame containing team game stats.
    
    Returns:
    - pd.DataFrame: Merged DataFrame with opponent details.
    """
    # Step 1: Rename 'Game_ID' to 'GAME_ID' in team_data if not already done
    if 'Game_ID' in team_data.columns:
        team_data.rename(columns={'Game_ID': 'GAME_ID', 'Team_ID':'TEAM_ID'}, inplace=True)
    
    # Step 2: Prepare opponent stats by renaming columns to avoid duplication
    teams_df_opp = team_data.copy()
    teams_df_opp.rename(columns={
        'TEAM_ID': 'OPP_TEAM_ID',
        'TEAM_PACE': 'OPP_TEAM_PACE',
        'TEAM_OFF_RATING': 'OPP_TEAM_OFF_RATING',
        'OPP_DRTG': 'OPP_DEF_RATING',
        'STL': 'OPP_STL',
        'BLK': 'OPP_BLK',
        'REB': 'OPP_REB'
    }, inplace=True)
    
    # Step 3: Merge team_data with teams_df_opp on 'GAME_ID'
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
        teams_df_merged,
        on=['GAME_ID', 'TEAM_ID'],
        how='left'
    )
    # Step 7: Reset index to ensure uniqueness
    player_data.reset_index(drop=True, inplace=True)
    
    # Step 8: Verify 'GAME_ID' presence
    if 'GAME_ID' not in player_data.columns:
        raise KeyError("'GAME_ID' column is missing from player_data after merging.")
    else:
        print("'GAME_ID' column is present in player_data.")
    
    # Step 9: Check and remove duplicate columns if any
    duplicate_columns = player_data.columns[player_data.columns.duplicated()].unique()
    if len(duplicate_columns) > 0:
        print(f"Duplicate columns found: {duplicate_columns}")
        # Drop duplicate columns
        player_data = player_data.loc[:, ~player_data.columns.duplicated()]
        print("Duplicate columns have been removed.")
    player_data = remove_suffixes(player_data)
    return player_data

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

def add_pace_to_player_data(player_data):
    # Check if necessary columns exist
    required_columns = ['TEAM_PACE', 'GAME_PACE', 'OPP_PACE']
    for col in required_columns:
        if col not in player_data.columns:
            player_data[col] = np.nan  # or handle appropriately
    
    return player_data

def remove_suffixes(df):
    new_columns = []
    for col in df.columns:
        if col.endswith('_x') or col.endswith('_y'):
            new_columns.append(col[:-2])  # Remove the last two characters
        else:
            new_columns.append(col)
    df.columns = new_columns
    return df

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
    player_data['HomeGame'] = player_data[matchup_col].apply(lambda x: 1 if 'vs.' in x else 0)
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










