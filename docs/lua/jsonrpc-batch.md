---

title: "JSONRPC batch protocol module for nginx-module-lua"
description: "RPM package lua-resty-jsonrpc-batch: JSONRPC batch protocol module for nginx-module-lua"

---
  
# *jsonrpc-batch*: JSONRPC batch protocol module for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-jsonrpc-batch
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-jsonrpc-batch
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-jsonrpc-batch [v0.0.1](https://github.com/mosasiru/lua-resty-jsonrpc-batch/releases/tag/v0.0.1){target=_blank} 
released on Jul 15 2015.
    
<hr />

The Lua-Openresty implementation of [JSON-RPC 2.0](http://www.jsonrpc.org/specification) Batch Request (http://www.jsonrpc.org/specification#batch).

The batch request is non-blocking and proceeded paralelly because this module makes use of location.capture_multi of ngx_lua. So the performance is high while the implementation is simple.

This module parses a batch request, validate it, and makes multi subrequest to upstream servers.
Note that you must have a upstream JSON-RPC server as you like, but upstream servers need not apply for JSON-RPC batch request.

## Synopsis

### Basic Usage

```lua
server {
    location /api {
        # jsonrpc endpoint
    }
    location /api/batch {
        lua_need_request_body on;

        content_by_lua '
            local jsonrpc_batch = require "resty.jsonrpc.batch"
            client = jsonrpc_batch:new()
            local res, err = client:batch_request({
                path    = "/api",
                request = ngx.var.request_body,
            })
            if err then
                ngx.exit(500)
            end
            ngx.say(res)
        ';
    }
}
```

### Advanced Usage


```lua
http {

    init_by_lua '
        local jsonrpc_batch = require "resty.jsonrpc.batch"
        client = jsonrpc_batch.new({
            -- make limitation to batch request array size
            max_batch_array_size = 10,
            -- for logging upstream response time
            before_subrequest = function(self, ctx, req)
                ctx.start_at = ngx.now()
            end,
            after_subrequest = function(self, ctx, resps, req)
                ngx.var.jsonrpc_upstream_response_time = ngx.now() - ctx.start_at
            end,
        })
    ';

    server {
        set $jsonrpc_upstream_response_time  -;

        location ~ /api/method/.* {
            # jsonrpc endpoint
        }

        location /api/batch {
            lua_need_request_body on;

            content_by_lua '
                local res, err = client:batch_request({
                    -- you can change the endpoint per request
                    path = function(self, ctx, req)
                        return "/api/method/" .. req.method
                    end,
                    request  = ngx.var.request_body,
                });
                if err then
                    ngx.log(ngx.CRIT, err);
                    ngx.exit(500);
                end
                ngx.say(res);
            ';
        }
    }
}

```

## Methods

### new
`usage:client = jsonrpc_batch:new(options)`

The options argument is a Lua table holding the following keys:

* `max_batch_array_size` [Int]

  Set limitation to json array size of batch request .  
  When a request whose json array size is over the limit comes, `request` method returns a invalid error json.

  The default value is `nil` (no limit).

* `allow_single_request` [Bool]

   This module can accept not only batch requests, but also single requests (no batch requests) . For example, ```{"id":1, "jsonrpc": "2.0", "params": {}, "method": "hoge"}``` is a single request.

   If `allow_single_request` is set to be `false`, a single request results to a invalid error json.

   The default value is `true`.
* `before_subrequest` [Function ```function(self, ctx)```]

    Specify the callback function fired just before throw subrequests.  `ctx` argument is a [Context](#Context) Object.

    For example, you can set nginx variable (`ngx.var`) for logging subrequests, and you can manipulate request parameters dynamically.

* `after_subrequest` [Function ```function(self, ctx)```]

    Specify the callback function fired just after throw subrequests. `ctx` argument is a [Context](#Context) Object.

    For example, we can set nginx variable (`ngx.var`) for logging subrequest results, and we can manipulate subrequest responses dynamically.

### request

```
usage:
res, err = client:request({
    path = "/api",
    request = ###jsonrpc request json###,
})
```

Decode request json and separate it, and make subrequest parallely to specified `path`.
It returns response json(`res`) which is generated by all the subrequest 's response json. `err` is set error message when lua script occurs an error.

It can accept following parameters.

* `request` [String] (requried)

    A request JSON.

* `path` [String or Function ```function(self, ctx, req)```] (required)

    Subrequest path like `"/api"`.

    The type can be Function which decides path for each subrequest dynamically.

    `ctx` argument is a [Context](#Context) Object.

    `req` argument is a single request json included by batch request json array. like ```{"id":1, "jsonrpc": "2.0", "params": {"user_id": 1}, "method": "getUser"}```.

    To give one example, we can use this function for separating api endpoints by JSON-RPC method, and we can throw original request path information to subrequest.

    Following configuration exmaple is that there are two endpoints, and dispatch batch requests to endpoints by jsonrpc method. Besides, endpoints have own API version as path prefix.

```lua
    location ~ ^/(\d+\.\d+)/getUser$ {
        # jsonrpc endpoint 1
    }

    location ~ ^/(\d+\.\d+)/updateUser$ {
        # jsonrpc endppoint 2
    }

    location ~ ^/(\d+\.\d+)/batch$ {
        set $version $1;
        lua_need_request_body on;
        content_by_lua {
            local res, err = client:batch_request({
                path = function(self, ctx, req)
                    return "/" .. ngx.var.version  .. "/" .. req.method
                end,
                request = ngx.var.request_body,
            });
            if err then
              ngx.log(ngx.CRIT, err);
              ngx.exit(500);
              return;
            end
        };
    }

```

* `method` (string) optional

    Specify HTTP method using by subrequests.
    The default value is `ngx.HTTP_POST`.

## Object
### Context

`before_subrequest`, `after_subrequest`, and `path` callback functions has Context object in arguments.
Context object includes information of requests and subrequest responses, so which value it has or not changes by the request proccess.

Context object is a lua table, and has following keys.

* `path` [String or Function]

 Specified by `request` method as `path`.

* `method` [String]

 Specified by `request` method as `method`.

* `raw_request` [String]

  request json specified by `request` method as `request`.

* `request` [Table]

  lua table generated by decoding `raw_request` json.

* `is_batch` [Bool]

  The request json is single request or batch request.

* subreq_reqs [Table]

  The array of subrequests parameters.
  This is the arguments of `ngx.location.capture_multi`.

* subreq_resps [Table]

  The array of subrequests responses.
  This is the response of `ngx.location.capture_multi`.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-jsonrpc-batch](https://github.com/mosasiru/lua-resty-jsonrpc-batch){target=_blank}.