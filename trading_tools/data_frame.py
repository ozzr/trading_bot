
import pandas as pd    

@staticmethod
def load_csv(csv_path)-> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
        df.drop(df.columns[0], axis=1, inplace=True)
        df["time"] = pd.to_datetime(df["time"])
        df.set_index("time", inplace=True)
    except:
        df = pd.read_csv(csv_path, index_col='time', parse_dates=['time'])      

    return df

@staticmethod
def filter_date_range(df:pd.DataFrame, start_datetime, end_datetime):
    """
    ### Filters the DataFrame to the input dates.\n
    **Date Format:** YYYY-MM-DD HH:MM:SS 
    """
    def _dt(date):
        if isinstance(date, str):
            date = pd.to_datetime(date)
        if not isinstance(date, pd.Timestamp):
            print(f"Invalid Date {start_datetime}")
            return None
        return date
    
    
    return df[(df.index >= _dt(start_datetime)) & (df.index <= _dt(end_datetime))]

@staticmethod
def modify_datetime(start_datetime='2024-10-21 06:27:00', seconds_to_add=1, debug:bool = False):
    """
    **start_datetime:** can be either a str formated as YYYY-MM-DD HH:MM:SS or a pd.Timestamp
    """
    if isinstance(start_datetime, str):
        start_datetime = pd.to_datetime(start_datetime)
    if not isinstance(start_datetime, pd.Timestamp):
        print(f"Invalid Date {start_datetime}")
        return None
    
    new_datetime = start_datetime + pd.Timedelta(seconds=seconds_to_add)
    if debug:
        print(new_datetime)
    return new_datetime

@staticmethod
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define lower and upper bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter out rows with values outside the bounds
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df_filtered
@staticmethod
def ensure_time_continuity(df, time_gap='5s'):
    df = df.sort_index()  # Ensure the DataFrame is chronologically ordered
    
    # Calculate the time difference between consecutive rows
    time_diff = df.index.to_series().diff()
    
    # Identify the first valid row where time_diff equals the required time gap
    first_valid_index = (time_diff == pd.Timedelta(time_gap)).idxmax()
    
    if first_valid_index == 0:  # idxmax returns 0 if no valid index is found
        first_valid_index = df.index[0]
    
    # Remove rows before the first valid row
    df = df.loc[first_valid_index:]
    
    return df

@staticmethod
def clean_and_sort(df: pd.DataFrame, columns_to_clean, time_gap='5s'):
    for column in columns_to_clean:
        df = remove_outliers(df, column)
    
    df = ensure_time_continuity(df, time_gap)
    
    # Identify rows with NaN values
    nan_rows = df[df.isna().any(axis=1)]
    
    # Print the number of rows affected and their indices
    print(f'Number of rows affected by NaN values: {nan_rows.shape[0]}')
    print(f'Indices of affected rows: {list(nan_rows.index)}')
    
    if not nan_rows.empty:
        # Remove rows before the highest affected index
        highest_affected_index = nan_rows.index.max()
        df = df.loc[highest_affected_index:]
    
    # Remove rows with NaN values
    df = df.dropna()
    
    return df

@staticmethod
def merge_dataframes(df_new:pd.DataFrame, df_existing:pd.DataFrame = None) -> pd.DataFrame:
    if df_existing is None:
        return df_new
    
    # Check if last date in existing data is contained in new data
    last_date_existing = df_existing.index.max()
    if not last_date_existing in df_new.index:
        return df_new
    
    # Combine and remove duplicates
    df_combined = pd.concat([df_existing, df_new])
    df_combined = df_combined[~df_combined.index.duplicated(keep='last')]
    
    return df_combined

@staticmethod
def resample_candles(df_1s:pd.DataFrame, timeframe_in_s:int):
    resampled = df_1s.resample(f"{timeframe_in_s}s").agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    }).dropna()
    return resampled