import pandas as pd
import json

def generate_json_from_spreadsheet(file_path):
    # Load the spreadsheet into a pandas DataFrame
    df = pd.read_excel(file_path)  # Update this to pd.read_csv(file_path) if using a CSV file

    # List to hold all JSON objects
    json_data = []

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        # Create a dictionary in the specified JSON format
        json_entry = {
            "id": row["url"],
            "name": row["fullname"].title(),  # Capitalize the name
            "webinar_title": "Modern Approaches to Procurement and Inventory Management",
            "Duration": "1.5hrs",
            "Course Outline / Webinar Contents": "<li>Strategic Sourcing and Supplier Relations: Discover techniques for evaluating and selecting suppliers, fostering strong partnerships, and leveraging strategic sourcing to drive value.</li><li>Data-Driven Inventory Optimization: Learn how to use data analytics to forecast demand accurately, optimize inventory levels, and reduce costs.</li><li>Sustainable and Ethical Procurement: Understand modern practices in ethical sourcing and sustainability, and their impact on brand reputation and long-term business success.</li><li>Technology and Automation in Procurement: Explore the latest tools and software for automating procurement processes, improving efficiency, and enhancing transparency.</li>",
            "Date": "October 27, 2024, Sunday 8:00pm - 9:30pm",
            "Mentor / Speaker": "Khantelle Genevieve Anore",
            "Certificate ID": row["id"]
        }
        # Append the dictionary to the list
        json_data.append(json_entry)

    # Convert the list of dictionaries to JSON format with ensure_ascii=False to keep special characters
    json_output = json.dumps(json_data, indent=4, ensure_ascii=False)

    # Save the output to a file
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_output)

    print("JSON data has been generated and saved to output.json")

# Example usage
file_path = './admin.xlsx'  # Update this path to your spreadsheet file
generate_json_from_spreadsheet(file_path)
