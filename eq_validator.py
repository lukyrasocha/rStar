import re

from common.utils import *

def validate_eqs(templates):

    for template in templates:
        
        errors = []
        
        id = template["id"]
        parent_id = template["parent_id"]
        solution = template["solution"]
        equation_pattern = r"<<(.*?)>>"
        equations = re.findall(equation_pattern, solution) # Finding equations
        
        for eq in equations:
            lhs, expected_result = eq.split("=")
            lhs = lhs.strip()
            expected_result = expected_result.strip()
            evaluated_result = eval(lhs)
            
            # Check equation
            if int(expected_result) != evaluated_result:
                print(f"({id}, {parent_id}): Error in equation '{eq}'! Expected: {lhs}={evaluated_result}")
                errors.append([id, parent_id, eq, f"{lhs}={evaluated_result}"])
                
    if errors == []:
        print("No errors found!")

def main():
    templates = read_json("data/GSM8K-Symbolic/variations.json")
    validate_eqs(templates)

if __name__ == "__main__":
    main()