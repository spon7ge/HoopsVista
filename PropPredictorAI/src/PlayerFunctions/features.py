import pandas as pd
import numpy as np

def add_PTS_features(player_data, player_id_col='PLAYER_ID', date_col='GAME_DATE'):
    # Sort by player and date to ensure rolling works correctly
    player_data = player_data.sort_values([player_id_col, date_col])

    # Add USG_PCT for last 3 and 5 games
    player_data['USG_PCT_LAST_3'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    player_data['USG_PCT_LAST_5'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

    # Add average PTS for last 3, 5, and 7 games
    for games in [3, 5, 7]:
        rolling_col_name = f"PTS_LAST_{games}"
        player_data[rolling_col_name] = (
            player_data.groupby(player_id_col)['PTS']
            .transform(lambda x: x.rolling(window=games, min_periods=1).mean())
        )

    # Add home and away average PTS
    for home_away in ['HOME', 'AWAY']:
        avg_column_name = f'PLAYER_{home_away}_AVG_PTS'
        is_home = player_data['HOME_GAME'] == (1 if home_away == 'HOME' else 0)
        player_data[avg_column_name] = (
            player_data.groupby(player_id_col)
            .apply(lambda group: group.loc[is_home, 'PTS'].expanding().mean())
            .reset_index(level=0, drop=True)
        )

    return player_data

def add_REB_features(player_data, player_id_col='PLAYER_ID', date_col='GAME_DATE'):
    # Sort by player and date to ensure rolling works correctly
    player_data = player_data.sort_values([player_id_col, date_col])
    # Add USG_PCT for last 3 and 5 games
    player_data['USG_PCT_LAST_3'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    player_data['USG_PCT_LAST_5'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

    for games in [3, 5, 7]:
        rolling_col_name = f"REB_LAST_{games}"
        player_data[rolling_col_name] = (
            player_data['REB']
            .groupby(player_data[player_id_col])
            .rolling(window=games, min_periods=1)
            .mean()
            .reset_index(level=0, drop=True)
        )

    for home_away in ['HOME', 'AWAY']:
        avg_column_name = f'PLAYER_{home_away}_AVG_REB'
        player_data[avg_column_name] = player_data.groupby(player_id_col).apply(
            lambda group: group['REB'].where(group['HOME_GAME'] == (1 if home_away == 'HOME' else 0)).expanding().mean()
        ).reset_index(level=0, drop=True)

    return player_data

def add_AST_features(player_data, player_id_col='PLAYER_ID', date_col='GAME_DATE'):
    # Sort by player and date to ensure rolling works correctly
    player_data = player_data.sort_values([player_id_col, date_col])
    # Add USG_PCT for last 3 and 5 games
    player_data['USG_PCT_LAST_3'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    player_data['USG_PCT_LAST_5'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

    # Add average PTS for last 3, 5, and 7 games
    for games in [3, 5, 7]:
        rolling_col_name = f"AST_LAST_{games}"
        player_data[rolling_col_name] = (
            player_data['AST']
            .groupby(player_data[player_id_col])
            .rolling(window=games, min_periods=1)
            .mean()
            .reset_index(level=0, drop=True)
        )

    for home_away in ['HOME', 'AWAY']:
        avg_column_name = f'PLAYER_{home_away}_AVG_AST'
        player_data[avg_column_name] = player_data.groupby(player_id_col).apply(
            lambda group: group['AST'].where(group['HOME_GAME'] == (1 if home_away == 'HOME' else 0)).expanding().mean()
        ).reset_index(level=0, drop=True)

    return player_data

def add_3PM_features(player_data, player_id_col='PLAYER_ID', date_col='GAME_DATE'):
    # Sort by player and date to ensure rolling works correctly
    player_data = player_data.sort_values([player_id_col, date_col])
    # Add USG_PCT for last 3 and 5 games
    player_data['USG_PCT_LAST_3'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    player_data['USG_PCT_LAST_5'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

    for games in [3, 5, 7]:
        rolling_col_name = f"3PM_LAST_{games}"
        player_data[rolling_col_name] = (
            player_data['FG3M']
            .groupby(player_data[player_id_col])
            .rolling(window=games, min_periods=1)
            .mean()
            .reset_index(level=0, drop=True)
        )

    for home_away in ['HOME', 'AWAY']:
        avg_column_name = f'PLAYER_{home_away}_AVG_3PM'
        player_data[avg_column_name] = player_data.groupby(player_id_col).apply(
            lambda group: group['FG3M'].where(group['HOME_GAME'] == (1 if home_away == 'HOME' else 0)).expanding().mean()
        ).reset_index(level=0, drop=True)

    return player_data

def add_STL_features(player_data, player_id_col='PLAYER_ID', date_col='GAME_DATE'):
    # Sort by player and date to ensure rolling works correctly
    player_data = player_data.sort_values([player_id_col, date_col])
    # Add USG_PCT for last 3 and 5 games
    player_data['USG_PCT_LAST_3'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    player_data['USG_PCT_LAST_5'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

    for games in [3, 5, 7]:
        rolling_col_name = f"STL_LAST_{games}"
        player_data[rolling_col_name] = (
            player_data['STL']
            .groupby(player_data[player_id_col])
            .rolling(window=games, min_periods=1)
            .mean()
            .reset_index(level=0, drop=True)
        )

    for home_away in ['HOME', 'AWAY']:
        avg_column_name = f'PLAYER_{home_away}_AVG_STL'
        player_data[avg_column_name] = player_data.groupby(player_id_col).apply(
            lambda group: group['STL'].where(group['HOME_GAME'] == (1 if home_away == 'HOME' else 0)).expanding().mean()
        ).reset_index(level=0, drop=True)

    return player_data

def add_BLK_features(player_data, player_id_col='PLAYER_ID', date_col='GAME_DATE'):
    # Sort by player and date to ensure rolling works correctly
    player_data = player_data.sort_values([player_id_col, date_col])
    # Add USG_PCT for last 3 and 5 games
    player_data['USG_PCT_LAST_3'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    player_data['USG_PCT_LAST_5'] = player_data.groupby(player_id_col)['USG_PCT'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

    for games in [3, 5, 7]:
        rolling_col_name = f"BLK_LAST_{games}"
        player_data[rolling_col_name] = (
            player_data['BLK']
            .groupby(player_data[player_id_col])
            .rolling(window=games, min_periods=1)
            .mean()
            .reset_index(level=0, drop=True)
        )

    for home_away in ['HOME', 'AWAY']:
        avg_column_name = f'PLAYER_{home_away}_AVG_BLK'
        player_data[avg_column_name] = player_data.groupby(player_id_col).apply(
            lambda group: group['BLK'].where(group['HOME_GAME'] == (1 if home_away == 'HOME' else 0)).expanding().mean()
        ).reset_index(level=0, drop=True)

    return player_data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Get days of rest in between games
def calculate_days_of_rest(df, player_id_col='PLAYER_ID', game_date_col='GAME_DATE'):
    df[game_date_col] = pd.to_datetime(df[game_date_col], format='%Y-%m-%d')
    df = df.sort_values(by=[player_id_col, game_date_col])
    df['DAYS_OF_REST'] = df.groupby(player_id_col)[game_date_col].diff().dt.days
    return df