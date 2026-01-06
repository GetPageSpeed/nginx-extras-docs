---

title: "High-performance WAF built on nginx-module-lua stack"
description: "RPM package lua-resty-waf: High-performance WAF built on nginx-module-lua stack"

---
  
# *waf*: High-performance WAF built on nginx-module-lua stack


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-waf
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-waf
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-waf [v0.11.1](https://github.com/p0pr0ck5/lua-resty-waf/releases/tag/v0.11.1){target=_blank} 
released on May 09 2017.
    
<hr />

lua-resty-waf is a reverse proxy WAF built using the OpenResty stack. It uses the Nginx Lua API to analyze HTTP request information and process against a flexible rule structure. lua-resty-waf is distributed with a ruleset that mimics the ModSecurity CRS, as well as a few custom rules built during initial development and testing, and a small virtual patchset for emerging threats. Additionally, lua-resty-waf is distributed with tooling to automatically translate existing ModSecurity rules, allowing users to extend lua-resty-waf implementation without the need to learn a new rule syntax.

lua-resty-waf was initially developed by Robert Paprocki for his Master's thesis at Western Governor's University.

## ./configure --with-pcre=/path/to/pcre/source --with-pcre-jit
```

You can download the PCRE source from the [PCRE website](http://www.pcre.org/). See also this [blog post](https://www.cryptobells.com/building-openresty-with-pcre-jit/) for a step-by-step walkthrough on building OpenResty with a JIT-enabled PCRE library.

## Performance

lua-resty-waf was designed with efficiency and scalability in mind. It leverages Nginx's asynchronous processing model and an efficient design to process each transaction as quickly as possible. Load testing has show that deployments implementing all provided rulesets, which are designed to mimic the logic behind the ModSecurity CRS, process transactions in roughly 300-500 microseconds per request; this equals the performance advertised by [Cloudflare's WAF](https://www.cloudflare.com/waf). Tests were run on a reasonable hardware stack (E3-1230 CPU, 32 GB RAM, 2 x 840 EVO in RAID 0), maxing at roughly 15,000 requests per second. See [this blog post](http://www.cryptobells.com/freewaf-a-high-performance-scalable-open-web-firewall) for more information.

lua-resty-waf workload is almost exclusively CPU bound. Memory footprint in the Lua VM (excluding persistent storage backed by `lua-shared-dict`) is roughly 2MB.

## make && sudo make install
```

Alternatively, install via Luarocks:

```
### process_multipart_body

*Default* true

Enable processing of multipart/form-data request bodies (when present), using the `lua-resty-upload` module. In the future, lua-resty-waf may use this processing to perform stricter checking of upload bodies; for now this module performs only minimal sanity checks on the request body, and will not log an event if the request body is invalid. Disable this option if you do not need this checking, or if bugs in the upstream module are causing problems with HTTP uploads.

*Example*:

```lua
location / {
    access_by_lua_block {
        -- disable processing of multipart/form-data requests
        -- note that the request body will still be sent to the upstream
        waf:set_option("process_multipart_body", false)
    }
}
```

### req_tid_header

*Default*: false

Set an HTTP header `X-Lua-Resty-WAF-ID` in the upstream request, with the value as the transaction ID. This ID will correlate with the transaction ID present in the debug logs (if set). This can be useful for request tracking or debug purposes.

*Example*:

```lua
location / {
    access_by_lua_block {
        waf:set_option("req_tid_header", true)
    }
}
```

### res_body_max_size

*Default*: 1048576 (1 MB)

Defines the content length threshold beyond which response bodies will not be processed. This size of the response body is determined by the Content-Length response header. If this header does not exist in the response, the response body will never be processed.

*Example*:

```lua
location / {
    access_by_lua_block {
        -- increase the max response size to 2 MB
        waf:set_option("res_body_max_size", 1024 * 1024 * 2)
    }
}
```
Note that by nature, it is required to buffer the entire response body in order to properly use the response as a collection, so increasing this number significantly is not recommended without justification (and ample server resources).

### res_body_mime_types

*Default*: "text/plain", "text/html"

Defines the MIME types with which lua-resty-waf will process the response body. This value is determined by the Content-Type header. If this header does not exist, or the response type is not in this list, the response body will not be processed. Setting this option will add the given MIME type to the existing defaults of `text/plain` and `text/html`.

*Example*:

```lua
location / {
    access_by_lua_block {
        -- mime types that will be processed are now text/plain, text/html, and text/json
        waf:set_option("res_body_mime_types", "text/json")
    }
}
```

Multiple MIME types can be added by passing a table of types to `set_option`.

### res_tid_header

*Default*: false

Set an HTTP header `X-Lua-Resty-WAF-ID` in the downstream response, with the value as the transaction ID. This ID will correlate with the transaction ID present in the debug logs (if set). This can be useful for request tracking or debug purposes.

*Example*:

```lua
location / {
    access_by_lua_block {
        waf:set_option("res_tid_header", true)
    }
}
```

### score_threshold

*Default*: 5

Sets the threshold for anomaly scoring. When the threshold is reached, lua-resty-waf will deny the request.

*Example*:

```lua
location / {
    access_by_lua_block {
        waf:set_option("score_threshold", 10)
    }
}
```

### storage_backend

*Default*: dict

Define an engine to use for persistent variable storage. Current available options are *dict* (ngx_lua shared memory zone), *memcached*, amd *redis*.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_backend", "memcached")
    }
}
```

### storage_keepalive

*Default*: true

Enable or disable TCP keepalive for connections to remote persistent storage hosts.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_keepalive", false)
    }
}
```

### storage_keepalive_timeout

*Default*: 10000

Configure (in milliseconds) the timeout for the cosocket keepalive pool for remote persistent storage hosts.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_keepalive_timeout", 30000)
    }
}
```

