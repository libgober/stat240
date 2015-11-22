#test sending an email in python

import smtplib


sender = 'darnell.jackson@comcast.net'
receivers = 'blibgober@g.harvard.edu'

message = """From: Darnell Jackson <darnell.jackson@comcast.net>
To: Brian <blibgober@g.harvard.edu>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

server = smtplib.SMTP("smtp.comcast.net:587")
server.starttls()
server.login("Darnell.Jackson","Aa123456")
server.sendmail(sender, receivers, message)     
server.quit()    
print "Successfully sent email"

#load the units

#exclude obviously bad units
#randomly shuffle their order
#assign deterministically to a treatment option
#compose a message and send based on treatment criteria
send(status)