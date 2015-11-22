import os

def savePlainTextToFile(data, fileName):
	print "Creating file"

	f = open(fileName, 'w')
	f.write( str(data) )
	f.close()

	print "File has been created"
	
	return

def saveItemsOnFile(items, file):
	f = open(file,'w')

	for i in items:
		f.write(removeNonAscii(i) + '\n')

	f.close()
	
	return

def deleteFile(fileName):
	print "Cleaning"

	os.remove(fileName)

	print "Done cleaning"

def removeNonAscii(i):
	result = ""
	
	for j in i:
		if ord(j) < 128 : result = result + j 
		
	return result