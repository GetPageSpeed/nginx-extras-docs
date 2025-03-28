---

title: "Utility functions for working with IP addresses in nginx-module-lua"
description: "RPM package lua-resty-iputils: Utility functions for working with IP addresses in nginx-module-lua"

---
  
# *iputils*: Utility functions for working with IP addresses in nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-iputils
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-iputils
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-iputils [v0.3.0](https://github.com/hamishforbes/lua-resty-iputils/releases/tag/v0.3.0){target=_blank} 
released on Mar 28 2017.
    
<hr />

Collection of utility functions for working with IP addresses.

## Overview

```
init_by_lua_block {
  local iputils = require("resty.iputils")
  iputils.enable_lrucache()
  local whitelist_ips = {
      "127.0.0.1",
      "10.10.10.0/24",
      "192.168.0.0/16",
  }

  -- WARNING: Global variable, recommend this is cached at the module level
  -- https://github.com/openresty/lua-nginx-module#data-sharing-within-an-nginx-worker
  whitelist = iputils.parse_cidrs(whitelist_ips)
}

access_by_lua_block {
    local iputils = require("resty.iputils")
    if not iputils.ip_in_cidrs(ngx.var.remote_addr, whitelist) then
      return ngx.exit(ngx.HTTP_FORBIDDEN)
    end
}
```

## Methods
### enable_lrucache
`syntax: ok, err = iputils.enable_lrucache(size?)`

Creates a global lrucache object for caching ip2bin lookups.

Size is optional and defaults to 4000 entries (~1MB per worker)

Calling this repeatedly will reset the cache

### ip2bin
`syntax: bin_ip, bin_octets = iputils.ip2bin(ip)`

Returns the binary representation of an IPv4 address and a table containing the binary representation of each octet

Returns `nil` and and error message for bad IPs

### parse_cidr
`syntax: lower, upper = iputils.parse_cidr(cidr)`

Returns a binary representation of the lowest (network) and highest (broadcast) addresses of an IPv4 network.

### parse_cidrs
`syntax: parsed = iputils.parse_cidrs(cidrs)`

Takes a table of CIDR format IPV4 networks and returns a table of tables containg the lower and upper addresses.

If an invalid network is in the table an error is logged and the other networks are returned

### ip_in_cidrs
`syntax: bool, err = iputils.ip_in_cidrs(ip, cidrs)`

Takes a string IPv4 address and a table of parsed CIDRs (e.g. from `iputils.parse_cidrs`).

Returns a `true` or `false` if the IP exists within *any* of the specified networks.

Returns `nil` and an error message with an invalid IP

### binip_in_cidrs
`syntax: bool, err = iputils.binip_in_cidrs(bin_ip, cidrs)`

Takes a nginx binary IPv4 address (e.g. `ngx.var.binary_remote_addr`) and a table of parsed CIDRs (e.g. from `iputils.parse_cidrs`).

This method is much faster than `ip_in_cidrs()` if the IP being checked is already available as a binary representation.

Returns a `true` or `false` if the IP exists within *any* of the specified networks.

Returns `nil` and an error message with an invalid IP

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-iputils](https://github.com/hamishforbes/lua-resty-iputils){target=_blank}.