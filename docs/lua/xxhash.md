# *xxhash*: LuaJIT FFI-bindings to xxHash, an Extremely fast non-cryptographic hash algorithm


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-xxhash
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-xxhash
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-xxhash [v1.0](https://github.com/bungle/lua-resty-xxhash/releases/tag/v1.0){target=_blank} 
released on Dec 03 2015.
    
<hr />

`lua-resty-xxhash` contains a LuaJIT FFI-bindings to xxHash, an Extremely fast non-cryptographic hash algorithm.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-xxhash](https://github.com/bungle/lua-resty-xxhash){target=_blank}.