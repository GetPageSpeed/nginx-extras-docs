# *jit-uuid*: Fast and dependency-free UUID library for LuaJIT/nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-jit-uuid
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-jit-uuid
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-jit-uuid [v0.0.7](https://github.com/thibaultcha/lua-resty-jit-uuid/releases/tag/0.0.7){target=_blank} 
released on Dec 16 2017.
    
<hr />

[![Module Version][badge-version-image]][luarocks-resty-jit-uuid]
[![Coverage Status][badge-coveralls-image]][badge-coveralls-url]

A pure LuaJIT (no dependencies) UUID library tuned for performance.

### Motivation

This module is aimed at being a free of dependencies, performant and
complete UUID library for LuaJIT and ngx_lua.

Unlike FFI and C bindings, it does not depend on libuuid being available
in your system. On top of that, it performs **better** than most (all?)
of the generators it was benchmarked against, FFI bindings included.

Finally, it provides additional features such as UUID v3/v4/v5 generation and
UUID validation.

See the [Benchmarks](#benchmarks) section for comparisons between other UUID
libraries for Lua/LuaJIT.

### Usage

LuaJIT:
```lua
local uuid = require 'resty.jit-uuid'

uuid.seed()        ---> automatic seeding with os.time(), LuaSocket, or ngx.time()

uuid()             ---> v4 UUID (random)
uuid.generate_v4() ---> v4 UUID

uuid.generate_v3() ---> v3 UUID (name-based with MD5)
uuid.generate_v5() ---> v5 UUID (name-based with SHA-1)

uuid.is_valid()    ---> true/false (automatic JIT PCRE or Lua patterns)
```

OpenResty:
```nginx
http {
    init_worker_by_lua_block {
        local uuid = require 'resty.jit-uuid'
        uuid.seed() -- very important!
    }

    server {
        location / {
            content_by_lua_block {
                local uuid = require 'resty.jit-uuid'
                ngx.say(uuid())
            }
        }
    }
}
```

**Note**: when generating v4 (random) UUIDs in ngx_lua, it is **very
important** that you seed this module in the `init_worker` phase. If you do
not, your workers will generate identical UUID sequences, which could lead to
serious issues in your application. The seeding requirement also applies in
uses outside of ngx_lua, although seeding is less delicate in such cases.
Additionally, you should be weary about the usage of the
[`lua_code_cache`](https://github.com/openresty/lua-nginx-module#lua_code_cache)
directive: if Lua code cache is disabled, all sequences of UUIDs generated
during subsequent requests will be identical, unless this module is seeded for
every request. Just like disabling Lua code cache, such behavior would be
considered an ngx_lua anti-pattern and you should avoid it.

### Documentation

Documentation is available online at
<http://thibaultcha.github.io/lua-resty-jit-uuid/>.

### Benchmarks

This module has been carefully benchmarked on each step of its implementation
to ensure the best performance for OpenResty and plain LuaJIT. For example,
UUID validation will use JIT PCRE over Lua patterns when possible.

The `bench.lua` file provides benchmarks of UUID generation for several popular
UUID libraries.

Run `make bench` to run them:
```
LuaJIT 2.1.0-beta1 with 1e+06 UUIDs
UUID v4 (random) generation
1. resty-jit-uuid   took:   0.064228s    0%
2. FFI binding      took:   0.093374s   +45%
3. C binding        took:   0.220542s   +243%
4. Pure Lua         took:   2.051905s   +3094%

UUID v3 (name-based and MD5) generation if supported
1. resty-jit-uuid   took:   1.306127s

UUID v5 (name-based and SHA-1) generation if supported
1. resty-jit-uuid   took:   4.834929s

UUID validation if supported (set of 70% valid, 30% invalid)
1. resty-jit-uuid (JIT PCRE enabled)    took:   0.223060s
2. FFI binding                          took:   0.256580s
3. resty-jit-uuid (Lua patterns)        took:   0.444174s
```

* FFI binding: <https://github.com/bungle/lua-resty-uuid>
* C binding: <https://github.com/Mashape/lua-uuid>
* Pure Lua: <https://github.com/Tieske/uuid>
* resty-jit-uuid: this module (base reference for generation % comparison)

**Note**: UUID validation performance in ngx_lua (JIT PCRE) can be greatly
improved by enabling
[lua-resty-core](https://github.com/openresty/lua-resty-core).

### Contributions

Suggestions improving this module's or the benchmarks' performance
(of any benchmarked library) are particularly appreciated.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-jit-uuid](https://github.com/thibaultcha/lua-resty-jit-uuid){target=_blank}.