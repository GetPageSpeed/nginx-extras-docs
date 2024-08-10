# *injection*: LuaJIT FFI bindings to libinjection (https://github.com/client9/libinjection)


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-injection
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-injection
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-injection [v1.0](https://github.com/bungle/lua-resty-injection/releases/tag/v1.0){target=_blank} 
released on Sep 15 2016.
    
<hr />

LuaJIT FFI bindings to libinjection (https://github.com/client9/libinjection) — SQL / SQLI / XSS tokenizer parser analyzer.

## Synopsis

```lua
local injection = require "resty.injection"

-- Print version of libinjection
print(injection.version)

-- Testing SQL injection detection
print(injection.sql("test; DROP users;"))
print(injection.sql("test"))
print(injection.sql("test<script></script>"))

-- Testing Cross-Site Scripting injection detection
print(injection.xss("test; DROP users;"))
print(injection.xss("test"))
print(injection.xss("test<script></script>"))
```

The above would output something similar to this:

```
3.9.1
true	n;Tn;
false
false
false
false
true
```

*The second line contains fingerprint of the injection.*

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-injection](https://github.com/bungle/lua-resty-injection){target=_blank}.