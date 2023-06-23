# *perf*: A small ngx resty lua library to benchmark memory and throughput of a function


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-perf
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-perf
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-perf [v1.0.4](https://github.com/leandromoreira/lua-resty-perf/releases/tag/1.0.4){target=_blank} 
released on Apr 14 2021.
    
<hr />

A simple resty lua library to benchmark memory and throughput of a function.

```lua
local function mycode()
  local x = {}
  for i = 1, 1e3 do
    local now = ngx.now()
    now = now - 45 + i
    x[i] = now
  end
  return x
end

perf.perf_time("mycode cpu profiling", function()
   mycode()
end)

perf.perf_mem("mycode memory profiling", function()
   mycode()
end)
```
To run it, you can use the openresty docker image:

```bash
docker run -it --rm -v ${PWD}/test.lua:/test.lua -v ${PWD}/lib/resty/perf.lua:/lib/resty/perf.lua openresty/openresty:xenial resty /test.lua
```

![perf command line result](example.jpg "A graph with experiments results")

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-perf](https://github.com/leandromoreira/lua-resty-perf){target=_blank}.