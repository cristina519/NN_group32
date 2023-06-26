import pandas as pd
import glob
import pathlib
import os
import py_midicsv as pm


most_used_drums = {
    0 : ' 42',
    1 : ' 38',
    2 : ' 36',
    3 : ' 37',
    4 : ' 46',
    5 : ' 51',
    6 : ' 54',
    7 : ' 44' 
    }
#Get the binary txt files (or some other format to be determined)
directoryPath = pathlib.Path(__file__).parent.resolve()
path = os.getcwd()

txt_files = glob.glob(os.path.join(directoryPath, "*.txt"))

for file_name in txt_files:
    file = open (file_name, 'r')
    working_file_name = str(file_name)
    working_file_name = working_file_name.replace('.txt', '.csv')


    with open(working_file_name, 'w') as f:
        f.write("0, 0, Header, 0, 1, 480\n")
        f.write("1, 0, Start_track\n")

    
        binary_data = file.read() #Returns big string
        print(binary_data)
        size = len(binary_data)
        print(size)
        print(binary_data[0])
        print(binary_data[1])
        print(binary_data[2])
        print(binary_data[3])
        print(binary_data[4])
        print(binary_data[5])
        x = 0
        time = 0
        flag0 = 0
        flag1 = 0
        flag2 = 0
        flag3 = 0
        flag4 = 0
        flag5 = 0
        flag6 = 0
        flag7 = 0
        while x < (size - 7):
            if binary_data[x] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[0] + ', 100\n')
                flag0 = 1
                #do thing 
            elif binary_data[x+1] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[1] + ', 100\n')
                flag1 = 1
                #do other thing
            elif binary_data[x+2] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[2] + ', 100\n')
                flag2 = 1
                #do other thing
            elif binary_data[x + 3] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[3] + ', 100\n')
                flag3 = 1
                #do other thing
            elif binary_data[x+4] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[4] + ', 100\n')
                flag4 = 1
                #do other thing
            elif binary_data[x+5] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[5] + ', 100\n')
                flag5 = 1
                #do other thing
            elif binary_data[x+6] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[6] + ', 100\n')
                flag6 = 1
                #do other thing
            elif binary_data[x+7] == '1':
                f.write('1,' + str(time) + ', Note_on_c, 0,' + most_used_drums[7] + ', 100\n')
                flag7 = 1
                #do other thing
            
            
            if flag0:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[0] + ', 0\n')
                flag0 = 0
                #do thing 
            if flag1:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[1] + ', 0\n')
                flag1 = 0
                #do other thing
            if flag2:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[2] + ', 0\n')
                flag2 = 0
                #do other thing
            if flag3:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[3] + ', 0\n')
                flag3 = 0
                #do other thing
            if flag4:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[4] + ', 0\n')
                flag4 = 0
                #do other thing
            if flag5:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[5] + ', 0\n')
                flag5 = 0
                #do other thing
            if flag6:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[6] + ', 0\n')
                flag6 = 0
                #do other thing
            elif flag7:
                f.write('1,' + str(time+60) + ', Note_off_c, 0,' + most_used_drums[7] + ', 0\n')
                flag7 = 0
                #do other thing
            x += 8
            time += 120
        time = time - 120
        f.write("1," + str(time)+ ', End_track\n')
        f.write("0,0,End_of_file")




#Do the csv to midi conversion typathing
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
