# *snappy*: LuaJIT FFI bindings for Snappy, a fast compressor/decompressor (https://code.google.com/p/snappy/)


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-snappy
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-snappy [v1.0](https://github.com/bungle/lua-resty-snappy/releases/tag/v1.0){target=_blank} 
released on Oct 01 2014.
    
<hr />

`lua-resty-snappy` provides LuaJIT FFI bindings to Snappy, a fast compressor/decompressor (https://code.google.com/p/snappy/).

## Lua API

#### Error Codes

```c
  SNAPPY_OK               = 0,
  SNAPPY_INVALID_INPUT    = 1,
  SNAPPY_BUFFER_TOO_SMALL = 2
```

#### string,len snappy.compress(input)

Compresses `input` with Snappy algorithm, and returns compressed data and its length.
On error this will return nil and an error code.

##### Example

```lua
local snappy    = require "resty.snappy"
local comp, err = snappy.compress("test")
if comp then
    -- do something with compressed data and length
    -- (length is stored in err value)...
else
    if err = 1 then
        print "Invalid input"
    elseif err == 2 then
        print "Buffer too small"
    end
end
```

#### string,len snappy.uncompress(compressed)

Uncompresses `compressed` with Snappy algorithm, and returns uncompressed data and its length.
On error this will return nil and an error code.

##### Example

```lua
local snappy      = require "resty.snappy"
local uncomp, err = snappy.uncompress(snappy.compress("test"))
```

#### number snappy.max_compressed_length(source_length)

Returns maximum-possible length as a number of bytes of compressed data when
uncompressed `source_length` is given. This is used to create buffer for compressing,
but can also be used in quick measurement (and it may have nothing to do with
final compressed output length, other than it cannot be larger than what this
function returns).

##### Example

```lua
local snappy = require "resty.snappy"
local number = snappy.max_compressed_length(1000)
```

#### number snappy.uncompressed_length(compressed)

This is quicker way (than using `snappy.uncompress` to determine how many bytes
the compressed data will be when it is uncompressed.

##### Example

```lua
local snappy = require "resty.snappy"
local number = snappy.uncompressed_length(snappy.compress("test"))
```

#### boolean snappy.validate_compressed_buffer(compressed)

This can be used to check if the compressed bytes are actually Snappy compressed
bytes or something else. I.e. something that can be uncompressed with Snappy.

##### Example

```lua
local snappy = require "resty.snappy"
local bool   = snappy.validate_compressed_buffer(snappy.compress("test"))
```

## License

`lua-resty-libcjson` uses two clause BSD license.

```
Copyright (c) 2014, Aapo Talvensaari
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
nginx-module-snappy](https://github.com/bungle/lua-resty-snappy){target=_blank}.