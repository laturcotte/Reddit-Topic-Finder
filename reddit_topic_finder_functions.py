# Core functions for finder.py 
import sys 
import praw 

# Import smtplib library for email sending functions
# Import email.message for message formatting 
import smtplib
from email.message import EmailMessage 

def displayInitialMessage():
    # This is the first message the user sees on the console. 
    prompt = "This bot will send you an email containing Reddit threads " 
    prompt += "from a specific subreddit that relate to a keyword you enter." 
    prompt += '\nEnter "q" to quit.' 
    print(prompt) 
    
    
def getSubreddit(inputData, reddit): 
    # Get subreddit name from the user 
    subredditName = input("\nPlease enter the subreddit name (no special symbols): ") 
    
    # Quit if q is entered 
    if (subredditName == 'q'):
        sys.exit() 
    
    
    # Check if the subreddit name entered exists, firstly by making sure that it
    # it follows the required subreddit naming format/conventions 
    # two naming restrictions:
    
    # 1. no spaces  
    if (' ' in subredditName):
        print("A subreddit name cannot contain spaces. Please try again.")
        return False
    
    # 2. three to twenty-one upper or lowercase characters, digits, or underscores 
    elif (len(subredditName) < 3):
        print("Not enough characters, please try again.") 
        return False
    elif (len(subredditName) > 21): 
        print("Too many characters, please try again.") 
        return False
    
    # Check if the subreddit exists 
    # when using exact=True with search_by_name, it returns a list containing 
    # the subreddit if it exists, or an exception if it does not 
    subredditName = subredditName.lower() 
    try:
        subList = reddit.subreddits.search_by_name(subredditName, exact = True) 
    except:
        print("The subreddit", subredditName, "does not exist. Please try again.") 
        return False 
        
    # If it passes all of these checks, it is a valid subreddit 
    # Add it to the inputData and return true since it is a successful 
    # operation of it reaches this point 
    inputData.append(subredditName)
    return True 


def getKeyword(inputData): 
    # get keyword from user 
    input_msg = "\nPlease enter the keyword you want to search for in the "
    input_msg += "subreddit /r/" + inputData[0] + ": " 
    keyword = input(input_msg)  
    
    # Quit if q is entered  
    if (keyword == 'q'):
        sys.exit() 
    
    # Make sure that there aren't any spaces in keyword/that it is only one word 
    elif (' ' in keyword): 
        print("Please re-enter a keyword without spaces") 
        return False 
    
    # Otherwise, keyword can be added to inputData 
    inputData.append(keyword) 
    return True 


def getEmail(inputData):
    emailAddress = input("\nPlease enter your email address: ") 
    
    # Quit if q is entered  
    if (emailAddress == 'q'):
        sys.exit() 
        
    inputData.append(emailAddress) 
    
    
def getUserInput(inputData, reddit): 
    # will take user input and will place into inputData if they pass all checks
    
    # Get subreddit name and keyword to search for inside that subreddit 
    while (getSubreddit(inputData, reddit) == False):
        # continue the prompt until the user quits or enters a proper subreddit name 
        continue 
        
    while (getKeyword(inputData) == False):
        # continue the prompt until the user quits or enters a proper keyword
        continue 
        
    getEmail(inputData) 
    
        
def findSubmissions(inputData, submissionList, reddit): 
    # Find submissions in the subreddit that match the keyword 
    submissionCount = 0 
    sub = reddit.subreddit(inputData[0]) 
    
    wordToCheck = inputData[1].lower()  
    
    # only check the top 25 "hot" submissions for recent popular posts 
    for submission in sub.hot(limit = 25):
        lowercaseTitle = submission.title.lower() 
        if wordToCheck in lowercaseTitle: 
            submissionList.append(submission) 
            submissionCount += 1 
            
    return submissionCount 
    
    
def sendEmail(inputData, count, submissionList, email, password): 
    # Uses en EmailMessage object to hold message content, sends that message 
    # using smtp library 
     
    msg = EmailMessage() 
    
    subjectMsg = 'Your results for searching "' + inputData[1] + '" in the ' 
    subjectMsg += "subreddit /r/" + inputData[0] 
    msg['Subject'] = subjectMsg 
    
    # send message from bot email to the email address the user entered 
    msg['From'] = email
    msg['To'] = inputData[2] 
    
    
    # Start content with intro message 
    contentMsg = "Task completed; found " + str(count) + " hot posts " 
    contentMsg += 'matching "' + inputData[1] + '" in the subreddit /r/' 
    contentMsg += inputData[0] + '\n' 
    
    # Add each submission to email content 
    for i in range(0, len(submissionList)):
        contentMsg += "\nTitle: " + submissionList[i].title + "\nURL: " 
        contentMsg += submissionList[i].url + "\n"
    
    msg.set_content(contentMsg)  

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp: 
        smtp.ehlo() # identify ourselves with mail server 
        smtp.starttls() # encrypt traffic
        smtp.ehlo() # run again w/ encrypted server 
        
        smtp.login(email, password)  
        smtp.send_message(msg)  
    
    
def finalConsoleMessage(inputData, count): 
    print("\n\nTask completed; found", count, "hot posts matching", 
        '"' + inputData[1] + '"', "in the subreddit /r/" + inputData[0]) 
    print("These results have been sent to your email (" + inputData[2] + ")") 
    