### storage_keepalive_pool_size

*Default*: 100

Configure the pool size for the cosocket keepalive pool for remote persistent storage hosts.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_keepalive_pool_size", 50)
    }
}
```

### storage_memcached_host

*Default*: 127.0.0.1

Define a host to use when using memcached as a persistent variable storage engine.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_memcached_host", "10.10.10.10")
    }
}
```

### storage_memcached_port

*Default*: 11211

Define a port to use when using memcached as a persistent variable storage engine.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_memcached_port", 11221)
    }
}
```

### storage_redis_host

*Default*: 127.0.0.1

Define a host to use when using redis as a persistent variable storage engine.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_redis_host", "10.10.10.10")
    }
}
```

### storage_redis_port

*Default*: 6379

Define a port to use when using redis as a persistent variable storage engine.

*Example*:

```lua
location / {
    acccess_by_lua_block {
        waf:set_option("storage_redis_port", 6397)
    }
}
```

### storage_zone

*Default*: none

Defines the `lua_shared_dict` that will be used to hold persistent storage data. This zone must be defined in the `http{}` block of the configuration.

*Example*:_

```lua
http {
    -- define a 64M shared memory zone to hold persistent storage data
    lua_shared_dict persistent_storage 64m;
}

location / {
    access_by_lua_block {
        waf:set_option("storage_zone", "persistent_storage")
    }
}
```

Multiple shared zones can be defined and used, though only one zone can be defined per configuration location. If a zone becomes full and the shared dictionary interface cannot add additional keys, the following will be entered into the error log:

`Error adding key to persistent storage, increase the size of the lua_shared_dict`

## Phase Handling

lua-resty-waf is designed to run in multiple phases of the request lifecycle. Rules can be processed in the following phases:

* **access**: Request information, such as URI, request headers, URI args, and request body are available in this phase.
* **header_filter**: Response headers and HTTP status are available in this phase.
* **body_filter**: Response body is available in this phase.
* **log**: Event logs are automatically written at the completion of this phase.

These phases correspond to their appropriate Nginx lua handlers (`access_by_lua`, `header_filter_by_lua`, `body_filter_by_lua`, and `log_by_lua`, respectively). Note that running lua-resty-waf in a lua phase handler not in this list will lead to broken behavior. All data available in an earlier phase is available in a later phase. That is, data available in the `access` phase is also available in the `header_filter` and `body_filter` phases, but not vice versa.

## Included Rulesets

lua-resty-waf is distributed with a number of rulesets that are designed to mimic the functionality of the ModSecurity CRS. For reference, these rulesets are listed here:

* **11000_whitelist**: Local policy whitelisting
* **20000_http_violation**: HTTP protocol violation
* **21000_http_anomaly**: HTTP protocol anomalies
* **35000_user_agent**: Malicious/suspect user agents
* **40000_generic_attack**: Generic attacks
* **41000_sqli**: SQLi
* **42000_xss**: XSS
* **90000_custom**: Custom rules/virtual patching
* **99000_scoring**: Anomaly score handling

## Rule Definitions

lua-resty-waf parses rules definitions from JSON blobs stored on-disk. Rules are grouped based on purpose and severity, defined as a ruleset. The included rulesets were created to mimic some functionality of the ModSecurity CRS, particularly the `base_rules` definitions. Additionally, the included `modsec2lua-resty-waf.pl` script can be used to translate additional or custom rulesets to a lua-resty-waf-compatible JSON blob.

Note that there are several limitations in the translation script, with respect to unsupported actions, collections, and operators. Please see [this wiki page](https://github.com/p0pr0ck5/lua-resty-waf/wiki/Known-ModSecurity-Translation-Limitations) for an up-to-date list of known incompatibilities.

## Notes

### Pull Requests

Please target all pull requests towards the development branch, or a feature branch if the PR is a significant change. Commits to master should only come in the form of documentation updates or other changes that have no impact of the module itself (and can be cleanly merged into development).

## Roadmap

* **Expanded virtual patch ruleset**: Increase coverage of emerging threats.
* **Expanded integration/acceptance testing**: Increase coverage of common threats and usage scenarios.
* **Expanded ModSecurity syntax translations**: Support more operators, variables, and actions.
* **Common application profiles**: Tuned rulesets for common CMS/applications.
* **Support multiple socket/file logger targets**: Likely requires forking the lua-resty-logger-socket project.

## Limitations

lua-resty-waf is undergoing continual development and improvement, and as such, may be limited in its functionality and performance. Currently known limitations can be found within the GitHub issue tracker for this repo.

## See Also

- The OpenResty project: <http://openresty.org/>
- My personal blog for updates and notes on lua-resty-waf development: <http://www.cryptobells.com/tag/lua-resty-waf/>

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-waf](https://github.com/p0pr0ck5/lua-resty-waf){target=_blank}.