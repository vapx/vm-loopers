import pandas as pd

# Read the Excel file
excel_file = './Taxation.xlsx'
data = pd.read_excel(excel_file)

# Get the 'id' column values
id_values = data['id'].tolist()

# Write the IDs to a text file
with open('ids.txt', 'w') as file:
    for cert_id in id_values:
        file.write(f"{cert_id}\n")

print("IDs have been successfully written to ids.txt")
