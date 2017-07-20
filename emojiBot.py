import praw
import time
import config
import requests
import bs4

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

#I'm not really sure what this does
def verifyConnection(request):
	print(requests.url())


#Pretty sure this parses through all the comments in a subreddit
#and if the trigger string is found, then the script writes to file
#the comment ID

def botGetComment(trigger):
	#putting 'test' as reddit.subreddit parameter so that
	#I can properly test the bot before "deploying"
	for comment in reddit.subreddit('test').comments(limit=50):
		if comment == trigger and comment.id not in idList:
			writeToFile(comment.id)

#This is the function that would connect to emojipasta.co
#paste the comment, then return the emojified string.
def emojify():
	req = requests.get("emojipasta.co")
