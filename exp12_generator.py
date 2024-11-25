from common.utils import read_json  # Import your utility function
import re

def name_or_var(word, exp):
    if exp==2:
        return word.startswith("{name_") and word.endswith("}") or word.endswith("}’s")
    else:
        return "{" in word and "}" in word and not word.startswith("{name_")

def replace_words(template, original, exp):
    template_words = template.split()
    original_words = original.split()
    if not len(template_words)-len(original_words) == 0:
        raise Exception("template and original need to be same size!")
    
    for i, word in enumerate(template_words):
        if name_or_var(word, exp):
            template_words[i] = original_words[i]  # Replace with the corresponding word from the filled string
    return " ".join(template_words)
    
def replace_either(template, original, exp=1):
    problem = replace_words(template["problem"], original["problem"], exp)
    solution = replace_words(template["solution"], original["solution"], exp)

    return {
        **template,  # Include all unchanged keys
        "problem": problem,
        "solution": solution,
    }

def generate_templates(templates, experiment):
    originals = read_json("data/GSM8K/test_all.json")
    # Create a lookup dictionary for originals
    originals_lookup = {original["id"]: original for original in originals}
    
    new_templates = []
    
    # Iterate through templates and find matching originals by ID
    for template in templates:
        id = template["id"]
        
        # Find the matching original object
        matching_original = originals_lookup.get(id)
        
        if matching_original:
            print(f"Matching original found for ID {id}:")
            #print(matching_original)
            new_templates.append(replace_either(template, matching_original, experiment))
        else:
            print(f"No matching original found for ID {id}")
    
    return new_templates



def compare_temp_or(templates):
    """
    For each template, return a comparison of the problems and solutions, 
    word by word, from the template and the originals.
    """
    # Read the originals from the JSON file
    originals = read_json("data/GSM8K/test_all.json")
    
    # Create a lookup dictionary for originals
    originals_lookup = {original["id"]: original for original in originals}
    
    result = []
    
    # Iterate through templates and find matching originals by ID
    for template in templates:
        id = template["id"]
        
        # Find the matching original object
        matching_original = originals_lookup.get(id)
        
        if matching_original:
            # Split problems and solutions into words
            template_problem_words = template.get("problem", "").split()
            template_solution_words = template.get("solution", "").split()
            original_problem_words = matching_original.get("problem", "").split()
            original_solution_words = matching_original.get("solution", "").split()
            
            print(f"Comparison for Template ID: {id} (Problem)")
            if not len(template_problem_words)-len(original_problem_words) == 0:
                # Compare problems word by word
                
                max_len_prob = max(len(template_problem_words), len(original_problem_words))
                for i in range(max_len_prob):
                    temp_prob_word = template_problem_words[i] if i < len(template_problem_words) else ""
                    orig_prob_word = original_problem_words[i] if i < len(original_problem_words) else ""
                    print(f"{temp_prob_word}, {orig_prob_word}")
            else:
                print("Are the same")
            print("-" * 30)
            
            print(f"Comparison for Template ID: {id} (Solution)")
            if not len(template_solution_words)-len(original_solution_words) == 0:
                # Compare solutions word by word
                #print(f"Comparison for Template ID: {id} (Solution)")
                max_len_sol = max(len(template_solution_words), len(original_solution_words))
                for i in range(max_len_sol):
                    temp_sol_word = template_solution_words[i] if i < len(template_solution_words) else ""
                    orig_sol_word = original_solution_words[i] if i < len(original_solution_words) else ""
                    print(f"{temp_sol_word}, {orig_sol_word}")
            else:
                print("Are the same")
            print("=" * 50)
            
            # Append results to the result list for further processing if needed
            result.append({
                "template_id": id,
                "template_problem_words": template_problem_words,
                "template_solution_words": template_solution_words,
                "original_problem_words": original_problem_words,
                "original_solution_words": original_solution_words,
            })
        else:
            print(f"No matching original found for ID {id}")
    
    return result

def main():
    #print("test")
    # Read JSON files
    templates = read_json("data/GSM-Symbolic/templates/templates_baseline_2.json")
    
    #comparisons = extract_problem_and_solution(templates)
    
    # Extract problems and solutions
    compare_temp_or([templates[6]])
    
    #print(generate_templates(templates, 1))
    
if __name__ == "__main__":
    main()
