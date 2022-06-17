import csv
import os
import sys

rootdir = sys.argv[1]
csv_name = sys.argv[2]

slash = "/" if os.name != "nt" else "\\"
rarity_csv = f"{rootdir}{slash}{csv_name}"

input_file = csv.DictReader(open(rarity_csv))

rarity_data = list(input_file)

renaming_info = {}
for row in rarity_data:
    attrs = []
    for key in row:
        if "Rarity" not in key and row[key] != '':
            attrs.append(key)
    for attr in attrs:
        file_end = f"{attr}{slash}{row[attr]}"
        file_rarity = row[f"{attr} Rarity"]
        if '#' not in file_end:
            file_end_list = file_end.split(".")
            renaming_info[file_end] = f"{file_end_list[0]}#{file_rarity}.{file_end_list[1]}"
        else:
            old_rarity = file_end[file_end.find('#') + len('#'):file_end.rfind('.')]
            renaming_info[file_end] = file_end.replace(old_rarity, file_rarity)

for key, value in renaming_info.items():
    print(f"Renaming from {key} -> {value}")
    os.rename(f"{rootdir}{slash}{key}", f"{rootdir}{slash}{value}")