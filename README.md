![](https://travis-ci.org/sdelrio/claymore-exporter.svg?branch=master)

# Claymore prometheus exporter

The script will get values from the IP where Claymore is running and export on port default 8601 for prometheus metrics.

# Usage

```
 claymore [-h] -t <ip> [-f <seconds>] [-p <port>]
```
- `-h` Help
- `-t` IP address where claymore is running
- `-f` Seconds to wait on each measure. Default 1 second
- `-p` port to listen (where prometheus will connect). Default port 8110

Sample:
```
./claymore -t 192.168.1.34 -f 2 -p 8601
```

# Grafana sample

You can get later the data exported to prometheus to use into grafana like this:

![](img/grafana-claymore-exporter.png?raw=true "Grafana Screenshot")
