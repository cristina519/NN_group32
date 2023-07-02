import pandas as pd
import glob
import pathlib
import os
import py_midicsv as pm

#Script to convert all .csv files in a folder to MIDI
directoryPath = pathlib.Path(__file__).parent.resolve()
path = os.getcwd()




csv_files = glob.glob(os.path.join(directoryPath, "*.csv"))

for file in csv_files:

    # Parse the CSV output of the previous command back into a MIDI file
    midi_object = pm.csv_to_midi(file)
    file_name = str(file)
    file_name = file_name.replace('.csv', '.mid')
    # Save the parsed MIDI file to disk
    with open(file_name, "wb") as output_file:
        midi_writer = pm.FileWriter(output_file)
        midi_writer.write(midi_object)
