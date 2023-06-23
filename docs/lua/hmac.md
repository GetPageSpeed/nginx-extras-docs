# *hmac*: HMAC functions for nginx-module-lua and LuaJIT


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-hmac
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-hmac
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-hmac [v0.6.1](https://github.com/jkeys089/lua-resty-hmac/releases/tag/0.06-1){target=_blank} 
released on May 31 2023.
    
<hr />

lua-resty-hmac - HMAC functions for ngx_lua and LuaJIT

## Status

This library is still under active development and is considered production ready.

## Description

This library requires an nginx build with OpenSSL,
the [ngx_lua module](http://wiki.nginx.org/HttpLuaModule), and [LuaJIT 2.0](http://luajit.org/luajit.html).

## Synopsis

```lua
    # nginx.conf:

    server {
        location = /test {
            content_by_lua_file conf/test.lua;
        }
    }

    -- conf/test.lua:

    local hmac = require "resty.hmac"

    local hmac_sha1 = hmac:new("secret_key", hmac.ALGOS.SHA1)
    if not hmac_sha1 then
        ngx.say("failed to create the hmac_sha1 object")
        return
    end

    local ok = hmac_sha1:update("he")
    if not ok then
        ngx.say("failed to add data")
        return
    end

    ok = hmac_sha1:update("llo")
    if not ok then
        ngx.say("failed to add data")
        return
    end

    local mac = hmac_sha1:final()  -- binary mac

    local str = require "resty.string"
    ngx.say("hmac_sha1: ", str.to_hex(mac))
        -- output: "hmac_sha1: aee4b890b574ea8fa4f6a66aed96c3e590e5925a"

    -- dont forget to reset after final!
    if not hmac_sha1:reset() then
        ngx.say("failed to reset hmac_sha1")
        return
    end

    -- short version
    ngx.say("hmac_sha1: ", hmac_sha1:final("world", true))
        -- output: "hmac_sha1: 4e9538f1efbe565c522acfb72fce6092ea6b15e0"
```

## Methods

To load this library,

1. you need to specify this library's path in ngx_lua's [lua_package_path](https://github.com/openresty/lua-nginx-module#lua_package_path) directive. For example, `lua_package_path "/path/to/lua-resty-hmac/lib/?.lua;;";`.
2. you use `require` to load the library into a local Lua variable:

```lua
    local hmac = require "resty.hmac"
```

new
---
`syntax: local hmac_sha256 = hmac:new(key [, hash_algorithm])`

Creates a new hmac instance. If failed, returns `nil`.

The `key` argument specifies the key to use when calculating the message authentication code (MAC).
`key` is a lua string which may contain printable characters or binary data.

The `hash_algorithm` argument specifies which hashing algorithm to use (`hmac.ALGOS.MD5`, `hmac.ALGOS.SHA1`, `hmac.ALGOS.SHA256`, `hmac.ALGOS.SHA512`).
The default value is `hmac.ALGOS.MD5`.

update
---
`syntax: hmac_sha256:update(data)`

Updates the MAC calculation to include new data. If failed, returns `false`.

The `data` argument specifies the additional data to include in the MAC.
`data` is a lua string which may contain printable characters or binary data.

final
---
`syntax: local mac = hmac_sha256:final([data, output_hex])`

Finalizes the MAC calculation and returns the final MAC value. If failed, returns `nil`.
When `output_hex` is not `true` returns a lua string containing the raw, binary MAC. When `output_hex` is `true` returns a lua string containing the hexadecimal representation of the MAC.

The `data` argument specifies the additional data to include in the MAC before finalizing the calculation.
The default value is `nil`.

The `output_hex` argument specifies wether the MAC should be returned as hex or binary. If `true` the MAC will be returned as hex.
The default value is `false`.

## reset
`syntax: hmac_sha256:reset()`

Resets the internal hmac context so it can be re-used to calculate a new MAC. If failed, returns `false`.
If successful, the `key` and `hash_algorithm` remain the same but all other information is cleared.

This MUST be called after `hmac_sha256:final()` in order to calculate a new MAC using the same hmac instance.

## Prerequisites

* [LuaJIT](http://luajit.org) 2.0+
* [ngx_lua module](http://wiki.nginx.org/HttpLuaModule)
* [lua-resty-string](https://github.com/openresty/lua-resty-string) 0.8+
* [OpenSSL](https://www.openssl.org/) 1.0.0+

## Copyright and License

This module is licensed under the BSD license.

Copyright (C) 2012-2023, Thought Foundry Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## See Also
* the ngx_lua module: http://wiki.nginx.org/HttpLuaModule


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-hmac](https://github.com/jkeys089/lua-resty-hmac){target=_blank}.