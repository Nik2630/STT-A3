import json
from collections import defaultdict
import sys

def calculate_metrics_from_dict(json_file_path):
    
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}", file=sys.stderr)
        return None

    if not isinstance(data, dict):
        print(f"Error: Expected JSON root to be a dictionary, but got {type(data)}", file=sys.stderr)
        return None

    modules_info = {}
    fan_in = defaultdict(int)
    fan_out = defaultdict(int)
    all_module_names = set(data.keys()) # Get all modules defined in the JSON

    # --- Calculate Fan-Out and gather data for Fan-In calculation ---
    module_imports_map = {} # Store the valid imports for each module

    for module_name, module_data in data.items():
        if not isinstance(module_data, dict):
            print(f"Warning: Skipping invalid data for module '{module_name}'", file=sys.stderr)
            continue

        imports_list = module_data.get('imports', [])
        # Filter out self-imports and ensure imports are strings
        actual_imports = [
            imp for imp in imports_list
            if isinstance(imp, str) and imp != module_name
        ]
        module_imports_map[module_name] = actual_imports
        fan_out[module_name] = len(actual_imports) # Calculate Fan-Out

    # --- Calculate Fan-In robustly based on actual imports ---
    for source_module, imported_modules in module_imports_map.items():
        for imported_module in imported_modules:
            
             if imported_module in all_module_names:
                 fan_in[imported_module] += 1

            # fan_in[imported_module] += 1 # This would include potentially external modules


    # --- Combine results ---
    # Ensure all modules from the input JSON are included, even if they have 0 fan-in/out
    final_metrics = {}
    for module_name in all_module_names:
         final_metrics[module_name] = {
            
            'fan_in': fan_in.get(module_name, 0),
            'fan_out': fan_out.get(module_name, 0)
         }



    return final_metrics

# --- Main Execution ---
if __name__ == "__main__":
    json_input_file = 'flask_deps.json'  
    text_output_file = 'flask_fan_metrics.txt' 

    metrics = calculate_metrics_from_dict(json_input_file)

    if metrics:
        # Sort modules by Fan-In descending for clarity
        sorted_modules = sorted(metrics.items(), key=lambda item: item[1]['fan_in'], reverse=True)

        # Prepare header and lines for output
        header = f"{'Module':<40} | {'Fan-In':<7} | {'Fan-Out':<7}"
        separator = "-" * (40 + 3 + 7 + 3 + 7)
        output_lines = [header, separator]

        for name, data in sorted_modules:
            line = f"{name:<40} | {data['fan_in']:<7} | {data['fan_out']:<7}"
            output_lines.append(line)

        # --- Print to Console ---
        print(f"--- Fan-In/Fan-Out Analysis for {json_input_file} ---")
        for line in output_lines:
            print(line)
        print(f"--- End of Console Output ---")

        # --- Save to File ---
        try:
            with open(text_output_file, 'w') as f:
                f.write(f"Fan-In/Fan-Out Analysis from: {json_input_file}\n")
                f.write("="*len(header) + "\n")
                for line in output_lines:
                    f.write(line + '\n')
            print(f"\nResults also saved to: {text_output_file}")
        except IOError as e:
            print(f"\nError writing output to file {text_output_file}: {e}", file=sys.stderr)

    else:
        print("Could not calculate metrics due to errors.", file=sys.stderr)