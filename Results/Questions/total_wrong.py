import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to analyze all incorrect cases across baseline and experiments
def analyze_all_incorrect_cases(baseline_path, experiment_paths):
    # Load baseline data
    baseline = pd.read_csv(baseline_path)
    
    # Collect all incorrect cases in the baseline (where correct == False)
    baseline_filtered = baseline[baseline["correct"] == False]
    baseline_details = [(row["problem_id"], "baseline", row["file_name"]) for _, row in baseline_filtered.iterrows()]
    
    # Initialize results dictionary with baseline data
    experiment_results = {
        "baseline": {"count": len(baseline_details), "details": baseline_details}
    }
    
    # Collect all incorrect cases in the experiments
    for i, exp_path in enumerate(experiment_paths, start=1):
        experiment = pd.read_csv(exp_path)
        
        # Ensure all required columns exist
        required_columns = ["problem_id", "variation", "file_name", "correct"]
        for col in required_columns:
            if col not in experiment.columns:
                raise ValueError(f"The file {exp_path} must contain a '{col}' column.")
        
        # Filter rows where correct == False
        experiment_filtered = experiment[experiment["correct"] == False]
        experiment_details = [(row["problem_id"], row["variation"], row["file_name"]) for _, row in experiment_filtered.iterrows()]
        
        # Store the results for this experiment
        experiment_results[f"exp_{i}"] = {"count": len(experiment_details), "details": experiment_details}
    
    return experiment_results

# Function to collect all incorrect cases into a DataFrame
def collect_all_incorrect_results(experiment_results):
    # Gather all unique problem IDs from baseline and experiments
    all_problem_ids = set()
    for exp, result in experiment_results.items():
        all_problem_ids.update([row[0] for row in result["details"]])
    
    problem_data = {"problem_id": sorted(all_problem_ids)}
    
    # Add baseline incorrect counts
    baseline_counts = {row[0]: 0 for row in experiment_results["baseline"]["details"]}
    for detail in experiment_results["baseline"]["details"]:
        baseline_counts[detail[0]] += 1
    problem_data["baseline"] = [baseline_counts.get(pid, 0) for pid in problem_data["problem_id"]]
    
    # Add experiment incorrect counts
    for exp, result in experiment_results.items():
        if exp == "baseline":
            continue
        counts = {row[0]: 0 for row in result["details"]}
        for detail in result["details"]:
            counts[detail[0]] += 1
        problem_data[exp] = [counts.get(pid, 0) for pid in problem_data["problem_id"]]
    
    # Convert to DataFrame
    df = pd.DataFrame(problem_data)
    df.set_index("problem_id", inplace=True)
    df.fillna(0, inplace=True)

    
    # Ensure the DataFrame is sorted by problem_id
    df.sort_index(inplace=True)
    return df

# Function to plot visualizations
def plot_visualizations(df):
    # Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=False, cmap="Reds", cbar=True, linewidths=0.5)
    plt.title("Incorrect Variations Across Baseline and Experiments", fontsize=20)
    plt.ylabel("Problem ID", fontsize=16)
    plt.xlabel("Baseline and Experiments", fontsize=16)
    plt.savefig("/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/total_wrong_var.svg",dpi=300, bbox_inches='tight')
    plt.show()
    

# File paths
baseline_path = "/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/baseline_results.csv"
experiment_paths = [
    "/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/exp_1_results.csv",
    "/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/exp_2_results.csv",
    "/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/exp_3_results.csv",
    "/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/exp_4_results.csv",
    "/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/exp_5_results.csv"
]

# Output path for DataFrame
output_path = "/dtu/blackhole/17/209207/DL_project/rStar/Results/Questions/all_incorrect_results.csv"

# Workflow
experiment_results = analyze_all_incorrect_cases(baseline_path, experiment_paths)
df_all_incorrect = collect_all_incorrect_results(experiment_results)

# Verify results
print(df_all_incorrect.head())

# Save DataFrame
df_all_incorrect.to_csv(output_path)
print(f"Results saved to {output_path}")

# Plot visualizations
plot_visualizations(df_all_incorrect)
