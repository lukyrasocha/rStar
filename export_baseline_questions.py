# questions: 314, 741, 65, 3
#⁠104, 32, 1145, 424
#⁠550, 117, 249, 1235
#⁠835, 170, 1244, 27
#⁠1180, 376, 1254, 367

# i need to extract from the following .json file the following index questions and save them into a new .json file called baseline 


import json
import os

path_to_json = '/dtu/blackhole/17/209207/DL_project/rStar/data/GSM8K/test_all.json'

with open(path_to_json) as f:
    data = json.load(f)


indices = [314, 741, 65, 3, 104, 32, 1145, 424, 550, 117, 249, 1235, 835, 170, 1244, 27, 1180, 376, 1254, 367]

sort_indices = sorted(indices)

new_data = []

for i in sort_indices:
    new_data.append(data[i])

with open('baseline.json', 'w') as f:
    json.dump(new_data, f)
    os.makedirs('/dtu/blackhole/17/209207/DL_project/rStar/data/GSM8K/Baseline', exist_ok=True)

print('done')

# the new file is saved in the data/GSM8K folder and is called baseline.json


