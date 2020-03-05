SpamGrabber
==============

## Welcome to SpamGrabber!

Spamgrabber is a simple python script I have developed to assist me with a project for a class. As the script stands right now, it grabs 30 days worth of spam messages from your Gmail **(and only Gmail)** account and prints data from it in a csv format. By csv format, I mean it is literally printing it as a comma separated format. It is super rough right now, but my main concern is getting my project done so I will return to clean up the code later.

Note that this is performing a GET request to Gmail servers, not actually opening the email or downloading anything.

## Running the Script

To use this script yourself, make sure you follow [this API quickstart guide](https://developers.google.com/gmail/api/quickstart/python). It will guide you through the process needed to create an authorized instance so you can communicate with your gmail account.

Once your token.pickle file has been created and you have run the necessary packages in place (which should have been installed as a part of the quickstart process) I would recommend creating a csv file to redirect output to, just to make processing easier. Otherwise it will print to the terminal.

## Next Steps

* Clean up code!!!

* Add functions for csv python library.

* Grab only the metadata that we need from Gmail.

* Maybe even get the MIME raw content.

* Download files and hash them for analysis.