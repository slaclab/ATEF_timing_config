import csv

# Read data from the input file
with open('IOC.txt', 'r') as file:
    input_data = file.readlines()

data_list = []
for line in input_data:
    line = line.replace(",\n", "")
    # Remove curly braces and split key-value pairs
    items = line.strip('{}').split(', ')
    # Create a dictionary from key-value pairs
    print(items)
    data_dict = {}
    for item in items:
        print(item)
        if 'id' in item:
            key, value = item.split(':')
            data_dict[key] = value.strip("'")
        elif 'host' in item:
            key, value = item.split(": ")
            data_dict[key] = value.strip("'")
        elif 'dir' in item:
            key, value = item.split(": ")
            data_dict[key] = value.strip("'")
    # Append the dictionary to the output list
    print(data_dict)
    print("\n")
    if data_dict != {}:
        data_list.append(data_dict)


# Define the output CSV file name
csv_file_path = 'IOC.csv'
# Extract column names (keys of the dictionaries)
fieldnames = data_list[0].keys()

# Write dictionaries to CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header row (column names)
    writer.writeheader()

    # Write data rows
    for data in data_list:
        writer.writerow(data)

print(f"CSV file '{csv_file_path}' has been created successfully.")


