import pandas as pd
import numpy as np
import json
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler


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


# Remove or Impute Missing Values
def handle_missing_values(df, strategy='mean'):
    """
    This function handles missing values by either removing rows or imputing with a chosen strategy.
    Options for strategy: 'mean', 'median', or 'remove'.
    """
    if strategy == 'remove':
        df_cleaned = df.dropna()
    else:
        if strategy == 'mean':
            df_cleaned = df.fillna(df.mean())
        elif strategy == 'median':
            df_cleaned = df.fillna(df.median())
    
    return df_cleaned


def handle_outliers(df, method='z-score', threshold=3):
    """
    This function handles outliers using either the z-score or IQR method.
    """
    if method == 'z-score':
        # Z-score method
        z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
        df_cleaned = df[(z_scores < threshold).all(axis=1)]
    elif method == 'iqr':
        # IQR method
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        df_cleaned = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    
    return df_cleaned

def convert_data_types(df):
    """
    This function converts data types as needed, such as converting date fields to datetime.
    """
    if 'GAME_DATE' in df.columns:
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    
    return df


def normalize_or_standardize(df, method='normalize'):
    """
    This function normalizes or standardizes the numeric columns of the dataframe.
    Options for method: 'normalize' (MinMax scaling) or 'standardize' (Standard scaling).
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if method == 'normalize':
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    elif method == 'standardize':
        scaler = StandardScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    return df


# Full preprocessing pipeline
def preprocess_data(df, missing_value_strategy='mean', outlier_method='z-score', outlier_threshold=3, scaling_method='normalize'):
    """
    This function applies the entire preprocessing pipeline on the raw data.
    """
    # Step 1: Handle missing values
    df = handle_missing_values(df, strategy=missing_value_strategy)
    
    # Step 2: Handle outliers
    df = handle_outliers(df, method=outlier_method, threshold=outlier_threshold)
    
    # Step 3: Convert data types
    df = convert_data_types(df)
    
    # Step 4: Normalize or standardize the data
    df = normalize_or_standardize(df, method=scaling_method)
    
    return df


# Save the cleaned data to a CSV file
def save_cleaned_data(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Cleaned data saved to {file_path}")



# Example usage
if __name__ == "__main__":
    raw_data_path = 'raw_nba_player_stats.csv'  # Raw data CSV file
    cleaned_data_path = 'cleaned_nba_player_stats.csv'  # Output file for cleaned data
    
    # Load raw data
    raw_data = load_raw_data(raw_data_path)
    
    # Preprocess data
    cleaned_data = preprocess_data(raw_data, missing_value_strategy='mean', outlier_method='z-score', scaling_method='normalize')
    
    # Save the cleaned data to a CSV file
    save_cleaned_data(cleaned_data, cleaned_data_path)