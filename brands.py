import json

def preprocess_json(input_file, output_file):
    with open(input_file, 'r') as f_in:
        for line in f_in:
            try:
                obj = json.loads(line.strip())
                
                # Process _id field if it contains $oid
                if "_id" in obj and isinstance(obj["_id"], dict) and "$oid" in obj["_id"]:
                    obj["_id"] = obj["_id"]["$oid"]
                
                # Process cpg field if it contains $id
                if "cpg" in obj and isinstance(obj["cpg"], dict) and "$id" in obj["cpg"]:
                    if "$oid" in obj["cpg"]["$id"]:
                        obj["cpg_id"] = obj["cpg"]["$id"]["$oid"]
                    del obj["cpg"]

                # Write each processed JSON object directly to output file
                with open(output_file, 'a') as f_out:
                    json.dump(obj, f_out)
                    f_out.write('\n')
                    
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")

# Example usage
input_file = 'brands.json'   # Replace with your input file path
output_file = 'output_brands.json' # Replace with desired output file path

# Clear existing content of output file if it exists
open(output_file, 'w').close()

preprocess_json(input_file, output_file)
