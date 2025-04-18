---

title: "DNS resolver for nginx-module-lua"
description: "RPM package lua-resty-dns: DNS resolver for nginx-module-lua"

---
  
# *dns*: DNS resolver for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-dns
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-dns
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-dns [v0.23](https://github.com/openresty/lua-resty-dns/releases/tag/v0.23){target=_blank} 
released on Aug 06 2023.
    
<hr />

lua-resty-dns - Lua DNS resolver for the ngx_lua based on the cosocket API

## Status

This library is considered production ready.

## Description

This Lua library provides a DNS resolver for the ngx_lua nginx module:

https://github.com/openresty/lua-nginx-module/#readme

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

Note that at least [ngx_lua 0.5.12](https://github.com/openresty/lua-nginx-module/tags) or [OpenResty 1.2.1.11](http://openresty.org/#Download) is required.

Also, the [bit library](http://bitop.luajit.org/) is also required. If you're using LuaJIT 2.0 with ngx_lua, then the `bit` library is already available by default.

Note that, this library is bundled and enabled by default in the [OpenResty bundle](http://openresty.org/).

IMPORTANT: to be able to generate unique ids, the random generator must be properly seeded using `math.randomseed` prior to using this module.

## Synopsis

```nginx
server {
    location = /dns {
        content_by_lua_block {
            local resolver = require "resty.dns.resolver"
            local r, err = resolver:new{
                nameservers = {"8.8.8.8", {"8.8.4.4", 53} },
                retrans = 5,  -- 5 retransmissions on receive timeout
                timeout = 2000,  -- 2 sec
                no_random = true, -- always start with first nameserver
            }

            if not r then
                ngx.say("failed to instantiate the resolver: ", err)
                return
            end

            local answers, err, tries = r:query("www.google.com", nil, {})
            if not answers then
                ngx.say("failed to query the DNS server: ", err)
                ngx.say("retry historie:\n  ", table.concat(tries, "\n  "))
                return
            end

            if answers.errcode then
                ngx.say("server returned error code: ", answers.errcode,
                        ": ", answers.errstr)
            end

            for i, ans in ipairs(answers) do
                ngx.say(ans.name, " ", ans.address or ans.cname,
                        " type:", ans.type, " class:", ans.class,
                        " ttl:", ans.ttl)
            end
        }
    }
}
```

## Methods

## new
`syntax: r, err = class:new(opts)`

Creates a dns.resolver object. Returns `nil` and a message string on error.

It accepts a `opts` table argument. The following options are supported:

* `nameservers`

	a list of nameservers to be used. Each nameserver entry can be either a single hostname string or a table holding both the hostname string and the port number. The nameserver is picked up by a simple round-robin algorithm for each `query` method call. This option is required.
* `retrans`

	the total number of times of retransmitting the DNS request when receiving a DNS response times out according to the `timeout` setting. Defaults to `5` times. When trying to retransmit the query, the next nameserver according to the round-robin algorithm will be picked up.
* `timeout`

	the time in milliseconds for waiting for the response for a single attempt of request transmission. note that this is ''not'' the maximal total waiting time before giving up, the maximal total waiting time can be calculated by the expression `timeout x retrans`. The `timeout` setting can also be changed by calling the `set_timeout` method. The default `timeout` setting is 2000 milliseconds, or 2 seconds.
* `no_recurse`

	a boolean flag controls whether to disable the "recursion desired" (RD) flag in the UDP request. Defaults to `false`.
* `no_random`

	a boolean flag controls whether to randomly pick the nameserver to query first, if `true` will always start with the first nameserver listed. Defaults to `false`.

## destroy
`syntax: r:destroy()`

Destroy the dns.resolver object by releasing all the internal occupied resources.

## query
`syntax: answers, err, tries? = r:query(name, options?, tries?)`

Performs a DNS standard query to the nameservers specified by the `new` method,
and returns all the answer records in an array-like Lua table. In case of errors, it will
return `nil` and a string describing the error instead.

If the server returns a non-zero error code, the fields `errcode` and `errstr` will be set accordingly in the Lua table returned.

Each entry in the `answers` returned table value is also a hash-like Lua table
which usually takes some of the following fields:

* `name`

	The resource record name.
* `type`

	The current resource record type, possible values are `1` (`TYPE_A`), `5` (`TYPE_CNAME`), `28` (`TYPE_AAAA`), and any other values allowed by RFC 1035.
* `address`

	The IPv4 or IPv6 address in their textual representations when the resource record type is either `1` (`TYPE_A`) or `28` (`TYPE_AAAA`), respectively. Successive 16-bit zero groups in IPv6 addresses will not be compressed by default, if you want that, you need to call the `compress_ipv6_addr` static method instead.
* `section`

	The identifier of the section that the current answer record belongs to. Possible values are `1` (`SECTION_AN`), `2` (`SECTION_NS`), and `3` (`SECTION_AR`).
* `cname`

	The (decoded) record data value for `CNAME` resource records. Only present for `CNAME` records.
* `ttl`

	The time-to-live (TTL) value in seconds for the current resource record.
* `class`

	The current resource record class, possible values are `1` (`CLASS_IN`) or any other values allowed by RFC 1035.
* `preference`

	The preference integer number for `MX` resource records. Only present for `MX` type records.
* `exchange`

	The exchange domain name for `MX` resource records. Only present for `MX` type records.
* `nsdname`

	A domain-name which specifies a host which should be authoritative for the specified class and domain. Usually present for `NS` type records.
* `rdata`

	The raw resource data (RDATA) for resource records that are not recognized.
* `txt`

	The record value for `TXT` records. When there is only one character string in this record, then this field takes a single Lua string. Otherwise this field takes a Lua table holding all the strings.
* `ptrdname`

	The record value for `PTR` records.

This method also takes an optional `options` argument table, which takes the following fields:

* `qtype`

	The type of the question. Possible values are `1` (`TYPE_A`), `5` (`TYPE_CNAME`), `28` (`TYPE_AAAA`), or any other QTYPE value specified by RFC 1035 and RFC 3596. Default to `1` (`TYPE_A`).
* `authority_section`

	When set to a true value, the `answers` return value includes the `Authority` section of the DNS response. Default to `false`.
* `additional_section`

	When set to a true value, the `answers` return value includes the `Additional` section of the DNS response. Default to `false`.

The optional parameter `tries` can be provided as an empty table, and will be
returned as a third result. The table will be an array with the error message
for each (if any) failed try.

When data truncation happens, the resolver will automatically retry using the TCP transport mode
to query the current nameserver. All TCP connections are short lived.

## tcp_query
`syntax: answers, err = r:tcp_query(name, options?)`

Just like the `query` method, but enforce the TCP transport mode instead of UDP.

All TCP connections are short lived.

Here is an example:

```lua
    local resolver = require "resty.dns.resolver"

    local r, err = resolver:new{
        nameservers = { "8.8.8.8" }
    }
    if not r then
        ngx.say("failed to instantiate resolver: ", err)
        return
    end

    local ans, err = r:tcp_query("www.google.com", { qtype = r.TYPE_A })
    if not ans then
        ngx.say("failed to query: ", err)
        return
    end

    local cjson = require "cjson"
    ngx.say("records: ", cjson.encode(ans))
```

## set_timeout
`syntax: r:set_timeout(time)`

Overrides the current `timeout` setting by the `time` argument in milliseconds for all the nameserver peers.

## compress_ipv6_addr
`syntax: compressed = resty.dns.resolver.compress_ipv6_addr(address)`

Compresses the successive 16-bit zero groups in the textual format of the IPv6 address.

For example,

```lua
    local resolver = require "resty.dns.resolver"
    local compress = resolver.compress_ipv6_addr
    local new_addr = compress("FF01:0:0:0:0:0:0:101")
```

will yield `FF01::101` in the `new_addr` return value.

## expand_ipv6_addr
`syntax: expanded = resty.dns.resolver.expand_ipv6_addr(address)`

Expands the successive 16-bit zero groups in the textual format of the IPv6 address.

For example,

```lua
    local resolver = require "resty.dns.resolver"
    local expand = resolver.expand_ipv6_addr
    local new_addr = expand("FF01::101")
```

will yield `FF01:0:0:0:0:0:0:101` in the `new_addr` return value.

## arpa_str
`syntax: arpa_record = resty.dns.resolver.arpa_str(address)`

Generates the reverse domain name for PTR lookups for both IPv4 and IPv6 addresses. Compressed IPv6 addresses
will be automatically expanded.

For example,

```lua
    local resolver = require "resty.dns.resolver"
    local ptr4 = resolver.arpa_str("1.2.3.4")
    local ptr6 = resolver.arpa_str("FF01::101")
```

will yield `4.3.2.1.in-addr.arpa` for `ptr4` and `1.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.F.F.ip6.arpa` for `ptr6`.

## reverse_query
`syntax: answers, err = r:reverse_query(address)`

Performs a PTR lookup for both IPv4 and IPv6 addresses. This function is basically a wrapper for the `query` command
which uses the `arpa_str` command to convert the IP address on the fly.

## Constants

## TYPE_A

The `A` resource record type, equal to the decimal number `1`.

## TYPE_NS

The `NS` resource record type, equal to the decimal number `2`.

## TYPE_CNAME

The `CNAME` resource record type, equal to the decimal number `5`.

## TYPE_SOA

The `SOA` resource record type, equal to the decimal number `6`.

## TYPE_PTR

The `PTR` resource record type, equal to the decimal number `12`.

## TYPE_MX

The `MX` resource record type, equal to the decimal number `15`.

## TYPE_TXT

The `TXT` resource record type, equal to the decimal number `16`.

## TYPE_AAAA
`syntax: typ = r.TYPE_AAAA`

The `AAAA` resource record type, equal to the decimal number `28`.

## TYPE_SRV
`syntax: typ = r.TYPE_SRV`

The `SRV` resource record type, equal to the decimal number `33`.

See RFC 2782 for details.

## TYPE_SPF
`syntax: typ = r.TYPE_SPF`

The `SPF` resource record type, equal to the decimal number `99`.

See RFC 4408 for details.

## CLASS_IN
`syntax: class = r.CLASS_IN`

The `Internet` resource record type, equal to the decimal number `1`.

## SECTION_AN
`syntax: stype = r.SECTION_AN`

Identifier of the `Answer` section in the DNS response. Equal to decimal number `1`.

## SECTION_NS
`syntax: stype = r.SECTION_NS`

Identifier of the `Authority` section in the DNS response. Equal to the decimal number `2`.

## SECTION_AR
`syntax: stype = r.SECTION_AR`

Identifier of the `Additional` section in the DNS response. Equal to the decimal number `3`.

## Automatic Error Logging

By default, the underlying [ngx_lua](https://github.com/openresty/lua-nginx-module/#readme) module
does error logging when socket errors happen. If you are already doing proper error
handling in your own Lua code, then you are recommended to disable this automatic error logging by turning off [ngx_lua](https://github.com/openresty/lua-nginx-module/#readme)'s [lua_socket_log_errors](https://github.com/openresty/lua-nginx-module/#lua_socket_log_errors) directive, that is,

```nginx
    lua_socket_log_errors off;
```

## Limitations

* This library cannot be used in code contexts like `set_by_lua*`, `log_by_lua*`, and
`header_filter_by_lua*` where the ngx_lua cosocket API is not available.
* The `resty.dns.resolver` object instance cannot be stored in a Lua variable at the Lua module level,
because it will then be shared by all the concurrent requests handled by the same nginx
 worker process (see
https://github.com/openresty/lua-nginx-module/#data-sharing-within-an-nginx-worker ) and
result in bad race conditions when concurrent requests are trying to use the same `resty.dns.resolver` instance.
You should always initiate `resty.dns.resolver` objects in function local
variables or in the `ngx.ctx` table. These places all have their own data copies for
each request.

## See Also
* the ngx_lua module: https://github.com/openresty/lua-nginx-module/#readme
* the [lua-resty-memcached](https://github.com/agentzh/lua-resty-memcached) library.
* the [lua-resty-redis](https://github.com/agentzh/lua-resty-redis) library.
* the [lua-resty-mysql](https://github.com/agentzh/lua-resty-mysql) library.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-dns](https://github.com/openresty/lua-resty-dns){target=_blank}.