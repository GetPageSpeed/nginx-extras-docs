# *libcjson*: LuaJIT FFI-based cJSON library for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-libcjson
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-libcjson [v1.4](https://github.com/bungle/lua-resty-libcjson/releases/tag/v1.4){target=_blank} 
released on Jul 04 2016.
    
<hr />

`lua-resty-libcjson` is a LuaJIT FFI-based cJSON library (tested with OpenResty too).

## Lua API
#### mixed json.decode(value)

Decodes JSON value or structure (JSON array or object), and returns either Lua `table` or some simple value (e.g. `boolean`, `string`, `number`, `nil` or `json.null` (when running in context of OpenResty the `json.null` is the same as `ngx.null`).

##### Example

```lua
local json = require "resty.libcjson"
local obj = json.decode "{}"       -- table (with obj.__jsontype == "object")
local arr = json.decode "[]"       -- table (with arr.__jsontype == "array")
local nbr = json.decode "1"        -- 1
local bln = json.decode "true"     -- true
local str = json.decode '"test"'   -- "test"
local str = json.decode '""'       -- ""
local num = json.decode(5)         -- 5
local num = json.decode(math)      -- math
local num = json.decode(json.null) -- json.null
local nul = json.decode "null"     -- json.null
local nul = json.decode ""         -- nil
local nul = json.decode(nil)       -- nil
local nul = json.decode()          -- nil
```

Nested JSON structures are parsed as nested Lua tables.

#### string json.encode(value, formatted)

Encodes Lua value or table, and returns equivalent JSON value or structure as a string. Optionally you may pass `formatted` argument with value of `false` to get unformatted JSON string as output.

##### Example

```lua
local json = require "resty.libcjson"
local str = json.encode{}                              -- "[]"
local str = json.encode(setmetatable({}, json.object)) -- "{}"
local str = json.encode(1)                             -- "1"
local str = json.encode(1.1)                           -- "1.100000"
local str = json.encode "test"                         -- '"test"'
local str = json.encode ""                             -- '""'
local str = json.encode(false)                         -- "false"
local str = json.encode(nil)                           -- "null"
local str = json.encode(json.null)                     -- "null"
local str = json.encode()                              -- "null"
local str = json.encode{ a = "b" }                     -- '{ "a": "b" }'
local str = json.encode{ "a", b = 1 }                  -- '{ "1": "a", "b": 1 }'
local str = json.encode{ 1, 1.1, "a", "", false }      -- '[1, 1.100000, "a", "", false]' 
```

Nested Lua tables are encoded as nested JSON structures (JSON objects or arrays).

#### About JSON Arrays and Object Encoding and Decoding

See this comment: https://github.com/bungle/lua-resty-libcjson/issues/1#issuecomment-38567447.

## Benchmarks

About 190 MB citylots.json:

```bash
## Lua cJSON
Decoding Time: 5.882825
Encoding Time: 4.902301
## lua-resty-libcjson
Decoding Time: 6.409872
Encoding Time: (takes forever)
```

## License

`lua-resty-libcjson` uses two clause BSD license.

```
Copyright (c) 2014 - 2016, Aapo Talvensaari
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-libcjson](https://github.com/bungle/lua-resty-libcjson){target=_blank}.