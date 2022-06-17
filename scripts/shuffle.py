import os
import random
import sys
import shutil
import json

rootdir = sys.argv[1]
slash = "/" if os.name != "nt" else "\\"

groups = {"male": [], "female": [], "legendary": []}
total_assets = 0

for group, _ in groups.items():
    group_path = f"{rootdir}{slash}{group}{slash}json{slash}"
    group_size = len(next(os.walk(group_path))[2])
    groups[group] = group_size

    total_assets += group_size
    groups[group] = [i for i in range(1, group_size + 1)]


def get_random_group_asset():
    random_group_idx = random.randint(0, len(groups.keys())-1)
    random_group = list(groups.keys())[random_group_idx]

    if len(groups[random_group]) > 0:
        random_asset_idx = random.randint(0, len(groups[random_group]) - 1)
        print(random_asset_idx, random_group, groups[random_group])
        chosen_asset = groups[random_group][random_asset_idx]
        groups[random_group].pop(random_asset_idx)
        return random_group, chosen_asset
    else:
        return get_random_group_asset()


final_location = f"{rootdir}{slash}final"
for i in range(1, total_assets + 1):
    assigned_group, assigned_asset_idx = get_random_group_asset()

    to_image_dest = f"{final_location}{slash}images{slash}{i}.png"
    from_image_dest = f"{rootdir}{slash}{assigned_group}{slash}images{slash}{assigned_asset_idx}.png"

    to_metadata_dest = f"{final_location}{slash}metadata{slash}{i}.json"
    from_metadata_dest = f"{rootdir}{slash}{assigned_group}{slash}json{slash}{assigned_asset_idx}.json"

    shutil.copy(from_image_dest, to_image_dest)
    shutil.copy(from_metadata_dest, to_metadata_dest)
    print(f"Copied from {assigned_group} #{assigned_asset_idx} to {i} in final location")

    with open(to_metadata_dest, "r") as file:
        metadata = json.load(file)

    metadata['image'] = metadata['image'].replace(str(assigned_asset_idx), str(i))

    with open(to_metadata_dest, "w") as file:
        file.write(json.dumps(metadata, indent=2))
