# *hyperscan*: Hyperscan for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-hyperscan
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-hyperscan
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-hyperscan [v0.3](https://github.com/LubinLew/lua-resty-hyperscan/releases/tag/v0.3){target=_blank} 
released on Apr 14 2022.
    
<hr />

lua-resty-hyperscan - [Hyperscan](https://github.com/intel/hyperscan) for [Openresty](https://github.com/openresty/openresty)

> !!! [Old Branch](https://github.com/LubinLew/lua-resty-hyperscan/tree/v0.1) got [too many callbacks](https://github.com/LubinLew/lua-resty-hyperscan/issues/1) problem, because luajit is not fully support [CALLBACK](https://luajit.org/ext_ffi_semantics.html#callback). So we need a [C wrapper](hs_wrapper/) to handle callbacks.
## 

## Status

This library is under development so far.

Support [Block Mode](http://intel.github.io/hyperscan/dev-reference/runtime.html#block-mode) and [Vectored Mode](http://intel.github.io/hyperscan/dev-reference/runtime.html#vectored-mode) now.
## 

## first, you should install openresty
git clone git@github.com:LubinLew/lua-resty-hyperscan.git
cd lua-resty-hyperscan
make
make install
make test
```
## 

## 

## Synopsis

configuration example

```lua
user  nobody;
worker_processes  auto;
error_log logs/error.log error;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    access_log  logs/access.log;

    init_by_lua_block {
       local whs, err = require('hyperscan')
        if not whs then
            ngx.log(ngx.ERR, "Failure:", err)
            return
        end

       -- new
       local obj = whs.block_new("a-uniq-name", true) -- true : enable debug mode

       local patterns = {
           {id = 1001, pattern = "\\d3",       flag = "iu"},
           {id = 1002, pattern = "\\s{3,5}",   flag = "u"},
           {id = 1003, pattern = "[a-d]{2,7}", flag = ""}
       }

        -- compile
        ret, err = obj:compile(patterns)
        if not ret then
           ngx.log(ngx.ERR, "hyperscan block compile failed, ", err)
           return
        end
    }

    server {
        listen       80;
        server_name  localhost;

        location / {
            content_by_lua_block {
                local whs = require('hyperscan')
                local obj = whs.block_get("a-uniq-name")
                -- scan
                local ret, id, from, to = obj:scan(ngx.var.uri)
                if ret then
                    return ngx.print("[", ngx.var.uri,"] match: ", id, " zone [", from, " - ", to, ").\n")
                else
                    return ngx.print("[", ngx.var.uri, "] not match any rule.\n")
                end
            }
        }
    }
}
```

test cases:

```bash
$ curl http://localhost
[/] not match any rule.

$ curl http://localhost/131111111
[/131111111] match: 1001 zone [0 - 3).

$ curl "http://localhost/      end"
[/      end] match: 1002 zone [0 - 4).

$ curl http://localhost/aaaaaaa
[/aaaaaaa] match: 1003 zone [0 - 3).
```

## 

## Methods

way to load this library

```lua
local whs,err = require('hyperscan')
if not whs then
    ngx.log(ngx.ERR, "reason: ", err)
end
```

### block_new

Create a hyperscan instance for block mode.

```lua
local handle, err = whs.block_new(name, debug)
if not handle then
    ngx.log(ngx.ERR, "reason: ", err)
end
```

| Field        | Name     | Lua Type  | Description                              |
| ------------ | -------- | --------- | ---------------------------------------- |
| Parameter    | `name`   | string    | instance name, mainly for log            |
|              | `debug`  | boolean   | enable/disable write debug log to syslog |
| Return Value | `handle` | table/nil | instance reference                       |
|              | `err`    | string    | reason of failure                        |

### block_free

Destroy a hyperscan instance for block mode.

```lua
whs.block_free(name)
```

### block_get

Get the instance reference by name.

```lua
local handle = whs.block_get(name)
```

| Filed        | Name     | Lua Type  | Description        |
| ------------ | -------- | --------- | ------------------ |
| Parameter    | `name`   | string    | instance name      |
| Return Value | `handle` | table/nil | instance reference |

### vector_new

Create a hyperscan instance for vector mode.

```lua
local handle, err = whs.vector_new(name, debug)
if not handle then
    ngx.log(ngx.ERR, "reason: ", err)
end
```

| Field        | Name     | Lua Type  | Description                              |
| ------------ | -------- | --------- | ---------------------------------------- |
| Parameter    | `name`   | string    | instance name, mainly for log            |
|              | `debug`  | boolean   | enable/disable write debug log to syslog |
| Return Value | `handle` | table/nil | instance reference                       |
|              | `err`    | string    | reason of failure                        |

### vector_free

Destroy a hyperscan instance for vector mode.

```lua
whs.vector_free(name)
```

### vector_get

Get the instance reference by name.

```lua
local handle = whs.vector_get(name)
```

| Filed        | Name     | Lua Type  | Description        |
| ------------ | -------- | --------- | ------------------ |
| Parameter    | `name`   | string    | instance name      |
| Return Value | `handle` | table/nil | instance reference |

### handle:compile

compile regular expression into a Hyperscan database.

```lua
--local handle = whs.block_new(name, debug)
local ok, err = handle:compile(patterns)
if not ok then
    ngx.log(ngx.ERR, "reason: ", err)
end
```

| Field        | Name       | Lua Type | Description       |
| ------------ | ---------- | -------- | ----------------- |
| parameter    | `patterns` | table    | pattern list      |
| Return Value | `ok`       | boolean  | success/failure   |
|              | `err`      | string   | reason of failure |

#### Pattern List

##### Example

```lua
local patterns = {
    {id = 1001, pattern = "\\d3",       flag = "iu"   },
    {id = 1002, pattern = "\\s{3,5}",   flag = "dmsu" },
    {id = 1003, pattern = "[a-d]{2,7}", flag = ""     }
}
```

##### Flags

| Flag  | Hyperscan Value                                                                                              | Description                                             |
| ----- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| `'i'` | [HS_FLAG_CASELESS](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_CASELESS)         | Set case-insensitive matching                           |
| `'d'` | [HS_FLAG_DOTALL](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_DOTALL)             | Matching a `.` will not exclude newlines.               |
| `'m'` | [HS_FLAG_MULTILINE](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_MULTILINE)       | Set multi-line anchoring.                               |
| `'s'` | [HS_FLAG_SINGLEMATCH](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_SINGLEMATCH)   | Set single-match only mode.                             |
| `'e'` | [HS_FLAG_ALLOWEMPTY](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_ALLOWEMPTY)     | Allow expressions that can match against empty buffers. |
| `'u'` | [HS_FLAG_UTF8](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_UTF8)                 | Enable UTF-8 mode for this expression.                  |
| `'p'` | [HS_FLAG_UCP](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_UCP)                   | Enable Unicode property support for this expression.    |
| `'f'` | [HS_FLAG_PREFILTER](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_PREFILTER)       | Enable prefiltering mode for this expression.           |
| `'l'` | [HS_FLAG_SOM_LEFTMOST](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_SOM_LEFTMOST) | Enable leftmost start of match reporting.               |
| `'c'` | [HS_FLAG_COMBINATION](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_COMBINATION)   | Logical combination.                                    |
| `'q'` | [HS_FLAG_QUIET](http://intel.github.io/hyperscan/dev-reference/api_files.html#c.HS_FLAG_QUIET)               | Don't do any match reporting.                           |

### handle:scan

The actual pattern matching takes place for block-mode pattern databases.

```lua
--local handle = whs.block_get(name)
local ok, id, from, to = handle:scan(data)
if ok then
    ngx.log(ngx.INFO, "match success", id, from, to)
end
```

The actual pattern matching takes place for vector-mode pattern databases.

```lua
--local handle = whs.vector_get(name)
--local data = {"s","s2"}
--local data = "s"
local ok, id, dataindex, to = handle:scan(data)
if ok then
    ngx.log(ngx.INFO, "match success", id, from, to)
end
```

| Field        | Name        | Lua Type        | Description                                     |
| ------------ | ----------- | --------------- | ----------------------------------------------- |
| Parameter    | `data`      | string/string[] | string to be scanned(string[] only vector mode) |
| Return Value | `ok`        | boolean         | `ture` for match, `false` for not match         |
|              | `id`        | number          | match id                                        |
|              | `from`      | number          | match from byte arrary index(include itself)    |
|              | `to`        | number          | match end byte arrary index(exclude itself)     |
|              | `dataindex` | number          | match data index(only vector mode)              |

### handle:free

Destroy a hyperscan instance.

```lua
--local handle = whs.block_get(name)
handle:free()
```

## 

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-hyperscan](https://github.com/LubinLew/lua-resty-hyperscan){target=_blank}.