# *uuid*: LuaJIT FFI bindings for libuuid, a DCE compatible Universally Unique Identifier library


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-uuid
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-uuid
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-uuid [v1.1](https://github.com/bungle/lua-resty-uuid/releases/tag/v1.1){target=_blank} 
released on Apr 13 2016.
    
<hr />

LuaJIT FFI bindings for libuuid, a DCE compatible Universally Unique Identifier library.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-uuid](https://github.com/bungle/lua-resty-uuid){target=_blank}.