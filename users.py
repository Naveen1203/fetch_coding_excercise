import json

def preprocess_json(input_file, output_file):
    with open(input_file, 'r') as f_in:
        for line in f_in:
            try:
                obj = json.loads(line.strip())
                
                # Process _id field if it contains $oid
                if "_id" in obj and isinstance(obj["_id"], dict) and "$oid" in obj["_id"]:
                    obj["_id"] = obj["_id"]["$oid"]
                
                # Process createdDate and lastLogin fields if they contain $date
                for field in ["createdDate", "lastLogin"]:
                    if field in obj and isinstance(obj[field], dict) and "$date" in obj[field]:
                        obj[field] = obj[field]["$date"]
                
                # Write each processed JSON object directly to output file
                with open(output_file, 'a') as f_out:
                    json.dump(obj, f_out)
                    f_out.write('\n')
                    
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")

# Example usage
input_file = 'users.json'   # Replace with your input file path
output_file = 'output.json' # Replace with desired output file path

# Clear existing content of output file if it exists
open(output_file, 'w').close()

preprocess_json(input_file, output_file)
