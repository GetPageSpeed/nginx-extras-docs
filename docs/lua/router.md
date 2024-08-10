# *router*: Lua http router for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-router
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-router
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-router [v0.1.0](https://github.com/git-hulk/lua-resty-router/releases/tag/v0.1.0){target=_blank} 
released on Jun 26 2017.
    
<hr />

lua-resty-router - Lua http router for the ngx_lua

## Status

This library is considered production ready.

## Description

This Lua library is a http router for the ngx_lua nginx module:

http://wiki.nginx.org/HttpLuaModule

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

Note that at least [ngx_lua 0.5.0rc29](https://github.com/chaoslawful/lua-nginx-module/tags) or [OpenResty 1.0.15.7](http://openresty.org/#Download) is required.

## Synopsis

```lua
    server {
        location /test {
            content_by_lua '
                local Router = require "resty.router"
              router = Router:new()
              router:get("/a/:b/:c", function(params)
                ngx.print(params["b"].."-"..parmams["c"])
              end)
              router:post("/b/c/*.html", function(params)
                ngx.print("echo html")
              end)
              router:any("/c/d/", function(params)
                ngx.print("hello, world")
              end)
            ';
        }
    }
```

## Methods

The `key` argument provided in the following methods will be automatically escaped according to the URI escaping rules before sending to the memcached server.

## new
`syntax: r, err = router:new()`

Creates a router object, never return an error.

## route
#### Using GET, POST, HEAD, PUT, PATCH, DELETE, ANY and OPTIONS

```lua
local R = require("resty.router")
local router = R:new()
router:get("/GetRoute", handler)
router:post("/PostRoute", handler)
router:head("/HeadRoute", handler)
router:put("/PutRoute", handler)
router:delete("/DeleteRoute", handler)
router:patch("/PatchRoute", handler)
router:options("/OptionsRoute", handler)
router:any("/AnyRoute", handler)
router:run()
```

#### Parameters in path

```lua
    local R = require("resty.router")
    local router = R:new()

    -- catch all when on route is match
    router:get("/*", function(params) -- /* or * is ok
        ngx.say("catch all") 
        ngx.exit(200)
    end)

    -- This handler will match /user/john but will not match neither /user/ or /user
    router:get("/user/:name", function(params)
        local name = params["name"]
        ngx.print("Hello", name)
        ngx.exit(200)
    end)

    -- However, this one will match /user/john/ and also /user/john/send
    -- If no other routers match /user/john, it will redirect to /user/john/
    router.get("/user/:name/*", function(params)
        local name = params("name")
        ngx.print("Hello", name)
        ngx.exit(200)
    end)
    
    -- This one will match /user/jhon/send.html, also match any uri start with /user/jhon/ and end with .html
    router:get("/user/jhon/*.html", function(params)
        ngx.print("Hello")
        ngx.exit(200)
    end)
    
    router:run()
```

#### handler

Type of parameter handler should be function or string, when type is:

* function, handler would be called when uri is matched
* string, router would require `a.b`, when ret type is table, search method `handle`, if ret type is function, return function would be called.

#### Tips

* '*' rule can be used at the end of the route
* throw http code 500 when route conflicts

## run

Method run would find route, and callback the handler. when not handler was found and notfound_handler is set, callback the handler.


```lua
    local R = require("resty.router")
    local router = R:new()
    router:run() -- or router:run(notfound_handler)
``` 


## Limitations

* This library cannot be used in code contexts like `set_by_lua*`, `log_by_lua*`, and
`header_filter_by_lua*` where the ngx\_lua cosocket API is not available.
* The `resty.memcached` object instance cannot be stored in a Lua variable at the Lua module level,
because it will then be shared by all the concurrent requests handled by the same nginx
 worker process (see
http://wiki.nginx.org/HttpLuaModule#Data_Sharing_within_an_Nginx_Worker ) and
result in bad race conditions when concurrent requests are trying to use the same `resty.memcached` instance.
You should always initiate `resty.memcached` objects in function local
variables or in the `ngx.ctx` table. These places all have their own data copies for
each request.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-router](https://github.com/git-hulk/lua-resty-router){target=_blank}.