import pandas as pd

def calculate_pts_last_5(player_data, player_id_col='PLAYER_ID', prop='PTS',games=5):
    name = f"{prop}_LAST_{games}"
    player_data['PTS_LAST_5'] = player_data.groupby(player_id_col)[pts_col].rolling(window=games).mean().reset_index(0, drop=True)
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

def add_pace_to_player_data(player_data, teams_df):
    player_data['TEAM_PACE'] = None
    player_data['GAME_PACE'] = None
    player_data['OPP_PACE'] = None
    
    # Iterate through each row in the player_data
    for idx, player in player_data.iterrows():
        game_id = player['GAME_ID']  # Get the Game_ID from player_data
        team_id = player['Team_ID']  # Get the Team_ID from player_data
        
        # Get the game data from teams_df corresponding to this game
        game_data = teams_df[teams_df['Game_ID'] == game_id]
        
        # Make sure there are exactly 2 teams in the game
        if len(game_data) != 2:
            continue  # Skip if the game data doesn't have exactly 2 teams
        
        # Find the player's team and opponent team in the game data
        if game_data.iloc[0]['Team_ID'] == team_id:
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

# adds the opposing teams defensive stats
def add_opp_team_stats(player_data, teams_df): # use the parameters, how they are 
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

def get_team_off_rating(player_data, teams_df):
    player_data['TEAM_OFF_RATING'] = None
    
    # Iterate through each row in the player_data
    for idx, player in player_data.iterrows():
        game_id = player['GAME_ID']  # Get the GAME_ID from player_data
        team_id = player['Team_ID']  # Get the Team_ID from player_data
        
        # Get the game data from teams_df corresponding to this game
        game_data = teams_df[teams_df['Game_ID'] == game_id]
        
        # Ensure that the team data exists for the player's team
        team_data = game_data[game_data['Team_ID'] == team_id]
        
        # Check if we have exactly one matching team
        if len(team_data) != 1:
            continue  # Skip if the team data is not found uniquely
        
        # Get the TEAM_OFF_RATING from team_data
        team_off_rating = team_data.iloc[0]['TEAM_OFF_RATING']
        
        # Assign the team's offensive rating to the player
        player_data.loc[idx, 'TEAM_OFF_RATING'] = team_off_rating
    
    return player_data

# Adds Player Efficiency Rating to each game they played in 
def add_player_PER(player_data):
    # Create a new column in player_data to store the PER
    player_data['PER'] = None
    
    # Constants used in PER calculation
    uPER_constants = {
        'FG': 85.910,  
        'FT': 53.897,   
        '3P': 51.757,   
        'ORB': 39.190,  
        'DRB': 39.190, 
        'AST': 34.677,  
        'STL': 53.897, 
        'BLK': 53.897, 
        'TO': 17.174,   
        'PF': 20.091,   
    }
    
    # Iterate through each row in the player_data
    for idx, player in player_data.iterrows():
        # Calculate the various components for uPER
        FG_value = uPER_constants['FG'] * player['FGM']
        FT_value = uPER_constants['FT'] * player['FTM']
        _3P_value = uPER_constants['3P'] * player['FG3M']
        ORB_value = uPER_constants['ORB'] * player['OREB']
        DRB_value = uPER_constants['DRB'] * player['DREB']
        AST_value = uPER_constants['AST'] * player['AST']
        STL_value = uPER_constants['STL'] * player['STL']
        BLK_value = uPER_constants['BLK'] * player['BLK']
        TO_value = uPER_constants['TO'] * player['TOV']
        PF_value = uPER_constants['PF'] * player['PF']
        
        # Calculate uPER (unadjusted PER)
        uPER = (FG_value + FT_value + _3P_value + ORB_value + DRB_value + 
                AST_value + STL_value + BLK_value - TO_value - PF_value)
        
        # Calculate the player's minutes
        minutes = player['MIN']
        
        # Calculate final PER
        if minutes > 0:  # Avoid division by zero
            PER = uPER / minutes
        else:
            PER = 0
        
        # Assign the calculated PER to the player_data DataFrame
        player_data.loc[idx, 'PER'] = PER
    
    return player_data

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
    player_data['USG_DRTG_INTERACTION'] = playe_data['USG_PCT'] * player_data['OPP_DRTG']
    return player_data

# def add_streak(player_data,prop):
#     streak = f'{prop}_STREAK'
#     player_data[streak] = player_data.groupby('PLAYER_ID')[prop].apply(lambda x: (x > x.mean()).cumsum())
#     return player_data

# teams_data['TEAM_AVG_OFF_RATING_LAST_5'] = teams_data.groupby('Team_ID')['OFF_RATING'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())










