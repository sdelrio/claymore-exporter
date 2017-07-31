#!/bin/bash

if [ -z "$IP" ]; then
    echo "Enviroment var 'IP' is required"
    exit -1
fi

if [ -z "$FREQUENCY" ]; then
    FREQUENCY=1
fi

if [ -z "$LISTENPORT" ]; then
    LISTENPORT=8601
fi

if [ -z "$CLAYMOREPORT" ]; then
    CLAYMOREPORT=3333
fi


python /usr/local/bin/claymore-exporter.py -t $IP -f $FREQUENCY -p $LISTENPORT -c $CLAYMOREPORT

