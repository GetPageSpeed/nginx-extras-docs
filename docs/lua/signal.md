---

title: "Lua library for killing or sending signals to UNIX processes"
description: "RPM package lua-resty-signal: Lua library for killing or sending signals to UNIX processes"

---
  
# *signal*: Lua library for killing or sending signals to UNIX processes


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-signal
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-signal
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-signal [v0.4](https://github.com/openresty/lua-resty-signal/releases/tag/v0.04){target=_blank} 
released on Aug 08 2024.
    
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


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-signal](https://github.com/openresty/lua-resty-signal){target=_blank}.