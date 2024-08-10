# *logger-socket*: Raw-socket-based Logger Library for NGINX (based on nginx-module-lua)


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-logger-socket
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-logger-socket
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-logger-socket [v0.1](https://github.com/cloudflare/lua-resty-logger-socket/releases/tag/v0.1){target=_blank} 
released on Feb 18 2015.
    
<hr />

lua-resty-logger-socket - nonblocking remote access logging for Nginx

## Status

This library is still experimental and under early development.

## Description

This lua library is a remote logging module for ngx_lua:

http://wiki.nginx.org/HttpLuaModule

This is aimed to replace Nginx's standard [ngx_http_log_module](http://nginx.org/en/docs/http/ngx_http_log_module.html) to push access logs to a remote server via an nonblocking socket. A common remote log server supporting sockets is [syslog-ng](http://www.balabit.com/network-security/syslog-ng).

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

## Synopsis

```lua
    server {
        location / {
            log_by_lua '
                local logger = require "resty.logger.socket"
                if not logger.initted() then
                    local ok, err = logger.init{
                        host = 'xxx',
                        port = 1234,
                        flush_limit = 1234,
                        drop_limit = 5678,
                    }
                    if not ok then
                        ngx.log(ngx.ERR, "failed to initialize the logger: ",
                                err)
                        return
                    end
                end

                -- construct the custom access log message in
                -- the Lua variable "msg"

                local bytes, err = logger.log(msg)
                if err then
                    ngx.log(ngx.ERR, "failed to log message: ", err)
                    return
                end
            ';
        }
    }
```

## Methods

This logger module is designed to be shared inside an Nginx worker process by all the requests. So currently only one remote log server is supported. We may support multiple log server sharding in the future.

## init
`syntax: ok, err = logger.init(user_config)`

Initialize logger with user configurations. This logger must be initted before use. If you do not initialize the logger, you will get an error.

Available user configurations are listed as follows:

* `flush_limit`

    If the buffered messages' size plus the current message size reaches (`>=`) this limit (in bytes), the buffered log messages will be written to log server. Default to 4096 (4KB).

* `drop_limit`

    If the buffered messages' size plus the current message size is larger than this limit (in bytes), the current log message will be dropped because of limited buffer size. Default drop_limit is 1048576 (1MB).

* `timeout`

    Sets the timeout (in ms) protection for subsequent operations, including the *connect* method. Default value is 1000 (1 sec).

* `host`

    log server host.

* `port`

    log server port number.

* `path`

    If the log server uses a stream-typed unix domain socket, `path` is the socket file path. Note that host/port and path cannot both be empty. At least one must be supplied.

* `max_retry_times`

    Max number of retry times after a connect to a log server failed or send log messages to a log server failed.

* `retry_interval`

    The time delay (in ms) before retry to connect to a log server or retry to send log messages to a log server, default to 100 (0.1s).

* `pool_size`

    Keepalive pool size used by sock:keepalive. Default to 10.

* `max_buffer_reuse`

    Max number of reuse times of internal logging buffer before creating a new one (to prevent memory leak).

* `periodic_flush`

    Periodic flush interval (in seconds). Set to `nil` to turn off this feature.

* `ssl`

    Boolean, enable or disable connecting via SSL. Default to false.

* `ssl_verify`

    Boolean, enable or disable verifying host and certificate match. Default to true.

* `sni_host`

    Set the hostname to send in SNI and to use when verifying certificate match.

## initted
`syntax: initted = logger.initted()`

Get a boolean value indicating whether this module has been initted (by calling the [init](#init) method).

## log
`syntax: bytes, err = logger.log(msg)`

Log a message. By default, the log message will be buffered in the logger module until `flush_limit` is reached in which case the logger will flush all the buffered messages to remote log server via a socket.
`bytes` is the number of bytes that successfully buffered in the logger. If `bytes` is nil, `err` is a string describing what kind of error happens this time. If bytes is not nil, then `err` is a previous error message. `err` can be nil when `bytes` is not nil.

## flush
`syntax: bytes, err = logger.flush()`

Flushes any buffered messages out to remote immediately. Usually you do not need
to call this manually because flushing happens automatically when the buffer is full.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-logger-socket](https://github.com/cloudflare/lua-resty-logger-socket){target=_blank}.