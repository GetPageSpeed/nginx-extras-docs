---

title: "Consul Events HTTP API Wrapper"
description: "RPM package lua-resty-consul-event: Consul Events HTTP API Wrapper"

---
  
# *consul-event*: Consul Events HTTP API Wrapper


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-consul-event
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-consul-event
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-consul-event [v0.3.0](https://github.com/Kong/lua-resty-consul-event/releases/tag/0.3.0){target=_blank} 
released on Jun 17 2019.
    
<hr />

Consul Events HTTP API Wrapper

## Overview

This module provides an OpenResty client wrapper for the [Consul Events API](https://www.consul.io/api/event.html). This allows for OpenResty integration with Consul's custom user event mechanism, which can be used to build scripting infrastructure to do automated deploys, restart services, or perform any other orchestration action.

This module leverages Consul's concept of [blocking queries](https://www.consul.io/api/index.html#blocking-queries) to watch for events broadcast on a given event name.

## Synopsis

```lua
local event = require "resty.consul.event"

local e, err = event.new({
  host = "127.0.0.1",
  port = 8500,
})

if err then
  ngx.log(ngx.ERR, err)
end

e:watch("foo", function(event)
  ngx.log(ngx.INFO, "i got ", ngx.decode_base64(event.payload))
end)
```

## Usage

## new

`syntax: e, err = event.new(opts?)`

Instantiates a new watch object. `opts` may be a table with the following options: 

 * `host`: String defining the Consul host
 * `port`: Number defining the Consul port
 * `timeout`: Number, in seconds, to pass to Consul blocking query API via the `wait` parameter. This value is also used to to define TCP layer timeouts, which are set higher than the application-layer timeout.
 * `ssl_verify`: Boolean defining whether to validate the TLS certificate presented by the remote Consul server.
 * `token`: String defining the Consul ACL token to send via the `X-Consul-Token` request header.

## watch

`syntax: e:watch(name, callback, initial_index, seen_ids)`

Watch the Consul events API for events broadcast under a given `name`, and execute the function `callback` . `callback` is passed a single parameter `event`, which contains the body of a single event as defined by the [Consul Events API](https://www.consul.io/api/event.html). Callback functions are wrapped in `pcall`, so it is safe to throw an error from within this function. Callback functions may return a single value but this value is largely meaningless; currently, this single value is logged as a debug entry.

The values `initial_index` and `seen_ids` are optional, and can be used to initialize the watch against a certain state in the Consul events ring. `initial_index` is expected to be a string output by a previous `X-Consul-Index` header. `seen_ids` is expected to be a list of Consul Event ID values for whom callback events should not be executed. For example, the current state of the event buffer can be used to initialize a given watch:

```lua
local h = require("resty.http").new()

-- get the current events
local res, err = h:request_uri("http://127.0.0.1:8500/v1/event/list?name=foo")
if err then
  ngx.log(ngx.ERR, err)
end

local event = require "resty.consul.event"

local e, err = event.new({
  host = "127.0.0.1",
  port = 8500,
})
if err then
  ngx.log(ngx.ERR, err)
end

local l = {}

for _, e in ipairs(require("cjson").decode(res.body)) do
  table.insert(l, e.ID)
end

ngx.timer.at(0, function()
  e:watch(
    "foo",
    function(p) ngx.log(ngx.DEBUG, p.payload) end,
    res.headers["X-Consul-Index"],
    l
  )
end)
```

*Note: This body of this function runs in an infinite loop in order to watch the Consul events API indefinitely. As a result, it is strongly recommended to call this function inside a background timer generated via ngx.timer.at*

## Testing

A test suite for this repo is provided. Tests are written using [Test::Nginx](https://metacpan.org/pod/Test::Nginx::Socket) and executed with `prove`.

To best test library behavior, the suite expects a Consul server to be running and accessible. By default, Consul is accessed at `127.0.0.1:8500`; the Consul host and port can be overriden by defining the environmental variables `TEST_NGINX_CONSUL_ADDR` and `TEST_NGINX_CONSUL_PORT`, respectively.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-consul-event](https://github.com/Kong/lua-resty-consul-event){target=_blank}.