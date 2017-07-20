import praw
import time
import config
import requests

'''
This comment is the "trigger"
that when found in a reddit comment
will prompt our script to reply to the comment
with the emojified text of the parent comment.
'''

trigger = "!emojify"


def login(r):

	'''
	Initializes a reddit instance
	logs in by importing config.txt.

	Username, password, client_id, and client_secret are all strings.
	'''

	reddit = praw.Reddit(username = config.username,
 		     	    password = config.password,
		     	    client_id = config.client_id,
		     	    client_secret = config.client_secret)

	return reddit #Returns a reddit object, essentially "logs in"


def writeToFile(commentID):

	#Opens a file called "idFile.txt"
	infile = open('idFile.txt', 'a+')

	#Creates list, one list index per line
	#This list contains post ID's unique to each 
	#reddit comment replied to.

	idList = infile.readlines()

	#If the commentID paramater passed to the function
	#is not in idList, then add the new commentID to 
	#the file "idFile.txt"

	if commentID not in idList:
		infile.write(commentID + "\n")
		infile.close()

def verifyConnection(request):
	print(requests.url())

#Pretty sure this parses through all the comments in a subreddit
#and if the trigger string is found, then the script writes to file
#the comment ID
def botGetComment(trigger):
	for comment in reddit.subreddit('all').comments(limit=50):
	if comment == trigger and comment.id not in idList:
		writeToFile(comment.id)

#I think this was supposed to be my "main"?
#AKA where I would have called all my helper functions
#and running the entire script
def emojify():
	req = requests.get("emojipasta.co")
