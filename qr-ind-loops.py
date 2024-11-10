import qrcode

# Base URL for the certificate
base_url = "https://mentors-global.com/certifications/profile?id="

# List of certificate IDs
cert_ids = [
   "iyfg-alwq-zyts"
]

# Loop through each certificate ID
for cert_id in cert_ids:
    # Construct the URL for the certificate
    url = f"{base_url}{cert_id}"
    
    # Generate the QR code
    qr = qrcode.make(url)
    
    # Save the QR code as an image file
    qr_filename = f"qrcode-{cert_id}.png"
    qr.save(qr_filename)
    
    print(f"QR code for certificate ID {cert_id} saved as {qr_filename}")
