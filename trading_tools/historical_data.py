import os
import pandas as pd
import time
from trading_tools.data_frame import resample_candles
from pocket_option_tools.platforms.pocketoption.stable_api import PocketOption


@staticmethod
def download_asset_history(asset:str, api: PocketOption, period=1) -> pd.DataFrame:  
    df = api.get_candles(asset, period=period, count=9000, count_request=100)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)    
    return df

@staticmethod  
def _merge_and_save(df_new, save_path):
    try:
        if os.path.exists(save_path):  
            df_existing = pd.read_csv(save_path, index_col='time', parse_dates=['time'])
            # Check if last date in existing data is contained in new data
            last_date_existing = df_existing.index.max()
            if last_date_existing in df_new.index:
                # Combine and remove duplicates
                df_combined = pd.concat([df_existing, df_new])
                df_combined = df_combined[~df_combined.index.duplicated(keep='last')]
                df_combined.to_csv(save_path)
            else:
                print("Discarding old dataframe.")
                # Save the existing file with -old suffix and override with new data
                os.rename(save_path, save_path.replace('.csv', '-old.csv'))
                df_new.to_csv(save_path)
        else:
            # Save new data if file does not exist
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df_new.to_csv(save_path)
    except Exception as ex:
        print("Unexpexted Error: ", ex)
        
@staticmethod   
def download_assets_history(assets:list, api: PocketOption, resample_timestamps_in_seconds:list = [5,15,30,60,120,300], start_at_index:int = 0) -> None:  
    
    for index, asset in enumerate(assets):
        print(f"[{asset}] - progress: {index + 1} / {len(assets)}")
        if index < start_at_index:
            continue
        
        df_path=f"actives/ACTIVO-{asset}-0001s.csv"
        
        df:pd.DataFrame = download_asset_history(asset, api, period=1)
        _merge_and_save(df, df_path)

        for v in resample_timestamps_in_seconds:
            _merge_and_save(resample_candles(df, v), f"actives/ACTIVO-{asset}-{str(v).zfill(4)}s.csv")
            
        time.sleep(2)
   
