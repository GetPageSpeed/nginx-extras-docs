# *vhost*: Hostname matching library for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-vhost
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-vhost
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-vhost [v0.1](https://github.com/hamishforbes/lua-resty-vhost/releases/tag/v0.01){target=_blank} 
released on Oct 14 2016.
    
<hr />

Library for matching hostnames to values.
Supports wildcard and `.hostname.tld` syntax in the same way as Nginx's [server_name](http://nginx.org/en/docs/http/ngx_http_core_module.html#server_name) directive.

Keys beginning with `.` or `*.` will match apex and all sub-domains, longest match wins. Non-wildcard matches always win.

Regex matches and prefix wildcards are not supported.

#Overview

```
init_by_lua_block {
    local vhost = require("resty.vhost")
    my_vhost = vhost:new()
    local ok, err = my_vhost:insert("example.com",      { key = "example.com.key",          cert = "example.com.crt" })
    local ok, err = my_vhost:insert("www.example.com",  { key = "example.com.key",          cert = "example.com.crt" })
    local ok, err = my_vhost:insert(".sub.example.com", { key = "star.sub.example.com.key", cert = "star.sub.example.com.crt" })
    local ok, err = my_vhost:insert("www.example2.com", { key = "www.example2.com.key",     cert = "www.example2.com.crt" })
}

server {
    listen 80 default_server;
    listen 443 ssl default_server;
    server_name vhost;

    ssl_certificate         /path/to/default/cert.crt;
    ssl_certificate_key     /path/to/default/key.crt;

    ssl_certificate_by_lua_block {
        local val, err = my_vhost:lookup(require("ngx.ssl").server_name())
        if not val then
            ngx.log(ngx.ERR, err)
        else
            ngx.log(ngx.DEBUG, "Match, setting certs: ", val.cert, " ", val.key)
            -- set_certs_somehow(val)
        end
    }

    location / {
        content_by_lua_block {
            local val, err = my_vhost:lookup(ngx.var.host)
            if val then
                -- do something based on val
                ngx.say("Matched: ", val.cert)
            else
                if err then
                    ngx.log(ngx.ERR, err)
                end
                ngx.exit(404)
            end
        }
    }
}
```

## Methods
### new
`syntax: my_vhost, err = vhost:new(size?)`

Creates a new instance of resty-vhost with an optional initial size

### insert
`syntax: ok, err = my_vhost:insert(key, value)`

Adds a new hostname key with associated value.

Keys must be strings.

Returns false and an error message on failure.

### lookup
`syntax: val, err = my_vhost:lookup(hostname)`

Retrieves value for best matching hostname entry.

Returns nil and an error message on failure

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-vhost](https://github.com/hamishforbes/lua-resty-vhost){target=_blank}.