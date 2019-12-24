import json

f = open('tweets.json', 'r')
data = f.read()
data = json.loads(data)

count = 0
timestamps = []
for tweet in data:
    timestamps.append(int(tweet['timestamp_epochs']))

timestamps.sort()
for timestamp in timestamps:
    print(timestamp)


