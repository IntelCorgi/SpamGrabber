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
 
# Authorization flow, copied from the API docs.
# If you already have the token.pickle file, this function will do nothing.
def run_authentication():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
       
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

if __name__ == '__run_authentication__':
    run_authentication()
run_authentication()

# Calls the Gmail API
service = build('gmail', 'v1', credentials=creds)

# Introduction
print("Welcome to SpamGrabber")
user_id = input("Enter the Gmail address to grab spam from: ")
print("Grabbing all spam from the last 30 days...")

# Get list of message ids for messages in Spam
def search_spam(service, user_id, search_string):
    try:
        search_string = "in:spam"
        spam_id = service.users().messages().list(userId = user_id, q = search_string).execute()
        count_results = spam_id["resultSizeEstimate"]
        
        results_list = []
        if count_results > 0:
            print("SpamGrabber has found %s message(s) in the spam folder for %s" % (count_results, user_id))
            message_ids = spam_id["messages"]
            for ids in message_ids:
                results_list.append(ids[id])
            return results_list
        else:
            print("There are currently no messages in your spam folder. Check your settings or consider yourself lucky")
            return ""
    except errors.HttpError as error:
        print("An error occured: %s") % error
            
search_spam()

# Get content from the messages in spam 
# TODO: Add all the fields I need to pull in this area
def spam_content(service, user_id, msg_id):
    try:
        spam_list = service.users().messages().get(userId = user_id, id = msg_id, format = "raw").execute()
        msg_raw = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
        msg_str = email.message_from_bytes(msg_raw)
        content_types = msg_str.get_content_maintype()

        if content_types == "multipart":
            plaintxt_content = msg_str.get_payload()
            return plaintxt_content.get_payload()
        else:
            return msg_str.get_payload







    except errors.HttpError as error:
        print("An error occured: %s") % error

spam_content()




















# # User-defined parameters. NOTE: MESSAGES DELETE AFTER 30 DAYS SO JUST GET ALL FROM SPAM
# user_ID = "me"
# earliest_spam = input("Start of date range (YYYY/MM/DD): ")
# latest_spam = input("End of date range (YYYY/MM/DD): ")
# print("\n")
# print("SpamGrabber will look for spam emails for %s between the dates of %s and %s" % ("me", earliest_spam, latest_spam))
# print("\n")





# request goal ==> GET https://www.googleapis.com/gmail/v1/users/user_id/messages?q=in:spam after:date before:date


# TODO: Pass results into CSV


















