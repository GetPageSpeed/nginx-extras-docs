# *fileinfo*: LuaJIT FFI bindings to libmagic, magic number recognition library - tries to determine file types


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-fileinfo
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-fileinfo
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-fileinfo [v1.0](https://github.com/bungle/lua-resty-fileinfo/releases/tag/v1.0){target=_blank} 
released on Oct 09 2014.
    
<hr />

`lua-resty-fileinfo` is a file information library implementing LuaJIT bindings to `libmagic`.

## Hello World with lua-resty-fileinfo

```lua
local fileinfo = require "resty.fileinfo"
fileinfo"a.txt"
```

This will return string containing `ASCII text`. But there are other information available as well.

## Lua API

TBD

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-fileinfo](https://github.com/bungle/lua-resty-fileinfo){target=_blank}.