# *balancer*: A generic consistent hash implementation for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-balancer
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-balancer [v0.3](https://github.com/openresty/lua-resty-balancer/releases/tag/v0.03){target=_blank} 
released on Jun 25 2019.
    
<hr />

lua-resty-chash - A generic consistent hash implementation for OpenResty/LuaJIT

lua-resty-roundrobin - A generic roundrobin implementation for OpenResty/LuaJIT

## Status

This library is still under early development and is still experimental.

## Description

This Lua library can be used with `balancer_by_lua*`.

## Synopsis

```lua
    init_by_lua_block {
        local resty_chash = require "resty.chash"
        local resty_roundrobin = require "resty.roundrobin"

        local server_list = {
            ["127.0.0.1:1985"] = 2,
            ["127.0.0.1:1986"] = 2,
            ["127.0.0.1:1987"] = 1,
        }

        -- XX: we can do the following steps to keep consistency with nginx chash
        local str_null = string.char(0)

        local servers, nodes = {}, {}
        for serv, weight in pairs(server_list) do
            -- XX: we can just use serv as id when we doesn't need keep consistency with nginx chash
            local id = string.gsub(serv, ":", str_null)

            servers[id] = serv
            nodes[id] = weight
        end

        local chash_up = resty_chash:new(nodes)

        package.loaded.my_chash_up = chash_up
        package.loaded.my_servers = servers

        local rr_up = resty_roundrobin:new(server_list)
        package.loaded.my_rr_up = rr_up
    }

    upstream backend_chash {
        server 0.0.0.1;
        balancer_by_lua_block {
            local b = require "ngx.balancer"

            local chash_up = package.loaded.my_chash_up
            local servers = package.loaded.my_servers

            -- we can balancer by any key here
            local id = chash_up:find(ngx.var.arg_key)
            local server = servers[id]

            assert(b.set_current_peer(server))
        }
    }

    upstream backend_rr {
        server 0.0.0.1;
        balancer_by_lua_block {
            local b = require "ngx.balancer"

            local rr_up = package.loaded.my_rr_up

            -- Note that Round Robin picks the first server randomly
            local server = rr_up:find()

            assert(b.set_current_peer(server))
        }
    }

    server {
        location /chash {
            proxy_pass http://backend_chash;
        }

        location /roundrobin {
            proxy_pass http://backend_rr;
        }
    }
```

## Methods

Both `resty.chash` and `resty.roundrobin` have the same apis.

new
---
**syntax:** `obj, err = class.new(nodes)`

Instantiates an object of this class. The `class` value is returned by the call `require "resty.chash"`.

The `id` should be `table.concat({host, string.char(0), port})` like the nginx chash does,
when we need to keep consistency with nginx chash.

The `id` can be any string value when we do not need to keep consistency with nginx chash.

```lua
local nodes = {
    -- id => weight
    server1 = 10,
    server2 = 2,
}

local resty_chash = require "resty.chash"

local chash = resty_chash:new(nodes)

local id = chash:find("foo")

ngx.say(id)
```

## reinit
**syntax:** `obj:reinit(nodes)`

Reinit the chash obj with the new `nodes`.

## set
**syntax:** `obj:set(id, weight)`

Set `weight` of the `id`.

## delete
**syntax:** `obj:delete(id)`

Delete the `id`.

## incr
**syntax:** `obj:incr(id, weight?)`

Increments weight for the `id` by the step value `weight`(default to 1).

## decr
**syntax:** `obj:decr(id, weight?)`

Decrease weight for the `id` by the step value `weight`(default to 1).

## find
**syntax:** `id, index = obj:find(key)`

Find an id by the `key`, same key always return the same `id` in the same `obj`.

The second return value `index` is the index in the chash circle of the hash value of the `key`.

## next
**syntax:** `id, new_index = obj:next(old_index)`

If we have chance to retry when the first `id`(server) doesn't work well,
then we can use `obj:next` to get the next `id`.

The new `id` may be the same as the old one.

## Performance

There is a benchmark script `t/bench.lua`.

I got the result when I run `make bench`:

```
chash new servers
10000 times
elasped: 0.61600017547607

chash new servers2
1000 times
elasped: 0.77300000190735

chash new servers3
10000 times
elasped: 0.66899991035461

new in func
10000 times
elasped: 0.62000012397766

new dynamic
10000 times
elasped: 0.75499987602234

incr server3
10000 times
elasped: 0.19000029563904

incr server1
10000 times
elasped: 0.33699989318848

decr server1
10000 times
elasped: 0.27300024032593

delete server3
10000 times
elasped: 0.037999868392944

delete server1
10000 times
elasped: 0.065000057220459

set server1 9
10000 times
elasped: 0.26600003242493

set server1 8
10000 times
elasped: 0.32000017166138

set server1 1
10000 times
elasped: 0.56699991226196

base for find
1000000 times
elasped: 0.01800012588501

find
1000000 times
elasped: 0.9469997882843
```

## Author

Dejiang Zhu (doujiang24) <doujiang24@gmail.com>.

## Copyright and License

This module is licensed under the BSD license.

Copyright (C) 2015-2016, by Yichun Zhang (agentzh) <agentzh@gmail.com>, CloudFlare Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## See Also
* the ngx_lua module: http://wiki.nginx.org/HttpLuaModule
* the json lib for Lua and C: https://github.com/cloudflare/lua-resty-json


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-balancer](https://github.com/openresty/lua-resty-balancer){target=_blank}.