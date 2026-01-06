---

title: "CDN-Loop header support for request loop prevention"
description: "RPM package nginx-module-loop-detect. The loop detect module allows NGINX to use the CDN-Loop header to prevent request loops. This is particularly important for CDN configurations where requests may inadvertently loop between servers. The module implements RFC 8586 for loop detection in content delivery networks."

---

# *loop-detect*: CDN-Loop header support for request loop prevention


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
    dnf -y install nginx-module-loop-detect
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-loop-detect
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_loop_detect_module.so;
```


This document describes nginx-module-loop-detect [v0.1.0](https://github.com/dvershinin/ngx_http_loop_detect_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />

`ngx_http_loop_detect_module` allows NGINX to use the [CDN-Loop](https://datatracker.ietf.org/doc/rfc8586/) header to prevent request loops.

## Table of Content

- [Name](#name)
- [Table of Content](#table-of-content)
- [Status](#status)
- [Synopsis](#synopsis)
- [Installation](#installation)
- [Directives](#directives)
  - [loop\_detect](#loop_detect)
  - [loop\_detect\_cdn\_id](#loop_detect_cdn_id)
  - [loop\_detect\_status](#loop_detect_status)
  - [loop\_detect\_max\_allow\_loops](#loop_detect_max_allow_loops)
- [Variables](#variables)
  - [$loop\_detect\_current\_loops](#loop_detect_current_loops)
  - [$loop\_detect\_proxy\_add\_cdn\_loop](#loop_detect_proxy_add_cdn_loop)
- [How It Works](#how-it-works)
- [Author](#author)
- [License](#license)

## Status

This Nginx module is currently considered experimental. Issues and PRs are welcome if you encounter any problems.

## Synopsis

```nginx
http {
    # Enable the module in a location block
    loop_detect on;
    loop_detect_cdn_id my_cdn_id;
    loop_detect_status 508;
    loop_detect_max_allow_loops 10;

    server {
        listen 80;
        server_name example.com;
        location / {
            proxy_set_header CDN-Loop $loop_detect_proxy_add_cdn_loop;
            proxy_pass http://example.upstream.com;
        }
    }
}
```

## Directives

## loop_detect

**Syntax:** *loop_detect on | off;*

**Default:** *loop_detect off;*

**Context:** *http, server, location*

Enables or disables the loop detection for the current scope. When enabled, the module checks the `CDN-Loop` header to track the number of hops and blocks requests exceeding the allowed limit.

## loop_detect_cdn_id

**Syntax:** *loop_detect_cdn_id string;*

**Default:** *loop_detect_cdn_id openresty;*

**Context:** *http, server, location*

Sets the unique identifier for your clusters. This identifier is used to parse and track loops in the CDN-Loop header.

## loop_detect_status

**Syntax:** *loop_detect_status code;*

**Default:** *loop_detect_status 508;*

**Context:** *http, server, location*

Sets the HTTP status code returned when a request exceeds the allowed loop limit. The code must be between `400` and `599` (client or server errors).

## loop_detect_max_allow_loops

**Syntax:** *loop_detect_max_allow_loops number;*

**Default:** *loop_detect_max_allow_loops 10;*

**Context:** *http, server, location*

Sets the maximum number of allowed loops before blocking the request. The number must be greater than 0.

## Variables

## $loop_detect_current_loops

Returns the current detected loop count extracted from the CDN-Loop header. This value represents the number of hops your request has already passed through CDN nodes.

## $loop_detect_proxy_add_cdn_loop

Constructs the new `CDN-Loop` header value to be sent to downstream proxies. This value includes:

1. The current CDN node's identifier and incremented loop count (e.g., `my_cdn; loops=2`).
2. Remaining other entries from the original `CDN-Loop` header (if any).

Example Usage:

```nginx
location / {
    proxy_set_header CDN-Loop $loop_detect_proxy_add_cdn_loop;
    proxy_pass http://backend;
}
```


## How It Works
1. Detection:
The module parses the `CDN-Loop` header to identify the number of hops. Each hop is formatted as:
Format: `Cdn-Loop: <cdn_id>; loops=<count>, ...`
Example: `Cdn-Loop: my_cdn; loops=2, another_cdn; loops=1`.

2. Tracking:
The current hop count (current_loops) is extracted from the header.
The module increments the count and constructs a new `CDN-Loop` value for downstream proxies.

3. Blocking:
If the detected loop count exceeds `loop_detect_max_allow_loops`, NGINX returns the configured `loop_detect_status` (e.g., 508).

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-loop-detect](https://github.com/dvershinin/ngx_http_loop_detect_module){target=_blank}.