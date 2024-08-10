# *ts*: NGINX MPEG-TS Live Module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-ts
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-ts
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_ts_module.so;
```


This document describes nginx-module-ts [v0.1.1](https://github.com/arut/nginx-ts-module/releases/tag/v0.1.1){target=_blank} 
released on Jul 14 2017.

<hr />
NGINX MPEG-TS Live Module
=========================

Features
--------

-   receives MPEG-TS over HTTP
-   produces and manages live [HLS](https://tools.ietf.org/html/draft-pantos-http-live-streaming-23)
-   produces and manages live [MPEGDDASH](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)

Compatibility
-------------

-   [nginx](http://nginx.org) version \>= 1.11.5

Build
-----

Building nginx with the module:

``` {.sourceCode .bash}

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-ts](https://github.com/arut/nginx-ts-module){target=_blank}.