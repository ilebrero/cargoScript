from BeautifulSoup import BeautifulSoup

def retrieveRef(html, name):
	soup = BeautifulSoup(html)
	for link in soup.findAll('a'):
		if name in str(link):
			return link.get('href')