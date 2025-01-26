---

title: "Ini parser for nginx-module-lua"
description: "RPM package lua-resty-ini: Ini parser for nginx-module-lua"

---
  
# *ini*: Ini parser for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-ini
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-ini
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-ini [v0.1](https://github.com/doujiang24/lua-resty-ini/releases/tag/v0.01){target=_blank} 
released on May 31 2016.
    
<hr />

lua-resty-ini - Lua ini parser

## Status

This library is still under early development and is still experimental.


## See Also
* the ngx_lua module: http://wiki.nginx.org/HttpLuaModule


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-ini](https://github.com/doujiang24/lua-resty-ini){target=_blank}.