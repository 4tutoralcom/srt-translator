from asyncio.windows_events import NULL
import os
import re

from translator_options import *
if(dry_run):
    from code.translate import Translate

# Specify input and output Folder
input_folder = "tmp_inputs"
output_folder = "tmp_outputs"

start_input_folder = "inputs"
final_output_folder = "outputs"

# Get All Files in input Folder
dir_path = os.path.dirname(os.path.realpath(__file__))

# Clean out ALL Folder
#folders=[output_folder,input_folder,final_output_folder]
folders=[input_folder,final_output_folder]
for folder in folders:
    files_in_folder = [i for i in os.listdir(dir_path + "/" + folder) if '__init__.py' not in i]
    for each_file in files_in_folder:
        file = dir_path + "\\" + folder + "\\" + each_file
        print(file)
        os.remove(file)


all_input_files = [i for i in os.listdir(dir_path + "/" + start_input_folder) if '__init__.py' not in i]

# Determine which files to translate
if translate_all_files:
    file_list = all_input_files
else:
    file_list = set(all_input_files).intersection(specific_files)



#Split into parts
for each_file in file_list:
    print(each_file)
    line_incrementer=1
    file_part_incrementer=1
    input_file = dir_path + "/" + start_input_folder + "/" + each_file

    with open(input_file, 'r') as data_file:
        split_file = dir_path + "/" + input_folder + "/"+ "_part_" + (str(file_part_incrementer).zfill(padding_fill))+"_" + each_file
        f = open(split_file, "w")
        for line in data_file:
            if(line != "\n"):
                f.write(line)
            else:
                f.write(line)
                line_incrementer+=1
            if (line_incrementer >lines_to_split):
                line_incrementer=0
                file_part_incrementer+=1
                f.close()
                split_file = dir_path + "/" + input_folder + "/"+ "_part_" + (str(file_part_incrementer).zfill(padding_fill))+"_" + each_file
                f = open(split_file, "a")
        f.close()

# Translate all files in file_list
file_list = [i for i in os.listdir(
    dir_path + "/" + input_folder) if '__init__.py' not in i]
if(dry_run):
    for each_file in file_list:
        file_to_translate=dir_path + "/" + input_folder + "/" + each_file
        for each_language in output_languages:
            output_filename=each_file[:each_file.find('.srt')]+'-'+each_language+'.srt'
            file_to_output=dir_path + "/" + output_folder + "/" + output_filename
            results=Translate(input_filepath=file_to_translate,
            output_filepath=file_to_output, in_language=input_language,
            out_language=each_language, dir_path=dir_path)
            # print (results)


# merge parts back together
all_output_files = [i for i in os.listdir(
    dir_path + "/" + output_folder) if '__init__.py' not in i]

for each_file in all_output_files:
    split_file = dir_path + "\\" + output_folder + "\\" + each_file
    final_file_name=re.sub("_part_[0-9]+_","",each_file)
    final_file = dir_path + "\\" + final_output_folder + "\\" + final_file_name
    print(split_file)
    print(final_file)
    fa = open(final_file, "ab")
    with open(split_file, 'rb') as data_file:
        for line in data_file:
            s = line.replace(b"\xef\xbb\xbf", b"")
            fa.write(s)
    
    fa.close()

#Final Cleanup
folders=[start_input_folder]
for folder in folders:
    files_in_folder = [i for i in os.listdir(dir_path + "/" + folder) if '__init__.py' not in i]
    for each_file in files_in_folder:
        file = dir_path + "\\" + folder + "\\" + each_file
        print(file)
        os.remove(file)
