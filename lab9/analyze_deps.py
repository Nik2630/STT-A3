import json
from collections import defaultdict
import sys

# --- Configuration ---
JSON_INPUT_FILE = 'flask_deps.json'
ANALYSIS_OUTPUT_FILE = 'flask_dependency_analysis.txt'
HIGH_COUPLING_THRESHOLD_FAN_IN = 7  
HIGH_COUPLING_THRESHOLD_FAN_OUT = 7 
# potential primary entry points for reachability analysis
ENTRY_POINTS = ['__main__', 'flask']

# --- Helper Functions ---

def load_json_data(filepath):
  
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(f"Error: Expected JSON root to be a dictionary, but got {type(data)}", file=sys.stderr)
            return None
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}", file=sys.stderr)
        return None

def build_graph(dep_data):
   
    graph = defaultdict(list)
    all_nodes = set(dep_data.keys())
    for module_name, module_info in dep_data.items():
        if isinstance(module_info, dict):
            imports = module_info.get('imports', [])
            for imp in imports:
                # Only add edges to modules that are part of our analysis scope
                # and avoid self-loops in the graph representation for traversal
                if imp in all_nodes and imp != module_name:
                    graph[module_name].append(imp)
    return graph, all_nodes

def calculate_fan_metrics(dep_data, graph, all_nodes):
    
    fan_in = defaultdict(int)
    fan_out = defaultdict(int)

    # Calculate Fan-Out based on the graph (imports within the analyzed scope)
    for module_name, imports in graph.items():
        fan_out[module_name] = len(imports)

    # Calculate Fan-In by checking who imports whom
    for source_module, imported_modules in graph.items():
        for imported_module in imported_modules:
             # Check if imported_module is part of the analysis
             if imported_module in all_nodes:
                fan_in[imported_module] += 1

    # Ensure all modules have an entry, even if 0
    metrics = {}
    for node in all_nodes:
        metrics[node] = {
            'fan_in': fan_in.get(node, 0),
            'fan_out': fan_out.get(node, 0)
        }
    return metrics

def detect_cycles(graph, all_nodes):
    
    path = set()  # Nodes currently in the recursion stack (visiting)
    visited = set() # Nodes whose subtree has been fully explored
    cycles = []

    # Sort nodes for deterministic cycle finding (optional)
    sorted_nodes = sorted(list(all_nodes))

    for node in sorted_nodes:
        if node not in visited:
            stack = [(node, iter(graph.get(node, [])))] # Store node and iterator over its neighbors
            path.add(node)
            path_list = [node] # Keep track of the actual path taken

            while stack:
                parent, children = stack[-1]

                try:
                    child = next(children)

                    if child in path: # Cycle detected!
                        cycle_path = path_list[path_list.index(child):] + [child]
                        # Store cycles uniquely (sort nodes within cycle)
                        sorted_cycle = tuple(sorted(cycle_path[:-1])) # Use the nodes, ignore repeat
                        if sorted_cycle not in [tuple(sorted(c[:-1])) for c in cycles]:
                             cycles.append(cycle_path)
                        # Continue search from this point to find other cycles

                    elif child not in visited:
                        path.add(child)
                        path_list.append(child)
                        stack.append((child, iter(graph.get(child, []))))

                except StopIteration: # Finished exploring children of 'parent'
                    path.remove(parent)
                    visited.add(parent)
                    path_list.pop()
                    stack.pop()

    return cycles


def find_reachable(graph, entry_points, all_nodes):
    
    reachable = set()
    queue = collections.deque()

    # Initialize queue with valid entry points that exist in our graph
    for point in entry_points:
        if point in all_nodes:
            if point not in reachable:
                reachable.add(point)
                queue.append(point)

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)

    return reachable

# --- Main Analysis Function ---

