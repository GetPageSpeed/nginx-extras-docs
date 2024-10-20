# *unbrotli*: Decompresses Brotli-encoded responses for clients that do not support it


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
    yum -y install nginx-module-unbrotli
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-unbrotli
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_unbrotli_filter_module.so;
```


This document describes nginx-module-unbrotli [v0.0.1](https://github.com/dvershinin/ngx_unbrotli/releases/tag/v0.0.1){target=_blank} 
released on Oct 13 2024.

<hr />
The `ngx_unbrotli` module is a filter that decompresses responses with `Content-Encoding: br` for clients that do not support `brotli` encoding method.

#### Usage

`load_module modules/ngx_http_unbrotli_filter_module.so;`

Usage is similar to [ngx_http_gunzip_module](http://nginx.org/en/docs/http/ngx_http_gunzip_module.html)

- Replace `gunzip` with `unbrotli`
- Replace `gunzip_buffers` with `unbrotli_buffers`

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-unbrotli](https://github.com/dvershinin/ngx_unbrotli){target=_blank}.