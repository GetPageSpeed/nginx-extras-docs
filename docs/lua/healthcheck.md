# *healthcheck*: Healthcheck library for nginx-module-lua to validate upstream service status


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-healthcheck
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-healthcheck [v2.0.0](https://github.com/Kong/lua-resty-healthcheck/releases/tag/2.0.0){target=_blank} 
released on Sep 22 2020.
    
<hr />

A health check library for OpenResty.

## Synopsis

```nginx
http {
    lua_shared_dict test_shm 8m;
    lua_shared_dict my_worker_events 8m;
    init_worker_by_lua_block {

        local we = require "resty.worker.events"
        local ok, err = we.configure({
            shm = "my_worker_events",
            interval = 0.1
        })
        if not ok then
            ngx.log(ngx.ERR, "failed to configure worker events: ", err)
            return
        end

        local healthcheck = require("resty.healthcheck")
        local checker = healthcheck.new({
            name = "testing",
            shm_name = "test_shm",
            checks = {
                active = {
                    type = "https",
                    http_path = "/status",
                    healthy  = {
                        interval = 2,
                        successes = 1,
                    },
                    unhealthy  = {
                        interval = 1,
                        http_failures = 2,
                    }
                },
            }
        })

        local ok, err = checker:add_target("127.0.0.1", 8080, "example.com", false)

        local handler = function(target, eventname, sourcename, pid)
            ngx.log(ngx.DEBUG,"Event from: ", sourcename)
            if eventname == checker.events.remove
                -- a target was removed
                ngx.log(ngx.DEBUG,"Target removed: ",
                    target.ip, ":", target.port, " ", target.hostname)
            elseif eventname == checker.events.healthy
                -- target changed state, or was added
                ngx.log(ngx.DEBUG,"Target switched to healthy: ",
                    target.ip, ":", target.port, " ", target.hostname)
            elseif eventname ==  checker.events.unhealthy
                -- target changed state, or was added
                ngx.log(ngx.DEBUG,"Target switched to unhealthy: ",
                    target.ip, ":", target.port, " ", target.hostname)
            else
                -- unknown event
            end
        end
    }
}
```

## Description

This library supports performing active and passive health checks on arbitrary hosts.

Control of the library happens via its programmatic API. Consumption of its events
happens via the [lua-resty-worker-events](https://github.com/Kong/lua-resty-worker-events) library.

Targets are added using `checker:add_target(host, port)`.
Changes in status ("healthy" or "unhealthy") are broadcasted via worker-events.

Active checks are executed in the background based on the specified timer intervals.

For passive health checks, the library receives explicit notifications via its
programmatic API using functions such as `checker:report_http_status(host, port, status)`.

See the [online LDoc documentation](http://kong.github.io/lua-resty-healthcheck)
for the complete API.

## Async behaviour

Since this library heavily uses the SHM to share data between workers, it must
use locks. The locks themselves need access to `ngx.sleep` which is not available
in all contexts. Most notably not during startup; `init` and `init_worker`.

The library will try and acquire the lock and update, but if it fails it will
schedule an async update (timer with delay 0).

One workaround for this in the initial phases would be to replace `ngx.sleep` with
a version that does a blocking sleep in `init`/`init_worker`. This will enable
the usage of locks in those phases.


## History

Versioning is strictly based on [Semantic Versioning](https://semver.org/)

### Releasing new versions:

* update changelog below (PR's should be merged including a changelog entry)
* based on changelog determine new SemVer version
* create a new rockspec
* render the docs using `ldoc` (don't do this within PR's)
* commit as "release x.x.x" (do not include rockspec revision)
* tag the commit with "x.x.x" (do not include rockspec revision)
* push commit and tag
* upload rock to luarocks: `luarocks upload rockspecs/[name] --api-key=abc`

### 2.0.0 (22-Sep-2020)

* BREAKING: fallback for deprecated top-level field `type` is now removed
  (deprecated since `0.5.0`) [#56](https://github.com/Kong/lua-resty-healthcheck/pull/56)
* BREAKING: Bump `lua-resty-worker-events` dependency to `2.0.0`. This makes
  a lot of the APIs in this library asynchronous as the worker events `post`
  and `post_local` won't anymore call `poll` on a running worker automatically,
  for more information, see:
  https://github.com/Kong/lua-resty-worker-events#200-16-september-2020
* BREAKING: tcp_failures can no longer be 0 on http(s) checks (unless http(s)_failures
  are also set to 0) [#55](https://github.com/Kong/lua-resty-healthcheck/pull/55)
* feature: Added support for https_sni [#49](https://github.com/Kong/lua-resty-healthcheck/pull/49)
* fix: properly log line numbers by using tail calls [#29](https://github.com/Kong/lua-resty-healthcheck/pull/29)
* fix: when not providing a hostname, use IP [#48](https://github.com/Kong/lua-resty-healthcheck/pull/48)
* fix: makefile; make install
* feature: added a status version field [#54](https://github.com/Kong/lua-resty-healthcheck/pull/54)
* feature: add headers for probe request [#54](https://github.com/Kong/lua-resty-healthcheck/pull/54)
* fix: exit early when reloading during a probe [#47](https://github.com/Kong/lua-resty-healthcheck/pull/47)
* fix: prevent target-list from being nil, due to async behaviour [#44](https://github.com/Kong/lua-resty-healthcheck/pull/44)
* fix: replace timer and node-wide locks with resty-timer, to prevent interval
  skips [#59](https://github.com/Kong/lua-resty-healthcheck/pull/59)
* change: added additional logging on posting events [#25](https://github.com/Kong/lua-resty-healthcheck/issues/25)
* fix: do not run out of timers during init/init_worker when adding a vast
  amount of targets [#57](https://github.com/Kong/lua-resty-healthcheck/pull/57)
* fix: do not call on the module table, but use a method for locks. Also in
  [#57](https://github.com/Kong/lua-resty-healthcheck/pull/57)

### 1.3.0 (17-Jun-2020)

* Adds support to mTLS to active healthchecks. This feature  can be used adding
  the fields `ssl_cert` and `ssl_key`, with certificate and key respectively,
  when creating a new healthcheck object.
  [#41](https://github.com/Kong/lua-resty-healthcheck/pull/41)

### 1.2.0 (13-Feb-2020)

 * Adds `set_all_target_statuses_for_hostname`, which sets the targets for
   all entries with a given hostname at once.

### 1.1.2 (19-Dec-2019)

 * Fix: when `ngx.sleep` API is not available (e.g. in the log phase) it is not
   possible to lock using lua-resty-lock and any function that needs exclusive
   access would fail. This fix adds a retry method that starts a new light
   thread, which has access to `ngx.sleep`, to lock the critical path.
   [#37](https://github.com/Kong/lua-resty-healthcheck/pull/37);

### 1.1.1 (14-Nov-2019)

 * Fix: fail when it is not possible to get exclusive access to the list of
   targets. This fix prevents that workers get to an inconsistent state.
   [#34](https://github.com/Kong/lua-resty-healthcheck/pull/34);

### 1.1.0 (30-Sep-2019)

 * Add support for setting the custom `Host` header to be used for active checks.
 * Fix: log error on SSL Handshake failure
   [#28](https://github.com/Kong/lua-resty-healthcheck/pull/28);

### 1.0.0 (05-Jul-2019)

 * BREAKING: all API functions related to hosts require a `hostname` argument
   now. This way different hostnames listening on the same IP and ports
   combination do not have an effect on each other.
 * Fix: fix reporting active TCP probe successes
   [#20](https://github.com/Kong/lua-resty-healthcheck/pull/20);
   fixes issue [#19](https://github.com/Kong/lua-resty-healthcheck/issues/19)

### 0.6.1 (04-Apr-2019)

 * Fix: set up event callback only after target list is loaded
   [#18](https://github.com/Kong/lua-resty-healthcheck/pull/18);
   fixes Kong issue [#4453](https://github.com/Kong/kong/issues/4453)

### 0.6.0 (26-Sep-2018)

 * Introduce `checks.active.https_verify_certificate` field.
   It is `true` by default; setting it to `false` disables certificate
   verification in active healthchecks over HTTPS.

### 0.5.0 (25-Jul-2018)

 * Add support for `https` -- thanks @gaetanfl for the PR!
 * Introduce separate `checks.active.type` and `checks.passive.type` fields;
   the top-level `type` field is still supported as a fallback but is now
   deprecated.

### 0.4.2 (23-May-2018)

 * Fix `Host` header in active healthchecks

### 0.4.1 (21-May-2018)

 * Fix internal management of healthcheck counters

### 0.4.0 (20-Mar-2018)

 * Correct setting of defaults in `http_statuses`
 * Type and bounds checking to `checks` table

### 0.3.0 (18-Dec-2017)

 * Disable individual checks by setting their counters to 0

### 0.2.0 (30-Nov-2017)

 * Adds `set_target_status`

### 0.1.0 (27-Nov-2017) Initial release

 * Initial upload

## Copyright and License

```
Copyright 2017-2020 Kong Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

[badge-travis-url]: https://travis-ci.org/Kong/lua-resty-healthcheck/branches
[badge-travis-image]: https://travis-ci.org/Kong/lua-resty-healthcheck.svg?branch=master

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-healthcheck](https://github.com/Kong/lua-resty-healthcheck){target=_blank}.