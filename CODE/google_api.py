from __future__ import print_function
import os.path
import io
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(os.getcwd(), 'credentials\\credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

def create_folder(service, folder_name, parent_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    file = service.files().create(body=file_metadata,
                                  fields='id').execute()
    return file.get('id')

def list_folders(service, q="mimeType = 'application/vnd.google-apps.folder'", get_root: bool=False):
    # Call the Drive v3 API
    results = service.files().list(q=q,
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    folder_id = None
    if not items:
        logging.warning('No folders found')
    else:
        for item in items:
            if item['name'] == 'cloud_savedata_manager':
                folder_id = item['id']
                break
        if not folder_id:
            logging.warning('No folder named "cloud_savedata_manager" found')
            folder_id = create_folder(service=service,
                                      folder_name='cloud_savedata_manager')

    results = service.files().list(q=f"'{folder_id}' in parents",
                                   pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if get_root:
        return folder_id
    return items


def return_id(service, find: str, q="mimeType = 'application/vnd.google-apps.folder'"):
    items = list_folders(service=service, q=q)
    for item in items:
        if find:
            if item['name'] == find:
                return item['id']


def download_file(service, file_id: str, output_path: str):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    fh = open(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

def upload_file(service, file_path: str, parent_id: str = None):
    file_metadata = {'name': os.path.basename(file_path)}
    if parent_id:
        file_metadata['parents'] = [parent_id]
    media = MediaFileUpload(file_path, mimetype='zipfile/zip')
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    file_id = file.get('id')
    return file_id

def update_file(service, file_path: str, file_id: str):
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='zipfile/zip')
    file = service.files().update(fileId=file_id,
                                  body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return file.get('id')

if __name__ == '__main__':
    service = get_service()
    #download_file(service=service,
    #              file_id='1LXIdgCPd5-bTHc5Tzv2JqUwae7DXvk_w',
    #              output_path='output.pdf')

    #upload_file(service=service,
    #            file_path='testing_file.txt')

    list_folders(service)

