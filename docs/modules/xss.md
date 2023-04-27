# *xss*: Native cross-site scripting support in NGINX


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
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


## TODO

* add cross-site POST support.


## Author

Yichun "agentzh" Zhang (章亦春) &lt;agentzh@gmail@com&gt;


## Copyright & License

The implementation of the builtin connection pool has borrowed
a lot of code from Maxim Dounin's upstream_keepalive module.
This part of code is copyrighted by Maxim Dounin.

This module is licenced under the BSD license.

Copyright (C) 2009-2018 by Yichun "agentzh" Zhang (章亦春) &lt;agentzh@gmail.com&gt; OpenResty Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## See Also

* [Introduction to JSONP](http://en.wikipedia.org/wiki/JSONP)
* [ngx_lua](https://github.com/openresty/lua-nginx-module)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-xss](https://github.com/dvershinin/xss-nginx-module){target=_blank}.