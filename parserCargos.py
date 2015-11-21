import os
import sys
import subprocess
import pdfquery
import urllib2
import MyHTMLparser

def retrieveFileFromUrl(url, fileNameContent):
	print "Retrieving URL"

	#download the web HTML
	page = urllib2.urlopen(url)
	HTML = page.read().decode('utf-8')

	#Looks for file link
	fileLink = MyHTMLparser.retrieveRef(HTML, fileNameContent)

	#completes the link
	fileLink = 'https://sites.google.com' + str(fileLink)

	#downloads the file
	PDFFile = urllib2.urlopen(fileLink)
	print "File has been downloaded"
	
	return PDFFile

def dumpDataToFile(data, fileName):
	print "Creating file"

	f = open('pagecontent/' + fileName, 'w')
	f.write( str(data) )
	f.close()

	print "File has been created"
	
	return

def retrieveFromPdf(fileName, category):
	print "Opening PDF"

	pdf = pdfquery.PDFQuery(fileName)
	pdf.load()
	
	print "PDF succesfully opened"

	print "Doing magic in the file"
	#gives format and recovers data
	label = pdf.pq('LTTextLineHorizontal:contains(' + category + ')')

	items = []
	
	for i in label.items('LTTextLineHorizontal'):
		left_corner   = float(i.attr('x0'))
		bottom_corner = float(i.attr('y0'))
		items.append(pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner-800, bottom_corner, left_corner+700, bottom_corner+20)).text())
	
	return items

def saveFile(items, file):
	f = open(file,'w')

	for i in items:
		f.write(removeNonAscii(i) + '\n')
	f.close()
	
	return

def deleteFile(fileName):
	print "Cleaning"

	os.remove('pagecontent/' + fileName)

	print "Done cleaning"

def removeNonAscii(i):
	result = ""
	
	for j in i:
		if ord(j) < 128 : result = result + j 
	return result


#MAIN#--------------------------------------
data = retrieveFileFromUrl("https://sites.google.com/site/informaciondocente/remanente-de-actos-publicos", 'Junta%20V')

#saves it into a file
dumpDataToFile(data, "actaV.pdf")

#now reads it and modifies it
items = retrieveFromPdf("pagecontent/acto.pdf", "MECANICA")

#clear files
deleteFile("actaV.pdf")

#TODO: revisar como no poner explicitamente usuario y contrasena
#sendFileContent("CargosComputacion.txt", "cargos computacion", "from", "me@algo.com")

if(items == []):
	subprocess.Popen(['notify-send', "no hay cargos nuevos"])	
else:
	#notifies the OS about the new messages
	subprocess.Popen(['notify-send', "tenes cargos nuevos :)"])
	saveFile(items, "CargosComputacion.txt")