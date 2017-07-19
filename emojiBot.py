import praw
import time
import config
import requests


trigger = "!emojify"

def login(r):

	reddit = praw.Reddit(username = config.username,
 		     	    password = config.password,
		     	    client_id = config.client_id,
		     	    client_secret = config.client_secret)

	return reddit


def writeToFile(commentID):
	infile = open('idFile.txt', 'a+')
	idList = infile.readlines()
	if commentID not in idList:
		infile.write(commentID + "\n")
		infile.close()

def verifyConnection(request):
	print(requests.url())
	print()

def emojify():
	req = requests.get("emojipasta.co")


def botGetComment(trigger):
	for comment in reddit.subreddit('all').comments(limit=50):
	if comment == trigger and comment.id not in idList:
		writeToFile(comment.id)

