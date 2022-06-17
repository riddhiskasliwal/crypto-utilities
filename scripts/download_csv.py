import os
import sys

rootdir = sys.argv[1]
slash = "/" if os.name != "nt" else "\\"

attributes = {}
max_len = 0

for root, _, files in os.walk(rootdir):
    if len(files) > 0:
        root_list = root.split(slash)
        attribute = root_list[-1]
        attributes[attribute] = files
        if max_len < len(files):
            max_len = len(files)

if '' in attributes.keys():
    del attributes['']

for attribute, types in attributes.items():
    if len(types) < max_len:
        for i in range(max_len-len(types)):
            attributes[attribute].append("")

rows = []
header_row = []
for attribute, _ in attributes.items():
    header_row.append(attribute)
    header_row.append(f"{attribute} Rarity")

rows.append(header_row)
for idx in range(0, max_len):
    row = []
    for k in attributes.keys():
        trait = attributes[k][idx]
        if '#' in trait:
            rarity = trait[trait.find('#')+len('#'):trait.rfind('.')]
        else:
            rarity = "0"
        row.append(trait)
        row.append(rarity)
    rows.append(row)

with open(f"{rootdir}{slash}rarity.csv", "w") as file:
    for row in rows:
        record = ",".join(row)
        file.write(f"{record}\n")

