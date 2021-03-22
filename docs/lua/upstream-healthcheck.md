# *upstream-healthcheck*: Health Checker for NGINX Upstream Servers in Pure Lua


## Installation

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-upstream-healthcheck
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](modules/lua.md) is installed.

This document describes lua-resty-upstream-healthcheck [v0.6](https://github.com/openresty/lua-resty-upstream-healthcheck/releases/tag/v0.06){target=_blank} 
released on Feb 28 2019.
    
<hr />

lua-resty-upstream-healthcheck - Health-checker for Nginx upstream servers

## Status

This library is still under early development but is already production ready.

## Synopsis

```nginx
http {
    # sample upstream block:
    upstream foo.com {
        server 127.0.0.1:12354;
        server 127.0.0.1:12355;
        server 127.0.0.1:12356 backup;
    }

    # the size depends on the number of servers in upstream {}:
    lua_shared_dict healthcheck 1m;

    lua_socket_log_errors off;

    init_worker_by_lua_block {
        local hc = require "resty.upstream.healthcheck"

        local ok, err = hc.spawn_checker{
            shm = "healthcheck",  -- defined by "lua_shared_dict"
            upstream = "foo.com", -- defined by "upstream"
            type = "http",

            http_req = "GET /status HTTP/1.0\r\nHost: foo.com\r\n\r\n",
                    -- raw HTTP request for checking

            interval = 2000,  -- run the check cycle every 2 sec
            timeout = 1000,   -- 1 sec is the timeout for network operations
            fall = 3,  -- # of successive failures before turning a peer down
            rise = 2,  -- # of successive successes before turning a peer up
            valid_statuses = {200, 302},  -- a list valid HTTP status code
            concurrency = 10,  -- concurrency level for test requests
        }
        if not ok then
            ngx.log(ngx.ERR, "failed to spawn health checker: ", err)
            return
        end

        -- Just call hc.spawn_checker() for more times here if you have
        -- more upstream groups to monitor. One call for one upstream group.
        -- They can all share the same shm zone without conflicts but they
        -- need a bigger shm zone for obvious reasons.
    }

    server {
        ...

        # status page for all the peers:
        location = /status {
            access_log off;
            allow 127.0.0.1;
            deny all;

            default_type text/plain;
            content_by_lua_block {
                local hc = require "resty.upstream.healthcheck"
                ngx.say("Nginx Worker PID: ", ngx.worker.pid())
                ngx.print(hc.status_page())
            }
        }
    }
}
```

## Description

This library performs healthcheck for server peers defined in NGINX `upstream` groups specified by names.

## Methods

## spawn_checker
**syntax:** `ok, err = healthcheck.spawn_checker(options)`

**context:** *init_worker_by_lua&#42;*

Spawns background timer-based "light threads" to perform periodic healthchecks on
the specified NGINX upstream group with the specified shm storage.

The healthchecker does not need any client traffic to function. The checks are performed actively
and periodically.

This method call is asynchronous and returns immediately.

Returns true on success, or `nil` and a string describing an error otherwise.

## status_page
**syntax:** `str, err = healthcheck.status_page()`

**context:** *any*

Generates a detailed status report for all the upstreams defined in the current NGINX server.

One typical output is

```
Upstream foo.com
    Primary Peers
        127.0.0.1:12354 up
        127.0.0.1:12355 DOWN
    Backup Peers
        127.0.0.1:12356 up

Upstream bar.com
    Primary Peers
        127.0.0.1:12354 up
        127.0.0.1:12355 DOWN
        127.0.0.1:12357 DOWN
    Backup Peers
        127.0.0.1:12356 up
```

If an upstream has no health checkers, then it will be marked by `(NO checkers)`, as in

```
Upstream foo.com (NO checkers)
    Primary Peers
        127.0.0.1:12354 up
        127.0.0.1:12355 up
    Backup Peers
        127.0.0.1:12356 up
```

If you indeed have spawned a healthchecker in `init_worker_by_lua*`, then you should really
check out the NGINX error log file to see if there is any fatal errors aborting the healthchecker threads.

## Multiple Upstreams

One can perform healthchecks on multiple `upstream` groups by calling the [spawn_checker](#spawn_checker) method
multiple times in the `init_worker_by_lua*` handler. For example,

```nginx
upstream foo {
    ...
}

upstream bar {
    ...
}

lua_shared_dict healthcheck 1m;

lua_socket_log_errors off;

init_worker_by_lua_block {
    local hc = require "resty.upstream.healthcheck"

    local ok, err = hc.spawn_checker{
        shm = "healthcheck",
        upstream = "foo",
        ...
    }

    ...

    ok, err = hc.spawn_checker{
        shm = "healthcheck",
        upstream = "bar",
        ...
    }
}
```

Different upstreams' healthcheckers use different keys (by always prefixing the keys with the
upstream name), so sharing a single `lua_shared_dict` among multiple checkers should not have
any issues at all. But you need to compensate the size of the shared dict for multiple users (i.e., multiple checkers).
If you have many upstreams (thousands or even more), then it is more optimal to use separate shm zones
for each (group) of the upstreams.

## nginx.conf
http {
    ...
}
```

## TODO

## Community

## English Mailing List

The [openresty-en](https://groups.google.com/group/openresty-en) mailing list is for English speakers.

## Chinese Mailing List

The [openresty](https://groups.google.com/group/openresty) mailing list is for Chinese speakers.

## Bugs and Patches

Please report bugs or submit patches by

1. creating a ticket on the [GitHub Issue Tracker](http://github.com/openresty/lua-resty-upstream-healthcheck/issues),
1. or posting to the [OpenResty community](#community).

## Author

Yichun "agentzh" Zhang (章亦春) <agentzh@gmail.com>, OpenResty Inc.

## Copyright and License

This module is licensed under the BSD license.

Copyright (C) 2014-2017, by Yichun "agentzh" Zhang, OpenResty Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## See Also
* the ngx_lua module: https://github.com/openresty/lua-nginx-module
* the ngx_lua_upstream module: https://github.com/openresty/lua-upstream-nginx-module
* OpenResty: http://openresty.org


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-upstream-healthcheck](https://github.com/openresty/lua-resty-upstream-healthcheck){target=_blank}.