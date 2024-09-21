def calculate_pts_last_5(player_data, player_id_col='PLAYER_ID', pts_col='PTS'):
    """
    Calculates the rolling average of the last 5 games' points for each player.
    
    Parameters:
    player_data (pd.DataFrame): The player data containing player IDs and points.
    player_id_col (str): The column name of the player IDs (default is 'PLAYER_ID').
    pts_col (str): The column name of the points (default is 'PTS').
    
    Returns:
    pd.DataFrame: Updated DataFrame with a 'PTS_LAST_5' column.
    """
    player_data['PTS_LAST_5'] = player_data.groupby(player_id_col)[pts_col].rolling(window=5).mean().reset_index(0, drop=True)
    return player_data

def calculate_pts_last_10(player_data, player_id_col='PLAYER_ID', pts_col='PTS'):
    """
    Calculates the rolling average of the last 5 games' points for each player.
    
    Parameters:
    player_data (pd.DataFrame): The player data containing player IDs and points.
    player_id_col (str): The column name of the player IDs (default is 'PLAYER_ID').
    pts_col (str): The column name of the points (default is 'PTS').
    
    Returns:
    pd.DataFrame: Updated DataFrame with a 'PTS_LAST_5' column.
    """
    player_data['PTS_LAST_10'] = player_data.groupby(player_id_col)[pts_col].rolling(window=10).mean().reset_index(0, drop=True)
    return player_data


def calculate_pts_last_15(player_data, player_id_col='PLAYER_ID', pts_col='PTS'):
    """
    Calculates the rolling average of the last 5 games' points for each player.
    
    Parameters:
    player_data (pd.DataFrame): The player data containing player IDs and points.
    player_id_col (str): The column name of the player IDs (default is 'PLAYER_ID').
    pts_col (str): The column name of the points (default is 'PTS').
    
    Returns:
    pd.DataFrame: Updated DataFrame with a 'PTS_LAST_5' column.
    """
    player_data['PTS_LAST_15'] = player_data.groupby(player_id_col)[pts_col].rolling(window=15).mean().reset_index(0, drop=True)
    return player_data

def add_home_away_indicator(player_data, matchup_col='MATCHUP'):
    """
    Adds a Home/Away indicator based on the 'MATCHUP' column.
    
    Parameters:
    player_data (pd.DataFrame): The player data containing the 'MATCHUP' column.
    matchup_col (str): The column name of the matchups (default is 'MATCHUP').
    
    Returns:
    pd.DataFrame: Updated DataFrame with a 'HomeGame' column.
    """
    player_data['HomeGame'] = player_data[matchup_col].apply(lambda x: 1 if 'vs.' in x else 0)
    return player_data

def calculate_days_of_rest(player_data, player_id_col='PLAYER_ID', game_date_col='GAME_DATE'):
    """
    Calculates the days of rest between games for each player.
    
    Parameters:
    player_data (pd.DataFrame): The player data containing player IDs and game dates.
    player_id_col (str): The column name of the player IDs (default is 'PLAYER_ID').
    game_date_col (str): The column name of the game dates (default is 'GAME_DATE').
    
    Returns:
    pd.DataFrame: Updated DataFrame with 'PREV_GAME_DATE' and 'DAYS_OF_REST' columns.
    """
    # Add previous game date column
    player_data['PREV_GAME_DATE'] = player_data.groupby(player_id_col)[game_date_col].shift(1)
    
    # Calculate days of rest
    player_data['DAYS_OF_REST'] = (player_data[game_date_col] - player_data['PREV_GAME_DATE']).dt.days.fillna(0)
    
    return player_data

def add_pace_to_player_data(player_data, teams_df):
    # Create new columns in player_data to store the pace stats
    player_data['TEAM_PACE'] = None
    player_data['GAME_PACE'] = None
    
    # Iterate through each row in the player_data
    for idx, player in player_data.iterrows():
        game_id = player['GAME_ID']  # Get the Game_ID from player_data
        team_id = player['Team_ID']  # Get the Team_ID from player_data
        
        # Get the game data from teams_df corresponding to this game
        game_data = teams_df[teams_df['Game_ID'] == game_id]
        
        # Make sure there are exactly 2 teams in the game
        if len(game_data) != 2:
            continue  # Skip if the game data doesn't have exactly 2 teams
        
        # Find the player's team in the game data
        if game_data.iloc[0]['Team_ID'] == team_id:
            team_row = game_data.iloc[0]  # This is the player's team
        else:
            team_row = game_data.iloc[1]  # This is the player's team
        
        # Assign the team's pace and game pace to the player
        player_data.loc[idx, 'TEAM_PACE'] = team_row['PACE']  # Player's team's pace
        player_data.loc[idx, 'GAME_PACE'] = team_row['GAME_PACE']  # Overall game pace (same for both teams)
    
    return player_data

def add_opp_team_stats(player_data, teams_df):
    # Create new columns in player_data to store the opponent stats
    player_data['OPP_DRTG'] = None
    player_data['OPP_STL'] = None
    player_data['OPP_BLK'] = None
    player_data['OPP_REB'] = None
    
    # Iterate through each row in the player_data
    for idx, player in player_data.iterrows():
        game_id = player['GAME_ID']  # Get the Game_ID from player_data
        team_id = player['Team_ID']  # Get the Team_ID from player_data
        
        # Get the game data from teams_df corresponding to this game
        game_data = teams_df[teams_df['Game_ID'] == game_id]
        
        # Make sure there are exactly 2 teams in the game
        if len(game_data) != 2:
            continue  # Skip if the game data doesn't have exactly 2 teams
        
        # Identify the player's opponent (the other team in the game)
        if game_data.iloc[0]['Team_ID'] == team_id:
            opp_team = game_data.iloc[1]  # The opponent is the second team
        else:
            opp_team = game_data.iloc[0]  # The opponent is the first team
        
        # Assign the opponent's stats to the player
        player_data.loc[idx, 'OPP_DRTG'] = opp_team['OPP_DRTG']
        player_data.loc[idx, 'OPP_STL'] = opp_team['OPP_STL']
        player_data.loc[idx, 'OPP_BLK'] = opp_team['OPP_BLK']
        player_data.loc[idx, 'OPP_REB'] = opp_team['OPP_REB']
    
    return player_data




