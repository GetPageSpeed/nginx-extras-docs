---

title: "Reverse-proxying of websocket frames"
description: "RPM package lua-resty-websocket-proxy: Reverse-proxying of websocket frames"

---
  
# *websocket-proxy*: Reverse-proxying of websocket frames


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-websocket-proxy
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-websocket-proxy
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-websocket-proxy [v0.0.1](https://github.com/Kong/lua-resty-websocket-proxy/releases/tag/0.0.1){target=_blank} 
released on Apr 04 2022.
    
<hr />

Reverse-proxying of websocket frames with in-flight inspection/update/drop and
frame aggregation support.

Resources:

- [RFC-6455](https://datatracker.ietf.org/doc/html/rfc6455)
- [lua-resty-websocket](https://github.com/openresty/lua-resty-websocket)

## Synopsis

```lua
http {
    server {
        listen 9000;

        location / {
            content_by_lua_block {
                local ws_proxy = require "resty.websocket.proxy"

                local proxy, err = ws_proxy.new({
                    aggregate_fragments = true,
                    on_frame = function(origin, typ, payload, last, code)
                        --  origin: [string]      "client" or "upstream"
                        --     typ: [string]      "text", "binary", "ping", "pong", "close"
                        -- payload: [string|nil]  payload if any
                        --    last: [boolean]     fin flag for fragmented frames; true if aggregate_fragments is on
                        --    code: [number|nil]  code for "close" frames

                        if update_payload then
                            -- change payload + code before forwarding
                            return "new payload", 1001
                        end

                        -- forward as-is
                        return payload
                    end
                })
                if not proxy then
                    ngx.log(ngx.ERR, "failed to create proxy: ", err)
                    return ngx.exit(444)
                end

                local ok, err = proxy:connect("ws://127.0.0.1:9001")
                if not ok then
                    ngx.log(ngx.ERR, err)
                    return ngx.exit(444)
                end

                -- Start a bi-directional websocket proxy between
                -- this client and the upstream
                local done, err = proxy:execute()
                if not done then
                    ngx.log(ngx.ERR, "failed proxying: ", err)
                    return ngx.exit(444)
                end
            }
        }
    }
}
```

## Limitations

* Built with [lua-resty-websocket](https://github.com/openresty/lua-resty-websocket)
  which only supports `Sec-Websocket-Version: 13` (no extensions) and denotes
  its client component a
  [work-in-progress](https://github.com/openresty/lua-resty-websocket/blob/master/lib/resty/websocket/client.lua#L4-L5).


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-websocket-proxy](https://github.com/Kong/lua-resty-websocket-proxy){target=_blank}.