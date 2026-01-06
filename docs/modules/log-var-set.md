---

title: "Set variables before access log writing"
description: "RPM package nginx-module-log-var-set. The log var set module allows setting NGINX variables to given values before access log writing. This enables computing or modifying variable values specifically for logging purposes without affecting request processing."

---

# *log-var-set*: Set variables before access log writing


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
    dnf -y install nginx-module-log-var-set
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-log-var-set
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_log_var_set_module.so;
```


This document describes nginx-module-log-var-set [v0.1.0](https://github.com/dvershinin/ngx_http_log_var_set_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />

`ngx_http_log_var_set_module` allows setting the variable to the given value before access log writing.

## Table of Content

- [Name](#name)
- [Table of Content](#table-of-content)
- [Status](#status)
- [Synopsis](#synopsis)
- [Installation](#installation)
- [Directives](#directives)
  - [log\_var\_set](#log_var_set)
- [Author](#author)
- [License](#license)

## Status

This Nginx module is currently considered experimental. Issues and PRs are welcome if you encounter any problems.

## Synopsis

```nginx
log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    '"$log_field1" "$log_field2"';
access_log /spool/logs/nginx-access.log;

server {
    listen 127.0.0.1:80;
    server_name localhost;

    location / {
        log_var_set $log_field1 $upstream_http_custom_header1;
        log_var_set $log_field2 $upstream_http_custom_header2;
        proxy_pass http://example.upstream.com;
    }
}
```

## Directives

## log_var_set

**Syntax:** *log_var_set $variable value [if=condition];*

**Default:** *-*

**Context:** *http, server, location*

Sets the request variable to the given value before access log writing. The value may contain variables from request or response, such as $upstream_http_*.
These directives are inherited from the previous configuration level only when there is no directive for the same variable defined at the current level.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-log-var-set](https://github.com/dvershinin/ngx_http_log_var_set_module){target=_blank}.