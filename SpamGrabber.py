# Libraries to call
import base64
import email
import csv
from apiclient import errors

print("Welcome to SpamGrabber")
print("Make sure your Gmail API has been authenticated", "\n")

# User-defined parameters
user_id = input("Gmail address: ")
earliest_spam = input("Start of date range (YYYY/MM/DD): ")
latest_spam = input("End of date range (YYYY/MM/DD): ")
print("\n")
print("SpamGrabber will look for spam emails for %s between the dates of %s and %s" % (user_id, earliest_spam, latest_spam))
print("\n")

#API Requests






# request goal ==> GET https://www.googleapis.com/gmail/v1/users/user_id/messages?q=in:spam after:date before:date





















