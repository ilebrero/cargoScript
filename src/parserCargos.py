import sys
import mail
import urllib2
import pdfquery
import subprocess
import FileManager
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
	
	return PDFFile.read()

def retrieveFromPdf(fileName, category):
	print "Opening PDF"

	pdf = pdfquery.PDFQuery(fileName)
	pdf.load()
	
	print "PDF succesfully opened", "Doing magic in the file"
	
	#gives format and recovers data
	label = pdf.pq('LTTextLineHorizontal:contains(' + category + ')')
	items = []
	
	for i in label.items('LTTextLineHorizontal'):
		left_corner   = float(i.attr('x0'))
		bottom_corner = float(i.attr('y0'))

		items.append(pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner-800, bottom_corner, left_corner+700, bottom_corner+20)).text())
	
	return items

def obtenerActa(numero):
	switcher = {
		"4" : "IV",
		"5" : "V",
	}

	return switcher.get(numero, numero)

def main(actaNumero, keyWord, mail_enabled, to):
	acta = obtenerActa(actaNumero)

	data = retrieveFileFromUrl("https://sites.google.com/site/informaciondocente/remanente-de-actos-publicos", 'Junta%20' + acta)

	#saves it into a file
	FileManager.savePlainTextToFile(data, 'acta' + acta + '.pdf')

	#now reads it and modifies it
	items = retrieveFromPdf('acta' + acta + '.pdf', keyWord)

	#clear files
	FileManager.deleteFile('acta' + acta + '.pdf')

	if (items == []) :
		subprocess.Popen(['notify-send', "no hay cargos nuevos"])	
	else:
		#notifies the OS about the new messages
		subprocess.Popen(['notify-send', "tenes cargos nuevos :)"])
		
		if (mail_enabled != 'no_mail'):
			#TODO: revisar como no poner explicitamente usuario y contrasena
			mail.sendFileContent(items, 'Cargos ' + keyWord, to)
		
		#FileManager.saveItemsOnFile(items, "CargosComputacion.txt")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))