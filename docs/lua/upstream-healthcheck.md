---

title: "Health Checker for NGINX Upstream Servers in Pure Lua"
description: "RPM package lua-resty-upstream-healthcheck: Health Checker for NGINX Upstream Servers in Pure Lua"

---
  
# *upstream-healthcheck*: Health Checker for NGINX Upstream Servers in Pure Lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-upstream-healthcheck
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-upstream-healthcheck
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-upstream-healthcheck [v0.8](https://github.com/openresty/lua-resty-upstream-healthcheck/releases/tag/v0.08){target=_blank} 
released on Mar 07 2023.
    
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
            type = "http", -- support "http" and "https"

            http_req = "GET /status HTTP/1.0\r\nHost: foo.com\r\n\r\n",
                    -- raw HTTP request for checking

            port = nil,  -- the check port, it can be different than the original backend server port, default means the same as the original backend server
            interval = 2000,  -- run the check cycle every 2 sec
            timeout = 1000,   -- 1 sec is the timeout for network operations
            fall = 3,  -- # of successive failures before turning a peer down
            rise = 2,  -- # of successive successes before turning a peer up
            valid_statuses = {200, 302},  -- a list valid HTTP status code
            concurrency = 10,  -- concurrency level for test requests
            -- ssl_verify = true, -- https type only, verify ssl certificate or not, default true
            -- host = foo.com, -- https type only, host name in ssl handshake, default nil
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

	# status page for all the peers (prometheus format):
        location = /metrics {
            access_log off;
            default_type text/plain;
            content_by_lua_block {
                local hc = require "resty.upstream.healthcheck"
                st , err = hc.prometheus_status_page()
                if not st then
                    ngx.say(err)
                    return
                end
                ngx.print(st)
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
        127.0.0.1:12354 UP
        127.0.0.1:12355 DOWN
    Backup Peers
        127.0.0.1:12356 UP

Upstream bar.com
    Primary Peers
        127.0.0.1:12354 UP
        127.0.0.1:12355 DOWN
        127.0.0.1:12357 DOWN
    Backup Peers
        127.0.0.1:12356 UP
```

If an upstream has no health checkers, then it will be marked by `(NO checkers)`, as in

```
Upstream foo.com (NO checkers)
    Primary Peers
        127.0.0.1:12354 UP
        127.0.0.1:12355 UP
    Backup Peers
        127.0.0.1:12356 UP
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

## See Also
* the ngx_lua module: https://github.com/openresty/lua-nginx-module
* the ngx_lua_upstream module: https://github.com/openresty/lua-upstream-nginx-module
* OpenResty: http://openresty.org


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-upstream-healthcheck](https://github.com/openresty/lua-resty-upstream-healthcheck){target=_blank}.