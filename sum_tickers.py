# import modules

import os
import glob
from pathlib import Path

# import from .py file
from fetch_data import raw_path

# set vars for data paths
sum_path = "sum_tickers/"

# create folder for summed tickers
if Path(sum_path).exists != True:
    try:
        os.makedirs(sum_path, exist_ok = True)
        print(f"Summed tickers will be saved to '{sum_path}' directory\n")
    except OSError as error:
        print(f"ERROR, '{sum_path}' not created\n")

# save all raw filenames to var
file_names = os.listdir(path = raw_path)

# in each text file, sum ticker
for text_file in file_names:
    with open(raw_path + text_file, "r") as f:
        data = f.readlines()
    f.close()
    # pop trailer to var
    # SAVE THIS TO SEPARATE FILE
    # CREATE FOLDER CONTAINING SUMMED TICKER WITH ITS TRAILER
    trailer = []
    while "Trailer" in data[-1]:
        add_to_trailer = data.pop(-1)
        trailer.append(add_to_trailer)
    # keep only "SYMBOL|QUANTITY|PRICE"
    new_data = []
    for line in data:
        try: 
            new_line = line.split("|")[2] + "|" + line.split("|")[3] + "|" + line.split("|")[4] + "|" + line.split("|")[5]
        except Exception as e:
            print(e)
            print(text_file)
            print(data.index(line))
            print(line)
        new_data.append(new_line)
    # remove header -> sort -> add header
    list_header = new_data.pop(0)
    new_data.sort()
    new_data.insert(0, list_header)
    # save data - filename as the date
    if "cnsfails" in text_file:
        text_file = text_file.replace("cnsfails", "")
    elif "cnsfail" in text_file:
        text_file = text_file.replace("cnsfail", "")
    with open(sum_path + text_file, "w") as f:
        f.writelines(new_data)
    f.close()