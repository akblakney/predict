import sys

def parseArgs():
    datapath = 'tweetdata/'

    if '--dir' in sys.argv:
        datapath = sys.argv[sys.argv.index('--dir') + 1]
    if '--user' not in sys.argv:
        print('error: no user given')
        sys.exit()
    username = sys.argv[sys.argv.index('--user') + 1]

    return datapath, username

datapath, username = parseArgs()



