import joblib
import pandas as pd

class DFScaler():
    def __init__(self, mean, std):
        self.mean  =  mean
        self.std = std
    def transform(self, df):
        return (df - self.mean) / self.std
    
    def inv_transform(self, df):
        return df * self.std + self.mean


@staticmethod
def dump_scaler(scaler:DFScaler, path:str = None):
        if path is None:
            print("Cannot dump DFScaler data to invalid path")
        joblib.dump(scaler, path)
@staticmethod        
def load_scaler(path:str = None) -> DFScaler:
        if path is None:
            print("Cannot load data from an invalid path")
        return joblib.load(path)
    
    