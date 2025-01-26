---

title: "Stash and apply the old ngx.ctx for avoiding being destoried after NGINX internal redirect happens"
description: "RPM package lua-resty-ctxdump: Stash and apply the old ngx.ctx for avoiding being destoried after NGINX internal redirect happens"

---
  
# *ctxdump*: Stash and apply the old ngx.ctx for avoiding being destoried after NGINX internal redirect happens


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-ctxdump
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-ctxdump
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-ctxdump [v0.1](https://github.com/tokers/lua-resty-ctxdump/releases/tag/v0.1){target=_blank} 
released on Jan 07 2021.
    
<hr />

lua-resty-ctxdump - stash and apply the ngx.ctx, avoiding being destoried after Nginx internal redirect happens.

![Build Status](https://travis-ci.org/tokers/lua-resty-ctxdump.svg?branch=master)

## Status

Probably production ready in most cases, though not yet proven in the wild.  Please check the issues list and let me know if you have any problems / questions.

## Synopsis

```lua

location /t1 {
    set $ctx_ref = "";
    content_by_lua_block {
         local ctxdump = require "resty.ctxdump"
         ngx.ctx = {
             Date = "Wed May  3 15:18:04 CST 2017",
             Site = "unknown"
        }
        ngx.var.ctx_ref = ctxdump.stash_ngx_ctx()
        ngx.exec("/t2")
    }
}

location /t2 {
    internal;
    content_by_lua_block {
         local ctxdump = require "resty.ctxdump"
         ngx.ctx = {
             Date = "Wed May  3 15:18:04 CST 2017",
             Site = "unknown"
        }
        ngx.ctx = ctxdump.apply_ngx_ctx(ngx.var.ctx_ref)
        ngx.say("Date: " .. ngx.ctx["Date"] .. " Site: " .. ngx.ctx["Site"])
    }
}

```

## Methods

## stash_ngx_ctx

**syntax:** *ref = stash_ngx_ctx()* <br>
**phase:** *init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*,
    content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*,
    ngx.timer.\*, balancer_by_lua\* 
    
Reference the `ngx.ctx`, returns an anchor(a new reference maintained by lua-resty-ctxdump).

Note: `stash_ngx_ctx` and `apply_ngx_ctx` must be called in pairs, otherwise memory leak will happen! See [apply_ngx_ctx](#apply_ngx_ctx).

## apply_ngx_ctx

**syntax:** *old_ngx_ctx = apply_ngx_ctx(ref)* <br>
**phase:** *init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*,
    content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*,
    ngx.timer.\*, balancer_by_lua\* 
    
fetch the old `ngx.ctx` with the anchor returns from `stash_ngx_ctx `. After that, the anchor will be out of work.

Note: `stash_ngx_ctx` and `apply_ngx_ctx ` must be called in pairs, otherwise memory leak will happen! See [stash_ngx_ctx](#stash_ngx_ctx).


## See Also

* upyun-resty: https://github.com/upyun/upyun-resty

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-ctxdump](https://github.com/tokers/lua-resty-ctxdump){target=_blank}.