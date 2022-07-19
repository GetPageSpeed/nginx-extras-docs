# *etcd*: Nonblocking Lua etcd driver library for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-etcd
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-etcd [v1.8.2](https://github.com/api7/lua-resty-etcd/releases/tag/v1.8.2){target=_blank} 
released on Jul 18 2022.
    
<hr />

[resty-etcd](https://github.com/iresty/lua-resty-etcd) Nonblocking Lua etcd driver library for OpenResty, this module supports etcd API v3.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/iresty/lua-resty-etcd/blob/master/LICENSE)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-etcd](https://github.com/api7/lua-resty-etcd){target=_blank}.