# *dns-server*: Lua DNS server driver for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-dns-server
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-dns-server
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-dns-server [v0.2](https://github.com/vislee/lua-resty-dns-server/releases/tag/v0.02){target=_blank} 
released on Jul 23 2019.
    
<hr />

lua-resty-dns-server - Lua DNS server driver for the OpenResty

## Status

This library is still under early development and is still experimental.

## Description

This Lua library provies a DNS server driver for the ngx_lua nginx module:

https://github.com/openresty/stream-lua-nginx-module/#readme

## Synopsis

```nginx
stream {
    server {
        listen 53 udp;
        content_by_lua_block {
            local server = require 'resty.dns.server'
            local sock, err = ngx.req.socket()
            if not sock then
                ngx.log(ngx.ERR, "failed to get the request socket: ", err)
                return ngx.exit(ngx.ERROR)
            end

            local req, err = sock:receive()
            if not req then
                ngx.log(ngx.ERR, "failed to receive: ", err)
                return ngx.exit(ngx.ERROR)
            end

            local dns = server:new()
            local request, err = dns:decode_request(req)
            if not request then
                ngx.log(ngx.ERR, "failed to decode request: ", err)

                local resp = dns:encode_response()
                local ok, err = sock:send(resp)
                if not ok then
                    ngx.log(ngx.ERR, "failed to send: ", err)
                    ngx.exit(ngx.ERROR)
                end

                return
            end

            local query = request.questions[1]
            ngx.log(ngx.DEBUG, "qname: ", query.qname, " qtype: ", query.qtype)

            local subnet = request.subnet[1]
            if subnet then
                ngx.log(ngx.DEBUG, "subnet addr: ",  subnet.address, " mask: ", subnet.mask, " family: ", subnet.family)
            end

            local cname = "sinacloud.com"

            if query.qtype == server.TYPE_CNAME or
                query.qtype == server.TYPE_AAAA or query.qtype == server.TYPE_A then

                local err = dns:create_cname_answer(query.qname, 600, cname)
                if err then
                    ngx.log(ngx.ERR, "failed to create cname answer: ", err)
                    return
                end
            else
                dns:create_soa_answer("test.com", 600, "a.root-test.com", "vislee.test.com", 1515161223, 1800, 900, 604800, 86400)
            end

            local resp = dns:encode_response()
            local ok, err = sock:send(resp)
            if not ok then
                ngx.log(ngx.ERR, "failed to send: ", err)
                return
            end
        }
    }

    server {
        listen 53;
        content_by_lua_block {
            local bit    = require 'bit'
            local lshift = bit.lshift
            local rshift = bit.rshift
            local band   = bit.band
            local byte   = string.byte
            local char   = string.char
            local server = require 'resty.dns.server'

            local sock, err = ngx.req.socket()
            if not sock then
                ngx.log(ngx.ERR, "failed to get the request socket: ", err)
                return ngx.exit(ngx.ERROR)
            end

            local buf, err = sock:receive(2)
            if not buf then
                ngx.log(ngx.ERR, "failed to receive: ", err)
                return ngx.exit(ngx.ERROR)
            end

            local len_hi = byte(buf, 1)
            local len_lo = byte(buf, 2)
            local len = lshift(len_hi, 8) + len_lo
            local data, err = sock:receive(len)
            if not data then
                ngx.log(ngx.ERR, "failed to receive: ", err)
                return ngx.exit(ngx.ERROR)
            end

            local dns = server:new()
            local request, err = dns:decode_request(data)
            if not request then
                ngx.log(ngx.ERR, "failed to decode dns request: ", err)
                return
            end

            local query = request.questions[1]
            ngx.log(ngx.DEBUG, "qname: ", query.qname, " qtype: ", query.qtype)

            local subnet = request.subnet[1]
            if subnet then
                ngx.log(ngx.DEBUG, "subnet addr: ",  subnet.address, " mask: ", subnet.mask, " family: ", subnet.family)
            end

            if query.qtype == server.TYPE_CNAME or query.qtype == server.TYPE_A then
                dns:create_cname_answer(query.qname, 600, "sinacloud.com")
            elseif query.qtype == server.TYPE_AAAA then
                local resp_header, err = dns:create_response_header(server.RCODE_NOT_IMPLEMENTED)
                resp_header.ra = 0
            else
                dns:create_soa_answer("test.com", 600, "a.root-test.com", "vislee.test.com", 1515161223, 1800, 900, 604800, 86400)
            end

            local resp = dns:encode_response()
            local len = #resp
            local len_hi = char(rshift(len, 8))
            local len_lo = char(band(len, 0xff))

            local ok, err = sock:send({len_hi, len_lo, resp})
            if not ok then
                ngx.log(ngx.ERR, "failed to send: ", err)
                return
            end
            return
        }
    }
}

```

## Methods

## new
`syntax: s, err = class:new()`

Creates a dns.server object. Returns `nil` and an message string on error.

## decode_request
`syntax: request, err = s:decode_request(buf)`

Parse the DNS request.

The request returned the lua table which takes some of the following fields:

* `header`: The `header` is also a lua table which usually takes some of the following fields:

    * `id` : The identifier assigned by the program that generates any kind of query.
    * `qr` : The field specifies whether this message is a query (`0`), or a response (`1`).
    * `opcode` : The field specifies kind of query in this message.
    * `tc` : The field specifies that this message was truncated due to length greater than that permitted on the transmission channel.
    * `rd` : Recursion Desired. If `RD` is set, it directs the name server to pursue the query recursively.
    * `rcode` : response code.
    * `qdcount` : The field specifying the number of entries in the question section.

* `questions` : Each entry in the `questions` is also a lua table which takes some of the following:

    * `qname` : A domain name of query.
    * `qtype` : Specifies the type of the query.
    * `qclass` : Specifies the class of the query. Usually the field is `IN` for the Internet.


## create_a_answer
`syntax: err = s:create_a_answer(name, ttl, ipv4)`

Create the A records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `ipv4`

    The IPv4 address.

## create_aaaa_answer
`syntax: err = s:create_aaaa_answer(name, ttl, ipv6)`

Create the AAAA records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `ipv6`

    The IPv6 address.

## create_cname_answer
`syntax: err = s:create_cname_answer(name, ttl, cname)`

Create the CNAME records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `cname`

    The name for an alias.

## create_txt_answer
`syntax: err = s:create_txt_answer(name, ttl, txt)`

Create the txt records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `txt`

    The text strings.

## create_ns_answer
`syntax: err = s:create_ns_answer(name, ttl, nsdname)`

Create the NS records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `nsdname`

    The specifies a host which should be authoritative for the specified class and domain.

## create_soa_answer
`syntax: err = s:create_soa_answer(name, ttl, mname, rname, serial, refresh, retry, expire, minimum)`

Create the SOA records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `mname`

    The the name server that was the original or primary source of data for this zone.
* `rname`

    The mailbox of the person responsible for this zone.
* `serial`

    The unsigned 32 bit version number of the original copy of the zone.
* `refresh`

    A 32 bit time interval before the zone should be refreshed.
* `retry`

    A 32 bit time interval that should elapse before a failed refresh should be retried.
* `expire`

    A 32 bit time value that specifies the upper limit on the time interval that can elapse before the zone is no longer authoritative.
* `minimum`

    The unsigned 32 bit minimum TTL field that should be exported with any RR from this zone.

## create_mx_answer
`syntax: err = s:create_mx_answer(name, ttl, preference, exchange)`

Create the MX records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `preference`

    The preference of this mail exchange.
* `exchange`

    The mail exchange.

## create_srv_answer
`syntax: err = s:create_srv_answer(name, ttl, priority, weight, port, target)`

Create the SRV records. Returns `nil` or an message string on error.
which usually takes some of the following fields:

* `name`

    The resource record name.
* `ttl`

    The time-to-live (TTL) value in seconds for the current resource record.
* `priority`

    The priority of this target host.
* `weight`

    The weight field specifies a relative weight for entries with the same priority.
* `port`

    The port on this target host of this service.
* `target`

    The domain name of the target host.

## create_response_header
`syntax: resp_header, err = s:create_response_header(rcode)`

## encode_response
`syntax: resp = s:encode_response()`

Encode the DNS answers. Returns an message string on response or `nil`.

## Constants

## TYPE_A

The `A` resource record type, equal to the decimal number `1`.

## TYPE_NS

The `NS` resource record type, equal to the decimal number `2`.

## TYPE_CNAME

The `CNAME` resource record type, equal to the decimal number `5`.

## TYPE_SOA

The `SOA` resource record type, equal to the decimal number `6`.

## TYPE_MX

The `MX` resource record type, equal to the decimal number `15`.

## TYPE_TXT

The `TXT` resource record type, equal to the decimal number `16`.

## TYPE_AAAA
`syntax: typ = s.TYPE_AAAA`

The `AAAA` resource record type, equal to the decimal number `28`.

## TYPE_SRV
`syntax: typ = s.TYPE_SRV`

The `SRV` resource record type, equal to the decimal number `33`.

See RFC 2782 for details.

## TYPE_ANY
`syntax: typ = s.TYPE_ANY`

The all resource record type, equal to the decimal number `255`.

## RCODE_FORMAT_ERROR

## RCODE_NOT_IMPLEMENTED

## See Also
* the stream-lua-nginx-module: https://github.com/openresty/stream-lua-nginx-module/#readme
* the [lua-resty-dns](https://github.com/openresty/lua-resty-dns) library.
* this [ngx_stream_ipdb_module](https://github.com/vislee/ngx_stream_ipdb_module) library can support region resolution. 


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-dns-server](https://github.com/vislee/lua-resty-dns-server){target=_blank}.
