# Docker Nginx Proxy

This package reads in a minimal proxy configuration via a yaml file (/config.yml) and uses it to generate an nginx configuration and start the service.

It also supports websockets!


## Usage
You can either create a config file, or use environment variables, or a mixture of both.
Environment variables override the values specified in the config file if they exist in both. The exception to this is vhosts, any vhosts defined on the command line are just appended to the config.

### Config file
Bind a config file to `/config.yml` with content similar to the below:
```
tld: foo.com
port: 8080
services:
  - name: "transmission"
    host: "vpn:9091"
  - name: "couchpotato"
    host: "vpn:5050"
```

## Environment variables
The following environment variables map to the config file example above. The same config above using only environment variables looks like this:

```
DNS_TLD=foo.com
PROXY_PORT=8080
PROXY_ENDPOINTS="transmission,vpn:9091;couchpotato,vpn:5050"
```
