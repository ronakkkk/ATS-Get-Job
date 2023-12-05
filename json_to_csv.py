import pandas as pd
import json

# Load JSON data into a Python dictionary
with open('response.json') as f:
    json_data = json.load(f)

# Specify the key you want to extract
desired_key = 'results'

# Extract the specified key and convert it to a DataFrame
data = pd.DataFrame(json_data[desired_key])

# Convert DataFrame to CSV and save it to a file
data.to_csv('output.csv', index=False)
