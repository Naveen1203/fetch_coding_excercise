import json

def extract_cpg_info(input_file, output_file):
    with open(input_file, 'r') as f_in:
        with open(output_file, 'w') as f_out:
            for line in f_in:
                try:
                    obj = json.loads(line.strip())
                    
                    # Extract cpg id and ref if present
                    if "cpg" in obj and isinstance(obj["cpg"], dict):
                        cpg_info = {}
                        if "$id" in obj["cpg"] and "$oid" in obj["cpg"]["$id"]:
                            cpg_info["cpg_id"] = obj["cpg"]["$id"]["$oid"]
                        if "$ref" in obj["cpg"]:
                            cpg_info["cpg_ref"] = obj["cpg"]["$ref"]
                        
                        # Write the extracted cpg info to the output file
                        if cpg_info:  # Only write if cpg_info is not empty
                            json.dump(cpg_info, f_out)
                            f_out.write('\n')
                
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line.strip()}")

# Example usage
input_file = 'brands.json'   # Replace with your input file path
output_file = 'output_cpg.json' # Replace with desired output file path

# Clear existing content of output file if it exists
open(output_file, 'w').close()

extract_cpg_info(input_file, output_file)
