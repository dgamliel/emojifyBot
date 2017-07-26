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
	Initializes a reddit instance
	logs in by importing config.txt.

	Username, password, client_id, and client_secret are all strings.
	'''

	reddit = praw.Reddit(username = config.username,
 		     	    password = config.password,
		     	    client_id = config.client_id,
		     	    client_secret = config.client_secret,
					user_agent = config.user_agent)

	print ("Successfully logged into reddit")

	return reddit #Returns a reddit instance, essentially "logs in"

#Writes to 'idFile.txt' to make sure we only respond to a comment once
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



#Returns parent comment of comment that triggered bot response
def getComment(trigger):

	#Generates a list of ID's to parse through
	#TODO: Make this a hashbank/Dict somehow?
	idFile = open('idFile.txt', 'r')
	idList = idFile.readlines()
	idFile.close()

	#Parses comments and returns the parent of trigger comment
	#TODO: fetch and return parent comment
	for comment in reddit.subreddit('test').comments(limit=75):
		if comment == trigger and comment.id not in idList and not comment.is_root():
			
			print('FOUND MATCHING COMMENT')
			writeToFile(comment.id)
			parent = comment.parent()

			print(parent.body())
			return parent.body()

		else:
			print('COMMENT NOT FOUND')

def scrape(comment):
	textBox = "<textarea class='form-control animated' rows='6' id='text' accept-charset='utf-8'></textarea>"

	#sends a get requests to emojipasta.co and receives index.html data
	req = requests.get("http://emojipasta.co")
	print ("GET request sent to : http://emojipasta.co")
	
	#intializes a BS4 object passing the HTML of the text box from the emojipasta website
	#Uses 'lxml' to parse (I don't know what this means)
	soup = bs4.BeautifulSoup(textBox, "lxml")

	#inserts our comment into the box?
	soup.textarea.append(comment)
	print ("Soup object now looks like : ")
	print (soup)

	#TODO: figure out how the fuck server requests work.

#--------------------------------------------------------

while True:
	reddit = login()
	copyPasta = getComment(phrase)
	scrape(copyPasta)
	print ('NOW SLEEPING FOR 10000 UNITS')
	time.sleep(10000)
