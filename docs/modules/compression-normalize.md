---

title: "NGINX Accept-Encoding Normalization module"
description: "RPM package nginx-module-compression-normalize. NGINX module that parses, normalizes, and manages the Accept-Encoding  headers from client requests. It ensures consistent handling of  compression algorithms by standardizing the Accept-Encoding values, reducing cache variant explosion and improving vary cache performance.  This is essential for proxy caching with Vary: Accept-Encoding to  prevent creating multiple cache entries for equivalent compression  preferences like gzip, br vs br, gzip."

---

# *compression-normalize*: NGINX Accept-Encoding Normalization module


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
    dnf -y install nginx-module-compression-normalize
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-compression-normalize
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_compression_normalize_module.so;
```


This document describes nginx-module-compression-normalize [v1.0.0](https://github.com/dvershinin/ngx_http_compression_normalize_module/releases/tag/1.0.0){target=_blank} 
released on Jan 06 2026.

<hr />

## Describe

`ngx_http_compression_normalize_module` is an Nginx module designed to parse, normalize, and manage the Accept-Encoding headers from client requests. It ensures consistent handling of compression algorithms by standardizing the Accept-Encoding values, facilitating better compression management and improved vary cache performance.

## Synopsis

```nginx
http {
    compression_normalize_accept_encoding gzip,br,zstd gzip,br zstd br gzip;

    server {
        listen 80;
        server_name example.com;

        location / {
            # Your configurations
        }
    }
}
```

## Directives

## compression_normalize_accept_encoding

**Syntax:** *compression_normalize_accept_encoding combinations1 \[combinations2 ..\] | off;*

**Default:** *compression_normalize_accept_encoding off;*

**Context:** *http, server, location*

Enables the normalization of the Accept-Encoding header by specifying preferred combinations of compression algorithms. This directive accepts a list of compression methods, allowing to define the order and priority of encoding types that the server should prefer when responding to client requests.

For example, with the following configuration

```nginx
compression_normalize_accept_encoding gzip,br,zstd gzip,br zstd br gzip;
```

If the request header Accept-Encoding contains gzip, br and zstd at the same time, the value of the standardized Accept-Encoding header is `gzip,br,zstd`. If the above conditions are not met, but the request header contains gzip and br, the value of the standardized Accept-Encoding header is `gzip,br`. And so on, until all the combinations given by the `compression_normalize_accept_encoding` directive are checked. If no combination is hit at this time, the Accept-Encoding header is directly deleted.

A value of `off` will disable this feature.

## Variables

## \$compression_original_accept_encoding

keeps the original value of request Accept-Encoding header.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-compression-normalize](https://github.com/dvershinin/ngx_http_compression_normalize_module){target=_blank}.