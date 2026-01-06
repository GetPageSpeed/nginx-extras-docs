---

title: "Enhanced Vary header handling for compression"
description: "RPM package nginx-module-compression-vary. The compression vary filter module is a header filter used instead of the standard gzip_vary directive. It provides more control over Vary header handling for gzip, brotli, and zstd compression, which is important for proper cache behavior with compressed content."

---

# *compression-vary*: Enhanced Vary header handling for compression


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
    dnf -y install nginx-module-compression-vary
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-compression-vary
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_compression_vary_filter_module.so;
```


This document describes nginx-module-compression-vary [v0.1.0](https://github.com/dvershinin/ngx_http_compression_vary_filter_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />

## Synopsis

```nginx
server {
    listen 127.0.0.1:8080;
    server_name localhost;

    location / {
        gzip on;
        compression_vary on;

        proxy_pass http://foo.com;
    }
}
```

## Directives

## compression_vary

**Syntax:** *compression_vary on | off;*

**Default:** *compression_vary off;*

**Context:** *http, server, location*

Enables or disables inserting the `Vary: Accept-Encoding` response header field if the directives `gzip`, `gzip_static`, or `gunzip` are active.

Unlike `gzip_vary`, if a `Vary` header exists for the original response, it will append the `Accept-Encoding` to the original `Vary` header. In addition, multiple `Vary` headers will be merged into one and separated by commas. Duplicate header values ​​in `Vary` will be removed.

This module is also effective when the directives from third-party compression modules such as `brotli`, `brotli_static`, `unbrotli`, `zstd`, `zstd_static`, and `unzstd` are activated.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-compression-vary](https://github.com/dvershinin/ngx_http_compression_vary_filter_module){target=_blank}.