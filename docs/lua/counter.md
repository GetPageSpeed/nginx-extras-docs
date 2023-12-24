# *counter*: Lock-free counter for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-counter
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-counter
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-counter [v0.2.1](https://github.com/Kong/lua-resty-counter/releases/tag/v0.2.1){target=_blank} 
released on Apr 09 2020.
    
<hr />

lua-resty-counter - Lock-free counter for OpenResty.

![Build Status](https://travis-ci.com/kong/lua-resty-counter.svg?branch=master) ![luarocks](https://img.shields.io/luarocks/v/kong/lua-resty-counter?color=%232c3e67)

## Description

When number of workers increase, the penalty of acquiring a lock becomes noticable.
This library implements a lock-free counter that does incrementing operation in worker's Lua VM.
Each worker then sync its local counter to a shared dict timely.


## Status

Production

## API

## counter.new

**syntax**: *c, err = counter.new(shdict_name, sync_interval?)*

Create a new counter instance. Take first argument as the shared dict name in
string. And an optional second argument as interval to sync local state to
shared dict in number. If second argument is omitted, local counter will not be
synced automatically, user are responsible to call `counter:sync` on each worker.

## counter.sync

**syntax**: *ok = counter:sync()*

Sync current worker's local counter to shared dict. Not needed if a counter is
created with `sync_interval` not set to `nil`.

## counter.incr

**syntax**: *counter:incr(key, step?)*

Increase counter of key `k` with a step of `step`. If `step` is omitted, it's
default to `1`.

## counter.reset

**syntax**: *newval, err, forcible? = counter:reset(key, number)*

Reset the counter in shdict with a decrease of `number`. This function is a wrapper of
`ngx.shared.DICT:incr(key, -number, number)`, please refer to
[lua-nginx-module doc](https://github.com/openresty/lua-nginx-module#ngxshareddictincr)
for return values.

## counter.get

**syntax**: *value = counter:get(key)*

Get the value of counter from shared dict.

## counter.get_keys

**syntax**: *keys = counter:get_keys(max_count?)*

Get the keys of counters in shared dict. This function is a wrapper of
`ngx.shared.DICT:get_keys`, please refer to
[lua-nginx-module doc](https://github.com/openresty/lua-nginx-module#ngxshareddictget_keys)
for return values.


## See Also
* [lua-nginx-module](https://github.com/openresty/lua-nginx-module)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-counter](https://github.com/Kong/lua-resty-counter){target=_blank}.