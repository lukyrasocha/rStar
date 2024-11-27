import argparse
import json
import random
import re

def main():
    parser = argparse.ArgumentParser(description="Generate variations for templates.")
    parser.add_argument('--input', type=str, required=True, help="Input JSON template file")
    parser.add_argument('--output', type=str, required=True, help="Output JSON file")
    parser.add_argument('--type', type=str, choices=['name', 'numbers', 'combined', 'irrelevant'], required=True, help="Type of variation: 'name', 'numbers', 'combined', or 'irrelevant'")
    parser.add_argument('--num_variations', type=int, required=True, help="Number of variations per template")

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        templates = json.load(f)

    # Generate variations
    variations = []
    for template in templates:
        num_generated = 0
        attempts = 0
        max_attempts = args.num_variations * 1000
        while num_generated < args.num_variations and attempts < max_attempts:
            variation = generate_variation(template, args.type)
            attempts += 1
            if variation is not None:
                variations.append(variation)
                num_generated += 1
            else:
                pass
        if num_generated < args.num_variations:
            print(f"Only generated {num_generated} variations for template id {template.get('id')} after {attempts} attempts.")

    with open(args.output, 'w') as f:
        json.dump(variations, f, indent=4)

def generate_variation(template, variation_type):
    variation = template.copy()

    numerical_context = {}
    name_context = {}
    if variation_type == 'name':
        # Use default numerical values
        numerical_context = get_numerical_context(variation, default=True)
        if numerical_context is None:
            return None
        # Replace name variables with random names
        name_context = get_name_context(variation, default=False)
        if name_context is None:
            return None
    elif variation_type == 'numbers':
        # Generate random numerical values within ranges
        numerical_context = get_numerical_context(variation, default=False)
        if numerical_context is None:
            return None
        # Use default names
        name_context = get_name_context(variation, default=True)
        if name_context is None:
            return None
    elif variation_type == 'combined':
        # Generate random numerical values within ranges
        numerical_context = get_numerical_context(variation, default=False)
        if numerical_context is None:
            return None
        # Replace name variables with random names
        name_context = get_name_context(variation, default=False)
        if name_context is None:
            return None
    elif variation_type == 'irrelevant':
        # Use default numerical values
        numerical_context = get_numerical_context(variation, default=True)
        if numerical_context is None:
            return None
        # Use default names
        name_context = get_name_context(variation, default=True)
        if name_context is None:
            return None
    else:
        raise ValueError("Invalid variation type")

    context = {}
    context.update(numerical_context)
    context.update(name_context)

    try:
        variation['problem'] = variation['problem'].format(**context)
        variation['solution'] = variation['solution'].format(**context)
    except KeyError as e:
        print(f"Variable {e} not found when formatting")
        return None  

    variation = evaluate_expressions(variation, context)

    # If type is 'irrelevant', insert an irrelevant sentence into the problem
    if variation_type == 'irrelevant':
        variation['problem'] = insert_irrelevant_sentence(variation['problem'])

    if not final_answer_is_integer(variation['solution']):
        return None  # Discard and try again

    variation = {
        "id": variation.get('id'),
        "problem": variation.get('problem'),
        "solution": variation.get('solution')
    }

    return variation

def get_numerical_context(variation, default=False):
    variables = variation.get('variables', {}).get('numerical', {})
    calculations = variation.get('calculations', {})
    conditions = variation.get('conditions', {})

    if default:
        default_values = variation.get('default_values', {})
        assigned_vars = {}
        for var in variables:
            default_var_name = var + '_default'
            if default_var_name in default_values:
                assigned_vars[var] = default_values[default_var_name]
            else:
                print(f"Default value for numerical variable {var} not found")
                return None
        # Use default calculated variables if any
        context = assigned_vars.copy()
        try:
            for var, expr in calculations.items():
                context[var] = eval_expr(expr, context)
        except Exception as e:
            print(f"Error in calculation of {var}: {e}")
            return None
    else:
        # Randomly assign values to numerical variables within their ranges, satisfying conditions
        max_attempts = 1000  # Increase max_attempts to allow more tries
        for attempt in range(max_attempts):
            assigned_vars = {}
            for var, range_ in variables.items():
                if isinstance(range_, list) and len(range_) == 2:
                    low, high = range_
                    if all(isinstance(n, int) for n in range_):
                        assigned_vars[var] = random.randint(low, high)
                    else:
                        assigned_vars[var] = round(random.uniform(low, high), 2)
                else:
                    print(f"Invalid range for variable {var}")
                    return None
            # Compute calculations
            calc_vars = {}
            context = assigned_vars.copy()
            try:
                for var, expr in calculations.items():
                    calc_vars[var] = eval_expr(expr, context)
                    context[var] = calc_vars[var]
            except Exception as e:
                continue  
            # Check conditions
            conditions_met = True
            for var, range_ in conditions.items():
                value = context.get(var)
                if value is None:
                    conditions_met = False
                    break
                if isinstance(range_, list) and len(range_) == 2:
                    if not (range_[0] <= value <= range_[1]):
                        conditions_met = False
                        break
                else:
                    print(f"Invalid condition for variable {var}")
                    conditions_met = False
                    break
            if conditions_met:
                break
        else:
            # Max attempts reached
            return None

        assigned_vars.update(calc_vars)
        context = assigned_vars
    return context

