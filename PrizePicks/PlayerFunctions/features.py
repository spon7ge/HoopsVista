import pandas as pd
import numpy as np

# adds the opposing teams defensive stats
def merge_player_with_team(player_data, team_data):
    # Perform a left merge to add all team details to each player
    merged_data = pd.merge(
        player_data,
        team_data,
        on=['GAME_ID', 'TEAM_ID'],
        how='left'
    )
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
def add_back_to_back(player_data): #isnt working need to get back to it
    """
    Adds a 'BACK_TO_BACK' column to the DataFrame. 
    The value is 1 if the 'DAYS_OF_REST' is equal to 1, otherwise 0.
    """
    player_data['BACK_TO_BACK'] = player_data['DAYS_OF_REST'].apply(lambda x: 1 if x == 1 else 0)
    return player_data


def add_player_home_avg(player_data, props): 
    # Create a new column for each prop or combination of props
    if isinstance(props, list):  # Case for multiple properties like PTS + AST
        avg_column_name = f'PLAYER_HOME_AVG_{"_".join(props)}'
        # Sum or combine the selected properties
        player_data[avg_column_name] = player_data[props].sum(axis=1)
    else:  # Case for a single property
        avg_column_name = f'PLAYER_HOME_AVG_{props}'
    
    # Calculate the expanding mean for home games
    player_data[avg_column_name] = player_data.groupby('PLAYER_ID').apply(
        lambda group: group[avg_column_name].where(group['HOME_GAME'] == 1).expanding().mean()
    ).reset_index(level=0, drop=True)
    
    return player_data

def add_player_away_avg(player_data, props): 
    # Create a new column for each prop or combination of props
    if isinstance(props, list):  # Case for multiple properties like PTS + AST
        avg_column_name = f'PLAYER_AWAY_AVG_{"_".join(props)}'
        # Sum or combine the selected properties
        player_data[avg_column_name] = player_data[props].sum(axis=1)
    else:  # Case for a single property
        avg_column_name = f'PLAYER_AWAY_AVG_{props}'
    
    # Calculate the expanding mean for home games
    player_data[avg_column_name] = player_data.groupby('PLAYER_ID').apply(
        lambda group: group[avg_column_name].where(group['HOME_GAME'] == 0).expanding().mean()
    ).reset_index(level=0, drop=True)
    
    return player_data


def add_usg_pct_last_5(player_data):
    player_data['USG_PCT_LAST_5'] = player_data.groupby('PLAYER_ID')['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    return player_data

def add_usg_drtg_interaction(player_data):
    player_data['USG_DRTG_INTERACTION'] = player_data['USG_PCT'] * player_data['OPP_DEF_RATING']
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




