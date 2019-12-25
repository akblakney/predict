#!/bin/bash

user=$1
now=$(date +%s)
logfile="twitterdata/${user}-${now}"

echo $logfile
twitterscraper $user --user -o ${logfile}
