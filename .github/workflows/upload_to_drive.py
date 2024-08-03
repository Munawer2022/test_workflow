import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path, folder_id):
    creds = Credentials.from_authorized_user_info({
        "client_id": os.environ['GDRIVE_CLIENT_ID'],
        "client_secret": os.environ['GDRIVE_CLIENT_SECRET'],
        "refresh_token": os.environ['GDRIVE_REFRESH_TOKEN']
    })

    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python upload_to_drive.py <apk_path> <ipa_path> <folder_id>")
        sys.exit(1)

    apk_path, ipa_path, folder_id = sys.argv[1], sys.argv[2], sys.argv[3]
    upload_to_drive(apk_path, folder_id)
    upload_to_drive(ipa_path, folder_id)
