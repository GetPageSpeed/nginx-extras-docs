# *core*: New FFI-based API for lua-nginx-module


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-core
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-core
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-core [v0.1.27](https://github.com/openresty/lua-resty-core/releases/tag/v0.1.27){target=_blank} 
released on Jun 19 2023.
    
<hr />

lua-resty-core - New FFI-based Lua API for ngx_http_lua_module and/or ngx_stream_lua_module

## Status

This library is production ready.

## Synopsis

This library is automatically loaded by default in OpenResty 1.15.8.1. This
behavior can be disabled via the
[lua_load_resty_core](https://github.com/openresty/lua-nginx-module#lua_load_resty_core)
directive, but note that the use of this library is vividly recommended, as its
FFI implementation is both faster, safer, and more complete than the Lua C API
of the ngx_lua module.

If you are using an older version of OpenResty, you must load this library like
so:

```nginx
    # nginx.conf

    http {
        # you do NOT need to configure the following line when you
        # are using the OpenResty bundle 1.4.3.9+.
        init_by_lua_block {
            require "resty.core"
            collectgarbage("collect")  -- just to collect any garbage
        }

        ...
    }
```

## Description

This pure Lua library reimplements part of the [ngx_lua](https://github.com/openresty/lua-nginx-module#readme) module's
[Nginx API for Lua](https://github.com/openresty/lua-nginx-module#nginx-api-for-lua)
with LuaJIT FFI and installs the new FFI-based Lua API into the ngx.* and ndk.* namespaces
used by the ngx_lua module.

In addition, this Lua library implements any significant new Lua APIs of
the [ngx_lua](https://github.com/openresty/lua-nginx-module#readme) module
as proper Lua modules, like [ngx.semaphore](#ngxsemaphore) and [ngx.balancer](#ngxbalancer).

The FFI-based Lua API can work with LuaJIT's JIT compiler. ngx_lua's default API is based on the standard
Lua C API, which will never be JIT compiled and the user Lua code is always interpreted (slowly).

Support for the new [ngx_stream_lua_module](https://github.com/openresty/stream-lua-nginx-module) has also begun.

This library is shipped with the OpenResty bundle by default. So you do not really need to worry about the dependencies
and requirements.

## Prerequisites

**WARNING** This library is included with every OpenResty release. You should use the bundled version
of this library in the particular OpenResty release you are using. Otherwise you may run
into serious compatibility issues.

* LuaJIT 2.1 (for now, it is the v2.1 git branch in the official luajit-2.0 git repository: http://luajit.org/download.html )
* [ngx_http_lua_module](https://github.com/openresty/lua-nginx-module) v0.10.21.
* [ngx_stream_lua_module](https://github.com/openresty/stream-lua-nginx-module) v0.0.11.
* [lua-resty-lrucache](https://github.com/openresty/lua-resty-lrucache)

## API Implemented

## resty.core.hash

* [ngx.md5](https://github.com/openresty/lua-nginx-module#ngxmd5)
* [ngx.md5_bin](https://github.com/openresty/lua-nginx-module#ngxmd5_bin)
* [ngx.sha1_bin](https://github.com/openresty/lua-nginx-module#ngxsha1_bin)

## resty.core.base64

* [ngx.encode_base64](https://github.com/openresty/lua-nginx-module#ngxencode_base64)
* [ngx.decode_base64](https://github.com/openresty/lua-nginx-module#ngxdecode_base64)

## resty.core.uri

* [ngx.escape_uri](https://github.com/openresty/lua-nginx-module#ngxescape_uri)
* [ngx.unescape_uri](https://github.com/openresty/lua-nginx-module#ngxunescape_uri)

## resty.core.regex

* [ngx.re.match](https://github.com/openresty/lua-nginx-module#ngxrematch)
* [ngx.re.gmatch](https://github.com/openresty/lua-nginx-module#ngxregmatch)
* [ngx.re.find](https://github.com/openresty/lua-nginx-module#ngxrefind)
* [ngx.re.sub](https://github.com/openresty/lua-nginx-module#ngxresub)
* [ngx.re.gsub](https://github.com/openresty/lua-nginx-module#ngxregsub)

## resty.core.exit

* [ngx.exit](https://github.com/openresty/lua-nginx-module#ngxexit)

## resty.core.shdict

* [ngx.shared.DICT.get](https://github.com/openresty/lua-nginx-module#ngxshareddictget)
* [ngx.shared.DICT.get_stale](https://github.com/openresty/lua-nginx-module#ngxshareddictget_stale)
* [ngx.shared.DICT.incr](https://github.com/openresty/lua-nginx-module#ngxshareddictincr)
* [ngx.shared.DICT.set](https://github.com/openresty/lua-nginx-module#ngxshareddictset)
* [ngx.shared.DICT.safe_set](https://github.com/openresty/lua-nginx-module#ngxshareddictsafe_set)
* [ngx.shared.DICT.add](https://github.com/openresty/lua-nginx-module#ngxshareddictadd)
* [ngx.shared.DICT.safe_add](https://github.com/openresty/lua-nginx-module#ngxshareddictsafe_add)
* [ngx.shared.DICT.replace](https://github.com/openresty/lua-nginx-module#ngxshareddictreplace)
* [ngx.shared.DICT.delete](https://github.com/openresty/lua-nginx-module#ngxshareddictdelete)
* [ngx.shared.DICT.ttl](https://github.com/openresty/lua-nginx-module#ngxshareddictttl)
* [ngx.shared.DICT.expire](https://github.com/openresty/lua-nginx-module#ngxshareddictexpire)
* [ngx.shared.DICT.flush_all](https://github.com/openresty/lua-nginx-module#ngxshareddictflush_all)
* [ngx.shared.DICT.free_space](https://github.com/openresty/lua-nginx-module#ngxshareddictfree_space)
* [ngx.shared.DICT.capacity](https://github.com/openresty/lua-nginx-module#ngxshareddictcapacity)

## resty.core.var

* [ngx.var.VARIABLE](https://github.com/openresty/lua-nginx-module#ngxvarvariable)

## resty.core.ctx

* [ngx.ctx](https://github.com/openresty/lua-nginx-module#ngxctx)

## get_ctx_table

**syntax:** *ctx = resty.core.ctx.get_ctx_table(ctx?)*

Similar to [ngx.ctx](#restycorectx) but it accepts an optional `ctx` argument.
It will use the `ctx` from caller instead of creating a new table
when the `ctx` table does not exist.

Notice: the `ctx` table will be used in the current request's whole life cycle.
Please be very careful when you try to reuse the `ctx` table.
You need to make sure there is no Lua code using or going to use the `ctx` table
in the current request before you reusing the `ctx` table in some other place.

## resty.core.request

* [ngx.req.get_headers](https://github.com/openresty/lua-nginx-module#ngxreqget_headers)
* [ngx.req.get_uri_args](https://github.com/openresty/lua-nginx-module#ngxreqget_uri_args)
* [ngx.req.start_time](https://github.com/openresty/lua-nginx-module#ngxreqstart_time)
* [ngx.req.get_method](https://github.com/openresty/lua-nginx-module#ngxreqget_method)
* [ngx.req.set_method](https://github.com/openresty/lua-nginx-module#ngxreqset_method)
* [ngx.req.set_header](https://github.com/openresty/lua-nginx-module#ngxreqset_header)
* [ngx.req.clear_header](https://github.com/openresty/lua-nginx-module#ngxreqclear_header)

## resty.core.response

* [ngx.header.HEADER](https://github.com/openresty/lua-nginx-module#ngxheaderheader)

## resty.core.misc

* [ngx.status](https://github.com/openresty/lua-nginx-module#ngxstatus)
* [ngx.is_subrequest](https://github.com/openresty/lua-nginx-module#ngxis_subrequest)
* [ngx.headers_sent](https://github.com/openresty/lua-nginx-module#ngxheaders_sent)
* [ngx.req.is_internal](https://github.com/openresty/lua-nginx-module#ngxreqis_internal)

## resty.core.time

* [ngx.time](https://github.com/openresty/lua-nginx-module#ngxtime)
* [ngx.now](https://github.com/openresty/lua-nginx-module#ngxnow)
* [ngx.update_time](https://github.com/openresty/lua-nginx-module#ngxupdate_time)
* [ngx.localtime](https://github.com/openresty/lua-nginx-module#ngxlocaltime)
* [ngx.utctime](https://github.com/openresty/lua-nginx-module#ngxutctime)
* [ngx.cookie_time](https://github.com/openresty/lua-nginx-module#ngxcookie_time)
* [ngx.http_time](https://github.com/openresty/lua-nginx-module#ngxhttp_time)
* [ngx.parse_http_time](https://github.com/openresty/lua-nginx-module#ngxparse_http_time)
* [monotonic_msec](./lib/resty/core/time.md#monotonic_msec)
* [monotonic_time](./lib/resty/core/time.md#monotonic_time)

## resty.core.worker

* [ngx.worker.exiting](https://github.com/openresty/lua-nginx-module#ngxworkerexiting)
* [ngx.worker.pid](https://github.com/openresty/lua-nginx-module#ngxworkerpid)
* [ngx.worker.id](https://github.com/openresty/lua-nginx-module#ngxworkerid)
* [ngx.worker.count](https://github.com/openresty/lua-nginx-module#ngxworkercount)

## resty.core.phase

* [ngx.get_phase](https://github.com/openresty/lua-nginx-module#ngxget_phase)

## resty.core.ndk

* [ndk.set_var](https://github.com/openresty/lua-nginx-module#ndkset_vardirective)

## resty.core.socket

* [socket.setoption](https://github.com/openresty/lua-nginx-module#tcpsocksetoption)
* [socket.setclientcert](https://github.com/openresty/lua-nginx-module#tcpsocksetclientcert)
* [socket.sslhandshake](https://github.com/openresty/lua-nginx-module#tcpsocksslhandshake)

## resty.core.param

* [ngx.arg](https://github.com/openresty/lua-nginx-module#ngxarg) (getter only)

## ngx.semaphore

This Lua module implements a semaphore API for efficient "light thread" synchronization,
which can work across different requests (but not across nginx worker processes).

See the [documentation](./lib/ngx/semaphore.md) for this Lua module for more details.

## ngx.balancer

This Lua module implements for defining dynamic upstream balancers in Lua.

See the [documentation](./lib/ngx/balancer.md) for this Lua module for more details.

## ngx.ssl

This Lua module provides a Lua API for controlling SSL certificates, private keys,
SSL protocol versions, and etc in NGINX downstream SSL handshakes.

See the [documentation](./lib/ngx/ssl.md) for this Lua module for more details.

## ngx.ssl.clienthello

This Lua module provides a Lua API for post-processing SSL client hello message
for NGINX downstream SSL connections.

See the [documentation](./lib/ngx/ssl/clienthello.md) for this Lua module for more details.

## ngx.ssl.session

This Lua module provides a Lua API for manipulating SSL session data and IDs
for NGINX downstream SSL connections.

See the [documentation](./lib/ngx/ssl/session.md) for this Lua module for more details.

## ngx.re

This Lua module provides a Lua API which implements convenience utilities for
the `ngx.re` API.

See the [documentation](./lib/ngx/re.md) for this Lua module for more details.

## ngx.resp

This Lua module provides Lua API which could be used to handle HTTP response.

See the [documentation](./lib/ngx/resp.md) for this Lua module for more details.

## ngx.pipe

This module provides a Lua API to spawn processes and communicate with them in
a non-blocking fashion.

See the [documentation](./lib/ngx/pipe.md) for this Lua module for more
details.

This module was first introduced in lua-resty-core v0.1.16.

## ngx.process

This Lua module is used to manage the nginx process in Lua.

See the [documentation](./lib/ngx/process.md) for this Lua module for more details.

This module was first introduced in lua-resty-core v0.1.12.

## ngx.errlog

This Lua module provides Lua API to capture and manage nginx error log messages.

See the [documentation](./lib/ngx/errlog.md) for this Lua module for more details.

This module was first introduced in lua-resty-core v0.1.12.

## ngx.base64

This Lua module provides Lua API to urlsafe base64 encode/decode.

See the [documentation](./lib/ngx/base64.md) for this Lua module for more details.

This module was first introduced in lua-resty-core v0.1.14.

## Caveat

If the user Lua code is not JIT compiled, then use of this library may
lead to performance drop in interpreted mode. You will only observe
speedup when you get a good part of your user Lua code JIT compiled.

## TODO

* Re-implement `ngx_lua`'s cosocket API with FFI.
* Re-implement `ngx_lua`'s `ngx.eof` and `ngx.flush` API functions with FFI.

## See Also
* the ngx_lua module: https://github.com/openresty/lua-nginx-module#readme
* LuaJIT FFI: http://luajit.org/ext_ffi.html


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-core](https://github.com/openresty/lua-resty-core){target=_blank}.