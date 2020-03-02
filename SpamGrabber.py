# Libraries to call
import pickle
import os.path
import base64
import email
import csv
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Necessary Scopes for the script to operate
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
 
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
########################

    # List Spam Ids
    try:
        spam_id = service.users().messages().list(userId = "me", q = "in:spam").execute()
        count_results = spam_id["resultSizeEstimate"]
        print(count_results)
        
        spam_list = []
        message_ids = spam_id["messages"]
        for ids in message_ids:
            spam_list.append(ids["id"])
    
    except errors.HttpError as error:
        print("An error occured: %s") % error

    # Gets content from Spam
    try:
        # Put contents in CSV
        f = csv.writer(open('GrabbedSpam.csv', "w"))
        f.writerow(["ID", "Snippet", "Payload"]) 

        for ids in spam_list:
            extract_spam_content = service.users().messages().get(userId = "me", id = ids, format = "metadata", metadataHeaders = ["From", "Subject", "Received", "Return-Path"]).execute()
        
            # Pulls required comments out
            spam_snippet = extract_spam_content["snippet"]
            spam_payload = extract_spam_content["payload"]
            



            # Prints spam info for each message
            # print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------" + '\r')
            # print("Spam Id: " + ids + "\n")
            # print("Spam Snippet: " + spam_snippet + "\n")
            # print("Spam Payload (filtered): " + "\n")
            # print(spam_payload)
            # print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------" + '\r')
            # print("\n")
            # print("\n")
        for ids in extract_spam_content:
            f.writerow([spam_id_csv, spam_snippet, spam_payload])


        
            

    

    except errors.HttpError as error:
        print("An error occured: %s") % error
    
    

    
    
    
    
    
    
    
    # get mime content
    # try:
    #     spam_list = service.users().messages().get(userId = "me", id = message_ids, format = "raw").execute()
    #     msg_raw = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
    #     msg_str = email.message_from_bytes(msg_raw)
    #     content_types = msg_str.get_content_maintype()

    #     if content_types == "multipart":
    #         plaintxt_content = msg_str.get_payload()
    #         return plaintxt_content.get_payload()
    #     else:
    #         return msg_str.get_payload

    # except errors.HttpError as error:
    #     print("An error occured: %s") % error








if __name__ == '__main__':
    main()