def analyze_dependencies(dep_data):
    
    if not dep_data:
        return "Error: No dependency data provided."

    graph, all_nodes = build_graph(dep_data)
    metrics = calculate_fan_metrics(dep_data, graph, all_nodes)
    cycles = detect_cycles(graph, all_nodes)
    reachable_nodes = find_reachable(graph, ENTRY_POINTS, all_nodes)

    analysis_results = []
    analysis_results.append("--- Dependency Analysis Report ---")
    analysis_results.append(f"Total modules analyzed: {len(all_nodes)}")
    analysis_results.append("-" * 30)

    # 1. Highly Coupled Modules
    analysis_results.append("[Highly Coupled Modules]")
    high_fan_in = {m: d['fan_in'] for m, d in metrics.items() if d['fan_in'] >= HIGH_COUPLING_THRESHOLD_FAN_IN}
    high_fan_out = {m: d['fan_out'] for m, d in metrics.items() if d['fan_out'] >= HIGH_COUPLING_THRESHOLD_FAN_OUT}

    if high_fan_in:
        analysis_results.append(f"Modules with High Fan-In (>= {HIGH_COUPLING_THRESHOLD_FAN_IN}):")
        for mod, count in sorted(high_fan_in.items(), key=lambda item: item[1], reverse=True):
            analysis_results.append(f"  - {mod} (Fan-In: {count})")

    else:
        analysis_results.append(f"No modules found with Fan-In >= {HIGH_COUPLING_THRESHOLD_FAN_IN}.")

    if high_fan_out:
        analysis_results.append(f"\nModules with High Fan-Out (>= {HIGH_COUPLING_THRESHOLD_FAN_OUT}):")
        for mod, count in sorted(high_fan_out.items(), key=lambda item: item[1], reverse=True):
            analysis_results.append(f"  - {mod} (Fan-Out: {count})")
    else:
        analysis_results.append(f"No modules found with Fan-Out >= {HIGH_COUPLING_THRESHOLD_FAN_OUT}.")
    analysis_results.append("-" * 30)

    # 2. Cyclic Dependencies
    analysis_results.append("[Cyclic Dependencies]")
    if cycles:
        analysis_results.append(f"Found {len(cycles)} cycle(s):")
        for i, cycle in enumerate(cycles):
            analysis_results.append(f"  Cycle {i+1}: {' -> '.join(cycle)}")
    else:
        analysis_results.append("No cyclic dependencies detected.")
    analysis_results.append("-" * 30)

    # 3. Unused Modules (Zero Fan-In)
    analysis_results.append("[Potentially Unused Modules (Zero Fan-In)]")
    zero_fan_in_modules = [m for m, d in metrics.items() if d['fan_in'] == 0]
    if zero_fan_in_modules:
        analysis_results.append("Modules with Fan-In = 0:")
        # Filter out typical entry points if desired, but list them for completeness
        
        for mod in sorted(zero_fan_in_modules):
             analysis_results.append(f"  - {mod}")        

    else:
        analysis_results.append("No modules found with zero Fan-In (within the analyzed scope).")
    analysis_results.append("-" * 30)

    # 4. Disconnected Modules (Not reachable from entry points)
    analysis_results.append("[Potentially Disconnected Modules]")
    all_analyzed_nodes = set(metrics.keys()) # Use keys from metrics to ensure we only consider analyzed modules
    unreachable_nodes = all_analyzed_nodes - reachable_nodes
    if unreachable_nodes:
        analysis_results.append(f"Modules not reachable from entry points {ENTRY_POINTS}:")
        for mod in sorted(list(unreachable_nodes)):
             analysis_results.append(f"  - {mod}")
    else:
        analysis_results.append(f"All analyzed modules appear reachable from entry points: {ENTRY_POINTS}.")
    analysis_results.append("-" * 30)

    # 5. Dependency Depth (ignoring cycles)
    analysis_results.append("[Dependency Depth]")
    depth = {}
    for node in all_nodes:
        depth[node] = 0
        visited = set()
        stack = [(node, 0)]
        while stack:
            current, d = stack.pop()
            if current not in visited:
                visited.add(current)
                depth[node] = max(depth[node], d)
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        stack.append((neighbor, d + 1))
    analysis_results.append("Maximum dependency depth for each module:")
    for mod in sorted(depth.keys()):
        analysis_results.append(f"  - {mod}: {depth[mod]}")
    analysis_results.append("-" * 30)
    analysis_results.append("End of Analysis Report")

    return "\n".join(analysis_results)

# --- Main Execution ---
if __name__ == "__main__":
    import collections # Make sure deque is available

    print(f"Loading dependency data from: {JSON_INPUT_FILE}")
    dependency_data = load_json_data(JSON_INPUT_FILE)

    if dependency_data:
        print("Performing dependency analysis...")
        analysis_report = analyze_dependencies(dependency_data)

        # Print report to console
        print("\n" + analysis_report)

        # Save report to file
        try:
            with open(ANALYSIS_OUTPUT_FILE, 'w') as f:
                f.write(analysis_report)
            print(f"\nAnalysis report saved to: {ANALYSIS_OUTPUT_FILE}")
        except IOError as e:
            print(f"\nError writing analysis report to file {ANALYSIS_OUTPUT_FILE}: {e}", file=sys.stderr)
    else:
        print("Analysis aborted due to errors loading data.", file=sys.stderr)