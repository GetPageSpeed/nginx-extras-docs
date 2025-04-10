---

title: "Consistent hash for nginx-module-lua"
description: "RPM package lua-resty-jump-consistent-hash: Consistent hash for nginx-module-lua"

---
  
# *jump-consistent-hash*: Consistent hash for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-jump-consistent-hash
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-jump-consistent-hash
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-jump-consistent-hash [v0.1.4](https://github.com/ruoshan/lua-resty-jump-consistent-hash/releases/tag/v0.1.4){target=_blank} 
released on May 09 2016.
    
<hr />
A simple implementation of [this paper](http://arxiv.org/pdf/1406.2294.pdf).

## Features
- small memory footprint and fast
- consistence is maintained through servers' updating

## Usage

* you can use the basic jchash module to do consistent-hash
```
local jchash = require "resty.chash.jchash"

local buckets = 8
local id = jchash.hash_short_str("random key", buckets)
```

* or you can use the wrapping module `resty.chash.server` to consistent-hash a list of servers
```
local jchash_server = require "resty.chash.server"

local my_servers = {
    { "127.0.0.1", 80, 1},   -- {addr, port, weight} weight can be left out if it's 1
    { "127.0.0.2", 80 },
    { "127.0.0.3", 80 }
}

local cs, err = jchash_server.new(my_servers)
local uri = ngx.var.uri
local svr = cs:lookup(uri)
local addr = svr[1]
local port = svr[2]

-- now you can use the ngx.balancer to do some consistent LB

-- you can even update the servers list, and still maintain the consistence, eg.
local my_new_servers = {
    { "127.0.0.2", 80 },
    { "127.0.0.3", 80 },
    { "127.0.0.4", 80 }
}

cs:update_servers(my_new_servers)
svr = cs:lookup(uri)   -- if the server was 127.0.0.2, then it stays the same,
                       -- as we only update the 127.0.0.4.

-- what's more, consistence is maintained even the number of servers changes! eg.
local my_less_servers = {
    { "127.0.0.2", 80 },
    { "127.0.0.3", 80 }
}
cs:update_servers(my_less_servers)
svr = cs:lookup(uri)   -- if the server was 127.0.0.2, then it stays the same,
                       -- if the server was 127.0.0.4, then it has 50% chance to be
                       -- 127.0.0.3 or 127.0.0.4

cs:update_servers(my_new_servers)
svr = cs:lookup(uri)   -- if the server was 127.0.0.2, then it has 66% chance to stay the same

```

## Test

```
make test
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-jump-consistent-hash](https://github.com/ruoshan/lua-resty-jump-consistent-hash){target=_blank}.