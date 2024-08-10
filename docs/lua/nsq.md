# *nsq*: Lua nsq client driver for nginx-module-lua based on the cosocket API


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-nsq
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-nsq
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-nsq [v0.1](https://github.com/rainingmaster/lua-resty-nsq/releases/tag/v0.01){target=_blank} 
released on Aug 07 2018.
    
<hr />

lua-resty-nsq - Lua nsq client driver for the ngx_lua based on the cosocket API

## Status

This library is developing.

## Description

This Lua library is a NSQ client driver for the ngx_lua nginx module:

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

## Synopsis

```lua
    server {
        location /test {
            content_by_lua_block {
                local config = {
                    read_timeout = 3,
                    heartbeat = 1,
                }
                local producer = require "resty.nsq.producer"
                local consumer = require "resty.nsq.consumer"

                local cons = consumer:new()
                local prod = producer:new()

                local ok, err = cons:connect("127.0.0.1", 4150, config)
                if not ok then
                    ngx.say("failed to connect: ", err)
                    return
                end

                local ok, err = prod:connect("127.0.0.1", 4150)
                if not ok then
                    ngx.say("failed to connect: ", err)
                    return
                end

                ok, err = prod:pub("new_topic", "hellow world!")
                if not ok then
                    ngx.say("failed to pub: ", err)
                    return
                end

                ok, err = prod:close()
                if not ok then
                    ngx.say("failed to close: ", err)
                    return
                end

                ok, err = cons:sub("new_topic", "new_channel")
                if not ok then
                    ngx.say("failed to sub: ", err)
                    return
                end

                local function read(c)
                    c:rdy(10)
                    local ret = cons:message()
                    ngx.say("sub success: ", require("cjson").encode(ret))
                end

                local co = ngx.thread.spawn(read, cons) -- read message in new thread
                ngx.thread.wait(co)

                ok, err = cons:close()
                if not ok then
                    ngx.say("failed to close: ", err)
                    return
                end
            }
        }
    }
```

## Modules

## resty.nsq.producer

### Methods

#### new

#### pub

## resty.nsq.consumer

### Methods

#### new

## See Also
* the ngx_lua module: https://github.com/openresty/lua-nginx-module/#readme
* the nsq wired protocol specification: https://nsq.io/clients/tcp_protocol_spec.html
* [the semaphore in openresty: ngx.sema](https://github.com/openresty/lua-resty-core/blob/master/lib/ngx/semaphore.md)
* [the thread in openresty: ngx.thread](https://github.com/openresty/lua-nginx-module#ngxthreadspawn)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-nsq](https://github.com/rainingmaster/lua-resty-nsq){target=_blank}.