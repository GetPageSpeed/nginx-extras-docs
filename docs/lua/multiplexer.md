# *multiplexer*: Transparent port service multiplexer for stream subsystem


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-multiplexer
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-multiplexer
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-multiplexer [v0.2](https://github.com/fffonion/lua-resty-multiplexer/releases/tag/0.02){target=_blank} 
released on Aug 31 2020.
    
<hr />

lua-resty-multiplexer - Transparent port service multiplexer for stream subsystem 

## Description

This library implemented a transparent port service multiplexer, which can be used to run multiple TCP services on the same port.

Note that nginx [stream module](https://nginx.org/en/docs/stream/ngx_stream_core_module.html) and [stream-lua-nginx-module](https://github.com/openresty/stream-lua-nginx-module) is required.

Tested on Openresty >= 1.13.6.1.

With OpenResty 1.13.6.1, a customed [patch](patches/stream-lua-readpartial.patch) from [@fcicq](https://github.com/fcicq) is needed. The origin discussion can be found [here](https://github.com/fffonion/lua-resty-sniproxy/issues/1). And native
proxying is not supported as `reqsock:peek` is missing.

Starting OpenResty 1.15.8.1, only native proxying is supported and no patch is needed. Lua land proxying will be
possible when stream-lua-nginx-module implemented `tcpsock:receiveany`.

## Status

Experimental.

## Synopsis


```lua
stream {
    init_by_lua_block {
        local mul = require("resty.multiplexer")
        mul.load_protocols(
            "http", "ssh", "dns", "tls", "xmpp"
        )
        mul.set_rules(
            {{"client-host", "10.0.0.1"}, "internal-host", 80},
            {{"protocol", "http"}, {"client-host", "10.0.0.2"}, "internal-host", 8001},
            {{"protocol", "http"}, "example.com", 80},
            {{"protocol", "ssh"}, "github.com", 22},
            {{"protocol", "dns"}, "1.1.1.1", 53},
            {{"protocol", "tls"}, {"time", nil}, "twitter.com", 443},
            {{"protocol", "tls"}, "www.google.com", 443},
            {{"default", nil}, "127.0.0.1", 80}
        )
        mul.matcher_config.time = {
            minute_match = {0, 30},
            minute_not_match = {{31, 59}},
        }
    }

    resolver 8.8.8.8;

    # for OpenResty >= 1.13.6.1, native Nginx proxying
    lua_add_variable $multiplexer_upstream;
    server {
            error_log /var/log/nginx/multiplexer-error.log error;
            listen 443;

            resolver 8.8.8.8;

            preread_by_lua_block {
                local mul = require("resty.multiplexer")
                local mp = mul:new()
                mp:preread_by()
            }
            proxy_pass $multiplexer_upstream;
    }

    # for OpenResty < 1.13.6.1, Lua land proxying
    server {
            error_log /var/log/nginx/multiplexer-error.log error;
            listen 443;

            resolver 8.8.8.8;

            server {
                listen 80;
                content_by_lua_block {
                    local mul = require("resty.multiplexer")
                    local mp = mul:new()
                    mp:content_by()
                }
            }
    }
}
```

This module consists of two parts: protocol identifiers and matchers.

Protocol identifies need to loaded through `load_protocols` in `init_by_lua_block` directive. See [protocol](#protocol) section for currently supported protocols and guide to add a new protocol.

Rules are defined through `set_rules` to route traffic to different upstreams. For every matcher that is defined in the rule, the corresponding matcher is loaded automatically. See [matcher](#matcher) section for currently implmented matchers and guide to add a new matcher.

See [API](#api) section for syntax of `load_protocols` and `set_rules`.

The rules defined is prioritized. In the example above, we defined a rule such that:

- If client address is `10.0.0.1`, proxy to **internal-host.com:80**
- If protocol is `HTTP` and client address is `10.0.0.2`, proxy to **internal-host:8001**
- If protocol is `SSH`, proxy to **github.com:22**
- If protocol is `DNS`, proxy to **1.1.1.1:53**
- If protocol is `SSL/TLS` and current minute is between **0** and **30**,  proxy to **twitter:443**
- If protocol is `SSL/TLS` and current minute is between **31** and **59**, proxy to **www.google.com:443**
- Otherwise, proxy to **127.0.0.1:80**


## Protocol

The protocol part analyzes the first request that is sent from client and try to match it using known protocol signatures.

Currently supported: `dns`, `http`, `ssh`, `tls`, `xmpp`. Based on the bytes of signature, each protocol may have different possibilities to be falsely identified.

| Protocol  |  Length of signature |   False rate  |
|---|---|---|
| dns  |  9 1/4 | 5.29e-23  |
| http  | 4  |  2.33e-10 |
| ssh  |  4  |  2.33e-10 |
| tls  |  6 |  3.55e-15 |
| xmpp  |  6 in 8 1/4 |  ? |


## Add new protocol

Create a new `protocol_name.lua` file under `resty/multiplexer/protocol` in the format of:

```lua
return {
    required_bytes = ?,
    check = function(buf)
    -- check with the buf and return true if the protocol is identified
    end
}
```

`required_bytes` is the length of bytes we need to read before identifying the protocol. 


## Matcher

## client-host

Match if `$remote_addr` equals to expected value.

## protocol

Match if protocol equals to expected value.

## time

Match if current time is in configured range in `mul.matcher_config.time`. If no range is defined, the matcher will always return *false*.

For example, to match year `2018`, `January` and `March` and hour `6` to `24` except for hour `12`:

```lua
 init_by_lua_block {
    local mul = require("resty.multiplexer")
    mul.load_protocols(
        "http", "ssh", "dns", "tls", "xmpp"
    )
    mul.set_rules(
        {{"time", ""}, "twitter.com", 443}
    )
    mul.matcher_config.time = {
        year_match = {2018},
        year_not_match = {},
        month_match = {{1}, {3}},
        month_not_match = {},
        day_match = {}, -- day of month
        day_not_match = {},
        hour_match = {{6, 24}},
        hour_not_match = {{12}},
        minute_match = {},
        minute_not_match = {},
        second_match = {},
        second_not_match = {},
    }
 }
```

## default

Always matches.

## Add new matcher

Create a new `matcher_name.lua` file under `resty/multiplexer/matchers` in the format of:

```lua
local _M = {}

function _M.match(protocol, expected)
    -- return true if it's a match
end

return _M
```

Where `protocol` is the identified protocol in lowercase string, and `expected` is the expected value for this matcher defined in `set_rules`.


## API

## multiplexer.new
**syntax:** *multiplexer:new(connect_timeout, send_timeout, read_timeout)*

Initialize the multiplexer instance. And sets the connect timeout thresold, send timeout threshold, and read timeout threshold, as in [tcpsock:settimeouts](https://github.com/openresty/lua-nginx-module#tcpsocksettimeouts).


## multiplexer.load_protocols
**syntax:** *multiplexer:load_protocols("protocol-1", "protocol-2", ...)*

Load the protocol modules into memory.

Supported protocols can be found in [protocol](lib/resty/multiplexer/protocol).

## multiplexer.set_rules
**syntax:** *multiplexer:set_rules(rule1, rule2, ...)*

Load rules in order. Each *rule* is an array table that is in the format of:

```lua
{{"matcher-1", "expected-value-1"}, {"matcher-2", "expected-value-2"}, ..., "upstream_host", upstream_port}
```

Supported matchers can be found in [matcher](lib/resty/multiplexer/matcher).


## See Also
* [Original patch to add the read partial mode](https://gist.github.com/fcicq/82e1c6d0c85cbc2d3f8e9f1523bfd1d1)
* [stream-lua-nginx-module](https://github.com/openresty/stream-lua-nginx-module)
* [yrutschle/sslh](https://github.com/yrutschle/sslh)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-multiplexer](https://github.com/fffonion/lua-resty-multiplexer){target=_blank}.