---

title: "LuaJIT FFI-based scrypt library for nginx-module-lua"
description: "RPM package lua-resty-scrypt: LuaJIT FFI-based scrypt library for nginx-module-lua"

---
  
# *scrypt*: LuaJIT FFI-based scrypt library for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-scrypt
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-scrypt
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-scrypt [v1.0](https://github.com/bungle/lua-resty-scrypt/releases/tag/v1.0){target=_blank} 
released on Oct 09 2014.
    
<hr />

`lua-resty-scrypt` is a scrypt (password) hashing library for OpenResty.

## Hello World with lua-resty-scrypt

```lua
local scrypt = require "resty.scrypt"
local hash   = scrypt.crypt "My Secret"         -- returns a hash that can be stored in db
local valid  = scrypt.check("My Secret", hash)  -- valid holds true
local valid  = scrypt.check("My Guess",  hash)  -- valid holds false

local n,r,p  = scrypt.calibrate()               -- returns n,r,p calibration values
```

## Lua API

#### string scrypt.crypt(opts)

Uses scrypt algorithm to generate hash from the input. Input parameter `opts` can
either be `string` (a `secret`) or a table. If it is a table you may pass in some
configuration parameters as well. Available table options (defaults are as follows):

```lua
local opts = {
    secret   = "",
    keysize  = 32,
    n        = 32768
    r        = 8,
    p        = 1,
    salt     = "random (saltsize) bytes generated with OpenSSL",
    saltsize = 8
}
```

If you pass opts anything other than a table, it will be `tostring`ified and used
as a `secret`. `keysize` can be between 16 and 512, `saltsize` can be between 8
and 32.

This function returns string that looks like this:

```lua
n$r$p$salt$hash
```

All parts present a `hex dump` of their values.

##### Example

```lua
local h1 = scrypt.crypt "My Secret"
local h2 = scrypt.crypt{
    secret  = "My Secret",
    keysize = 512 
}
```

#### boolean scrypt.check(secret, hash)

With this function you can check if the `secret` really matches with the `hash` that
was generated with `scrypt.crypt` from the same `secret`. The `hash` contains also the
configuration parameters like `n`, `r`, `p` and `salt`.

##### Example

```lua
local b1 = scrypt.check("My Secret", scrypt.crypt "My Secret") -- returns true
local b2 = scrypt.check("My Secret", scrypt.crypt "No Secret") -- returns false
```

#### n, r, p scrypt.calibrate(maxmem, maxmemfrac, maxtime)

This function can be used to count `n`, `r`, and `p` configuration values from
`maxmem`, `maxmemfrac` and `maxtime` parameters. These are the defaults for those:

```lua
maxmem     = 1048576
maxmemfrac = 0.5
maxtime    = 0.2
```

The results may change depending on your computer's processing power.

##### Example

```lua
local n,r,p = scrypt.calibrate()
local hash  = scrypt.crypt{
    secret  = "My Secret",
    n = n,
    r = r,
    p = p
}
```

#### number scrypt.memoryuse(n, r, p)

Counts the memory use of scrypt-algorigth with the provided `n`, `r`, and `p`
arguments.

##### Example

```lua
local memoryuse = scrypt.memoryuse(scrypt.calibrate())
```

Default parameters for `n`, `r`, and `p` are:

```lua
n = 32768
r = 8
p = 1
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-scrypt](https://github.com/bungle/lua-resty-scrypt){target=_blank}.