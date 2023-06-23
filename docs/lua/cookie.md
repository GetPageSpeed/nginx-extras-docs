# *cookie*: Lua library for HTTP cookie manipulations for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-cookie
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-cookie
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-cookie [v0.1.0](https://github.com/cloudflare/lua-resty-cookie/releases/tag/v0.1.0){target=_blank} 
released on Jul 16 2015.
    
<hr />

lua-resty-cookie - This library parses HTTP Cookie header for Nginx and returns each field in the cookie.

## Status

This library is production ready.

## Synopsis
```lua
    server {
        location /test {
            content_by_lua '
                local ck = require "resty.cookie"
                local cookie, err = ck:new()
                if not cookie then
                    ngx.log(ngx.ERR, err)
                    return
                end

                -- get single cookie
                local field, err = cookie:get("lang")
                if not field then
                    ngx.log(ngx.ERR, err)
                    return
                end
                ngx.say("lang", " => ", field)

                -- get all cookies
                local fields, err = cookie:get_all()
                if not fields then
                    ngx.log(ngx.ERR, err)
                    return
                end

                for k, v in pairs(fields) do
                    ngx.say(k, " => ", v)
                end

                -- set one cookie
                local ok, err = cookie:set({
                    key = "Name", value = "Bob", path = "/",
                    domain = "example.com", secure = true, httponly = true,
                    expires = "Wed, 09 Jun 2021 10:18:14 GMT", max_age = 50,
                    extension = "a4334aebaec"
                })
                if not ok then
                    ngx.log(ngx.ERR, err)
                    return
                end

                -- set another cookie, both cookies will appear in HTTP response
                local ok, err = cookie:set({
                    key = "Age", value = "20",
                })
                if not ok then
                    ngx.log(ngx.ERR, err)
                    return
                end
            ';
        }
    }
```

## Methods

new
---
`syntax: cookie_obj = cookie()`

Create a new cookie object for current request. You can get parsed cookie from client or set cookie to client later using this object.

get
---
`syntax: cookie_val, err = cookie_obj:get(cookie_name)`

Get a single client cookie value. On error, returns `nil` and an error message.

## get_all
`syntax: fields, err = cookie_obj:get_all()`

Get all client cookie key/value pairs in a lua table. On error, returns `nil` and an error message.

set
---
```lua
syntax: ok, err = cookie_obj:set({
    key = "Name",
    value = "Bob",
    path = "/",
    domain = "example.com",
    secure = true, httponly = true,
    expires = "Wed, 09 Jun 2021 10:18:14 GMT",
    max_age = 50,
    extension = "a4334aebaec"
})
```

Set a cookie to client. This will add a new 'Set-Cookie' response header. `key` and `value` are required, all other fields are optional.
If the same cookie (whole cookie string, e.g. "Name=Bob; Expires=Wed, 09 Jun 2021 10:18:14 GMT; Max-Age=50; Domain=example.com; Path=/; Secure; HttpOnly;") has already been setted, new cookie will be ignored.

## Authors

Jiale Zhi <vipcalio@gmail.com>, CloudFlare Inc.

Yichun Zhang (agentzh) <agentzh@gmail.com>, CloudFlare Inc.

## Copyright and License

This module is licensed under the BSD license.

Copyright (C) 2013, by Jiale Zhi <vipcalio@gmail.com>, CloudFlare Inc.

Copyright (C) 2013, by Yichun Zhang <agentzh@gmail.com>, CloudFlare Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-cookie](https://github.com/cloudflare/lua-resty-cookie){target=_blank}.