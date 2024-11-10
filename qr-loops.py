import pandas as pd
import qrcode

# Read the Excel file
excel_file = './admin.xlsx'
data = pd.read_excel(excel_file)

# Base URL for the certificate
base_url = "https://mentors-global.com/certifications/profile?id="

# Loop through each row in the Excel file
for index, row in data.iterrows():
    # Get the certificate ID
    cert_id = row['url']
    
    # Construct the URL for the certificate
    url = f"{base_url}{cert_id}"
    
    # Generate the QR code
    qr = qrcode.make(url)
    
    # Save the QR code as an image file
    qr_filename = f"qrcode-{cert_id}.png"
    qr.save(qr_filename)
    
    print(f"QR code for certificate ID {cert_id} saved as {qr_filename}")

