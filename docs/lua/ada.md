---

title: "LuaJIT FFI bindings to Ada — WHATWG-compliant and fast URL parser"
description: "RPM package lua-resty-ada: LuaJIT FFI bindings to Ada — WHATWG-compliant and fast URL parser"

---
  
# *ada*: LuaJIT FFI bindings to Ada — WHATWG-compliant and fast URL parser


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-ada
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-ada
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-ada [v1.1.0](https://github.com/bungle/lua-resty-ada/releases/tag/v1.1.0){target=_blank} 
released on Sep 03 2024.
    
<hr />

**lua-resty-ada** implements a LuaJIT FFI bindings to
[Ada — WHATWG-compliant and fast URL parser](https://github.com/ada-url/ada/).

## Synopsis

```lua
local ada = require("resty.ada")

local url = assert(ada.parse("https://www.7‑Eleven.com:1234/Home/../Privacy/Montréal"))

print(tostring(url))
-- prints: https://www.xn--7eleven-506c.com:1234/Privacy/Montr%C3%A9al

print(tostring(url:clear_port())) -- there are many more methods
-- prints: https://www.xn--7eleven-506c.com/Privacy/Montr%C3%A9al

url:free()
-- explicitly frees the memory without waiting for the garbage collector

-- There is also a static API

print(ada.get_href("https://www.7‑Eleven.com:1234/Home/../Privacy/Montréal"))
-- prints: https://www.xn--7eleven-506c.com:1234/Privacy/Montr%C3%A9al

print(ada.clear_port("https://www.7‑Eleven.com:1234/Home/../Privacy/Montréal"))
-- prints: https://www.xn--7eleven-506c.com/Privacy/Montr%C3%A9al
```


## API

LDoc generated API docs can be viewed at [bungle.github.io/lua-resty-ada](https://bungle.github.io/lua-resty-ada/).


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-ada](https://github.com/bungle/lua-resty-ada){target=_blank}.