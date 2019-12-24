import json

# load data
from urllib.request import urlopen
from bs4 import BeautifulSoup

pageUrl = 'https://www.predictit.org/api/marketdata/all/'
page = urlopen(pageUrl)
parsed = BeautifulSoup(page,'html.parser')

#f = open('data','r')
#data = f.read()
data = json.loads(str(parsed))

print('assessing negative risk at ' + data['markets'][0]['timeStamp'])

for market in data['markets']:
    contracts = market['contracts']
    if len(contracts) < 2:
        continue
    risk = 0
    for item in contracts:
#        print('hhh')
#        print(item)
#        print(item['bestBuyNoCost'])
        if item['bestBuyNoCost'] is None:
            continue
        risk += 1 - float(item['bestBuyNoCost'])
    risk *= 100
    if risk >= 108:
        print('market: ' + market['name'] + ' (id: ' + str(market['id']) + ')')
        print('risk: ' + str(round(risk)))

