---

title: "Lua scripting support for NGINX streams"
description: "RPM package nginx-module-stream-lua. Embed the power of Lua into Nginx stream/TCP Servers. "

---

# *stream-lua*: Lua scripting support for NGINX streams


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9 and 10
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023+"

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-stream-lua
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-stream-lua
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_stream_lua_module.so;
```


This document describes nginx-module-stream-lua [v0.0.16](https://github.com/openresty/stream-lua-nginx-module/releases/tag/v0.0.16){target=_blank} 
released on Jan 17 2025.

<hr />

## Name

ngx_stream_lua_module - Embed the power of Lua into Nginx stream/TCP Servers.

This module is a core component of OpenResty. If you are using this module,
then you are essentially using OpenResty.

instructions](#installation).

## Status

Production ready.

## Synopsis

```nginx
events {
    worker_connections 1024;
}

stream {
    # define a TCP server listening on the port 1234:
    server {
        listen 1234;

        content_by_lua_block {
            ngx.say("Hello, Lua!")
        }
    }
}
```

Set up as an SSL TCP server:

```nginx
stream {
    server {
        listen 4343 ssl;

        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         AES128-SHA:AES256-SHA:RC4-SHA:DES-CBC3-SHA:RC4-MD5;
        ssl_certificate     /path/to/cert.pem;
        ssl_certificate_key /path/to/cert.key;
        ssl_session_cache   shared:SSL:10m;
        ssl_session_timeout 10m;

        content_by_lua_block {
            local sock = assert(ngx.req.socket(true))
            local data = sock:receive()  -- read a line from downstream
            if data == "thunder!" then
                ngx.say("flash!")  -- output data
            else
                ngx.say("boom!")
            end
            ngx.say("the end...")
        }
    }
}
```

Listening on a UNIX domain socket is also supported:

```nginx
stream {
    server {
        listen unix:/tmp/nginx.sock;

        content_by_lua_block {
            ngx.say("What's up?")
            ngx.flush(true)  -- flush any pending output and wait
            ngx.sleep(3)  -- sleeping for 3 sec
            ngx.say("Bye bye...")
        }
    }
}
```


## Description

This is a port of the
[ngx_http_lua_module](https://github.com/openresty/lua-nginx-module#readme) to
the Nginx "stream" subsystem so as to support generic stream/TCP clients.

The available Lua APIs and Nginx directives remain the same as those of the
ngx_http_lua module.


## Directives

The following directives are ported directly from ngx_http_lua. Please check
the documentation of ngx_http_lua for more details about their usage and
behavior.

* [lua_load_resty_core](https://github.com/openresty/lua-nginx-module#lua_load_resty_core)
* [lua_code_cache](https://github.com/openresty/lua-nginx-module#lua_code_cache)
* [lua_regex_cache_max_entries](https://github.com/openresty/lua-nginx-module#lua_regex_cache_max_entries)
* [lua_package_path](https://github.com/openresty/lua-nginx-module#lua_package_path)
* [lua_package_cpath](https://github.com/openresty/lua-nginx-module#lua_package_cpath)
* [init_by_lua_block](https://github.com/openresty/lua-nginx-module#init_by_lua_block)
* [init_by_lua_file](https://github.com/openresty/lua-nginx-module#init_by_lua_file)
* [init_worker_by_lua_block](https://github.com/openresty/lua-nginx-module#init_worker_by_lua_block)
* [init_worker_by_lua_file](https://github.com/openresty/lua-nginx-module#init_worker_by_lua_file)
* [preread_by_lua_block](#preread_by_lua_block)
* [preread_by_lua_file](#preread_by_lua_file)
* [content_by_lua_block](https://github.com/openresty/lua-nginx-module#content_by_lua_block)
* [content_by_lua_file](https://github.com/openresty/lua-nginx-module#content_by_lua_file)
* [balancer_by_lua_block](https://github.com/openresty/lua-nginx-module#balancer_by_lua_block)
* [balancer_by_lua_file](https://github.com/openresty/lua-nginx-module#balancer_by_lua_file)
* [log_by_lua_block](#log_by_lua_block)
* [log_by_lua_file](#log_by_lua_file)
* [ssl_client_hello_by_lua_block](https://github.com/openresty/lua-nginx-module#ssl_client_hello_by_lua_block)
* [ssl_client_hello_by_lua_file](https://github.com/openresty/lua-nginx-module#ssl_client_hello_by_lua_file)
* [ssl_certificate_by_lua_block](https://github.com/openresty/lua-nginx-module#ssl_certificate_by_lua_block)
* [ssl_certificate_by_lua_file](https://github.com/openresty/lua-nginx-module#ssl_certificate_by_lua_file)
* [lua_shared_dict](https://github.com/openresty/lua-nginx-module#lua_shared_dict)
* [lua_socket_connect_timeout](https://github.com/openresty/lua-nginx-module#lua_socket_connect_timeout)
* [lua_socket_buffer_size](https://github.com/openresty/lua-nginx-module#lua_socket_buffer_size)
* [lua_socket_pool_size](https://github.com/openresty/lua-nginx-module#lua_socket_pool_size)
* [lua_socket_keepalive_timeout](https://github.com/openresty/lua-nginx-module#lua_socket_keepalive_timeout)
* [lua_socket_log_errors](https://github.com/openresty/lua-nginx-module#lua_socket_log_errors)
* [lua_ssl_ciphers](https://github.com/openresty/lua-nginx-module#lua_ssl_ciphers)
* [lua_ssl_crl](https://github.com/openresty/lua-nginx-module#lua_ssl_crl)
* [lua_ssl_protocols](https://github.com/openresty/lua-nginx-module#lua_ssl_protocols)
* [lua_ssl_certificate](https://github.com/openresty/lua-nginx-module#lua_ssl_certificate)
* [lua_ssl_certificate_key](https://github.com/openresty/lua-nginx-module#lua_ssl_certificate_key)
* [lua_ssl_trusted_certificate](https://github.com/openresty/lua-nginx-module#lua_ssl_trusted_certificate)
* [lua_ssl_verify_depth](https://github.com/openresty/lua-nginx-module#lua_ssl_verify_depth)
* [lua_ssl_conf_command](https://github.com/openresty/lua-nginx-module#lua_ssl_conf_command)
* [lua_check_client_abort](https://github.com/openresty/lua-nginx-module#lua_check_client_abort)
* [lua_max_pending_timers](https://github.com/openresty/lua-nginx-module#lua_max_pending_timers)
* [lua_max_running_timers](https://github.com/openresty/lua-nginx-module#lua_max_running_timers)
* [lua_sa_restart](https://github.com/openresty/lua-nginx-module#lua_sa_restart)
* [lua_add_variable](#lua_add_variable)
* [lua_capture_error_log](https://github.com/openresty/lua-nginx-module#lua_capture_error_log)
* [preread_by_lua_no_postpone](#preread_by_lua_no_postpone)

The [send_timeout](https://nginx.org/r/send_timeout) directive in the Nginx
"http" subsystem is missing in the "stream" subsystem. As such,
ngx_stream_lua_module uses the `lua_socket_send_timeout` directive for this
purpose instead.

**Note:** the lingering close directive that used to exist in older version of
`stream_lua_nginx_module` has been removed and can now be simulated with the
newly added [tcpsock:shutdown](#tcpsockshutdown) API if necessary.


## preread_by_lua_block

**syntax:** *preread_by_lua_block { lua-script }*

**context:** *stream, server*

**phase:** *preread*

Acts as a `preread` phase handler and executes Lua code string specified in `lua-script` for every connection
(or packet in datagram mode).
The Lua code may make [API calls](#nginx-api-for-lua) and is executed as a new spawned coroutine in an independent global environment (i.e. a sandbox).

It is possible to acquire the raw request socket using [ngx.req.socket](https://github.com/openresty/lua-nginx-module#ngxreqsocket)
and receive data from or send data to the client. However, keep in mind that calling the `receive()` method
of the request socket will consume the data from the buffer and such consumed data will not be seen by handlers
further down the chain.

The `preread_by_lua_block` code will always run at the end of the `preread` processing phase unless
[preread\_by\_lua\_no\_postpone](#preread_by_lua_no_postpone) is turned on.

This directive was first introduced in the `v0.0.3` release.

[Back to TOC](#directives)

## preread_by_lua_file

**syntax:** *preread_by_lua_file &lt;path-to-lua-script-file&gt;*

**context:** *stream, server*

**phase:** *preread*

Equivalent to [preread_by_lua_block](#preread_by_lua_block), except that the file specified by `<path-to-lua-script-file>` contains the Lua code
or LuaJIT bytecode to be executed.

Nginx variables can be used in the `<path-to-lua-script-file>` string to provide flexibility. This however carries some risks and is not ordinarily recommended.

When a relative path like `foo/bar.lua` is given, it will be turned into the absolute path relative to the `server prefix` path determined by the `-p PATH` command-line option given when starting the Nginx server.

When the Lua code cache is turned on (by default), the user code is loaded once at the first connection and cached. The Nginx config must be reloaded each time the Lua source file is modified. The Lua code cache can be temporarily disabled during development by switching [lua_code_cache](#lua_code_cache) `off` in `nginx.conf` to avoid having to reload Nginx.

This directive was first introduced in the `v0.0.3` release.

[Back to TOC](#directives)

## log_by_lua_block

**syntax:** *log_by_lua_block { lua-script }*

**context:** *stream, server*

**phase:** *log*

Runs the Lua source code specified as `<lua-script>` during the `log` request processing phase. This does not replace the current access logs, but runs before.

Yielding APIs such as `ngx.req.socket`, `ngx.socket.*`, `ngx.sleep`, or `ngx.say` are **not** available in this phase.

This directive was first introduced in the `v0.0.3` release.

[Back to TOC](#directives)

## log_by_lua_file

**syntax:** *log_by_lua_file &lt;path-to-lua-script-file&gt;*

**context:** *stream, server*

**phase:** *log*

Equivalent to [log_by_lua_block](#log_by_lua_block), except that the file specified by `<path-to-lua-script-file>` contains the Lua code
or LuaJIT bytecode to be executed.

Nginx variables can be used in the `<path-to-lua-script-file>` string to provide flexibility. This however carries some risks and is not ordinarily recommended.

When a relative path like `foo/bar.lua` is given, it will be turned into the absolute path relative to the `server prefix` path determined by the `-p PATH` command-line option given when starting the Nginx server.

When the Lua code cache is turned on (by default), the user code is loaded once at the first connection and cached. The Nginx config must be reloaded each time the Lua source file is modified. The Lua code cache can be temporarily disabled during development by switching [lua_code_cache](#lua_code_cache) `off` in `nginx.conf` to avoid having to reload Nginx.

This directive was first introduced in the `v0.0.3` release.

[Back to TOC](#directives)

## lua_add_variable

**syntax:** *lua_add_variable $var*

**context:** *stream*

Add the variable `$var` to the "stream" subsystem and makes it changeable. If `$var` already exists,
this directive will do nothing.

By default, variables added using this directive are considered "not found" and reading them
using `ngx.var` will return `nil`. However, they could be re-assigned via the `ngx.var.VARIABLE` API at any time.

This directive was first introduced in the `v0.0.4` release.

[Back to TOC](#directives)

## preread_by_lua_no_postpone

**syntax:** *preread_by_lua_no_postpone on|off*

**context:** *stream*

Controls whether or not to disable postponing [preread\_by\_lua*](#preread_by_lua_block) directives
to run at the end of the `preread` processing phase. By default, this directive is turned off
and the Lua code is postponed to run at the end of the `preread` phase.

This directive was first introduced in the `v0.0.4` release.

[Back to TOC](#directives)

## Nginx API for Lua

Many Lua API functions are ported from ngx_http_lua. Check out the official
manual of ngx_http_lua for more details on these Lua API functions.

* [ngx.var.VARIABLE](https://github.com/openresty/lua-nginx-module#ngxvarvariable)

This module fully supports the new variable subsystem inside the Nginx stream core. You may access any
[built-in variables](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#variables) provided by the stream core or
other stream modules.
* [Core constants](https://github.com/openresty/lua-nginx-module#core-constants)

    `ngx.OK`, `ngx.ERROR`, and etc.
* [Nginx log level constants](https://github.com/openresty/lua-nginx-module#nginx-log-level-constants)

    `ngx.ERR`, `ngx.WARN`, and etc.
* [print](https://github.com/openresty/lua-nginx-module#print)
* [ngx.ctx](https://github.com/openresty/lua-nginx-module#ngxctx)
* [ngx.balancer](https://github.com/openresty/lua-resty-core/blob/master/lib/ngx/balancer.md)

* [ngx.req.socket](https://github.com/openresty/lua-nginx-module#ngxreqsocket)

Only raw request sockets are supported, for obvious reasons. The `raw` argument value
is ignored and the raw request socket is always returned. Unlike ngx_http_lua,
you can still call output API functions like `ngx.say`, `ngx.print`, and `ngx.flush`
after acquiring the raw request socket via this function.

When the stream server is in UDP mode, reading from the downstream socket returned by the
`ngx.req.socket` call will only return the content of a single packet. Therefore
the reading call will never block and will return `nil, "no more data"` when all the
data from the datagram has been consumed. However, you may choose to send multiple UDP
packets back to the client using the downstream socket.

The raw TCP sockets returned by this module will contain the following extra method:

[Back to TOC](#directives)

## reqsock:receiveany

**syntax:** *data, err = reqsock:receiveany(max)*

**context:** *content_by_lua&#42;, ngx.timer.&#42;, ssl_certificate_by_lua&#42;*

This method is similar to [tcpsock:receiveany](https://github.com/openresty/lua-nginx-module#tcpsockreceiveany) method

This method was introduced into `stream-lua-nginx-module` since `v0.0.8`.

[Back to TOC](#directives)

## tcpsock:shutdown

**syntax:** *ok, err = tcpsock:shutdown("send")*

**context:** *content_by_lua&#42;*

Shuts down the write part of the request socket, prevents all further writing to the client
and sends TCP FIN, while keeping the reading half open.

Currently only the `"send"` direction is supported. Using any parameters other than "send" will return
an error.

If you called any output functions (like [ngx.say](https://github.com/openresty/lua-nginx-module#ngxsay))
before calling this method, consider use `ngx.flush(true)` to make sure all busy buffers are complely
flushed before shutting down the socket. If any busy buffers were detected, this method will return `nil`
will error message `"socket busy writing"`.

This feature is particularly useful for protocols that generate a response before actually
finishing consuming all incoming data. Normally, the kernel will send RST to the client when
[tcpsock:close](https://github.com/openresty/lua-nginx-module#tcpsockclose) is called without
emptying the receiving buffer first. Calling this method will allow you to keep reading from
the receiving buffer and prevents RST from being sent.

You can also use this method to simulate lingering close similar to that
[provided by the ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html#lingering_close)
for protocols in need of such behavior. Here is an example:

```lua
local LINGERING_TIME = 30 -- 30 seconds
local LINGERING_TIMEOUT = 5000 -- 5 seconds

