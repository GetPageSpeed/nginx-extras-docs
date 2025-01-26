---

title: "Port of Qless' web interface to nginx-module-lua environment"
description: "RPM package lua-resty-qless-web: Port of Qless' web interface to nginx-module-lua environment"

---
  
# *qless-web*: Port of Qless' web interface to nginx-module-lua environment


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-qless-web
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-qless-web
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-qless-web [v0.5](https://github.com/hamishforbes/lua-resty-qless-web/releases/tag/v0.05){target=_blank} 
released on Sep 20 2016.
    
<hr />

### Overview
Port of Moz's [qless](https://github.com/seomoz/qless) web interface to the [Openresty](http://www.openresty.org) environment.


### Methods

#### new
`syntax: ok, err = Qless_web:new(opts)`

`opts` is a table of options
 * `client` must be an instance of [lua-resty-qless](https://github.com/pintsized/lua-resty-qless)
 * `uri_prefix` defaults to `/`, sets the value prepended to all URIs


#### run

`syntax: ok, err = qless_web:run()`

Performs routing based on current uri.
Requires a sub-location `/__static` configure to serve static assets

### Config

```
init_by_lua '
    -- Require here to compile templates
    local Qless_Web = require("resty.qless-web")
';

location /web {

    default_type text/html;
    location /web/__static {
        internal;
        rewrite ^/web/__static(.*) $1 break;
        root /path/to/lua-resty-qless-web/static/;
    }

    content_by_lua '
        -- Connect Qless client
        local resty_qless = require "resty.qless"
        local qless, err = resty_qless.new(
            {
                redis = { host = "127.0.0.1", port = 6379 }
            },
            { database = 1 }
        )
        if not qless then
            return ngx.say("Qless.new(): ", err)
        end

        -- Create and run qless web
        local Qless_Web = require("resty.qless-web")
        local web = Qless_Web:new({ client = qless, uri_prefix = "/web" })

        web:run()
    ';
}

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-qless-web](https://github.com/hamishforbes/lua-resty-qless-web){target=_blank}.