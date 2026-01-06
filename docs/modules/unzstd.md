---

title: "Decompresses Zstd-encoded responses for clients that do not support it"
description: "RPM package nginx-module-unzstd. The ngx_unzstd module is a filter that decompresses responses with Content-Encoding: zstd for clients that do not support Zstd encoding method. It allows to save I/O by unconditional Zstd compression of responses. This complements the zstd compression module for full zstd support."

---

# *unzstd*: Decompresses Zstd-encoded responses for clients that do not support it


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9 and 10
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023+"

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-unzstd
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-unzstd
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_unzstd_filter_module.so;
```


This document describes nginx-module-unzstd [v0.1.0](https://github.com/dvershinin/ngx_http_unzstd_filter_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />
ngx_http_unzstd_filter_module is a filter that decompresses responses with “Content-Encoding: zstd” for clients that do not support “zstd” ([Zstandard compression](https://facebook.github.io/zstd/)) encoding method. The module will be useful when it is desirable to store data compressed to save space and reduce I/O costs.

## Table of Content

* [Name](#name)
* [Status](#status)
* [Synopsis](#synopsis)
* [Installation](#installation)
* [Directives](#directives)
  * [unzstd](#unzstd)
  * [unzstd_force](#unzstd_force)
  * [unzstd_buffers](#unzstd_buffers)
* [Author](#author)
* [License](#license)
## Status

This Nginx module is currently considered experimental. Issues and PRs are welcome if you encounter any problems.

> Known Issue: 
1. Due to improper handling of zstd library dependencies, this module needs to be built together with [zstd-nginx-module](https://github.com/tokers/zstd-nginx-module). I am currently unable to solve this problem. Welcome to submit PR.
2. This module occasionally has a problem of sending the chunked end marker (0\r\n\r\n) twice when decompressing chunked responses. I can't fix it at the moment, so I have to temporarily disable this module. If you are interested in this module, you can try to solve it, and your PR is welcome.

## Synopsis

```nginx
server {
    listen 127.0.0.1:8080;
    server_name localhost;

    location / {
        # enable zstd decompression for clients that do not support zstd compression
        unzstd on;

        proxy_pass http://foo.com;
    }
}
```

## Directives

## unzstd

**Syntax:** *unzstd on | off;*

**Default:** *unzstd off;*

**Context:** *http, server, location*

Enables or disables decompression of zstd compressed responses for clients that lack zstd support.

## unzstd_force

**Syntax:** *unzstd_force string ...;*

**Default:** *-*

**Context:** *http, server, location*

Defines the conditions for forced brotli decompression. If at least one value in the string parameter is not empty and not equal to "0", forced zstd decompression is performed. But it will not try to decompress responses that do not contain the response header Content-Encoding: zstd.

## unzstd_buffers

**Syntax:** *unzstd_buffers number size;*

**Default:** *unzstd_buffers 32 4k | 16 8k;*

**Context:** *http, server, location*

Sets the number and size of buffers used to decompress a response. By default, the buffer size is equal to one memory page. This is either 4K or 8K, depending on a platform.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-unzstd](https://github.com/dvershinin/ngx_http_unzstd_filter_module){target=_blank}.