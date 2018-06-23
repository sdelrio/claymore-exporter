#!/usr/bin/env python

import json
import socket
import select

timeout = 5

# Check if IP is valid

def validIP(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except socket.error:
        raise ValueError("Invalid IP Address.")
    return ip

# Sample for getting data from Claymore
# $ echo '{"id":0,"jsonrpc":"2.0","method":"miner_getstat1"}' | nc 192.168.1.34 3333
#
# Return Value:
# {"id": 0, "error": null, "result": ["9.3 - ETH", "25", "32490;6;0", "26799;5690", "649800;9;0", "535999;113801", "", "eth-eu1.nanopool.org:9999;sia-eu1.nanopool.org:7777", "0;0;0;0"]}
# {u'result': [u'11.3 - ETH', u'676', u'116239;459;0', u'29161;29163;27806;30108', u'0;0;0', u'off;off;off;off', u'64;40;67;40;65;43;73;33', u'eu1.nanopool.org:9999', u'0;0;0;0'], u'id': 0, u'error': None}

def netcat(hostname, port, content):
    """ Netcat equivalent to get data from Claymore. Normal http get doesn't works."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.settimeout(timeout)
        s.connect((hostname, port))
        s.sendall(content)
        s.shutdown(socket.SHUT_WR)
        s.setblocking(0)
        fulltext = ''
        while 1:
            ready = select.select([s], [], [], timeout)
            if ready[0]:
                data = s.recv(4096)
            if data == "":
                break
            fulltext += data
    except socket.error, e:
        fulltext='{"error": true, "id": 0, "result": ["No client", "6", "0;0;0", "0;0", "0;0;0", "0;0", "0;0;0;0", "-;--", "0;0;0;0"]}'
        print "Socket error: ", e
    except IOError, e:
        fulltext='{"error": true, "id": 0, "result": ["No client", "6", "0;0;0", "0;0", "0;0;0", "0;0", "0;0;0;0", "-;--", "0;0;0;0"]}'
        print "IOError: error: ", e
    finally:
        s.close()
    return parse_response(fulltext)


def parse_response(data):
    """ Get json from data."""
    received_data = json.loads(data)
    return received_data

