import pandas as pd
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams

def get_teams_gamelogs(season='2023-24'):
    # Retrieve all team information
    all_teams = teams.get_teams()
    team_ids = [team['id'] for team in all_teams]
    team_names = [team['full_name'] for team in all_teams]
    team_gamelogs_all = []

    total_teams = len(team_ids)
    columns_to_remove = ['MATCHUP', 'WL', 'W', 'L', 'W_PCT','GAME_DATE']

    # Iterate over each team to download and process their game logs
    for i, team_id in enumerate(team_ids):
        try:
            print(f"Processing team {i+1}/{total_teams}: {team_names[i]}")
            team_gamelogs = teamgamelog.TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
            team_gamelogs.columns = team_gamelogs.columns.str.upper()# makes each col upper case
            
            # Remove specified columns; use case-insensitive matching
            columns_to_remove_upper = [col.upper() for col in columns_to_remove]
            team_gamelogs = team_gamelogs.drop(columns=columns_to_remove_upper, errors='ignore')
            
            # Identify columns to prefix (exclude 'GAME_ID' and 'TEAM_ID')
            columns_to_prefix = [col for col in team_gamelogs.columns if col not in ['GAME_ID', 'TEAM_ID']]
            
            # Add 'team_' prefix to the identified columns
            team_gamelogs = team_gamelogs.rename(columns=lambda x: f"TEAM_{x}" if x in columns_to_prefix else x)
            
            # Append the processed DataFrame to the list
            team_gamelogs_all.append(team_gamelogs)
        
        except Exception as e:
            print(f"Error downloading data for {team_names[i]}: {e}")

    if team_gamelogs_all:
        team_gamelogs_all_df = pd.concat(team_gamelogs_all, ignore_index=True)
        print("All team game logs have been successfully retrieved and concatenated.")
        return team_gamelogs_all_df
    else:
        print("No data was retrieved.")
        return pd.DataFrame()
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
'''
The features i will be using that involve using team data before i add it to the player
'''

# Adds opponents DRTG, STL, BLK, and REB to each team for every game they played
def add_opponent_stats(teams_df):
    game_ids = teams_df['GAME_ID'].unique()
    
    for i in game_ids:
        # Filter data for the current game
        game_data = teams_df[teams_df['GAME_ID'] == i]

        if len(game_data) != 2:
            continue 

        # Split into two teams based on the matchup
        team_one = game_data.iloc[0]  # First team in the matchup
        team_two = game_data.iloc[1]  # Second team in the matchup

        # Calculate team one's DRTG (based on team two's offensive stats)
        team_one_DRTG = (team_two['TEAM_PTS'] / (team_two['TEAM_FGA'] + 0.44 * team_two['TEAM_FTA'] - team_two['TEAM_OREB'] + team_two['TEAM_TOV'])) * 100

        # Calculate team two's DRTG (based on team one's offensive stats)
        team_two_DRTG = (team_one['TEAM_PTS'] / (team_one['TEAM_FGA'] + 0.44 * team_one['TEAM_FTA'] - team_one['TEAM_OREB'] + team_one['TEAM_TOV'])) * 100

        # Update teams_df with the calculated DRTG values for both teams
        teams_df.loc[game_data.index[0], 'OPP_DEF_RATING'] = team_two_DRTG  # Update team one with team two's DRTG
        teams_df.loc[game_data.index[1], 'OPP_DEF_RATING'] = team_one_DRTG  # Update team two with team one's DRTG

        # Update team one's OPP stats based on team two's stats
        teams_df.loc[game_data.index[0], 'OPP_STL'] = team_two['TEAM_STL']  # Team one's opponent steals
        teams_df.loc[game_data.index[0], 'OPP_BLK'] = team_two['TEAM_BLK']  # Team one's opponent blocks
        teams_df.loc[game_data.index[0], 'OPP_REB'] = team_two['TEAM_OREB'] + team_two['TEAM_DREB']  # Team one's opponent total rebounds

        # Update team two's OPP stats based on team one's stats
        teams_df.loc[game_data.index[1], 'OPP_STL'] = team_one['TEAM_STL']  # Team two's opponent steals
        teams_df.loc[game_data.index[1], 'OPP_BLK'] = team_one['TEAM_BLK']  # Team two's opponent blocks
        teams_df.loc[game_data.index[1], 'OPP_REB'] = team_one['TEAM_OREB'] + team_one['TEAM_DREB']  # Team two's opponent total rebounds
    
    return teams_df


