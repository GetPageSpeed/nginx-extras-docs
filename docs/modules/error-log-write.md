---

title: "Conditional error log entries in configuration"
description: "RPM package nginx-module-error-log-write. The error log write module allows writing error log entries based on conditional expressions in NGINX configuration files. This is useful for debugging and monitoring specific conditions without modifying the application or using complex logging setups."

---

# *error-log-write*: Conditional error log entries in configuration


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
    dnf -y install nginx-module-error-log-write
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-error-log-write
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_error_log_write_module.so;
```


This document describes nginx-module-error-log-write [v0.1.0](https://github.com/dvershinin/ngx_http_error_log_write_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />

```nginx
error_log_write level=info message="main test log";

server {
    listen 127.0.0.1:80;
    server_name localhost;

    error_log_write  message="server test log" if=$arg_test; 

    location / {
        error_log_write level=warn message="auth required" if!=$http_authorization;
        auth_baisc "auth required";
        auth_basic_user_file conf/htpasswd;
        proxy_pass http://example.upstream.com;
    }
}
```

## Directives

## error_log_write

**Syntax:** *error_log_write [level=log_level] message=text [if=condition];*

**Default:** *-*

**Context:** *http, server, location*

Writing a new error log. All error log entries are inherited unconditionally from the previous configuration level.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-error-log-write](https://github.com/dvershinin/ngx_http_error_log_write_module){target=_blank}.