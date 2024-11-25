from common.utils import read_json  # Import your utility function
import re

def replace_variables(template, original):
    # Split both strings into words
    template_words = template.split()
    original_words = original.split()
    
    # Replace words in the template
    for i, word in enumerate(template_words):
        # Check if the word contains curly braces and doesn't start with {name_
        if "{" in word and "}" in word and not word.startswith("{name_"):
            template_words[i] = original_words[i]  # Replace with the corresponding word from the filled string
    
    # Join the words back into a single string
    return " ".join(template_words)


def replace_names(template, original):
    
    # Split both strings into words
    template_words = template.split()
    original_words = original.split()
    
    # Replace words in the template
    for i, word in enumerate(template_words):
        #print("----", original_words[i])
        if word.startswith("{name_") and word.endswith("}") or word.endswith("}’s"):  # Check if it's a placeholder
            
            template_words[i] = original_words[i]  # Replace with the corresponding word from the filled string
    
    # Join the words back into a single string
    return " ".join(template_words)

def main():
    # Read JSON files
    templates = read_json("data/GSM-Symbolic/templates/templates_jone.json")
    originals = read_json("data/GSM8K/test_all.json")
    
    # Create a lookup dictionary for originals
    originals_lookup = {original["id"]: original for original in originals}
    
    # Iterate through templates and find matching originals by ID
    for template in templates:
        id = template["id"]
        problem = template["problem"]
        variables = template["variables"]
        conditions = template["conditions"]
        calculations = template["calculations"]
        solution = template["solution"]
        
        # Find the matching original object
        matching_original = originals_lookup.get(id)
        
        if matching_original:
            print(f"Matching original found for ID {id}:")
            #print(matching_original)
        else:
            print(f"No matching original found for ID {id}")
        
        #print(replace_variables(problem, matching_original["problem"]))
    
if __name__ == "__main__":
    main()