local ok, err = sock:shutdown("send")
if not ok then
    ngx.log(ngx.ERR, "failed to shutdown: ", err)
    return
end

local deadline = ngx.time() + LINGERING_TIME

sock:settimeouts(nil, nil, LINGERING_TIMEOUT)

repeat
    local data, _, partial = sock:receive(1024)
until (not data and not partial) or ngx.time() >= deadline
```

[Back to TOC](#directives)

## reqsock:peek

**syntax:** *ok, err = reqsock:peek(size)*

**context:** *preread_by_lua&#42;*

Peeks into the [preread](https://nginx.org/en/docs/stream/stream_processing.html#preread_phase)
buffer that contains downstream data sent by the client without consuming them.
That is, data returned by this API will still be forwarded upstream in later phases.

This function takes a single required argument, `size`, which is the number of bytes to be peeked.
Repeated calls to this function always returns data from the beginning of the preread buffer.

Note that preread phase happens after the TLS handshake. If the stream server was configured with
TLS enabled, the returned data will be in clear text.

If preread buffer does not have the requested amount of data, then the current Lua thread will
be yielded until more data is available, [`preread_buffer_size`](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#preread_buffer_size)
has been exceeded, or [`preread_timeout`](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#preread_timeout)
has elapsed. Successful calls always return the requested amounts of data, that is, no partial
data will be returned.

When [`preread_buffer_size`](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#preread_buffer_size)
has been exceeded, the current stream session will be terminated with the
[session status code](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#var_status) `400`
immediately by the stream core module, with error message `"preread buffer full"` that will be printed to the error log.

When [`preread_timeout`](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#preread_timeout) has been exceeded,
the current stream session will be terminated with the
[session status code](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#var_status) `200` immediately by the stream core module.

In both cases, no further processing on the session is possible (except `log_by_lua*`). The connection will be closed by the
stream core module automatically.

Note that this API cannot be used if consumption of client data has occurred. For example, after calling
`reqsock:receive`. If such an attempt was made, the Lua error `"attempt to peek on a consumed socket"` will
be thrown. Consuming client data after calling this API is allowed and safe.

Here is an example of using this API:

```lua
local sock = assert(ngx.req.socket())

