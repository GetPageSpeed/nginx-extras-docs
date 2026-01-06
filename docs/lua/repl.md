---

title: "Interactive console (REPL) for nginx-module-lua and luajit code"
description: "RPM package lua-resty-repl: Interactive console (REPL) for nginx-module-lua and luajit code"

---
  
# *repl*: Interactive console (REPL) for nginx-module-lua and luajit code


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-repl
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-repl
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-repl [v0.1](https://github.com/saks/lua-resty-repl/releases/tag/0.01){target=_blank} 
released on Aug 29 2016.
    
<hr />

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-repl](https://github.com/saks/lua-resty-repl){target=_blank}.