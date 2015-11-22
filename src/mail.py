import smtplib

from email.mime.text import MIMEText

#for the moment only hotmail
def login(user, password):
	s = smtplib.SMTP('smtp.live.com', 587) #TODO:check this

	#identify ourselves
	s.ehlo()

	# secure encryption
	s.starttls()

	#identify again
	s.ehlo()

	#login
	print "login..."
	s.login(user, password)
	
	print "logged in :)"
	return s

def sendFileContent(data, subject, to):
	# Create a plain message
	#TODO: improve data format
	msg = MIMEText( str(data) )

	user 	 = raw_input('insert your username: ')
	password = raw_input('insert your password: ')
	
	msg['Subject'] = subject
	msg['From']	   = user
	msg['To'] 	   = to

	s = login(user, password)

	s.sendmail(user, to, msg.as_string())
	
	print "email sent to:", to
	s.quit()