import os
import json
import sys

slash = "/" if os.name != "nt" else "\\"

rootdir = sys.argv[1]

group = sys.argv[2]
group_path = f"{rootdir}{slash}{group}{slash}json"
group_size = len(next(os.walk(group_path))[2])
metadata = []

for i in range(1, group_size+1):
    with open(f"{group_path}{slash}{i}.json") as file:
        metadata.append(json.load(file))

for data in metadata:
    if 'compiler' in data.keys():
        del data['compiler']

    if 'dna' in data.keys():
        del data['dna']

    if 'edition' in data.keys():
        del data['edition']

    if 'date' in data.keys():
        del data['date']

    gender_exists = False
    for traits in data['attributes']:
        if traits['trait_type'] == 'Gender':
            gender_exists = True
            break

    if not gender_exists:
        data['attributes'].append({'trait_type': 'Gender', 'value': f'{group.capitalize()}'})

    title_exists = False
    for traits in data['attributes']:
        if traits['trait_type'] == 'Position Title':
            title_exists = True
            break

    if not title_exists:
        data['attributes'].append({'trait_type': 'Position Title', 'value': 'Coworker'})

    data['image'] = data['image'].replace("ipfs://NewUriToReplace/", "to-be-replaced")

for i in range(1, group_size+1):
    with open(f"{group_path}{slash}{i}.json", "w") as file:
        file.write(json.dumps(metadata[i - 1], indent=2))
        print(f"Finished updating: {group_path}{slash}{i}.json")
