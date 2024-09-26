import pandas as pd
import numpy as np
from scipy import stats
import json

def preprocess_nba_data(data):
    """
    Preprocesses NBA player data by handling outliers, converting data types, and normalizing data.
    
    Parameters:
    - data (pd.DataFrame): Raw data fetched from the NBA Stats API.
    
    Returns:
    - pd.DataFrame: Preprocessed data.
    """
    # Step 1: Convert data types as necessary
    # Convert 'GAME_DATE' to datetime
    data['GAME_DATE'] = pd.to_datetime(data['GAME_DATE'])
    
    # Ensure numerical columns are of appropriate types
    numeric_columns = ['PLAYER_NAME','PLAYER_ID','MATCHUP', 'TEAM','TEAM_ID', 'OPPONENT','GAME_ID', 'GAME_DATE','WL', 'PTS', 'AST', 'REB', 'MIN', 'FGM',
       'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
       'OREB', 'DREB', 'STL', 'BLK', 'TOV', 'PF','PLUS_MINUS','FANTASY_PTS', 'GAME_ID','PLAYER_ID','OFF_RATING', 'DEF_RATING', 'NET_RATING',
        'AST_PCT', 'AST_TOV', 'USG_PCT', 'TS_PCT', 'E_PACE']
    
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Step 2: Handle outliers using IQR method
    # Define a function to remove outliers based on IQR
    def remove_outliers_iqr(df, columns):
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            # Filter out outliers
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        return df

    # Apply the IQR outlier removal
    # data = remove_outliers_iqr(data, numeric_columns)
    
    # Alternatively, you can use z-score method
    # Define a function to remove outliers based on z-score
    def remove_outliers_zscore(df, columns, threshold=3):
        z_scores = np.abs(stats.zscore(df[columns], nan_policy='omit'))
        filter_mask = (z_scores < threshold).all(axis=1)
        return df[filter_mask]
    
    # Uncomment the following line to use z-score method instead
    data = remove_outliers_zscore(data, numeric_columns)
    
    # Step 3: Normalize or standardize the data
    # Choose between normalization and standardization
    # Normalization (Min-Max Scaling)
    # from sklearn.preprocessing import MinMaxScaler
    # scaler = MinMaxScaler()
    # data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
    
    # Standardization (Z-score Scaling)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
    
    # Return the preprocessed data
    return data

#read JSON file
def read_json(json_file):
    # Load the JSON file
    file_path = json_file
    with open(file_path, 'r') as file:
        data = json.load(file)

    df = pd.json_normalize(data['data'])
    return df


# Load raw data
def load_raw_data(file_path): # ex. file_path = r'c:\\Users\\alexg\\OneDrive\\Documents\\player_predictor\\HoopsVista\\PrizePicks\\Data\\csv_file\\combined_data\\combined_seasons_df.csv'
    return pd.read_csv(file_path) 

