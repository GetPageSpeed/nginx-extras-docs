---

title: "Extended timers for nginx-module-lua"
description: "RPM package lua-resty-timer: Extended timers for nginx-module-lua"

---
  
# *timer*: Extended timers for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-timer
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-timer
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-timer [v1.1.0](https://github.com/Kong/lua-resty-timer/releases/tag/1.1.0){target=_blank} 
released on Nov 06 2020.
    
<hr />

Extended timers for OpenResty. Provided recurring, cancellable, node-wide timers,
beyond what the basic OpenResty timers do.

## Status

This library is production ready.

## Synopsis

```nginx
http {
    lua_shared_dict timer_shm 1m;
    init_worker_by_lua_block {
        local timer = require("resty.timer")

        local options = {
            interval = 0.1,           -- expiry interval in seconds
            recurring = true,         -- recurring or single timer
            immediate = true,         -- initial interval will be 0
            detached = false,         -- run detached, or be garbagecollectible
            jitter = 0.1,             -- add a random interval
            expire = object.handler,  -- callback on timer expiry
            cancel = function(reason, self, param1)
                -- will be called when the timer gets cancelled
            end,
            shm_name = "timer_shm",   -- shm to use for node-wide timers
            key_name = "my_key",      -- key-name to use for node-wide timers
            sub_interval = 0.1,       -- max cross worker extra delay
        }

        local object
        object = {                            -- create some object with a timer
            count = 0,
            handler = function(self, param1)  -- the timer callback as a method
                -- do something here
                print(param1)                 --> "Param 1"
            end,

            -- create and add to object, but also pass it as 'self' to the handler
            timer = timer(options, object, "Param 1"),
        }

        -- anchor the object and timer
        _M.global_object = object     -- will be collected if not anchored

        -- cancel the timer
        object.timer:cancel()
    }
}
```

## Description

The OpenResty timer is fairly limited, this timer adds a number of common
options as parameters without having to recode (and retest) them in each
project.

* recurring timers (supported by OR as well through `ngx.timer.every`)

* immediate first run for recurring timers

* cancellable timers

* cancel callback, called when the timer is cancelled

* garbage collectible timers, enabling timers to (optionally) be attached to
  objects and automatically stop when garbage collected.

* node-wide timers: the same timer started in each worker will still only
  run once across the system. If the worker running it is removed the
  timer will automatically be executed on another worker.

See the [online LDoc documentation](https://kong.github.io/lua-resty-timer/topics/README.md.html)
for the complete API.

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

### 1.1.0 (6-Nov-2020)

  * Feat: add a `jitter` option. This adds a random interval to distribute the
  timers (in case of scheduling many timers at once).

### 1.0.0 (21-Sep-2020)

  * Change [BREAKING]: the recurring timers are now implemented as a sleeping
  thread which is more efficient. Side effect is that the timer only gets
  rescheduled AFTER executing the handler. So if the handler is long running,
  then individual runs will be further apart.

### 0.3 (28-May-2018)

  * Feat: added cancellation callback invocation on timer being GC'ed. This
  changes the first argument of the `cancel` callback, and hence is
  breaking.

### 0.2 (12-Feb-2018) Bug fix

  * Fix: bugfix in `unpack` function not honoring table length parameter
  * Docs: small fixes and typo's

### 0.1 (22-Nov-2017) Initial release

  * Added `sub_interval` option to reduce delays
  * Initial upload

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-timer](https://github.com/Kong/lua-resty-timer){target=_blank}.