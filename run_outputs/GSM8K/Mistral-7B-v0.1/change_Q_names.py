import os
import re
import shutil


source_folder = 'run_outputs/GSM8K/Mistral-7B-v0.1/2024-11-16_22-43-39---[default]/answer_sheets'
destination_folder = 'run_outputs/GSM8K/Mistral-7B-v0.1/2024-11-16_22-43-39---[default]/renamed_answer_sheets'

os.makedirs(destination_folder, exist_ok=True)

# Loop through each file in the source folder
for filename in os.listdir(source_folder):
    
    match = re.match(r'Question (\d{4}) - (.+)', filename)
    if match:
        current_index = int(match.group(1))  
        new_index = current_index + 30      # Instead of 30, you put the number of the first id of the set of questions
        new_filename = f'Question {new_index:04d} - {match.group(2)}'  

        
        old_file_path = os.path.join(source_folder, filename)
        new_file_path = os.path.join(destination_folder, new_filename)

    
        shutil.move(old_file_path, new_file_path)

print("Renaming and moving completed.")
