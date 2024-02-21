# *dav-ext*: NGINX WebDAV PROPFIND,OPTIONS,LOCK,UNLOCK support


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-dav-ext
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_dav_ext_module.so;
```


This document describes nginx-module-dav-ext [v3.0.0](https://github.com/arut/nginx-dav-ext-module/releases/tag/v3.0.0){target=_blank} 
released on Dec 17 2018.

<hr />
nginx-dav-ext-module
====================

[nginx](http://nginx.org) [WebDAV](https://tools.ietf.org/html/rfc4918) PROPFIND,OPTIONS,LOCK,UNLOCK support.

About
-----

The standard [ngxhhttpddavmmodule](http://nginx.org/en/docs/http/ngx_http_dav_module.html) provides partial [WebDAV](https://tools.ietf.org/html/rfc4918) implementation and only supports GET,HEAD,PUT,DELETE,MKCOL,COPY,MOVE methods.

For full [WebDAV](https://tools.ietf.org/html/rfc4918) support in [nginx](http://nginx.org) you need to enable the standard [ngxhhttpddavmmodule](http://nginx.org/en/docs/http/ngx_http_dav_module.html) as well as this module for the missing methods.

Build
-----

Building [nginx](http://nginx.org) with the module:

``` {.sourceCode .bash}

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-dav-ext](https://github.com/arut/nginx-dav-ext-module){target=_blank}.