local data = assert(sock:peek(1)) -- peek the first 1 byte that contains the length
data = string.byte(data)

data = assert(sock:peek(data + 1)) -- peek the length + the size byte

local payload = data:sub(2) -- trim the length byte to get actual payload

ngx.log(ngx.INFO, "payload is: ", payload)
```

This API was first introduced in the `v0.0.6` release.

[Back to TOC](#directives)

* [ngx.print](https://github.com/openresty/lua-nginx-module#ngxprint)
* [ngx.say](https://github.com/openresty/lua-nginx-module#ngxsay)
* [ngx.log](https://github.com/openresty/lua-nginx-module#ngxlog)
* [ngx.flush](https://github.com/openresty/lua-nginx-module#ngxflush)

    This call currently ignores the `wait` argument and always wait for all the pending
output to be completely flushed out (to the system socket send buffers).
* [ngx.exit](https://github.com/openresty/lua-nginx-module#ngxexit)
* [ngx.eof](https://github.com/openresty/lua-nginx-module#ngxeof)
* [ngx.sleep](https://github.com/openresty/lua-nginx-module#ngxsleep)
* [ngx.escape_uri](https://github.com/openresty/lua-nginx-module#ngxescape_uri)
* [ngx.unescape_uri](https://github.com/openresty/lua-nginx-module#ngxunescape_uri)
* [ngx.encode_args](https://github.com/openresty/lua-nginx-module#ngxencode_args)
* [ngx.decode_args](https://github.com/openresty/lua-nginx-module#ngxdecode_args)
* [ngx.encode_base64](https://github.com/openresty/lua-nginx-module#ngxencode_base64)
* [ngx.decode_base64](https://github.com/openresty/lua-nginx-module#ngxdecode_base64)
* [ngx.crc32_short](https://github.com/openresty/lua-nginx-module#ngxcrc32_short)
* [ngx.crc32_long](https://github.com/openresty/lua-nginx-module#ngxcrc32_long)
* [ngx.hmac_sha1](https://github.com/openresty/lua-nginx-module#ngxhmac_sha1)
* [ngx.md5](https://github.com/openresty/lua-nginx-module#ngxmd5)
* [ngx.md5_bin](https://github.com/openresty/lua-nginx-module#ngxmd5_bin)
* [ngx.sha1_bin](https://github.com/openresty/lua-nginx-module#ngxsha1_bin)
* [ngx.quote_sql_str](https://github.com/openresty/lua-nginx-module#ngxquote_sql_str)
* [ngx.today](https://github.com/openresty/lua-nginx-module#ngxtoday)
* [ngx.time](https://github.com/openresty/lua-nginx-module#ngxtime)
* [ngx.now](https://github.com/openresty/lua-nginx-module#ngxnow)
* [ngx.update_time](https://github.com/openresty/lua-nginx-module#ngxupdate_time)
* [ngx.localtime](https://github.com/openresty/lua-nginx-module#ngxlocaltime)
* [ngx.utctime](https://github.com/openresty/lua-nginx-module#ngxutctime)
* [ngx.re.match](https://github.com/openresty/lua-nginx-module#ngxrematch)
* [ngx.re.find](https://github.com/openresty/lua-nginx-module#ngxrefind)
* [ngx.re.gmatch](https://github.com/openresty/lua-nginx-module#ngxregmatch)
* [ngx.re.sub](https://github.com/openresty/lua-nginx-module#ngxresub)
* [ngx.re.gsub](https://github.com/openresty/lua-nginx-module#ngxregsub)
* [ngx.shared.DICT](https://github.com/openresty/lua-nginx-module#ngxshareddict)
* [ngx.socket.tcp](https://github.com/openresty/lua-nginx-module#ngxsockettcp)
* [ngx.socket.udp](https://github.com/openresty/lua-nginx-module#ngxsocketudp)
* [ngx.socket.connect](https://github.com/openresty/lua-nginx-module#ngxsocketconnect)
* [ngx.get_phase](https://github.com/openresty/lua-nginx-module#ngxget_phase)
* [ngx.thread.spawn](https://github.com/openresty/lua-nginx-module#ngxthreadspawn)
* [ngx.thread.wait](https://github.com/openresty/lua-nginx-module#ngxthreadwait)
* [ngx.thread.kill](https://github.com/openresty/lua-nginx-module#ngxthreadkill)
* [ngx.on_abort](https://github.com/openresty/lua-nginx-module#ngxon_abort)
* [ngx.timer.at](https://github.com/openresty/lua-nginx-module#ngxtimerat)
* [ngx.timer.running_count](https://github.com/openresty/lua-nginx-module#ngxtimerrunning_count)
* [ngx.timer.pending_count](https://github.com/openresty/lua-nginx-module#ngxtimerpending_count)
* [ngx.config.debug](https://github.com/openresty/lua-nginx-module#ngxconfigdebug)
* [ngx.config.subsystem](https://github.com/openresty/lua-nginx-module#ngxconfigsubsystem)

    Always takes the Lua string value `"stream"` in this module.
* [ngx.config.prefix](https://github.com/openresty/lua-nginx-module#ngxconfigprefix)
* [ngx.config.nginx_version](https://github.com/openresty/lua-nginx-module#ngxconfignginx_version)
* [ngx.config.nginx_configure](https://github.com/openresty/lua-nginx-module#ngxconfignginx_configure)
* [ngx.config.ngx_lua_version](https://github.com/openresty/lua-nginx-module#ngxconfigngx_lua_version)
* [ngx.worker.exiting](https://github.com/openresty/lua-nginx-module#ngxworkerexiting)
* [ngx.worker.pid](https://github.com/openresty/lua-nginx-module#ngxworkerpid)
* [ngx.worker.pids](https://github.com/openresty/lua-nginx-module#ngxworkerpids)
* [ngx.worker.count](https://github.com/openresty/lua-nginx-module#ngxworkercount)
* [ngx.worker.id](https://github.com/openresty/lua-nginx-module#ngxworkerid)
* [coroutine.create](https://github.com/openresty/lua-nginx-module#coroutinecreate)
* [coroutine.resume](https://github.com/openresty/lua-nginx-module#coroutineresume)
* [coroutine.yield](https://github.com/openresty/lua-nginx-module#coroutineyield)
* [coroutine.wrap](https://github.com/openresty/lua-nginx-module#coroutinewrap)
* [coroutine.running](https://github.com/openresty/lua-nginx-module#coroutinerunning)
* [coroutine.status](https://github.com/openresty/lua-nginx-module#coroutinestatus)


## Nginx Compatibility

The latest version of this module is compatible with the following versions of Nginx:

* 1.25.x (last tested: 1.25.1)
* 1.21.x (last tested: 1.21.4)
* 1.19.x (last tested: 1.19.3)
* 1.17.x (last tested: 1.17.8)
* 1.15.x (last tested: 1.15.8)
* 1.13.x (last tested: 1.13.6)

Nginx cores older than 1.13.6 (exclusive) are *not* tested and may or may not
work. Use at your own risk!


## tell nginx's build system where to find LuaJIT 2.1:
export LUAJIT_LIB=/path/to/luajit/lib
export LUAJIT_INC=/path/to/luajit/include/luajit-2.1

## Here we assume Nginx is to be installed under /opt/nginx/.
./configure --prefix=/opt/nginx \
        --with-ld-opt="-Wl,-rpath,/path/to/luajit-or-lua/lib" \
        --with-stream \
        --with-stream_ssl_module \
        --add-module=/path/to/stream-lua-nginx-module

## Code Repository

The code repository of this project is hosted on GitHub at
[openresty/stream-lua-nginx-module](https://github.com/openresty/stream-lua-nginx-module).


## See Also

* [ngx_http_lua_module](https://github.com/openresty/lua-nginx-module)
* [ngx_stream_echo_module](https://github.com/openresty/stream-echo-nginx-module)
* [OpenResty](https://openresty.org/)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-stream-lua](https://github.com/openresty/stream-lua-nginx-module){target=_blank}.