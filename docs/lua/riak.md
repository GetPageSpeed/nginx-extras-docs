# *riak*: Lua riak protocol buffer client driver for nginx-module-lua based on the cosocket API


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-riak
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-riak
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-riak [v2.0.0](https://github.com/bakins/lua-resty-riak/releases/tag/v2.0.0){target=_blank} 
released on Dec 05 2013.
    
<hr />

lua-resty-riak - Lua riak protocol buffer client driver for the ngx_lua
based on the cosocket API.

Originally based on the
[lua-resty-memcached](https://github.com/agentzh/lua-resty-memcached)
library.

Influence by [riak-client-ruby](https://github.com/basho/riak-ruby-client/)

## Status ##

This library is currently _alpha_ quality. It passes all its unit
tests. A few billion requests per day are handled by it however.

## Description ##

This Lua library is a riak protocol buffer client driver for the [ngx_lua nginx module](http://wiki.nginx.org/HttpLuaModule)

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

Note that at least [ngx\_lua 0.5.0rc29](https://github.com/chaoslawful/lua-nginx-module/tags) or [ngx\_openresty 1.0.15.7](http://openresty.org/#Download) is required.

Depends on the following Lua modules:

* lua-pb - https://github.com/Neopallium/lua-pb
* struct - http://www.inf.puc-rio.br/~roberto/struct/
* lpack - http://www.tecgraf.puc-rio.br/~lhf/ftp/lua/#lpack 

## Synopsis ##

    location /t {
        content_by_lua '
            require "luarocks.loader"
            local riak = require "resty.riak"
            local client = riak.new()
            local ok, err = client:connect("127.0.0.1", 8087)
            if not ok then
                ngx.log(ngx.ERR, "connect failed: " .. err)
            end
            local bucket = client:bucket("test")
            local object = bucket:new("1")
            object.value = "test"
            object.content_type = "text/plain"
            local rc, err = object:store()
            ngx.say(rc)
            local object, err = bucket:get("1")
            if not object then
                ngx.say(err)
            else
                ngx.say(object.value)
            end
            client:close()
        ';
    }

## Usage ##

See the [generated docs](http://bakins.github.io/lua-resty-riak/)  for
usage and examples.

**Note** The high level API should be considered _stable_ - ie will
  not break between minor versions. The _low-level_ or _raw_ API
  should not be considered stable. 

## Potentially Breaking Change in 2.0 ##

2.0.0 now uses [vector clocks](http://docs.basho.com/riak/latest/theory/concepts/Vector-Clocks/) for gets,sets, and deletes of objects.  If you are using a bucket that allows multiple values (siblings) then this may break your application.

## Limitations ##

* This library cannot be used in code contexts like *set_by_lua*, *log_by_lua*, and
*header_filter_by_lua* where the ngx\_lua cosocket API is not available.
* The `resty.riak` object instances  cannot be stored in a Lua variable at the Lua module level,
because it will then be shared by all the concurrent requests handled by the same nginx
 worker process (see [Data Sharing within an Nginx Worker](http://wiki.nginx.org/HttpLuaModule#Data\_Sharing\_within\_an\_Nginx_Worker) ) and
result in bad race conditions when concurrent requests are trying to use the same instances.
You should always initiate these objects in function local
variables or in the `ngx.ctx` table. These places all have their own data copies for
each request.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-riak](https://github.com/bakins/lua-resty-riak){target=_blank}.