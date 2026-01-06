---

title: "Lua HTTP client cosocket driver for nginx-module-lua, interfaces are more flexible"
description: "RPM package lua-resty-httpipe: Lua HTTP client cosocket driver for nginx-module-lua, interfaces are more flexible"

---
  
# *httpipe*: Lua HTTP client cosocket driver for nginx-module-lua, interfaces are more flexible


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-httpipe
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-httpipe
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-httpipe [v0.5](https://github.com/timebug/lua-resty-httpipe/releases/tag/v0.05){target=_blank} 
released on Nov 25 2015.
    
<hr />

Lua HTTP client cosocket driver for [OpenResty](http://openresty.org/) / [ngx_lua](https://github.com/chaoslawful/lua-nginx-module).

## Features

* HTTP 1.0/1.1 and HTTPS
* Flexible interface design
* Streaming reader and uploads
* Chunked-encoding request / response body
* Sets the timeout for read and send operations
* Limit the maximum response body size
* Keepalive

## Synopsis

````lua
server {

  listen 9090;

  location /echo {
    content_by_lua '
      local raw_header = ngx.req.raw_header()

      if ngx.req.get_method() == "GET" then
          ngx.header["Content-Length"] = #raw_header
      end

      ngx.req.read_body()
      local body, err = ngx.req.get_body_data()

      ngx.print(raw_header)
      ngx.print(body)
    ';
  }

  location /simple {
    content_by_lua '
      local httpipe = require "resty.httpipe"

      local hp, err = httpipe:new()
      if not hp then
          ngx.log(ngx.ERR, "failed to new httpipe: ", err)
          return ngx.exit(503)
      end

      hp:set_timeout(5 * 1000) -- 5 sec

      local res, err = hp:request("127.0.0.1", 9090, {
                                     method = "GET", path = "/echo" })
      if not res then
          ngx.log(ngx.ERR, "failed to request: ", err)
          return ngx.exit(503)
      end

      ngx.status = res.status

      for k, v in pairs(res.headers) do
          ngx.header[k] = v
      end

      ngx.say(res.body)
    ';
  }

  location /generic {
    content_by_lua '
      local cjson = require "cjson"
      local httpipe = require "resty.httpipe"

      local hp, err = httpipe:new(10) -- chunk_size = 10
      if not hp then
          ngx.log(ngx.ERR, "failed to new httpipe: ", err)
          return ngx.exit(503)
      end

      hp:set_timeout(5 * 1000) -- 5 sec

      local ok, err = hp:connect("127.0.0.1", 9090)
      if not ok then
          ngx.log(ngx.ERR, "failed to connect: ", err)
          return ngx.exit(503)
      end

      local ok, err = hp:send_request{ method = "GET", path = "/echo" }
      if not ok then
          ngx.log(ngx.ERR, "failed to send request: ", err)
          return ngx.exit(503)
      end

      -- full streaming parser

      while true do
          local typ, res, err = hp:read()
          if not typ then
              ngx.say("failed to read: ", err)
              return
          end

          ngx.say("read: ", cjson.encode({typ, res}))

          if typ == 'eof' then
              break
          end
      end
    ';
  }

  location /advanced {
    content_by_lua '
      local httpipe = require "resty.httpipe"

      local hp, err = httpipe:new()

      hp:set_timeout(5 * 1000) -- 5 sec

      local r0, err = hp:request("127.0.0.1", 9090, {
                                     method = "GET", path = "/echo",
                                     stream = true })

      -- from one http stream to another, just like a unix pipe

      local pipe = r0.pipe

      pipe:set_timeout(5 * 1000) -- 5 sec

      --[[
          local headers = {["Content-Length"] = r0.headers["Content-Length"]}
          local r1, err = pipe:request("127.0.0.1", 9090, {
                                           method = "POST", path = "/echo",
                                           headers = headers,
                                           body = r0.body_reader })
      --]]
      local r1, err = pipe:request("127.0.0.1", 9090, {
                                       method = "POST", path = "/echo" })

      ngx.status = r1.status

      for k, v in pairs(r1.headers) do
          ngx.header[k] = v
      end

      ngx.say(r1.body)
    ';
  }

}
````

A typical output of the `/simple` location defined above is:

```
GET /echo HTTP/1.1
Host: 127.0.0.1
User-Agent: Resty/HTTPipe-1.00
Accept: */*

```

A typical output of the `/generic` location defined above is:

```
read: ["statusline","200"]
read: ["header",["Server","openresty\/1.5.12.1","Server: openresty\/1.5.12.1"]]
read: ["header",["Date","Tue, 10 Jun 2014 07:29:57 GMT","Date: Tue, 10 Jun 2014 07:29:57 GMT"]]
read: ["header",["Content-Type","text\/plain","Content-Type: text\/plain"]]
read: ["header",["Connection","keep-alive","Connection: keep-alive"]]
read: ["header",["Content-Length","84","Content-Length: 84"]]
read: ["header_end"]
read: ["body","GET \/echo "]
read: ["body","HTTP\/1.1\r\n"]
read: ["body","Host: 127."]
read: ["body","0.0.1\r\nUse"]
read: ["body","r-Agent: R"]
read: ["body","esty\/HTTPi"]
read: ["body","pe-1.00\r\nA"]
read: ["body","ccept: *\/*"]
read: ["body","\r\n\r\n"]
read: ["body_end"]
read: ["eof"]
```

A typical output of the `/advanced` location defined above is:

```
POST /echo HTTP/1.1
Content-Length: 84
User-Agent: Resty/HTTPipe-1.00
Accept: */*
Host: 127.0.0.1

GET /echo HTTP/1.1
Host: 127.0.0.1
User-Agent: Resty/HTTPipe-1.00
Accept: */*


```

## Connection

## new

`syntax: hp, err = httpipe:new(chunk_size?, sock?)`

Creates the httpipe object. In case of failures, returns `nil` and a string describing the error.

The argument, `chunk_size`, specifies the buffer size used by cosocket reading operations. Defaults to `8192`.

## connect

`syntax: ok, err = hp:connect(host, port, options_table?)`

`syntax: ok, err = hp:connect("unix:/path/to/unix.sock", options_table?)`

Attempts to connect to the web server.

Before actually resolving the host name and connecting to the remote backend, this method will always look up the connection pool for matched idle connections created by previous calls of this method.

An optional Lua table can be specified as the last argument to this method to specify various connect options:

* `pool`
: Specifies a custom name for the connection pool being used. If omitted, then the connection pool name will be generated from the string template `<host>:<port>` or `<unix-socket-path>`.

## set_timeout

`syntax: hp:set_timeout(time)`

Sets the timeout (in ms) protection for subsequent operations, including the `connect` method.

## ssl_handshake

`syntax: hp:ssl_handshake(reused_session?, server_name?, ssl_verify?)`

Does SSL/TLS handshake on the currently established connection.

See more: <http://wiki.nginx.org/HttpLuaModule#tcpsock:sslhandshake>

## set_keepalive

`syntax: ok, err = hp:set_keepalive(max_idle_timeout, pool_size)`

Attempts to puts the current connection into the ngx_lua cosocket connection pool.

**Note** Normally, it will be called automatically after processing the request. In other words, we cannot release the connection back to the pool unless you consume all the data.

You can specify the max idle timeout (in ms) when the connection is in the pool and the maximal size of the pool every nginx worker process.

In case of success, returns 1. In case of errors, returns nil with a string describing the error.

## get_reused_times

`syntax: times, err = hp:get_reused_times()`

This method returns the (successfully) reused times for the current connection. In case of error, it returns `nil` and a string describing the error.

If the current connection does not come from the built-in connection pool, then this method always returns `0`, that is, the connection has never been reused (yet). If the connection comes from the connection pool, then the return value is always non-zero. So this method can also be used to determine if the current connection comes from the pool.

## close

`syntax: ok, err = hp:close()`

Closes the current connection and returns the status.

In case of success, returns `1`. In case of errors, returns `nil` with a string describing the error.


## Requesting

## request

`syntax: res, err = hp:request(opts?)`

`syntax: res, err = hp:request(host, port, opts?)`

`syntax: res, err = hp:request("unix:/path/to/unix-domain.socket", opts?)`

The `opts` table accepts the following fields:

* `version`: Sets the HTTP version. Use `10` for HTTP/1.0 and `11` for HTTP/1.1. Defaults to `11`.
* `method`: The HTTP method string. Defaults to `GET`.
* `path`: The path string. Default to `/`.
* `query`: Specifies query parameters. Accepts either a string or a Lua table.
* `headers`: A table of request headers. Accepts a Lua table.
* `body`: The request body as a string, or an iterator function.
* `read_timeout`: Sets the timeout in milliseconds for network read operations specially.
* `send_timeout`: Sets the timeout in milliseconds for network send operations specially.
* `stream`: If set to `true`, return an iterable `res.body_reader` object instead of `res.body`.
* `maxsize`: Sets the maximum size in bytes to fetch. A response body larger than this will cause the fucntion to return a `exceeds maxsize` error. Defaults to nil which means no limit.
* `ssl_verify`: A Lua boolean value to control whether to perform SSL verification.

When the request is successful, `res` will contain the following fields:

* `res.status` (number): The resonse status, e.g. 200
* `res.headers` (table): A Lua table with response headers.
* `res.body` (string): The plain response body.
* `res.body_reader` (function): An iterator function for reading the body in a streaming fashion.
* `res.pipe` (httpipe): A new http pipe which use the current `body_reader` as input body by default.

**Note** All headers (request and response) are noramlized for capitalization - e.g., Accept-Encoding, ETag, Foo-Bar, Baz - in the normal HTTP "standard."

In case of errors, returns nil with a string describing the error.

## request_uri

`syntax: res, err = hp:request_uri(uri, opts?)`

The simple interface. Options supplied in the `opts` table are the same as in the generic interface, and will override components found in the uri itself.

Returns a res object as same as `hp:request` method.

In case of errors, returns nil with a string describing the error.

## res.body_reader

The `body_reader` iterator can be used to stream the response body in chunk sizes of your choosing, as follows:

````lua
local reader = res.body_reader

repeat
  local chunk, err = reader(8192)
  if err then
    ngx.log(ngx.ERR, err)
    break
  end

  if chunk then
    -- process
  end
until not chunk
````

## send_request

`syntax: ok, err = hp:send_request(opts?)`

In case of errors, returns nil with a string describing the error.

## read_response

`syntax: local res, err = hp:read_response(callback?)`

The `callback` table accepts the following fields:

* `header_filter`: A callback function for response headers filter

````lua
local res, err = hp:read_response{
    header_filter = function (status, headers)
        if status == 200 then
        	return 1
        end
end }
````

* `body_filter`: A callback function for response body filter

````lua
local res, err = hp:read_response{
    body_filter = function (chunk)
        ngx.print(chunk)
    end
}
````

Additionally there is no ability to stream the response body in this method. If the response is successful, res will contain the following fields: `res.status`, `res.headers`, `res.body`.

**Note** When return true in callback function，filter process will be interrupted.

In case of errors, returns nil with a string describing the error.

## read

`syntax: local typ, res, err = hp:read()`

Streaming parser for the full response.

The user just needs to call the read method repeatedly until a nil token type is returned. For each token returned from the read method, just check the first return value for the current token type. The token type can be `statusline`, `header`, `header_end`, `body`, `body_end` and `eof`. About the format of `res` value, please refer to the above example. For example, several body tokens holding each body data chunk, so `res` value is equal to the body data chunk.

In case of errors, returns nil with a string describing the error.

## eof

`syntax: local eof = hp:eof()`

If return `true` indicating already consume all the data; Otherwise, the request there is still no end, you need call `hp:close` to close the connection forcibly.

## Utility

## parse_uri

`syntax: local scheme, host, port, path, args = unpack(hp:parse_uri(uri))`

This is a convenience function allowing one to more easily use the generic interface, when the input data is a URI.

## get_client_body_reader

`syntax: reader, err = hp:get_client_body_reader(chunk_size?)`

Returns an iterator function which can be used to read the downstream client request body in a streaming fashion. For example:

```lua
local req_reader = hp:get_client_body_reader()

repeat
  local chunk, err = req_reader(8192)
  if err then
    ngx.log(ngx.ERR, err)
    break
  end

  if chunk then
    -- process
  end
until not chunk
```

This iterator can also be used as the value for the body field in request params, allowing one to stream the request body into a proxied upstream request.

```lua
local client_body_reader, err = hp:get_client_body_reader()

local res, err = hp:request{
   path = "/helloworld",
   body = client_body_reader,
}
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-httpipe](https://github.com/timebug/lua-resty-httpipe){target=_blank}.