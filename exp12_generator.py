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

def main():
    # Read JSON files
    templates = read_json("data/GSM-Symbolic/templates/templates_jone.json")
    
    print(generate_templates(templates, 1))
    
if __name__ == "__main__":
    main()
