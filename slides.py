import os
import io
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Define the required scopes for Google Drive and Slides APIs
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/presentations.readonly']

# Function to authenticate and create the API client
def authenticate_google():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # Create the API clients for Google Drive and Slides
    drive_service = build('drive', 'v3', credentials=creds)
    slides_service = build('slides', 'v1', credentials=creds)
    return drive_service, slides_service

# Function to get all Google Slides files in a specific folder
def get_google_slides_files_in_folder(drive_service, folder_id):
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.presentation'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def download_slide_as_image(slides_service, presentation_id, slide_object_id, output_dir, slide_name):
    # Use the Slides API to generate a thumbnail for the specified slide
    try:
        # Get the thumbnail for the slide with a default resolution
        thumbnail = slides_service.presentations().pages().getThumbnail(
            presentationId=presentation_id,
            pageObjectId=slide_object_id,
            thumbnailProperties_thumbnailSize='LARGE'  # Options: SMALL, MEDIUM, LARGE
        ).execute()

        # Extract the thumbnail URL from the response
        thumbnail_url = thumbnail.get('contentUrl')
        if not thumbnail_url:
            print(f"Thumbnail URL not found for slide {slide_name}.")
            return

        # Make a GET request to download the thumbnail
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            # Save the image file
            with open(os.path.join(output_dir, f"{slide_name}.png"), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {slide_name}.png")
        else:
            print(f"Failed to download slide {slide_name}.png, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {slide_name}.png: {str(e)}")

# Main function to automate the download of all slides in the specified folder
def main():
    folder_id = '15kj7x83Efz3FANNqxrd1TF04PZQhoBYY'  # Replace with your Google Drive folder ID
    output_dir = './certs3'       # Directory to save the images

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Authenticate and create the API clients
    drive_service, slides_service = authenticate_google()

    # Get the list of Google Slides files in the folder
    slides_files = get_google_slides_files_in_folder(drive_service, folder_id)
    if not slides_files:
        print("No Google Slides found in the specified folder.")
        return

    # Loop through each Google Slides file and download all slides as images
    for slide_file in slides_files:
        presentation_id = slide_file['id']
        presentation_name = slide_file['name']
        print(f"Processing presentation: {presentation_name}")

        # Get the slides from the presentation
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        # Download each slide as an image
        for index, slide in enumerate(slides):
            slide_object_id = slide['objectId']
            slide_name = f"{presentation_name}_slide_{index + 1}"
            download_slide_as_image(slides_service, presentation_id, slide_object_id, output_dir, slide_name)

    print("All slides downloaded successfully.")

if __name__ == '__main__':
    main()
