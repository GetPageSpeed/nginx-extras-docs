---

title: "Advanced access control based on variables"
description: "RPM package nginx-module-access-control. The access control module provides advanced access control based on variables. Unlike the standard allow/deny directives that work with IP addresses, this module allows access decisions based on any NGINX variable, enabling flexible access policies."

---

# *access-control*: Advanced access control based on variables


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
    dnf -y install nginx-module-access-control
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-access-control
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_access_control_module.so;
```


This document describes nginx-module-access-control [v0.1.0](https://github.com/dvershinin/ngx_http_access_control_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />

## Synopsis

```nginx
server {
    listen 80;
    server_name example.com;

    # Allow access if $var2 is non-empty and not zero. The allowed request will no longer match the remaining access control rules.
    access allow $var1;

    # Deny access if $var1 is non-empty and not zero
    access deny $var2;

    location / {
        # Your other configurations
    }

    location /restricted {
        # Override deny status code
        access_deny_status 404;

        # Deny access if $var3 is non-empty and not zero
        access deny $var3;
    }
}
```

## Directives

## access

**Syntax:** *access [allow|deny] variable;*

**Default:** *-*

**Context:** *http, server, location*

The access directive defines an access control rule based on a variable. The variable is evaluated at runtime, and if it is non-empty and not zero, the rule is considered matched.

allow: Allows access if the condition is met. The allowed request will no longer match the remaining access control rules.
deny: Denies access if the condition is met.


## access_rules_inherit

**Syntax:** *access_rules_inherit off | before | after;*

**Default:** *access_rules_inherit off;*

**Context:** *http, server, location*

determines whether and how access control rules from previous level are applied in the current configuration context. It accepts three values:

off: do not inherit any access rules from previous level, unless no access directive is defined at the current level.
before: apply access rules of previous level before the access rules of current level.
after: apply access rules of previous level after the access rules of current level.

## access_deny_status

**Syntax:** *access_deny_status code;*

**Default:** *access_deny_status 403;*

**Context:** *http, server, location*

Sets the HTTP status code to return in response when access is denied by a deny rule.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-access-control](https://github.com/dvershinin/ngx_http_access_control_module){target=_blank}.