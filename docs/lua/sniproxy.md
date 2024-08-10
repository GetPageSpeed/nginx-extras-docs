# *sniproxy*: SNI Proxy based on stream-lua-nginx-module


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-sniproxy
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-sniproxy
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-sniproxy [v0.22](https://github.com/fffonion/lua-resty-sniproxy/releases/tag/0.22){target=_blank} 
released on Aug 31 2020.
    
<hr />

lua-resty-sniproxy - SNI Proxy based on the ngx_lua cosocket API

## Description

This library is an [SNI](https://en.wikipedia.org/wiki/Server_Name_Indication) proxy written in Lua. TLS parsing part is rewritten from [dlundquist/sniproxy](https://github.com/dlundquist/sniproxy)

Note that nginx [stream module](https://nginx.org/en/docs/stream/ngx_stream_core_module.html) and [ngx_stream_lua_module](https://github.com/openresty/stream-lua-nginx-module) is required.

Tested on Openresty >= 1.9.15.1.

## Status

Experimental.

## Synopsis


```nginx
stream {
    init_by_lua_block {
        local sni = require("resty.sniproxy")
        sni.rules = { 
            {"www.google.com", "www.google.com", 443},
            {"www.facebook.com", "9.8.7.6", 443},
            {"api.twitter.com", "1.2.3.4"},
            {".+.twitter.com", nil, 443},
            -- to activate this rule, you must use Lua land proxying
            -- {"some.service.svc", "unix:/var/run/nginx-proxy-proto.sock", nil, sni.SNI_PROXY_PROTOCOL_UPSTREAM},
            -- {"some2.service.svc", "unix:/var/run/nginx-proxy-proto.sock", nil,
            --                            sni.SNI_PROXY_PROTOCOL_UPSTREAM + sni.SNI_PROXY_PROTOCOL},
            {".", "unix:/var/run/nginx-default.sock"}
        }   
    }

    # for OpenResty >= 1.13.6.1, native Nginx proxying
    lua_add_variable $sniproxy_upstream;
    server {
            error_log /var/log/nginx/sniproxy-error.log error;
            listen 443;

            resolver 8.8.8.8;

            prepread_by_lua_block {
                    local sni = require("resty.sniproxy")
                    local sp = sni:new()
                    sp:preread_by()
            }
            proxy_pass $sniproxy_upstream;
    }

    # for OpenResty < 1.13.6.1 or `flags` are configured, Lua land proxying
    server {
            error_log /var/log/nginx/sniproxy-error.log error;
            listen 443;

            resolver 8.8.8.8;

            content_by_lua_block {
                    local sni = require("resty.sniproxy")
                    local sp = sni:new()
                    sp:content_by()
            }
    }
}
```

A Lua array table `sni_rules` should be defined in the `init_worker_by_lua_block` directive.

The first value can be either whole host name or regular expression. Use `.` for a default host name. If no entry is matched, connection will be closed.

The second and third values are target host name and port. A host can be DNS name, IP address or UNIX domain socket path. If host is not defined or set to `nil`, **server_name** in SNI will be used. If the port is not defined or set to `nil` , **443** will be used.

The forth value is the flags to use. Available flags are:


        sni.SNI_PROXY_PROTOCOL -- use client address received from proxy protocol to send to upstream
        sni.SNI_PROXY_PROTOCOL_UPSTREAM -- send proxy protocol v1 handshake to upstream


To use flags, the server must be configured to do **Lua land proxying** (see above example).


Rules are applied with the priority as its occurrence sequence in the table. In the example above, **api.twitter.com** will match the third rule **api.twitter.com** rather than the fourth **.+.twitter.com**.

If the protocol version is less than TLSv1 (eg. SSLv3, SSLv2), connection will be closed, since SNI extension is not supported in these versions.


## See Also
* the ngx_stream_lua_module: https://github.com/openresty/stream-lua-nginx-module
* [dlundquist/sniproxy] (https://github.com/dlundquist/sniproxy)
* [ngx_stream_ssl_preread_module] (https://nginx.org/en/docs/stream/ngx_stream_ssl_preread_module.html) is available since Nginx 1.11.5 as an alternative to this module.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-sniproxy](https://github.com/fffonion/lua-resty-sniproxy){target=_blank}.