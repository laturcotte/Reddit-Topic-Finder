# reddit topic finder bot 
# The user can input a specific subreddit, a keyword they want to search for, 
# and their email address. This bot will send an email to the user which contains
# the title and URL of every "hot" post in that subreddit that contains the 
# keyword that was entered.   

import praw 

# Import bot functions 
import reddit_topic_finder_functions as f

# reddit api login 
reddit = praw.Reddit(client_id = id, 
                    client_secret = secret, 
                    username = user_name, password = pass_word, 
                    user_agent = short_description) 


# User prompt 
f.displayInitialMessage() 

# inputData will have 3 elements:
# subreddit name (index 0), keyword (index 1), and email (index 2) 
inputData = [] 
f.getUserInput(inputData, reddit) 

# check submissions 
submissionList = [] 
resultsCount = f.findSubmissions(inputData, submissionList, reddit) 

# send an email to the user once the data has been collected 
finderEmailAddress = bot_email 
finderEmailPassword = bot_password
f.sendEmail(inputData, resultsCount, submissionList, finderEmailAddress, 
                finderEmailPassword) 

f.finalConsoleMessage(inputData, resultsCount) 
