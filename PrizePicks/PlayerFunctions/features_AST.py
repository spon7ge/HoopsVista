import pandas as pd
import numpy as np

def add_usg_drtg_interaction(player_data):
    player_data['USG_DRTG_INTERACTION'] = player_data['USG_PCT'] * player_data['OPP_DEF_RATING']
    return player_data

def add_home_away_indicator(player_data, matchup_col='MATCHUP'):
    player_data['HOME_GAME'] = player_data[matchup_col].apply(lambda x: 1 if 'vs.' in x else 0)
    return player_data

def add_usg_pct_last_3(player_data):
    player_data['USG_PCT_LAST_3'] = player_data.groupby('PLAYER_ID')['USG_PCT'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    return player_data

def add_usg_pct_last_5(player_data):
    player_data['USG_PCT_LAST_3'] = player_data.groupby('PLAYER_ID')['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    return player_data

def avg_AST_last_3(player_data, player_id_col='PLAYER_ID', props=['AST'], games=3, date_col='GAME_DATE'):
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

def avg_AST_last_5(player_data, player_id_col='PLAYER_ID', props=['AST'], games=5, date_col='GAME_DATE'):
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

def avg_AST_last_7(player_data, player_id_col='PLAYER_ID', props=['AST'], games=7, date_col='GAME_DATE'):
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




def add_AST_home_avg(player_data, prop=['AST']): 
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

def add_AST_away_avg(player_data, props=['AST']): 
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
