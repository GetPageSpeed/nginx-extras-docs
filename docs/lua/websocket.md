---

title: "WebSocket support for nginx-module-lua module"
description: "RPM package lua-resty-websocket: WebSocket support for nginx-module-lua module"

---
  
# *websocket*: WebSocket support for nginx-module-lua module


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-websocket
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-websocket
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-websocket [v0.13](https://github.com/openresty/lua-resty-websocket/releases/tag/v0.13){target=_blank} 
released on Feb 11 2025.
    
<hr />

This Lua library implements a WebSocket server and client libraries based on the [ngx_lua module](http://wiki.nginx.org/HttpLuaModule).

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

Note that only [RFC 6455](http://tools.ietf.org/html/rfc6455) is supported. Earlier protocol revisions like "hybi-10", "hybi-07", and "hybi-00" are not and will not be considered.

## Synopsis

```lua
    local server = require "resty.websocket.server"

    local wb, err = server:new{
        timeout = 5000,  -- in milliseconds
        max_payload_len = 65535,
    }
    if not wb then
        ngx.log(ngx.ERR, "failed to new websocket: ", err)
        return ngx.exit(444)
    end

    local data, typ, err = wb:recv_frame()

    if not data then
        if not string.find(err, "timeout", 1, true) then
            ngx.log(ngx.ERR, "failed to receive a frame: ", err)
            return ngx.exit(444)
        end
    end

    if typ == "close" then
        -- for typ "close", err contains the status code
        local code = err

        -- send a close frame back:

        local bytes, err = wb:send_close(1000, "enough, enough!")
        if not bytes then
            ngx.log(ngx.ERR, "failed to send the close frame: ", err)
            return
        end
        ngx.log(ngx.INFO, "closing with status code ", code, " and message ", data)
        return
    end

    if typ == "ping" then
        -- send a pong frame back:

        local bytes, err = wb:send_pong(data)
        if not bytes then
            ngx.log(ngx.ERR, "failed to send frame: ", err)
            return
        end
    elseif typ == "pong" then
        -- just discard the incoming pong frame

    else
        ngx.log(ngx.INFO, "received a frame of type ", typ, " and payload ", data)
    end

    wb:set_timeout(1000)  -- change the network timeout to 1 second

    bytes, err = wb:send_text("Hello world")
    if not bytes then
        ngx.log(ngx.ERR, "failed to send a text frame: ", err)
        return ngx.exit(444)
    end

    bytes, err = wb:send_binary("blah blah blah...")
    if not bytes then
        ngx.log(ngx.ERR, "failed to send a binary frame: ", err)
        return ngx.exit(444)
    end

    local bytes, err = wb:send_close(1000, "enough, enough!")
    if not bytes then
        ngx.log(ngx.ERR, "failed to send the close frame: ", err)
        return
    end
```

## Modules

## resty.websocket.server

To load this module, just do this

```lua
    local server = require "resty.websocket.server"
```

### Methods

#### new
`syntax: wb, err = server:new()`

`syntax: wb, err = server:new(opts)`

Performs the websocket handshake process on the server side and returns a WebSocket server object.

In case of error, it returns `nil` and a string describing the error.

An optional options table can be specified. The following options are as follows:

* `max_payload_len`

    Specifies the maximal length of payload allowed when sending and receiving WebSocket frames. Defaults to `65535`.
* `max_recv_len`

    Specifies the maximal length of payload allowed when receiving WebSocket frames. Defaults to the value of `max_payload_len`.
* `max_send_len`

    Specifies the maximal length of payload allowed when sending WebSocket frames. Defaults to the value of `max_payload_len`.
* `send_masked`

    Specifies whether to send out masked WebSocket frames. When it is `true`, masked frames are always sent. Default to `false`.
* `timeout`

    Specifies the network timeout threshold in milliseconds. You can change this setting later via the `set_timeout` method call. Note that this timeout setting does not affect the HTTP response header sending process for the websocket handshake; you need to configure the [send_timeout](http://nginx.org/en/docs/http/ngx_http_core_module.html#send_timeout) directive at the same time.

#### set_timeout
`syntax: wb:set_timeout(ms)`

Sets the timeout delay (in milliseconds) for the network-related operations.

#### send_text
`syntax: bytes, err = wb:send_text(text)`

Sends the `text` argument out as an unfragmented data frame of the `text` type. Returns the number of bytes that have actually been sent on the TCP level.

In case of errors, returns `nil` and a string describing the error.

#### send_binary
`syntax: bytes, err = wb:send_binary(data)`

Sends the `data` argument out as an unfragmented data frame of the `binary` type. Returns the number of bytes that have actually been sent on the TCP level.

In case of errors, returns `nil` and a string describing the error.

#### send_ping
`syntax: bytes, err = wb:send_ping()`

`syntax: bytes, err = wb:send_ping(msg)`

Sends out a `ping` frame with an optional message specified by the `msg` argument. Returns the number of bytes that have actually been sent on the TCP level.

In case of errors, returns `nil` and a string describing the error.

Note that this method does not wait for a pong frame from the remote end.

#### send_pong
`syntax: bytes, err = wb:send_pong()`

`syntax: bytes, err = wb:send_pong(msg)`

Sends out a `pong` frame with an optional message specified by the `msg` argument. Returns the number of bytes that have actually been sent on the TCP level.

In case of errors, returns `nil` and a string describing the error.

#### send_close
`syntax: bytes, err = wb:send_close()`

`syntax: bytes, err = wb:send_close(code, msg)`

Sends out a `close` frame with an optional status code and a message.

In case of errors, returns `nil` and a string describing the error.

For a list of valid status code, see the following document:

http://tools.ietf.org/html/rfc6455#section-7.4.1

Note that this method does not wait for a `close` frame from the remote end.

#### send_frame
`syntax: bytes, err = wb:send_frame(fin, opcode, payload)`

Sends out a raw websocket frame by specifying the `fin` field (boolean value), the opcode, and the payload.

For a list of valid opcode, see

http://tools.ietf.org/html/rfc6455#section-5.2

In case of errors, returns `nil` and a string describing the error.

To control the maximal payload length allowed, you can pass the `max_payload_len` option to the `new` constructor.

To control whether to send masked frames, you can pass `true` to the `send_masked` option in the `new` constructor method. By default, unmasked frames are sent.

#### recv_frame
`syntax: data, typ, err = wb:recv_frame()`

Receives a WebSocket frame from the wire.

In case of an error, returns two `nil` values and a string describing the error.

The second return value is always the frame type, which could be one of `continuation`, `text`, `binary`, `close`, `ping`, `pong`, or `nil` (for unknown types).

For `close` frames, returns 3 values: the extra status message (which could be an empty string), the string "close", and a Lua number for the status code (if any). For possible closing status codes, see

http://tools.ietf.org/html/rfc6455#section-7.4.1

For other types of frames, just returns the payload and the type.

For fragmented frames, the `err` return value is the Lua string "again".

## resty.websocket.client

To load this module, just do this

```lua
    local client = require "resty.websocket.client"
```

A simple example to demonstrate the usage:

```lua
    local client = require "resty.websocket.client"
    local wb, err = client:new()
    local uri = "ws://127.0.0.1:" .. ngx.var.server_port .. "/s"
    local ok, err, res = wb:connect(uri)
    if not ok then
        ngx.say("failed to connect: " .. err)
        return
    end

    local data, typ, err = wb:recv_frame()
    if not data then
        ngx.say("failed to receive the frame: ", err)
        return
    end

    ngx.say("received: ", data, " (", typ, "): ", err)

    local bytes, err = wb:send_text("copy: " .. data)
    if not bytes then
        ngx.say("failed to send frame: ", err)
        return
    end

    local bytes, err = wb:send_close()
    if not bytes then
        ngx.say("failed to send frame: ", err)
        return
    end
```

### Methods

#### client:new
`syntax: wb, err = client:new()`

`syntax: wb, err = client:new(opts)`

Instantiates a WebSocket client object.

In case of error, it returns `nil` and a string describing the error.

An optional options table can be specified. The following options are as follows:

* `max_payload_len`

    Specifies the maximal length of payload allowed when sending and receiving WebSocket frames. Defaults to `65536`.
* `max_recv_len`

    Specifies the maximal length of payload allowed when receiving WebSocket frames. Defaults to the value of `max_payload_len`.
* `max_send_len`

    Specifies the maximal length of payload allowed when sending WebSocket frames. Defaults to the value of `max_payload_len`.
* `send_unmasked`

    Specifies whether to send out an unmasked WebSocket frames. When it is `true`, unmasked frames are always sent. Default to `false`. RFC 6455 requires, however, that the client MUST send masked frames to the server, so never set this option to `true` unless you know what you are doing.
* `timeout`

    Specifies the default network timeout threshold in milliseconds. You can change this setting later via the `set_timeout` method call.

#### client:connect
`syntax: ok, err, res = wb:connect("ws://<host>:<port>/<path>")`

`syntax: ok, err, res = wb:connect("wss://<host>:<port>/<path>")`

`syntax: ok, err, res = wb:connect("ws://<host>:<port>/<path>", options)`

`syntax: ok, err, res = wb:connect("wss://<host>:<port>/<path>", options)`

Connects to the remote WebSocket service port and performs the websocket handshake process on the client side.

Before actually resolving the host name and connecting to the remote backend, this method will always look up the connection pool for matched idle connections created by previous calls of this method.

The third return value of this method contains the raw, plain-text response (status line and headers) to the handshake request. This allows the caller to perform additional validation and/or extract the response headers. When the connection is reused and no handshake request is sent, the string `"connection reused"` is returned in lieu of the response.

An optional Lua table can be specified as the last argument to this method to specify various connect options:

* `protocols`

    Specifies all the subprotocols used for the current WebSocket session. It could be a Lua table holding all the subprotocol names or just a single Lua string.
* `origin`

    Specifies the value of the `Origin` request header.
* `pool`

    Specifies a custom name for the connection pool being used. If omitted, then the connection pool name will be generated from the string template `<host>:<port>`.
* `pool_size`

  specify the size of the connection pool. If omitted and no
  `backlog` option was provided, no pool will be created. If omitted
  but `backlog` was provided, the pool will be created with a default
  size equal to the value of the [lua_socket_pool_size](https://github.com/openresty/lua-nginx-module/tree/master#lua_socket_pool_size)
  directive.
  The connection pool holds up to `pool_size` alive connections
  ready to be reused by subsequent calls to [connect](#client:connect), but
  note that there is no upper limit to the total number of opened connections
  outside of the pool. If you need to restrict the total number of opened
  connections, specify the `backlog` option.
  When the connection pool would exceed its size limit, the least recently used
  (kept-alive) connection already in the pool will be closed to make room for
  the current connection.
  Note that the cosocket connection pool is per Nginx worker process rather
  than per Nginx server instance, so the size limit specified here also applies
  to every single Nginx worker process. Also note that the size of the connection
  pool cannot be changed once it has been created.
  This option was first introduced in the `v0.10.14` release.

* `backlog`

  if specified, this module will limit the total number of opened connections
  for this pool. No more connections than `pool_size` can be opened
  for this pool at any time. If the connection pool is full, subsequent
  connect operations will be queued into a queue equal to this option's
  value (the "backlog" queue).
  If the number of queued connect operations is equal to `backlog`,
  subsequent connect operations will fail and return `nil` plus the
  error string `"too many waiting connect operations"`.
  The queued connect operations will be resumed once the number of connections
  in the pool is less than `pool_size`.
  The queued connect operation will abort once they have been queued for more
  than `connect_timeout`, controlled by
  [settimeouts](#client:set_timeout), and will return `nil` plus
  the error string `"timeout"`.
  This option was first introduced in the `v0.10.14` release.
* `ssl_verify`

    Specifies whether to perform SSL certificate verification during the
SSL handshake if the `wss://` scheme is used.

* `headers`

    Specifies custom headers to be sent in the handshake request. The table is expected to contain strings in the format `{"a-header: a header value", "another-header: another header value"}`.

* `client_cert`

    Specifies a client certificate chain cdata object that will be used while TLS handshaking with remote server. 
    These objects can be created using 
    [ngx.ssl.parse_pem_cert](https://github.com/openresty/lua-resty-core/blob/master/lib/ngx/ssl.md#parse_pem_cert) 
    function provided by lua-resty-core. 
    Note that specifying the `client_cert` option requires corresponding `client_priv_key` be provided too. See below.

* `client_priv_key`

    Specifies a private key corresponds to the `client_cert` option above. 
    These objects can be created using 
    [ngx.ssl.parse_pem_priv_key](https://github.com/openresty/lua-resty-core/blob/master/lib/ngx/ssl.md#parse_pem_priv_key) 
    function provided by lua-resty-core.

* `host`

    Specifies the value of the `Host` header sent in the handshake request. If not provided, the `Host` header will be derived from the hostname/address and port in the connection URI.

* `server_name`

    Specifies the server name (SNI) to use when performing the TLS handshake with the server. If not provided, the `host` value or the `<host/addr>:<port>` from the connection URI will be used.

* `key`

    Specifies the value of the `Sec-WebSocket-Key` header in the handshake request. The value should be a base64-encoded, 16 byte string conforming to the client handshake requirements of the [WebSocket RFC](https://datatracker.ietf.org/doc/html/rfc6455#section-4.1). If not provided, a key is randomly generated.

The SSL connection mode (`wss://`) requires at least `ngx_lua` 0.9.11 or OpenResty 1.7.4.1.

#### client:close
`syntax: ok, err = wb:close()`

Closes the current WebSocket connection. If no `close` frame is sent yet, then the `close` frame will be automatically sent.

#### client:set_keepalive
`syntax: ok, err = wb:set_keepalive(max_idle_timeout, pool_size)`

Puts the current WebSocket connection immediately into the `ngx_lua` cosocket connection pool.

You can specify the max idle timeout (in ms) when the connection is in the pool and the maximal size of the pool every nginx worker process.

In case of success, returns `1`. In case of errors, returns `nil` with a string describing the error.

Only call this method in the place you would have called the `close` method instead. Calling this method will immediately turn the current WebSocket object into the `closed` state. Any subsequent operations other than `connect()` on the current objet will return the `closed` error.

#### client:set_timeout
`syntax: wb:set_timeout(ms)`

Identical to the `set_timeout` method of the `resty.websocket.server` objects.

#### client:send_text
`syntax: bytes, err = wb:send_text(text)`

Identical to the [send_text](#send_text) method of the `resty.websocket.server` objects.

#### client:send_binary
`syntax: bytes, err = wb:send_binary(data)`

Identical to the [send_binary](#send_binary) method of the `resty.websocket.server` objects.

#### client:send_ping
`syntax: bytes, err = wb:send_ping()`

`syntax: bytes, err = wb:send_ping(msg)`

Identical to the [send_ping](#send_ping) method of the `resty.websocket.server` objects.

#### client:send_pong
`syntax: bytes, err = wb:send_pong()`

`syntax: bytes, err = wb:send_pong(msg)`

Identical to the [send_pong](#send_pong) method of the `resty.websocket.server` objects.

#### client:send_close
`syntax: bytes, err = wb:send_close()`

`syntax: bytes, err = wb:send_close(code, msg)`

Identical to the [send_close](#send_close) method of the `resty.websocket.server` objects.

#### client:send_frame
`syntax: bytes, err = wb:send_frame(fin, opcode, payload)`

Identical to the [send_frame](#send_frame) method of the `resty.websocket.server` objects.

To control whether to send unmasked frames, you can pass `true` to the `send_unmasked` option in the `new` constructor method. By default, masked frames are sent.

#### client:recv_frame
`syntax: data, typ, err = wb:recv_frame()`

Identical to the [recv_frame](#recv_frame) method of the `resty.websocket.server` objects.

## resty.websocket.protocol

To load this module, just do this

```lua
    local protocol = require "resty.websocket.protocol"
```

### Methods

#### protocol.recv_frame
`syntax: data, typ, err = protocol.recv_frame(socket, max_payload_len, force_masking)`

Receives a WebSocket frame from the wire.

#### protocol.build_frame
`syntax: frame = protocol.build_frame(fin, opcode, payload_len, payload, masking)`

Builds a raw WebSocket frame.

#### protocol.send_frame
`syntax: bytes, err = protocol.send_frame(socket, fin, opcode, payload, max_payload_len, masking)`

Sends a raw WebSocket frame.

## Automatic Error Logging

By default the underlying [ngx_lua](http://wiki.nginx.org/HttpLuaModule) module
does error logging when socket errors happen. If you are already doing proper error
handling in your own Lua code, then you are recommended to disable this automatic error logging by turning off [ngx_lua](http://wiki.nginx.org/HttpLuaModule)'s [lua_socket_log_errors](http://wiki.nginx.org/HttpLuaModule#lua_socket_log_errors) directive, that is,

```nginx
    lua_socket_log_errors off;
```

## Limitations

* This library cannot be used in code contexts like init_by_lua*, set_by_lua*, log_by_lua*, and
header_filter_by_lua* where the ngx_lua cosocket API is not available.
* The `resty.websocket` object instance cannot be stored in a Lua variable at the Lua module level,
because it will then be shared by all the concurrent requests handled by the same nginx
 worker process (see
http://wiki.nginx.org/HttpLuaModule#Data_Sharing_within_an_Nginx_Worker ) and
result in bad race conditions when concurrent requests are trying to use the same `resty.websocket` instance.
You should always initiate `resty.websocket` objects in function local
variables or in the `ngx.ctx` table. These places all have their own data copies for
each request.

## See Also
* Blog post [WebSockets with OpenResty](https://medium.com/p/1778601c9e05) by Aapo Talvensaari.
* the ngx_lua module: http://wiki.nginx.org/HttpLuaModule
* the websocket protocol: http://tools.ietf.org/html/rfc6455
* the [lua-resty-upload](https://github.com/agentzh/lua-resty-upload) library
* the [lua-resty-redis](https://github.com/agentzh/lua-resty-redis) library
* the [lua-resty-memcached](https://github.com/agentzh/lua-resty-memcached) library
* the [lua-resty-mysql](https://github.com/agentzh/lua-resty-mysql) library


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-websocket](https://github.com/openresty/lua-resty-websocket){target=_blank}.