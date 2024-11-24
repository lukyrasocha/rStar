from common.utils import *

# Convert dict floats to ints
def convert_all_to_int(data):
    return {key: int(value) if isinstance(value, float) else value for key, value in data.items()}

# Resolve calculations
def resolve_calculations(variables, calculations):
    # Initialize storage for results and context for evaluation
    resolved_values = {}
    context = variables.copy()  # Start with the given variables

    for key, expression in calculations.items():
        try:
            # Evaluate the expression using the current context
            resolved_values[key] = eval(expression, {}, context)
            
            # Add the result to the context for future calculations
            context[key] = resolved_values[key]
        except Exception as e:
            print(f"Error resolving calculation {key}: {expression} -> {e}")
            resolved_values[key] = None

    return resolved_values

# Validates the conditions
# Validates the conditions
def validate_conditions(resolved_calculations, conditions):
    for key, condition in conditions.items():
        value = resolved_calculations.get(key)

        # Ensure the value exists and is either an integer or a float equivalent to an integer
        if value is None or not (isinstance(value, int) or (isinstance(value, float) and value.is_integer())):
            return False

        # Check numerical range if it's a list [min, max]
        if isinstance(condition, list):
            if not (condition[0] <= value <= condition[1]):
                return False
        else:
            print(f"No interval given for {condition}")
    return True

def generate_variation(template, variation_id, parent_id):
    variables = template["variables"]
    numerical = variables.get("numerical", {})
    conditions = template.get("conditions", {})
    
    while True:  # Retry until conditions are met
        current_vars = {}

        # Randomly assign values to numerical variables
        for var, range_ in numerical.items():
            if isinstance(range_, list):
                if len(range_) == 3:
                    # Range with step size
                    start, stop, step = range_
                    possible_values = list(range(start, stop + 1, step))
                    current_vars[var] = random.choice(possible_values)
                else:
                    # Simple range
                    current_vars[var] = random.randint(*range_)
            else:
                # Single value
                current_vars[var] = range_

        # Randomly assign values to list variables
        for var, values in variables.items():
            if var != "numerical":
                current_vars[var] = random.choice(values)

        # Resolve calculations
        resolved_calculations = resolve_calculations(current_vars, template.get("calculations", {}))

        # Merge calculations into variables for formatting
        current_vars.update(resolved_calculations)

        #print("="*50)
        #print(current_vars)
        #print("="*50)

        # Validate conditions
        if validate_conditions(current_vars, conditions):
            break  # Exit loop if conditions are met


    # Fill the problem and solution templates
    problem = template["problem"].format(**convert_all_to_int(current_vars))
    solution = template["solution"].format(**convert_all_to_int(current_vars))

    return {
        "id": variation_id,
        "parent_id": parent_id,
        "problem": problem,
        "solution": solution
    }

# Generate multiple variations for multiple templates
def generate_variations_for_templates(templates, n_per_template, starting_id=0):
    variations = []
    current_id = starting_id

    for template in templates:
        parent_id = template["id"]
        for _ in range(n_per_template):
            variation = generate_variation(template, current_id, parent_id)
            variations.append(variation)
            current_id += 1

    return variations

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate variations for GSM-Symbolic")
    parser.add_argument(
        "--templates", 
        type=str, 
        required=True,
        help="Filename of the templates (without extension, should be in the 'data/GSM-Symbolic/templates' folder)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        required=True, 
        help="Output filename (without extension, outputs into the 'data/GSM-Symbolic/variations/' folder)"
    )
    parser.add_argument(
        "--n_per_template", 
        type=int, 
        default=2, 
        help="Number of variations per template"
    )

    args = parser.parse_args()
    
    templates = read_json(f"data/GSM-Symbolic/templates/{args.templates}.json")
    # Generate variations
    variations = generate_variations_for_templates(templates, args.n_per_template)

    # Save to JSON file
    output_filename = f"data/GSM-Symbolic/variations/{args.output}.json"

    with open(output_filename, "w") as file:
        json.dump(variations, file, indent=4)

    print(f"Generated {len(variations)} variations across {len(templates)} templates and saved to '{output_filename}'.")


if __name__ == "__main__":
    main()