#Adds the teams OFF_RATING and oponents OFF_RATING
def add_team_off_rating(teams_df):
    game_ids = teams_df['GAME_ID'].unique()
    
    for i in game_ids:
        # Filter data for the current game
        game_data = teams_df[teams_df['GAME_ID'] == i]

        if len(game_data) != 2:
            continue 
        
        # Split into two teams based on the matchup
        team_one = game_data.iloc[0]  # First team in the matchup
        team_two = game_data.iloc[1]  # Second team in the matchup

        # Calculate possessions for both teams
        team_one_possessions = team_one['TEAM_FGA'] + 0.44 * team_one['TEAM_FTA'] - team_one['TEAM_OREB'] + team_one['TEAM_TOV']
        team_two_possessions = team_two['TEAM_FGA'] + 0.44 * team_two['TEAM_FTA'] - team_two['TEAM_OREB'] + team_two['TEAM_TOV']

        # Calculate team one's Offensive Rating (based on team one's own offensive stats)
        team_one_off_rating = (team_one['TEAM_PTS'] / team_one_possessions) * 100

        # Calculate team two's Offensive Rating (based on team two's own offensive stats)
        team_two_off_rating = (team_two['TEAM_PTS'] / team_two_possessions) * 100

        # Update teams_df with the calculated OFF_RATING values for both teams
        teams_df.loc[game_data.index[0], 'TEAM_OFF_RATING'] = team_one_off_rating  # Team one's offensive rating
        teams_df.loc[game_data.index[1], 'TEAM_OFF_RATING'] = team_two_off_rating  # Team two's offensive rating
    
    return teams_df


#adds pace for team, the overall game and oppenents
def add_pace_stats(teams_df):
    game_ids = teams_df['GAME_ID'].unique()
    
    for i in game_ids:
        game_data = teams_df[teams_df['GAME_ID'] == i]
        if len(game_data) != 2:
            continue 
        
        # Split into two teams based on the matchup
        team_one = game_data.iloc[0]  # First team in the matchup
        team_two = game_data.iloc[1]  # Second team in the matchup

        # Calculate possessions for each team
        team_one_possessions = team_one['TEAM_FGA'] + 0.44 * team_one['TEAM_FTA'] - team_one['TEAM_OREB'] + team_one['TEAM_TOV']
        team_two_possessions = team_two['TEAM_FGA'] + 0.44 * team_two['TEAM_FTA'] - team_two['TEAM_OREB'] + team_two['TEAM_TOV']

        # Total possessions for the game (average of both teams)
        total_possessions = (team_one_possessions + team_two_possessions) / 2

        # Assume total game time is 48 minutes for NBA (could be adjusted for other leagues)
        game_pace = 48 * total_possessions / 48  # Total minutes is 48 for NBA regulation time

        # Calculate pace for each team
        team_one_pace = 48 * team_one_possessions / 48
        team_two_pace = 48 * team_two_possessions / 48

        # Update teams_df with the calculated team pace values
        teams_df.loc[game_data.index[0], 'TEAM_PACE'] = team_one_pace  # Update team one's pace
        teams_df.loc[game_data.index[1], 'TEAM_PACE'] = team_two_pace  # Update team two's pace

        # Update teams_df with the overall game pace (same for both teams)
        teams_df.loc[game_data.index[0], 'GAME_PACE'] = game_pace  # Game pace (same for both teams)
        teams_df.loc[game_data.index[1], 'GAME_PACE'] = game_pace  # Game pace (same for both teams)

        # Update teams_df with the opponent's pace
        teams_df.loc[game_data.index[0], 'OPP_PACE'] = team_two_pace  # Opponent pace for team one is team two's pace
        teams_df.loc[game_data.index[1], 'OPP_PACE'] = team_one_pace  # Opponent pace for team two is team one's pace
    
    return teams_df