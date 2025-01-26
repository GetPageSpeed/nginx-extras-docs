---

title: "Woothee Lua-nginx-module-lua implementation"
description: "RPM package lua-resty-woothee: Woothee Lua-nginx-module-lua implementation"

---
  
# *woothee*: Woothee Lua-nginx-module-lua implementation


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-woothee
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-woothee
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-woothee [v1.12.0](https://github.com/woothee/lua-resty-woothee/releases/tag/v1.12.0-1){target=_blank} 
released on Oct 13 2021.
    
<hr />
[![CircleCI](https://circleci.com/gh/woothee/lua-resty-woothee.svg?style=svg)](https://circleci.com/gh/woothee/lua-resty-woothee)

## Woothee lua resty

The Lua-Openresty implementation of Project Woothee, which is multi-language user-agent strings parsers.

https://github.com/woothee/woothee

## Synopsis

#### Basic Usage

```lua
server {
    location /test {
        content_by_lua_block {
            local woothee = require "resty.woothee"

            -- parse
            local r = woothee.parse(ngx.var.http_user_agent)
            --  => {"name": "xxx", "category": "xxx", "os": "xxx", "version": "xxx", "vendor": "xxx"}

            -- crawler?
            local crawler = woothee.is_crawler(ngx.var.http_user_agent)
            --  => true

            ngx.header.content_type = "text/plain"
            ngx.say(r.name)
        }
    }
}
```

#### Include Nginx Log

```lua
log_format woothee_format
                  '$remote_addr - $remote_user [$time_local] '
                  '"$request" $status $body_bytes_sent '
                  '"$http_referer" "$http_user_agent" '
                  '"$x_wt_name" "$x_wt_category" "$x_wt_os" "$x_wt_version" "$x_wt_vendor" "$x_wt_os_version"'
                  ;

server {

    access_log /var/log/nginx/nginx-access-woothee.log woothee_format;

    # set nginx valiables
    set $x_wt_name       '-';
    set $x_wt_category   '-';
    set $x_wt_os         '-';
    set $x_wt_version    '-';
    set $x_wt_vendor     '-';
    set $x_wt_os_version '-';

    location /test {
        content_by_lua_block {
            local woothee = require "resty.woothee"
            local r = woothee.parse(ngx.var.http_user_agent)
            -- set nginx valiables
            ngx.var.x_wt_name       = r.name
            ngx.var.x_wt_category   = r.category
            ngx.var.x_wt_os         = r.os
            ngx.var.x_wt_version    = r.version
            ngx.var.x_wt_vendor     = r.vendor
            ngx.var.x_wt_os_version = r.os_version

            ngx.header.content_type = "text/plain"
            ngx.say(r.name)
        }
    }
}
```

#### Forward Backend Server

```lua
server {

    # set nginx valiables
    set $x_wt_name       '-';
    set $x_wt_category   '-';
    set $x_wt_os         '-';
    set $x_wt_version    '-';
    set $x_wt_vendor     '-';
    set $x_wt_os_version '-';

    location /test {
        rewrite_by_lua_block {
            local woothee = require "resty.woothee"
            local r = woothee.parse(ngx.var.http_user_agent)
            -- set nginx valiables
            ngx.var.x_wt_name       = r.name
            ngx.var.x_wt_category   = r.category
            ngx.var.x_wt_os         = r.os
            ngx.var.x_wt_version    = r.version
            ngx.var.x_wt_vendor     = r.vendor
            ngx.var.x_wt_os_version = r.os_version
        }

        proxy_pass http://backend-server/;
        # proxy set header
        proxy_set_header X-WT-NAME       $x_wt_name;
        proxy_set_header X-WT-CATEGORY   $x_wt_category;
        proxy_set_header X-WT-OS         $x_wt_os;
        proxy_set_header X-WT-VERSION    $x_wt_version;
        proxy_set_header X-WT-VENDOR     $x_wt_vendor;
        proxy_set_header X-WT-OS-VERSION $x_wt_os_version;
    }
}
```

## For Developer (on Docker)

#### docker run & run test

```
make local-all
```

* * * * *

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-woothee](https://github.com/woothee/lua-resty-woothee){target=_blank}.