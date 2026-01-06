---

title: "Rewrite response status codes"
description: "RPM package nginx-module-rewrite-status. The rewrite status filter module allows rewriting response status codes. This is useful for customizing HTTP status codes returned to clients based on various conditions, without modifying the upstream response."

---

# *rewrite-status*: Rewrite response status codes


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
    dnf -y install nginx-module-rewrite-status
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-rewrite-status
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_rewrite_status_filter_module.so;
```


This document describes nginx-module-rewrite-status [v0.1.0](https://github.com/dvershinin/ngx_http_rewrite_status_filter_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />

## Synopsis

```nginx
server {
    listen 127.0.0.1:8080;
    server_name localhost;

    location / {
        rewrite_status 404 if=$http_rsp_404_status;
        proxy_pass http://foo.com;
    }
}
```

## Directives

## rewrite_status

**Syntax:** *rewrite_status status \[if=condition\];*

**Default:** *-*

**Context:** *http, server, location*

Rewrite response status code.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-rewrite-status](https://github.com/dvershinin/ngx_http_rewrite_status_filter_module){target=_blank}.