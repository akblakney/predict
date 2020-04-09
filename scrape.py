from urllib.request import urlopen
from bs4 import BeautifulSoup
#from twisted.internet import task, reactor
import json
import time

pageUrl = 'https://www.predictit.org/api/marketdata/all/'


timeout = 60.0 # Sixty seconds

def doWork():
    page = urlopen(pageUrl)
    parsed = BeautifulSoup(page,'html.parser')
    data = json.loads(str(parsed))
    #filename = 'marketdata/' + data['markets'][0]['timeStamp']
    filename = str(time.time())
    filename = filename.split('.')[0]
    filename = 'marketdata/' + filename
    f = open(filename, 'w')
    print('writing to ' + filename)
    f.write(str(parsed))
    f.close()
    pass

#l = task.LoopingCall(doWork)
#l.start(timeout) # call every sixty seconds

#reactor.run()


starttime=time.time()
while True:
    doWork()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
