#!/usr/bin/env python

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import xlsxwriter
import base64
import mailparser


# We need to use this scope because we aren't sending emails.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Required authentication flow. This will only fire if no creds are detected.
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)

# Create excel file
row = 0
column = 0
xlsx_creation_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") #Idea: user-defined argument
#xlsx_title = "spam_info_" + xlsx_creation_timestamp
workbook = xlsxwriter.Workbook(f"spam_analysis_{xlsx_creation_timestamp}.xlsx")
worksheet = workbook.add_worksheet()
worksheet.write(column, row, f"contents of spam inbox ({xlsx_creation_timestamp})")

# Set up the spreadsheet
# Formatting
#Title_Format = workbook.add_format({"bold": 1, })
#body_column_width = workbook.add_format({# something to make it size 20})

# set up columns and stuff
column_titles = ["Message_ID", "Date", "From", "Received", "Subject", "Body"]
for title in column_titles:
    worksheet.write(row + 3, column + 1, title)
    column += 1



# Get Gmail's ID for each message in the spam inbox
try:
    spam_id = service.users().messages().list(userId = "me", q = "in:spam").execute()
    count_results = spam_id["resultSizeEstimate"]
    print(f"Grabbing {count_results} spam emails.")
    
    spam_list = []
    message_ids = spam_id["messages"]
    for ids in message_ids:
        spam_list.append(ids["id"])

except errors.HttpError as error:
    print(f"An error occured: {error}")

try:
    for ids in spam_list:
        extract_raw_content = service.users().messages().get(userId = "me", id = ids, format = "raw").execute()
        spam_contents = mailparser.parse_from_bytes(base64.urlsafe_b64decode(extract_raw_content["raw"]))
        
        # Grab all necessary elements
        body = spam_contents.body
        headers = spam_contents.headers

        # Write data to excel workbook
        
        for header, header_data in headers.items():
            if header in {"Received", "Return-Path", "Date", "From", "Subject"}:
                #print(f"{header} : {header_data}")

except errors.HttpError as error:
    print(f"An error occured: {error}")

workbook.close()