def is_integer(value):
    return isinstance(value, int) or (isinstance(value, float) and value.is_integer())

def eval_expr(expr, context):
    # Evaluate the expression using the context as local variables
    try:
        value = eval(expr, {}, context)
        # If value is float but represents an integer, convert it
        if isinstance(value, float) and value.is_integer():
            value = int(value)
    except Exception as e:
        return None
    return value

def get_name_context(variation, default=False):
    male_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kevin"]
    female_names = ["Mary", "Patricia", "Jennifer", "Elizabeth", "Linda", "Barbara", "Susan", "Margaret", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily", "Donna"]

    # Find all name placeholders in problem and solution
    text = variation.get('problem', '') + ' ' + variation.get('solution', '')
    name_placeholders = re.findall(r"{name_[mf]_\d+}", text)
    name_placeholders = list(set(name_placeholders))  

    name_mapping = {}
    for placeholder in name_placeholders:
        var_name = placeholder.strip('{}')
        if default:
            default_var_name = var_name + '_default'
            default_values = variation.get('default_values', {})
            if default_var_name in default_values:
                name_mapping[var_name] = default_values[default_var_name]
            else:
                print(f"Default value for name variable {var_name} not found")
                return None
        else:
            if placeholder.startswith('{name_m_'):
                name = random.choice(male_names)
            elif placeholder.startswith('{name_f_'):
                name = random.choice(female_names)
            else:
                continue  # not a name placeholder
            name_mapping[var_name] = name

    return name_mapping

def evaluate_expressions(variation, context):
    # Evaluate expressions inside << >> in the solution
    solution = variation['solution']
    # Evaluate expressions inside << >>
    pattern = r'<<([^>]*)>>'
    matches = re.findall(pattern, solution)
    for expr in matches:
        try:
            # Format the expression with context
            expr_formatted = expr.format(**context)
            # If '=' in expr_formatted, split into lhs and rhs
            if '=' in expr_formatted:
                lhs, rhs = expr_formatted.split('=')
                lhs = lhs.strip()
                rhs = rhs.strip()
                # Evaluate lhs using context
                lhs_value = eval(lhs, {}, context)
                # If lhs_value is float but represents an integer, convert it
                if isinstance(lhs_value, float) and lhs_value.is_integer():
                    lhs_value = int(lhs_value)
                evaluated_expr = f"{lhs}={lhs_value}"
            else:
                # No '=', just evaluate the expression
                lhs_value = eval(expr_formatted, {}, context)
                if isinstance(lhs_value, float) and lhs_value.is_integer():
                    lhs_value = int(lhs_value)
                evaluated_expr = str(lhs_value)
        except Exception as e:
            evaluated_expr = expr  # Keep as is

        solution = solution.replace(f"<<{expr}>>", f"<<{evaluated_expr}>>")
    variation['solution'] = solution
    return variation

def final_answer_is_integer(solution_text):
    # Extract the final answer after '####'
    final_answer_match = re.search(r'####\s*(.+)', solution_text)
    if final_answer_match:
        final_answer = final_answer_match.group(1).strip()
        # Remove any non-numeric characters
        final_answer_numeric = re.sub(r'[^\d\.\-]', '', final_answer)
        try:
            value = float(final_answer_numeric)
            return value.is_integer()
        except ValueError:
            return False
    else:
        return False

def insert_irrelevant_sentence(problem_text):
    irrelevant_sentences = [
        "The sun is approximately 149.6 million kilometers away from the Earth.",
        "There are 206 bones in the adult human body.",
        "Mount Everest is 8,848 meters tall.",
        "Light travels at a speed of about 299,792 kilometers per second.",
        "The Great Wall of China is over 21,000 kilometers long.",
        "A year on Mercury lasts 88 Earth days.",
        "The tallest building in the world is 828 meters high.",
        "The Earth's atmosphere is composed of 78% nitrogen.",
        "The average human heart beats about 100,000 times per day.",
        "There are 9.461 trillion kilometers in a light-year.",
        "Water boils at 100 degrees Celsius.",
        "The Pacific Ocean covers about 165 million square kilometers.",
        "The moon is about 384,400 kilometers away from Earth.",
        "There are 365 days in a non-leap year.",
        "The Eiffel Tower is 324 meters tall.",
        "An adult blue whale can weigh up to 150,000 kilograms.",
        "The human eye blinks approximately 4,200,000 times a year.",
        "There are about 7.8 billion people on Earth.",
        "A marathon is 42.195 kilometers long.",
        "The Amazon River is approximately 6,400 kilometers long."
    ]

    sentences = re.split('(?<=[.!?]) +', problem_text)
    # Choose a random position to insert the irrelevant sentence
    insert_position = random.randint(0, len(sentences))
    irrelevant_sentence = random.choice(irrelevant_sentences)
    sentences.insert(insert_position, irrelevant_sentence)
    # Reconstruct the problem text
    new_problem_text = ' '.join(sentences)
    return new_problem_text

if __name__ == "__main__":
    main()