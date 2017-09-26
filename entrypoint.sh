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

# Entrypoint that connects to IP $IP:$CLAYMOREPORT, each $FREQUENCY seconds and listen on port $LISTENPORT

python /usr/local/bin/claymoreexporter.py -t $IP -f $FREQUENCY -p $LISTENPORT -c $CLAYMOREPORT

