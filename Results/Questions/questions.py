import os
import json
import pandas as pd

# Define the paths
baseline_folder = "/dtu/blackhole/17/209207/DL_project/rStar/run_outputs/GSM8K/Mistral-7B-v0.1/Baseline_Discriminator/results/"
experiments_root = "/dtu/blackhole/17/209207/DL_project/rStar/run_outputs/GSM8K/Mistral-7B-v0.1/ExperimentsDiscriminator/"

# Function to process JSON files in a given folder
def process_experiment(experiment_path, experiment_name):
    experiment_data = []
    for variation_name in os.listdir(experiment_path):
        variation_path = os.path.join(experiment_path, variation_name, "results")  # Add "results" folder
        if os.path.isdir(variation_path):  # Ensure it's a directory
            print(f"Processing variation: {experiment_name}/{variation_name}")
            for filename in os.listdir(variation_path):
                if filename.startswith("problem-") and filename.endswith(".json"):
                    problem_file = os.path.join(variation_path, filename)
                    try:
                        with open(problem_file, 'r') as f:
                            content = json.load(f)
                            experiment_data.append({
                                "experiment": experiment_name,
                                "variation": variation_name,
                                "file_name": os.path.basename(problem_file),
                                "problem_id": content.get("problem_id", None),
                                "file_idx": content.get("file_idx", None),
                                "correct": content.get("correct", None),
                                "correct_majvote": content.get("correct_majvote", None),
                            })
                    except Exception as e:
                        print(f"Error processing {problem_file}: {e}")
    return experiment_data

# Process baseline and save to CSV
if os.path.exists(baseline_folder):
    baseline_data = []
    print(f"Processing baseline folder: {baseline_folder}")
    for filename in os.listdir(baseline_folder):
        if filename.startswith("problem-") and filename.endswith(".json"):
            problem_file = os.path.join(baseline_folder, filename)
            try:
                with open(problem_file, 'r') as f:
                    content = json.load(f)
                    baseline_data.append({
                        "experiment": "Baseline",
                        "variation": "Baseline",
                        "file_name": os.path.basename(problem_file),
                        "problem_id": content.get("problem_id", None),
                        "file_idx": content.get("file_idx", None),
                        "correct": content.get("correct", None),
                        "correct_majvote": content.get("correct_majvote", None),
                    })
            except Exception as e:
                print(f"Error processing {problem_file}: {e}")
    baseline_df = pd.DataFrame(baseline_data)
    baseline_csv = "baseline_results.csv"
    baseline_df.to_csv(baseline_csv, index=False)
    print(f"Baseline data saved to {baseline_csv}")
else:
    print(f"Baseline folder not found: {baseline_folder}")

# Process each experiment separately and save to CSV
if os.path.exists(experiments_root):
    print(f"Processing experiments root folder: {experiments_root}")
    for experiment_name in os.listdir(experiments_root):
        experiment_path = os.path.join(experiments_root, experiment_name)
        if os.path.isdir(experiment_path):  # Ensure it's a directory
            print(f"Processing experiment: {experiment_name}")
            experiment_data = process_experiment(experiment_path, experiment_name)
            experiment_df = pd.DataFrame(experiment_data)
            experiment_csv = f"{experiment_name}_results.csv"
            experiment_df.to_csv(experiment_csv, index=False)
            print(f"Experiment data for {experiment_name} saved to {experiment_csv}")
else:
    print(f"Experiments root folder not found: {experiments_root}")
