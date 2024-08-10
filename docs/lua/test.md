# *test*: Lua test frame for nginx-module-lua based on nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-test
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-test
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-test [v0.1](https://github.com/iresty/lua-resty-test/releases/tag/v0.1){target=_blank} 
released on Sep 03 2019.
    
<hr />
lua-resty-test is Ngx_lua test frame based on Openresty


## Description
This Lua library is a test frame for test your ngx_lua source or other server(tcp or udp):

http://wiki.nginx.org/HttpLuaModule

## Synopsis


```lua
-- test.lua
local iresty_test    = require "resty.iresty_test"
local tb = iresty_test.new({unit_name="example"})

function tb:init(  )
    self:log("init complete")
end

function tb:test_00001(  )
    error("invalid input")
end

function tb:atest_00002()
    self:log("never be called")
end

function tb:test_00003(  )
    self:log("ok")
end

-- units test
tb:run()
```

Run test case:

<img src="./images/run-test-result.png" width="50%" height="50%">

## See Also

* the ngx_lua module: http://wiki.nginx.org/HttpLuaModule

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-test](https://github.com/iresty/lua-resty-test){target=_blank}.