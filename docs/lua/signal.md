# *signal*: Lua library for killing or sending signals to UNIX processes


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-signal
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-signal [v0.3](https://github.com/openresty/lua-resty-signal/releases/tag/v0.03){target=_blank} 
released on May 07 2021.
    
<hr />

lua-resty-signal - Lua library for killing or sending signals to Linux processes

## Synopsis

```lua
local resty_signal = require "resty.signal"
local pid = 12345

local ok, err = resty_signal.kill(pid, "TERM")
if not ok then
    ngx.log(ngx.ERR, "failed to kill process of pid ", pid, ": ", err)
    return
end

-- send the signal 0 to check the existence of a process
local ok, err = resty_signal.kill(pid, "NONE")

local ok, err = resty_signal.kill(pid, "HUP")

local ok, err = resty_signal.kill(pid, "KILL")
```

## Functions

## kill

**syntax:** `ok, err = resty_signal.kill(pid, signal_name_or_num)`

Sends a signal with its name string or number value to the process of the
specified pid.

All signal names accepted by [signum](#signum) are supported, like `HUP`,
`KILL`, and `TERM`.

Signal numbers are also supported when specifying nonportable system-specific
signals is desired.

## signum

**syntax:** `num = resty_signal.signum(sig_name)`

Maps the signal name specified to the system-specific signal number. Returns
`nil` if the signal name is not known.

All the POSIX and BSD signal names are supported:

```
HUP
INT
QUIT
ILL
TRAP
ABRT
BUS
FPE
KILL
USR1
SEGV
USR2
PIPE
ALRM
TERM
CHLD
CONT
STOP
TSTP
TTIN
TTOU
URG
XCPU
XFSZ
VTALRM
PROF
WINCH
IO
PWR
EMT
SYS
INFO
```

The special signal name `NONE` is also supported, which is mapped to zero (0).

## Author

Yichun Zhang (agentzh) <yichun@openresty.com>

## Copyright & Licenses

This module is licensed under the BSD license.

Copyright (C) 2018-2019, [OpenResty Inc.](https://openresty.com)

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-signal](https://github.com/openresty/lua-resty-signal){target=_blank}.