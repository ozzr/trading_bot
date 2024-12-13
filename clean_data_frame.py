import pandas as pd
import numpy as np

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

def clean_and_sort_dataframe(df: pd.DataFrame, columns_to_clean, time_gap='5s'):
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


if __name__ == "__main__":
    import utils
    ASSET = "AUDCAD_otc" 
    df = utils.load_dataset(f"actives/ACTIVO-{ASSET}-0005s.csv")
    print(f"DF size before cleanup: {len(df)}")
    df = clean_and_sort_dataframe(df, df.columns)
    print(f"DF size after cleanup: {len(df)}")
    df.to_csv("df_cleaned.csv")