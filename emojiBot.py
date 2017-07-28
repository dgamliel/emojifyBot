import praw
import time
import config
import requests
import bs4

'''
This strings is the "trigger"
that when found in a reddit comment
will prompt our script to reply to the comment
with the emojified text of the parent comment.
'''

phrase = "!emojify"


def login():

	'''
	Initializes a reddit instance.
	logs in by importing config.txt.

	Username, password, client_id, and client_secret are all strings.
	'''

	reddit = praw.Reddit(username = config.username,
 		     	         password = config.password,
		     	         client_id = config.client_id,
		     	         client_secret = config.client_secret,
					     user_agent = config.user_agent)

	print ("Successfully logged into reddit" + '\n')

	return reddit #Returns a reddit instance, essentially "logs in"

#Writes to 'idFile.txt' to make sure we only respond to a comment once
def writeToFile(redditComment):

	#Opens a file called "idFile.txt"
	infile = open('idFile.txt', 'a+')

	#Creates list, one list index per line
	#This list contains post ID's unique to each 
	#reddit comment replied to.

	idList = infile.readlines()

	#If the commentID paramater passed to the function
	#is not in idList, then add the new commentID to 
	#the file "idFile.txt"

	if redditComment not in idList:
		infile.write(redditComment.id + '\n')
		infile.close()

#I'm not really sure what this does
def verifyConnection(request):
	print(requests.url())



#Returns parent comment of comment that triggered bot response
def getComment(trigger):

	#Generates a list of ID's to parse through
	idFile = open('idFile.txt', 'r')
	idList = idFile.readlines()
	idFile.close()

	#Test to verify bot is fetching comments in subreddit 'test' and returns unique comment each time.
	#NOTE: In testing we add 100 ID's to the file idFile.txt each time so if we want to make the bot
	#run smoothly it might be efficient to clear the file ever time after ever 100 tests or so.
	for comment in reddit.subreddit('test').comments(limit=100):
		if comment not in idList:
			print(comment.body + '\nComment ID is : ' + comment.id + '\n')
			writeToFile(comment)

def scrape(comment):
	textBox = "<textarea class='form-control animated' rows='6' id='text' accept-charset='utf-8'></textarea>"

	#sends a get requests to emojipasta.co and receives index.html data
	req = requests.get("http://emojipasta.co")
	print ("GET request sent to : http://emojipasta.co")
	
	#intializes a BS4 object passing the HTML of the text box from the emojipasta website
	soup = BeautifulSoup(textBox)

	#inserts our comment into the box?
	soup.insert(comment)
	print ("Soup object now looks like : ")
	print (soup)

	#TODO: figure out how the fuck server requests work.

#--------------------------------------------------------

while True:
	reddit = login()
	print ('ATTEMPTING FUNCTION: GET COMMENT')
	copyPasta = getComment(phrase)
	print ('SLEEPING')
	time.sleep(10000)
