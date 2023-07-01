import pandas as pd
import glob
import pathlib
import os
import py_midicsv as pm

directoryPath = pathlib.Path(__file__).parent.resolve()
path = os.getcwd()

csv_files = glob.glob(os.path.join(directoryPath, "*.csv"))


def get_drums(df):
    #Get correct headers from the files
    headers = list(df.columns.values)

    drum = headers[4]
    
    used_drums = df[drum].value_counts().nlargest(8)

    print(used_drums)
    return

for file_name in csv_files:
    df = pd.read_csv(file_name, on_bad_lines='skip')
    get_drums(df)
