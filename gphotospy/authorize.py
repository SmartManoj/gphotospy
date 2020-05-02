import os
import pickle
import logging
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


service_name = "photoslibrary"
version = "v1"
scopes_arr = [
    'https://www.googleapis.com/auth/photoslibrary',
    'https://www.googleapis.com/auth/photoslibrary.sharing'
]


def init(secrets):
    """
    Initializes the service, requesting the authorization from the browser.

    Parameters
    ----------
    secrets: str
        JSON file containing the secrets for OAuth,
        as created in the Google Cloud Consolle
    """
    credentials = None
    token_file = f'{service_name}_{version}.token'

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            app_flow = InstalledAppFlow.from_client_secrets_file(
                secrets, scopes_arr)
            credentials = app_flow.run_local_server()

        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)

    try:
        service = build(service_name, version, credentials=credentials)
        logging.info(service_name, 'service created successfully')
        return service
    except Exception as e:
        logging.error(e)
    return None
