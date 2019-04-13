# Builtin imports
import csv
import os
import json

DATA_DIR = 'raw'
OUT_DIR = 'dist'

# Read the CSV files and merge them into one large file

years = {}

# Read the location data in
for data_file in os.listdir(DATA_DIR):
    if data_file.endswith('csv'):
        reader = csv.reader(open(os.path.join(DATA_DIR, data_file), encoding='utf-8'))
        for line in list(reader)[1:]:
            year = int(line[0])
            location = line[1]
            if year not in years.keys():
                years.update({year: []})
            years[year].append(location)

# Export the data out to a JSON file

out_file = os.path.join(OUT_DIR, 'data.json')

with open(out_file, 'w') as out:
    out.write(json.dumps(years, indent=4))