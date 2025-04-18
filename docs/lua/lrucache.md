---

title: "Lua-land LRU Cache based on LuaJIT FFI"
description: "RPM package lua-resty-lrucache: Lua-land LRU Cache based on LuaJIT FFI"

---
  
# *lrucache*: Lua-land LRU Cache based on LuaJIT FFI


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-lrucache
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-lrucache
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-lrucache [v0.15](https://github.com/openresty/lua-resty-lrucache/releases/tag/v0.15){target=_blank} 
released on Oct 10 2024.
    
<hr />

lua-resty-lrucache - Lua-land LRU cache based on the LuaJIT FFI.

## Status

This library is considered production ready.

## Synopsis

```lua
-- file myapp.lua: example "myapp" module

local _M = {}

-- alternatively: local lrucache = require "resty.lrucache.pureffi"
local lrucache = require "resty.lrucache"

-- we need to initialize the cache on the lua module level so that
-- it can be shared by all the requests served by each nginx worker process:
local c, err = lrucache.new(200)  -- allow up to 200 items in the cache
if not c then
    error("failed to create the cache: " .. (err or "unknown"))
end

function _M.go()
    c:set("dog", 32)
    c:set("cat", 56)
    ngx.say("dog: ", c:get("dog"))
    ngx.say("cat: ", c:get("cat"))

    c:set("dog", { age = 10 }, 0.1)  -- expire in 0.1 sec
    c:delete("dog")

    c:flush_all()  -- flush all the cached data
end

return _M
```

```nginx
## nginx.conf

http {
    # only if not using an official OpenResty release
    server {
        listen 8080;

        location = /t {
            content_by_lua_block {
                require("myapp").go()
            }
        }
    }
}
```

## Description

This library implements a simple LRU cache for
[OpenResty](https://openresty.org) and the
[ngx_lua](https://github.com/openresty/lua-nginx-module) module.

This cache also supports expiration time.

The LRU cache resides completely in the Lua VM and is subject to Lua GC. As
such, do not expect it to get shared across the OS process boundary. The upside
is that you can cache arbitrary complex Lua values (such as deep nested Lua
tables) without the overhead of serialization (as with `ngx_lua`'s [shared
dictionary
API](https://github.com/openresty/lua-nginx-module#lua_shared_dict)).
The downside is that your cache is always limited to the current OS process
(i.e. the current Nginx worker process). It does not really make much sense to
use this library in the context of
[init_by_lua](https://github.com/openresty/lua-nginx-module#lua_shared_dict)
because the cache will not get shared by any of the worker processes (unless
you just want to "warm up" the cache with predefined items which will get
inherited by the workers via `fork()`).

This library offers two different implementations in the form of two classes:
`resty.lrucache` and `resty.lrucache.pureffi`. Both implement the same API.
The only difference is that the latter is a pure FFI implementation that also
implements an FFI-based hash table for the cache lookup, while the former uses
native Lua tables.

If the cache hit rate is relatively high, you should use the `resty.lrucache`
class which is faster than `resty.lrucache.pureffi`.

However, if the cache hit rate is relatively low and there can be a *lot* of
variations of keys inserted into and removed from the cache, then you should
use the `resty.lrucache.pureffi` instead, because Lua tables are not good at
removing keys frequently. You would likely see the `resizetab` function call in
the LuaJIT runtime being very hot in [on-CPU flame
graphs](https://github.com/openresty/stapxx#lj-lua-stacks) if you use the
`resty.lrucache` class instead of `resty.lrucache.pureffi` in such a use case.

## Methods

To load this library,

1. use an official [OpenResty release](https://openresty.org) or follow the
   [Installation](#installation) instructions.
2. use `require` to load the library into a local Lua variable:

```lua
local lrucache = require "resty.lrucache"
```

or

```lua
local lrucache = require "resty.lrucache.pureffi"
```

## new
`syntax: cache, err = lrucache.new(max_items [, load_factor])`

Creates a new cache instance. Upon failure, returns `nil` and a string
describing the error.

The `max_items` argument specifies the maximal number of items this cache can
hold.

The `load-factor` argument designates the "load factor" of the FFI-based
hash-table used internally by `resty.lrucache.pureffi`; the default value is
0.5 (i.e. 50%); if the load factor is specified, it will be clamped to the
range of `[0.1, 1]` (i.e. if load factor is greater than 1, it will be
saturated to 1; likewise, if load-factor is smaller than `0.1`, it will be
clamped to `0.1`). This argument is only meaningful for
`resty.lrucache.pureffi`.

## set
`syntax: cache:set(key, value, ttl?, flags?)`

Sets a key with a value and an expiration time.

When the cache is full, the cache will automatically evict the least recently
used item.

The optional `ttl` argument specifies the expiration time. The time value is in
seconds, but you can also specify the fraction number part (e.g. `0.25`). A nil
`ttl` argument means the value would never expire (which is the default).

The optional `flags` argument specifies a user flags value associated with the
item to be stored. It can be retrieved later with the item. The user flags are
stored as an unsigned 32-bit integer internally, and thus must be specified as
a Lua number. If not specified, flags will have a default value of `0`. This
argument was added in the `v0.10` release.

## get
`syntax: data, stale_data, flags = cache:get(key)`

Fetches a value with the key. If the key does not exist in the cache or has
already expired, `nil` will be returned.

Starting from `v0.03`, the stale data is also returned as the second return
value if available.

Starting from `v0.10`, the user flags value associated with the stored item is
also returned as the third return value. If no user flags were given to an
item, its default flags will be `0`.

## delete
`syntax: cache:delete(key)`

Removes an item specified by the key from the cache.

## count
`syntax: count = cache:count()`

Returns the number of items currently stored in the cache **including**
expired items if any.

The returned `count` value will always be greater or equal to 0 and smaller
than or equal to the `size` argument given to [`cache:new`](#new).

This method was added in the `v0.10` release.

## capacity
`syntax: size = cache:capacity()`

Returns the maximum number of items the cache can hold. The return value is the
same as the `size` argument given to [`cache:new`](#new) when the cache was
created.

This method was added in the `v0.10` release.

## get_keys
`syntax: keys = cache:get_keys(max_count?, res?)`

Fetch the list of keys currently inside the cache up to `max_count`. The keys
will be ordered in MRU fashion (Most-Recently-Used keys first).

This function returns a Lua (array) table (with integer keys) containing the
keys.

When `max_count` is `nil` or `0`, all keys (if any) will be returned.

When provided with a `res` table argument, this function will not allocate a
table and will instead insert the keys in `res`, along with a trailing `nil`
value.

This method was added in the `v0.10` release.

## flush_all
`syntax: cache:flush_all()`

Flushes all the existing data (if any) in the current cache instance. This is
an `O(1)` operation and should be much faster than creating a brand new cache
instance.

Note however that the `flush_all()` method of `resty.lrucache.pureffi` is an
`O(n)` operation.

## Prerequisites

* [LuaJIT](http://luajit.org) 2.0+
* [ngx_lua](https://github.com/openresty/lua-nginx-module) 0.8.10+

## nginx.conf

    http {
        ...
    }
```

and then load the library in Lua:

```lua
local lrucache = require "resty.lrucache"
```

## See Also

* OpenResty: https://openresty.org
* the ngx_http_lua module: https://github.com/openresty/lua-nginx-module
* the ngx_stream_lua module: https://github.com/openresty/stream-lua-nginx-module
* the lua-resty-core library: https://github.com/openresty/lua-resty-core


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-lrucache](https://github.com/openresty/lua-resty-lrucache){target=_blank}.