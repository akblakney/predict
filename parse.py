import sys
import json

# contract for a given market
# includes current price statistics
# includes shares owned
class Contract:
    def __init__(self,name, yes,no):
        self.name = name
        self.buyYesPrice = yes
        self.buyNoPrice = no
        

# snapshot for a market
# list of contracts includes current prices for each
# and number and type owned
class MarketSnapshot:
    def __init__(self, name):
        self.name = name
        self.entries = []
    def addContract(self,name, buyYesPrice,buyNoPrice):
        self.entries.append(Contract(name, buyYesPrice,buyNoPrice))

# stock owned in a market
class Stock:
    def __init__(self, initSnapshot, 

class Portfolio:
    # shares is a dict
    # {
    #   'contract1' :
    #     {
    #       'shareType' : 'yes/no'
    #       'numberOfShares' : number
    #     },
    #     ...
    #   'contract n' : {...}
    def __init__(self, initSnapshot, shares):
        self.initSnapshot = initSnapshot
        




f = open('data','r')
data = f.read()
data = json.loads(data)

snapshots = []
queries = sys.argv[1:]

# populate snapshots with relevant market snapshots
for market in data['markets']:
    for q in queries:
        if market['id'] == int(q):

            # create MarketSnapshot object
            snap = MarketSnapshot(market['shortName'])
            for contract in market['contracts']:
                print(contract)
                snap.addContract(contract['shortName'],contract['bestBuyYesCost'],
                        contract['bestBuyNoCost'])
            snapshots.append(snap)


