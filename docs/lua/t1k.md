# *t1k*: Lua implementation of the T1K protocol for Chaitin/SafeLine WAF


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-t1k
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-t1k
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-t1k [v1.1.5](https://github.com/chaitin/lua-resty-t1k/releases/tag/v1.1.5){target=_blank} 
released on Jul 04 2024.
    
<hr />

[![LuaRocks](https://img.shields.io/luarocks/v/blaisewang/lua-resty-t1k?style=flat-square)](https://luarocks.org/modules/blaisewang/lua-resty-t1k)
[![Releases](https://img.shields.io/github/v/release/chaitin/lua-resty-t1k?style=flat-square)](https://github.com/chaitin/lua-resty-t1k/releases)
[![License](https://img.shields.io/github/license/chaitin/lua-resty-t1k?color=ff69b4&style=flat-square)](https://github.com/chaitin/lua-resty-t1k/blob/main/LICENSE)

## Name

Lua implementation of the T1K protocol for [Chaitin/SafeLine](https://github.com/chaitin/safeline) Web Application Firewall.

## Status

Production ready.

[![Test](https://img.shields.io/github/actions/workflow/status/chaitin/lua-resty-t1k/test.yml?logo=github&style=flat-square)](https://github.com/chaitin/lua-resty-t1k/actions)

## Synopsis

```lua
location / {
    access_by_lua_block {
        local t1k = require "resty.t1k"

        local t = {
            mode = "block",                            -- block or monitor or off, default off
            host = "unix:/workdir/snserver.sock",      -- required, SafeLine WAF detection service host, unix domain socket, IP, or domain is supported, string
            port = 8000,                               -- required when the host is an IP or domain, SafeLine WAF detection service port, integer
            connect_timeout = 1000,                    -- connect timeout, in milliseconds, integer, default 1s (1000ms)
            send_timeout = 1000,                       -- send timeout, in milliseconds, integer, default 1s (1000ms)
            read_timeout = 1000,                       -- read timeout, in milliseconds, integer, default 1s (1000ms)
            req_body_size = 1024,                      -- request body size, in KB, integer, default 1MB (1024KB)
            keepalive_size = 256,                      -- maximum concurrent idle connections to the SafeLine WAF detection service, integer, default 256
            keepalive_timeout = 60000,                 -- idle connection timeout, in milliseconds, integer, default 60s (60000ms)
            remote_addr = "http_x_forwarded_for: 1",   -- remote address from ngx.var.VARIABLE, string, default from ngx.var.remote_addr
        }

        local ok, err, _ = t1k.do_access(t, true)
        if not ok then 
            ngx.log(ngx.ERR, err)
        end
    }

    header_filter_by_lua_block {
        local t1k = require "resty.t1k"
        t1k.do_header_filter()
    }
}
```

## Lua Resty T1K vs. C T1K

[C T1K](https://t1k.chaitin.com/), as part of SafeLine's enterprise edition, is a deployment mode crafted in C language for enhanced performance.
It is compatible with all versions of Nginx and does not require deployment via OpenResty (lua_nginx_module).

|                       | Lua Resty T1K | C T1K |
|-----------------------|---------------|-------|
| Request Detection     | ✅             | ✅     |
| Response Detection    | ❌             | ✅     |
| Health Checks*        | ❌             | ✅     |
| Cookie Protection     | ❌             | ✅     |
| Bot Protection        | ❌             | ✅     |
| Proxy-side Statistics | ❌             | ✅     |

&ast; APISIX implements health check functionality for the `chaitin-waf` plugin. For more information, please see the [chaitin-waf documentation](https://apisix.apache.org/docs/apisix/next/plugins/chaitin-waf/).

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-t1k](https://github.com/chaitin/lua-resty-t1k){target=_blank}.