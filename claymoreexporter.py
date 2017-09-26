#!/usr/bin/env python

from prometheus_client import start_http_server, Gauge, Counter
import argparse
import httplib
import time
import collections
import json
import socket
import select

version = 0.49
timeout = 5

# Check if IP is valid
def validIP(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except socket.error:
        parser.error("Invalid IP Address.")
    return ip

# Parse commandline arguments
parser = argparse.ArgumentParser(description="Claymore Prometheus exporter v" + str(version))
parser.add_argument("-t", "--target", metavar="<ip>", required=True, help="Target IP Address", type=validIP)
parser.add_argument("-f", "--frequency", metavar="<seconds>", required=False, help="Interval in seconds between checking measures", default=1, type=int)
parser.add_argument("-p", "--port", metavar="<port>", required=False, help="Port for listenin", default=8601, type=int)
parser.add_argument("-c", "--claymoreport", metavar="<claymoreport>", required=False, help="Port where claymore will be watching", default=3333, type=int)
args = parser.parse_args()

# Set target IP, port and command to send
ip = args.target
listen_port = args.port
sleep_time = args.frequency
port = args.claymoreport

received_data = {'claymore_version': '', 'running_time': '', 'gpu': {} , 'coin1': {}, 'coin2': {}}

REQUEST_GPU_TEMP  = Gauge('claymore_gpu_temp','Claymore GPU temp', ['gpu_id'])
REQUEST_GPU_FAN  = Gauge('claymore_gpu_fan','Claymore GPU fan', ['gpu_id'])
REQUEST_GPU_HR1  = Gauge('claymore_gpu_hashrate_1','Claymore GPU hashrate1', ['gpu_id'])
REQUEST_GPU_HR2  = Gauge('claymore_gpu_hashrate_2','Claymore GPU hashrate2', ['gpu_id'])

REQUEST_COIN1_SHARES = Counter('claymore_coin1_shares','Claymore coin1 share')
REQUEST_COIN1_REJECT = Counter('claymore_coin1_shares_reject','Claymore coin1 share reject')
REQUEST_COIN2_SHARES = Counter('claymore_coin2_shares','Claymore coin2 share')
REQUEST_COIN2_REJECT = Counter('claymore_coin2_shares_reject','Claymore coin2 share reject')

# Sample for getting data from Claymore
# $ echo '{"id":0,"jsonrpc":"2.0","method":"miner_getstat1"}' | nc 192.168.1.34 3333
#
# Return Value:
# {"id": 0, "error": null, "result": ["9.3 - ETH", "25", "32490;6;0", "26799;5690", "649800;9;0", "535999;113801", "", "eth-eu1.nanopool.org:9999;sia-eu1.nanopool.org:7777", "0;0;0;0"]}

def netcat(hostname, port, content):
    """ Netcat equivalent to get data from Claymore. Normal http get doesn't works."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
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

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(listen_port)

    # Main loop
    while True:
        data = netcat(ip, port, '{"id":0,"jsonrpc":"2.0","method":"miner_getstat1"}' )
        received_data['claymore_version'] = data['result'][0]
        received_data['running_time'] = data['result'][1]

        total_coin_array = data['result'][2].split(';')
        received_data['coin1']['total_hashrate'] = total_coin_array[0]

        if 'shares' in received_data['coin1']:
            last_share1  = int(received_data['coin1']['shares'])
        else:
            last_share1  = int(total_coin_array[1])

        if 'reject' in received_data['coin1']:
            last_reject1 = int(received_data['coin1']['reject'])
        else:
            last_reject1 = int(total_coin_array[2])

        received_data['coin1']['shares'] = total_coin_array[1]
        received_data['coin1']['reject'] = total_coin_array[2]

        if ( int(received_data['coin1']['shares']) > last_share1 ):
            REQUEST_COIN1_SHARES.inc( int(received_data['coin1']['shares']) - last_share1 )

        if ( int(received_data['coin1']['reject']) > last_reject1 ):
            REQUEST_COIN1_REJECT.inc( int(received_data['coin1']['reject']) - last_reject1 )


        total_coin_array = data['result'][4].split(';')
        received_data['coin2']['total_hashrate'] = total_coin_array[0]

        if 'shares' in received_data['coin2']:
            last_share2 = int(received_data['coin2']['shares'])
        else:
            last_share2 = int(total_coin_array[1])

        if 'reject' in received_data['coin2']:
            last_reject2 = int(received_data['coin2']['reject'])
        else:
            last_reject2 = int(total_coin_array[2])

        received_data['coin2']['shares'] = total_coin_array[1]
        received_data['coin2']['reject'] = total_coin_array[2]

        if ( int(received_data['coin2']['shares']) > last_share2 ):
            REQUEST_COIN2_SHARES.inc( int(received_data['coin2']['shares']) - last_share2 )

        if ( int(received_data['coin2']['reject']) > last_reject2 ):
            REQUEST_COIN2_REJECT.inc( int(received_data['coin2']['reject']) - last_reject2 )

        id = 0
        for i in data['result'][3].split(';'):
            received_data['gpu'][id] = {}
            if (i == "off" ):
                received_data['gpu'][id]['hashrate1'] = 0
            else:
                received_data['gpu'][id]['hashrate1'] = i
            id+=1

        id = 0
        for i in data['result'][5].split(';'):
            if (i == "off" ):
                received_data['gpu'][id]['hashrate2'] = 0
            else:
                received_data['gpu'][id]['hashrate2'] = i
            id+=1

        tf = data['result'][6].split(';')

        for i in range (0,len(received_data['gpu'])):
            received_data['gpu'][i]['temp'] = 0
            received_data['gpu'][i]['fan']  = 0

        id = 0
        for i in range (0,len(tf)/2):
            received_data['gpu'][id]['temp'] = tf[i*2]
            received_data['gpu'][id]['fan']  = tf[(i*2)+1]
            id+=1

        print received_data

        for i in range (0,len(received_data['gpu'])):
            REQUEST_GPU_TEMP.labels(i).set(received_data['gpu'][i]['temp'])
            REQUEST_GPU_FAN.labels(i).set(received_data['gpu'][i]['fan'])
            REQUEST_GPU_HR1.labels(i).set(received_data['gpu'][i]['hashrate1'])
            REQUEST_GPU_HR2.labels(i).set(received_data['gpu'][i]['hashrate2'])

        time.sleep(sleep_time)

