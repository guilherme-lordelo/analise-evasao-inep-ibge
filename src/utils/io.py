import pandas as pd

def read_csv(path, **kwargs):
    return pd.read_csv(path, **kwargs)

def write_csv(df, path, **kwargs):
    df.to_csv(path, index=False, **kwargs)
