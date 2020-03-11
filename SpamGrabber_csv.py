# Libraries to call
import pickle
import os.path
import base64
import email
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Necessary Scopes for the script to operate
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
 
def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

########### Begin the actual script #############

    # List Spam Ids
    try:
        spam_id = service.users().messages().list(userId = "me", q = "in:spam").execute()
        count_results = spam_id["resultSizeEstimate"]
        print(f"Grabbing {count_results} spam emails.")
        
        spam_list = []
        message_ids = spam_id["messages"]
        for ids in message_ids:
            spam_list.append(ids["id"])
    
    except errors.HttpError as error:
        print("An error occured: %s") % error

    # Gets content from Spam
    try:
        for ids in spam_list:
            extract_spam_content = service.users().messages().get(userId = "me", id = ids, format = "metadata", metadataHeaders = ["From", "Subject", "Received", "Return-Path"]).execute()
            extract_mime_content = service.users().messages().get(userId = "me", id = ids, format = "raw").execute()

            # Pulls basic message content
            spam_snippet = extract_spam_content["snippet"]
            spam_payload = extract_spam_content["payload"]["headers"]
            spam_metadata = (f"{ids}, {spam_snippet}, {spam_payload}")
            #output_edge = "=========================================================================================================="
            
            # Pulls MIME content
            msg_str = base64.urlsafe_b64decode(extract_mime_content["raw"].encode("ASCII"))
            mime_msg = email.message_from_bytes(msg_str)
            mime_payload = mime_msg.get_payload()
            
            print(csv_row, mime_payload,"\n")

    except errors.HttpError as error:
        print("An error occured: %s") % error


if __name__ == '__main__':
    main()


