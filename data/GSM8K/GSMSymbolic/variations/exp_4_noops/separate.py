import json
from collections import defaultdict

# Load the big JSON file
with open('placeholder.json', 'r') as infile:
    data = json.load(infile)

# Group entries by their IDs
grouped_data = defaultdict(list)
for entry in data:
    grouped_data[entry['id']].append(entry)

# Create 5 files and distribute entries
file_contents = [[] for _ in range(5)]

# Distribute each entry cyclically across the 5 files
for id_group in grouped_data.values():
    for i, entry in enumerate(id_group):
        file_contents[i % 5].append(entry)

# Save the data into 5 separate files
for i in range(5):
    filename = f'exp_4_noOps_variation_{i+1}.json'
    with open(filename, 'w') as outfile:
        json.dump(file_contents[i], outfile, indent=4)
    print(f'Saved {len(file_contents[i])} entries to {filename}')
