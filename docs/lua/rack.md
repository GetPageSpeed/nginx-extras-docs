---

title: "A simple and extensible HTTP server framework for nginx-module-lua"
description: "RPM package lua-resty-rack: A simple and extensible HTTP server framework for nginx-module-lua"

---
  
# *rack*: A simple and extensible HTTP server framework for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-rack
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-rack
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-rack [v0.3](https://github.com/pintsized/lua-resty-rack/releases/tag/v0.03){target=_blank} 
released on Jul 12 2012.
    
<hr />

A simple and extensible HTTP server framework for [OpenResty](http://openresty.org), providing a clean method for loading Lua HTTP applications ("resty" modules) into [Nginx](http://nginx.org).

Drawing inspiration from [Rack](http://rack.github.com/) and also [Connect](https://github.com/senchalabs/connect), **lua-resty-rack** allows you to load your application as a piece of middleware, alongside other middleware. Your application can either; ignore the current request, modify the request or response in some way and pass on to other middleware, or take responsibiliy for the request by generating a response. 

## Status

This library is considered experimental and the API may change without notice. Please feel free to offer suggestions or raise issues here on Github.

## Using Middleware

To install middleware for a given `location`, you simply call `rack.use(middleware)` in the order you wish the modules to run, and then finally call `rack.run()`.

```nginx
server {
    location / {
        content_by_lua '
            local rack = require "resty.rack"

            rack.use(rack.middleware.method_override)
            rack.use(require "my.module")
            rack.run()
        ';
    }
}
```

### rack.use(...)

**Syntax:** `rack.use(route?, middleware, options?)`

If `route` is supplied, the middleware will only be run for requests where `route` is in the path (`ngx.var.uri`). If the middleware requires any options to be selected they can be provided, usually as a table, as the third parameter.

```lua
rack.use('/some/path', app, { foo = 'bar' })
```

For simple cases, the `middleware` parameter can also be a simple function rather than a Lua module. Your function should accept `req`, `res`, and `next` as parameters. See below for instructions on writing middleware.

```lua
rack.use(function(req, res, next)
    res.header["X-Homer"] = "Doh!"
    next()
end)
```

### rack.run()

**Syntax:** `rack.run()`

Runs each of the middleware in order, until one chooses to handle the response. Thus, the order in which you call `rack.use()` is important.

## Bundled Middleware

### method_override
```lua
rack.use(rack.middleware.method_override, { key = "METHOD" })
```

Override the HTTP method using a querystring value. The default argument name is "_method" but this can be overriden by setting the option "key".


### read_request_headers
```lua
rack.use(rack.middleware.read_request_headers, { max = 50 })
```

This is only needed if you wish to iterate over the HTTP request headers. They will be lazy loaded when accessed via `req.header`.

You may specify a limit to the number of request headers to be read, which defaults to `100`. The limit can be removed by specifying a max of `0`, but is [strongly discouraged](http://wiki.nginx.org/HttpLuaModule#ngx.req.get_headers).

### read_body
```lua
rack.use(rack.middleware.read_body)
```

Explicitly reads the request body (raw).


## Creating Middleware

Middleware applications are simply Lua modules which use the HTTP request and response as a minimal interface. They must implement the function `call(options)` which returns a function. The parameters `(req, res, next)` are defined below.

```lua
module("resty.rack.method_override", package.seeall)

_VERSION = '0.01'

function call(options)
    return function(req, res, next)
        local key = options['key'] or '_method'
        req.method = string.upper(req.args[key] or req.method)
        next()
    end
end
```

## API

### req.method

The HTTP method, e.g. `GET`, set from `ngx.var.request_method`.

### req.scheme

The protocol scheme `http|https`, set from `ngx.var.scheme`.

### req.uri

e.g. `/my/uri`, set from `ngx.var.uri`.

### req.host

The hostname, e.g. `example.com`, set from `ngx.var.host`.

### req.query

The querystring, e.g. `var1=1&var2=2`, set from `ngx.var.query_string`.
 
### req.args

The query args, as a `table`, set from `ngx.req.get_uri_args()`.

### req.header

A table containing the request headers. Keys are matched case insensitvely, and optionally with underscores instead of hyphens. e.g.

```lua
req.header["X-Foo"] = "bar"
res.body = req.header.x_foo
    --> "bar"
```

HTTP Request headers are read on demand and so cannot be iterated over unless the `read_request_headers` middleware is in use).

### req.body

An empty string until read with the `read_body` middleware.

### res.status

The HTTP status code to return. There are [constants defined](http://wiki.nginx.org/HttpLuaModule#HTTP_status_constants) for common statuses.

### res.header

A table of response headers, which can be matched case insensitively and optionally with underscores instead of hyphens (see `req.header` above).

### res.body

The response body.

### next

This parameter is a function provided to the middleware, which may be called to indicate rack should try the next middleware. If your application does not intend to send the response to the browser, it must call this function. If however your application is taking responsibility for the response, simply return without calling next.

*Example purely modifying the request.*
```lua
function call(options)
    return function(req, res, next)
        local key = options['key'] or '_method'
        req.method = string.upper(req.args[key] or req.method)
        next()
    end
end
```

*Example generating a response.*
```lua
function call(options)
    return function(req, res)
        res.status = 200
        res.header['Content-Type'] = "text/plain"
        res.body = "Hello World"
    end
end
```

### Enhancing req / res

Your application can add new fields or even functions to the req / res tables where appropriate, which could be used by other middleware so long as the dependencies are clear (and one calls `use()` in the correct order). 

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-rack](https://github.com/pintsized/lua-resty-rack){target=_blank}.