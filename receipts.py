import json

def preprocess_json(input_file, output_file_main, output_file_items):
    with open(input_file, 'r') as f_in:
        with open(output_file_main, 'w') as f_out_main, open(output_file_items, 'w') as f_out_items:
            for line in f_in:
                try:
                    obj = json.loads(line.strip())
                    
                    # Process _id field if it contains $oid
                    if "_id" in obj and isinstance(obj["_id"], dict) and "$oid" in obj["_id"]:
                        obj["_id"] = obj["_id"]["$oid"]
                    
                    # Process all date fields if they contain $date
                    date_fields = ["createDate", "dateScanned", "finishedDate", "modifyDate", "pointsAwardedDate", "purchaseDate"]
                    for field in date_fields:
                        if field in obj and isinstance(obj[field], dict) and "$date" in obj[field]:
                            obj[field] = obj[field]["$date"]
                    
                    # Convert specific fields to integers
                    fields_to_convert = ["pointsEarned", "totalSpent"]
                    for field in fields_to_convert:
                        if field in obj:
                            try:
                                obj[field] = int(float(obj[field]))  # Convert string to float first to handle decimal strings, then to int
                            except ValueError:
                                pass  # Ignore conversion errors and keep the original value

                    # Remove rewardsReceiptItemList from the main document
                    rewards_items = obj.pop("rewardsReceiptItemList", None)

                    # Write main document fields to the main output file
                    json.dump(obj, f_out_main)
                    f_out_main.write('\n')

                    # Flatten nested rewardsReceiptItemList if it exists and write to separate file
                    if rewards_items:
                        for i, item in enumerate(rewards_items):
                            item_obj = {"_id": obj["_id"]}
                            for key, value in item.items():
                                # Convert specific fields to integers
                                if key in ["barcode", "finalPrice", "itemPrice", "partnerItemId", "userFlaggedBarcode", "userFlaggedPrice"]:
                                    try:
                                        item_obj[key] = int(float(value))  # Convert string to float first, then to int
                                    except ValueError:
                                        item_obj[key] = value  # Keep the original value if conversion fails
                                else:
                                    item_obj[key] = value
                            json.dump(item_obj, f_out_items)
                            f_out_items.write('\n')

                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line.strip()}")

# Example usage
input_file = 'receipts.json'           # Replace with your input file path
output_file_main = 'output_receipts.json'  # Replace with desired main output file path
output_file_items = 'output_receiptitems.json' # Replace with desired items output file path

# Clear existing content of output files if they exist
open(output_file_main, 'w').close()
open(output_file_items, 'w').close()

preprocess_json(input_file, output_file_main, output_file_items)
