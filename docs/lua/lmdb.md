# *lmdb*: Safe API for manipulating LMDB databases using nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-lmdb
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-lmdb
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-lmdb [v1.4.3](https://github.com/Kong/lua-resty-lmdb/releases/tag/v1.4.3){target=_blank} 
released on Aug 19 2024.
    
<hr />

This module allows OpenResty applications to use the LMDB (Lightning Memory-Mapped Database)
inside the Nginx worker process. It has two parts, a core module built into Nginx that
controls the life cycle of the database environment, and a FFI based Lua binding for
interacting with the module to access/change data.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-lmdb](https://github.com/Kong/lua-resty-lmdb){target=_blank}.