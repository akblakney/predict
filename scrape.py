from urllib.request import urlopen
from bs4 import BeautifulSoup

pageUrl = 'https://www.predictit.org/api/marketdata/all/'
page = urlopen(pageUrl)
parsed = BeautifulSoup(page,'html.parser')

f = open('data', 'w')
f.write(str(parsed))
f.close()
