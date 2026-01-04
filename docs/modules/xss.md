---

title: "Native cross-site scripting support in NGINX"
description: "RPM package nginx-module-xss. This module adds cross-site AJAX support to NGINX.  Currently only cross-site GET is supported.  But cross-site POST will be added in the future.  The cross-site GET is currently implemented as JSONP (or JSON with padding).  See http://en.wikipedia.org/wiki/JSON#JSONP for more details."

---

# *xss*: Native cross-site scripting support in NGINX


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
    dnf -y install nginx-module-xss
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-xss
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_xss_filter_module.so;
```


This document describes nginx-module-xss [v0.6](https://github.com/dvershinin/xss-nginx-module/releases/tag/v0.6){target=_blank} 
released on Dec 26 2022.

<hr />

xss-nginx-module - Native cross-site scripting support in nginx

## Synopsis

```nginx
## accessing /foo?callback=process gives the response
## body "process(...);" (without quotes) where "..."
## is the original response body of the /foo location.
server {
    location /foo {
        # your content handler goes here...

        xss_get on;
        xss_callback_arg 'callback';
        xss_input_types 'application/json'; # default
        xss_output_type 'application/x-javascript'; # default
    }
    ...
}
```

## Description

This module adds cross-site AJAX support to nginx. Currently only
cross-site GET is supported. But cross-site POST will be added
in the future.

The cross-site GET is currently implemented as JSONP
(or "JSON with padding"). See http://en.wikipedia.org/wiki/JSON#JSONP
for more details.

## Directives


## xss_get
**syntax:** *xss_get on | off*

**default:** *xss_get off*

**context:** *http, server, location, if location*

Enables JSONP support for GET requests.


## xss_callback_arg
**syntax:** *xss_callback_arg &lt;name&gt;*

**default:** *none*

**context:** *http, http, location, if location*

Specifies the JavaScript callback function name
used in the responses.

For example,

```nginx
location /foo {
    xss_get on;
    xss_callback_arg c;
    ...
}
```

then

```
GET /foo?c=blah
```

returns

```javascript
blah(...);
```


## xss_override_status
**syntax:** *xss_override_status on | off*

**default:** *xss_check_status on*

**context:** *http, server, location, if location*

Specifies whether to override 30x, 40x and 50x status to 200
when the response is actually being processed.


## xss_check_status
**syntax:** *xss_check_status on | off*

**default:** *xss_check_status on*

**context:** *http, server, location, if location*

By default, ngx_xss only process responses with the status code
200 or 201.


## xss_input_types
**syntax:** *xss_input_types [mime-type]...*

**default:** *xss_input_types application/json*

**context:** *http, server, location, if location*

Only processes the responses of the specified MIME types.

Example:

```nginx
xss_input_types application/json text/plain;
```


## Limitations

* ngx_xss will not work with [ngx_echo](https://github.com/openresty/echo-nginx-module)'s
subrequest interfaces, due to the underlying
limitations imposed by subrequests' "postponed chain" mechanism in the nginx core.
The standard ngx_addition module also falls into this category.  You're recommended,
however, to use [ngx_lua](https://github.com/openresty/lua-nginx-module) as the content
handler to issue subrequests *and* ngx_xss
to do JSONP, because [ngx_lua](https://github.com/openresty/lua-nginx-module)'s
[ngx.location.capture()](https://github.com/openresty/lua-nginx-module#ngxlocationcapture)
interface does not utilize the "postponed chain" mechanism, thus getting out of this
limitation. We're taking this approach in production and it works great.


## Trouble Shooting

Use the "info" error log level (or lower) to get more
diagnostics when things go wrong.


## See Also

* [Introduction to JSONP](http://en.wikipedia.org/wiki/JSONP)
* [ngx_lua](https://github.com/openresty/lua-nginx-module)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-xss](https://github.com/dvershinin/xss-nginx-module){target=_blank}.