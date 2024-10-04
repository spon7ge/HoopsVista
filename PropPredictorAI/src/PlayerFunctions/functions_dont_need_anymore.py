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