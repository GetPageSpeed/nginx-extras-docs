# *cookie-flag*: NGINX cookie flag module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-cookie-flag
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_cookie_flag_filter_module.so;
```


This document describes nginx-module-cookie-flag [v1.1.0](https://github.com/AirisX/nginx_cookie_flag_module/releases/tag/v1.1.0){target=_blank} 
released on Dec 15 2017.

<hr />

[![License](http://img.shields.io/badge/license-BSD-brightgreen.svg)](https://github.com/Airis777/nginx_cookie_flag_module/blob/master/LICENSE)

The Nginx module for adding cookie flag

## Synopsis

```Nginx
location / {
    set_cookie_flag Secret HttpOnly secure SameSite;
    set_cookie_flag * HttpOnly;
    set_cookie_flag SessionID SameSite=Lax secure;
    set_cookie_flag SiteToken SameSite=Strict;
}
```

## Description
This module for Nginx allows to set the flags "**HttpOnly**", "**secure**" and "**SameSite**" for cookies in the "*Set-Cookie*" response headers.
The register of letters for the flags doesn't matter as it will be converted to the correct value. The order of cookie declaration among multiple directives doesn't matter too.
It is possible to set a default value using symbol "*". In this case flags will be added to the all cookies if no other value for them is overriden.

## Directives

### set_cookie_flag

-| -
--- | ---
**Syntax**  | **set_cookie_flag** \<cookie_name\|*\> [HttpOnly] [secure] [SameSite\|SameSite=[Lax\|Strict]];
**Default** | -
**Context** | server, location

Description: Add flag to desired cookie.

## Author
Anton Saraykin [<Airisenator@gmail.com>]

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-cookie-flag](https://github.com/AirisX/nginx_cookie_flag_module){target=_blank}.