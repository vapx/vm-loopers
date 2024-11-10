import json

def generate_json_from_list(data_list):
    # List to hold all JSON objects
    json_data = []

    # Loop through each item in the data list
    for item in data_list:
        # Create a dictionary in the specified JSON format
        json_entry = {
            "id": item["id"],
            "name": item["fullname"],   
            "webinar_title": "Fundamentals of Bookkeeping",
            "Duration": "1.5hrs",
            "Course Outline / Webinar Contents": "<li>Understand the core principles of bookkeeping and financial reporting</li><li>Skilled in recording financial transactions</li><li>Appreciate the importance of compliance with financial regulations</li><li>Apply bookkeeping skills in real-world scenarios.</li>",
            "Date": "October 20, 2024, Sunday 6:00pm - 7:30pm",
            "Mentor / Speaker": "Atty. Verona D. Aguilar, CPA",
            "Certificate ID": item["cert_id"]
        }
        # Append the dictionary to the list
        json_data.append(json_entry)

    # Convert the list of dictionaries to JSON format
    json_output = json.dumps(json_data, indent=4)

    # Save the output to a file
    with open('output2.json', 'w') as json_file:
        json_file.write(json_output)

    print("JSON data has been generated and saved to output2.json")

# Example data based on your input
data_list = [
    {"fullname": "Piolo ReponiaTingson", "id": "eswu-xpqf-gadr", "cert_id": "IBKP-WB-01-0131"},
    {"fullname": "Geralyn M. Guitones", "id": "eubc-figv-dvir", "cert_id": "IBKP-WB-01-0132"},
    {"fullname": "Renzel Senadre Pacaco", "id": "akhx-ybew-alpf", "cert_id": "IBKP-WB-01-0133"},
    {"fullname": "ALYSSA P. BONA", "id": "yrns-qjqe-pqhf", "cert_id": "IBKP-WB-01-0134"},
    {"fullname": "Abegail D. Bobis", "id": "dpjp-thcc-dqgd", "cert_id": "IBKP-WB-01-0135"},
    {"fullname": "FRINTZ EMIL G. FLORES", "id": "dvfm-dluw-rmwa", "cert_id": "IBKP-WB-01-0136"},
    {"fullname": "Rowena M. Quimada", "id": "snvd-csej-uhvx", "cert_id": "IBKP-WB-01-0137"},
    {"fullname": "April Magnolia V. Dean", "id": "iedh-yjii-apsu", "cert_id": "IBKP-WB-01-0138"},
    {"fullname": "May Ann Daz Llaguno", "id": "mpbm-mdam-mwzf", "cert_id": "IBKP-WB-01-0139"},
    {"fullname": "Aleo Mae Salvo Baaclo", "id": "tdvt-jxle-ivik", "cert_id": "IBKP-WB-01-0140"}
]

generate_json_from_list(data_list)
