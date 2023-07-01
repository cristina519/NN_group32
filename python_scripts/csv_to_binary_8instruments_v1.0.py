import pandas as pd
import glob
import pathlib
import os
import py_midicsv as pm




#Create binary file from note_hits
def make_binary(df, file_name):
    #Get correct headers from the files
    headers = list(df.columns.values)
    time = headers[1]
    note_on = headers[2]
    velocity = headers[5]
    drum = headers[4]
    
    #get the most used drum for every file independantly!
    used_drums = df[drum].value_counts().nlargest(8)
    f_drum = list(used_drums.index)

    note_hits = pd.DataFrame()
    #Make loop to get all most used drums
    for idx in range(len(f_drum)):
        hits_drum_idx = df.loc[(df[drum] == f_drum[idx]) & 
                 (df[velocity] > 0) & (df[note_on] == ' Note_on_c')]
        note_hits = pd.concat([note_hits, hits_drum_idx])

    #Make all lists 8 long
    while len(f_drum) != 8:
        f_drum.append('0')

    #Find max time
    time_out = df[time].max()
    
    txt_file = str(file_name)
    txt_file = txt_file.replace('.csv', '.txt')
    time_count = 0
    
    with open(txt_file, 'w') as f:
        while time_count < time_out:
            #Check if a note is hit in the nearest 120ms interval
            note_check = note_hits[note_hits[time].between((time_count - 60), (time_count + 60))]

            for idx in range(8):
                if f_drum[idx] in note_check[drum].values:
                    f.write('1')
                else:
                    f.write('0')
            
            f.write(" ")

            time_count += 120
    return

#Get the files
directoryPath = pathlib.Path(__file__).parent.resolve()
path = os.getcwd()



#Midi gathering stuff (commented out because not neccesairy)
'''
midi_types = ('*.mid', '*.midi')
midi_files = []
for types in midi_types:
    midi_files.extend(glob.glob(os.path.join(directoryPath, types)))

#Create csv files:
for file_name in midi_files:
    current_file = str(file_name)
    if current_file.find('.midi'):
        current_file = current_file.replace('.midi', '.csv')
    else:
        current_file = current_file.replace('.mid', '.csv')
    csv_write = pm.midi_to_csv(file_name)
    with open(current_file, 'w') as f:
        f.writelines(csv_write)

'''
csv_files = glob.glob(os.path.join(directoryPath, "*.csv"))
data = pd.DataFrame()


#Go through files
for file_name in csv_files:
    df = pd.read_csv(file_name, on_bad_lines='skip')
    make_binary(df, file_name)

   

  