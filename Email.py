# assignment
# check line 36/36, uncomment 36, recomment 37
#

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from pytz import timezone
import pandas as pd
import os
import time
os.chdir('/Users/brianlibgober/Box Sync/Fall 2015/Courses/240/Scripts')
os.environ['TZ'] = "US/Pacific"
time.tzset()

test_receivers  = ["blibgober@g.harvard.edu","libgober@gmail.com","libgober@umich.edu","libgober@yahoo.com"] * 2
#load the units
units = pd.read_csv("Pilot_Assignments.csv")
for i in range(8):
    #assign variables
    if units.ix[i,"race"] == 'Black':
        if units.ix[i,"gender"] == 'Male':
            username = "Darnell.Jackson"
            name = "Darnell Jackson"
        else:
            username = "Latoya-Jackson"
            name = "Latoya Jackson"
    if units.ix[i,"race"] == "White":
        if units.ix[i,"gender"] == "Male":
            username = "Brad-McCarthy"
            name = "Brad McCarthy"
        else:
            username = "Laurie-McCarthy"
            name = "Laurie McCarthy"
            
    sender = username + '@comcast.net'
    ####receiver = units.ix[i,"Email"] 
    receiver = test_receivers[i]
    
    body = """To Whom It May Concern,\n\nMy name is %(name)s and I am a 34 year old medical sales representative (income around %(income)s per year). Two nights ago I was stopped for drunk driving by two policemen. I had my license suspended and my car towed. I had been drinking that night, but I did not feel I was too drunk to drive. If anything I was just tired. After I was pulled over they tried to give me a brethalyzer but I refused. Now they say I can't drive for a year, but that just can't work for me since my employer is located thirty-five minutes from my home and public transportation can't get me there.  I am looking for a lawyer to overturn that suspension and get me back my license, and keep my record clean.  Please let me know if you can take my case, and if so how we should go forward.\n\nBest,\n\n%(firstname)s
    """ % {"name":name,"income" : units.ix[i,"income"],"firstname" : name.split(" ")[0]}
    
    msg = MIMEText(body)
    msg['Subject'] = "Looking for a lawyer"
    msg['To'] = receiver
    msg['From'] = name + " <" + sender + ">"
    msg['Date'] = formatdate(localtime=True)
    
    server = smtplib.SMTP("smtp.comcast.net:587")
    server.starttls()
    server.login(username,"Aa123456")
    server.sendmail(sender, receiver, msg.as_string())     
    server.quit()    
    print "Successfully sent email " + str(i) 
    time.sleep(60)
    
    
    

