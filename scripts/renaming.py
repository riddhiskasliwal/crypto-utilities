import os
import sys

rootdir = sys.argv[1]
to_replace = " "
from_replace = "-"

slash = "/" if os.name != "nt" else "\\"

for root, subFolders, files in os.walk(rootdir):
    if len(files) > 0:
        for file in files:
            if from_replace in file:
                new_filename = file.replace(from_replace, to_replace)
                os.rename(root+slash+file, root+slash+new_filename)
                print(f"Renamed from {file} -> {new_filename}")

