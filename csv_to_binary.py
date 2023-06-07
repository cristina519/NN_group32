import pandas as pd
import glob
import pathlib
import os




#Specify the note channel you want to extract
current_drum = ' 47'


#Create binary file from note_hits
def make_binary(df, file_name):
    #Get correct headers from the files
    headers = list(df.columns.values)
    time = headers[1]
    note_on = headers[2]
    velocity = headers[5]
    drum = headers[4]
    
    #Get all the notes that are hit, disregard the rest
    note_hits = df.loc[(df[drum] == current_drum) & 
                 (df[velocity] > 0) & (df[note_on] == ' Note_on_c')]
    #Find max time
    time_out = df[time].max()
    
    txt_file = str(file_name)
    txt_file = txt_file.replace('.csv', '.txt')
    time_count = 0
    
    with open(txt_file, 'w') as f:
        while time_count < time_out:
            #Check if a note is hit in the nearest 120ms interval
            note_check = note_hits[time].between((time_count - 60), (time_count + 60))
            if note_check.any():
                f.write('1')
            else:
                f.write('0')
            time_count += 120
    return

#Get the files
directoryPath = pathlib.Path(__file__).parent.resolve()
path = os.getcwd()

csv_files = glob.glob(os.path.join(directoryPath, "*.csv"))

#Go through files
for file_name in csv_files:
    df = pd.read_csv(file_name, on_bad_lines='skip')
    make_binary(df, file_name)


    
   

  