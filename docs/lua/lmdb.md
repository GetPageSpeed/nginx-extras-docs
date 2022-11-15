# *lmdb*: Safe API for manipulating LMDB databases using nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-lmdb
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-lmdb [v1.0.0](https://github.com/Kong/lua-resty-lmdb/releases/tag/1.0.0){target=_blank} 
released on Aug 24 2022.
    
<hr />

This module allows OpenResty applications to use the LMDB (Lightning Memory-Mapped Database)
inside the Nginx worker process. It has two parts, a core module built into Nginx that
controls the life cycle of the database environment, and a FFI based Lua binding for
interacting with the module to access/change data.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-lmdb](https://github.com/Kong/lua-resty-lmdb){target=_blank}.