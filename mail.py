import smtplib

from email.mime.text import MIMEText

def sendFileContent(file, subject, fromp, to):
	fp = open(file, 'rb')

	# Create a plain message
	msg = MIMEText(fp.read())
	fp.close()

	#msg['Subject'] = subject
	#msg['From']	= fromp
	#msg['To'] 	    = to

	s = smtplib.SMTP('smtp.live.com', 587) #TODO:check this
	#identify ourselves
	s.ehlo()
	# secure encryption
	s.starttls()
	#identify again
	s.ehlo()
	
	#login
	print "login..."
	s.login('user@outlook.com', 'password')
	
	print "logged in :)"
	s.sendmail('me@gmail.com', 'you@gmail.com', msg.as_string())
	
	print "email sent"
	s.quit()