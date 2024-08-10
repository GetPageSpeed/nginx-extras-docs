# *ftpclient*: Lua ftp client driver for nginx-module-lua based on the cosocket API


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-ftpclient
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-ftpclient
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-ftpclient [v1.1](https://github.com/hongliang5316/lua-resty-ftpclient/releases/tag/v1.1){target=_blank} 
released on Aug 07 2018.
    
<hr />
lua-resty-ftpclient - Lua ftp client driver for the ngx_lua based on the cosocket API

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-ftpclient](https://github.com/hongliang5316/lua-resty-ftpclient){target=_blank}.