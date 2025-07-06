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

lua-resty-waf - High-performance WAF built on the OpenResty stack

## Status

[![Codewake](https://www.codewake.com/badges/ask_question.svg)](https://www.codewake.com/p/lua-resty-waf)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/761/badge)](https://bestpractices.coreinfrastructure.org/projects/761)

lua-resty-waf is currently in active development. New bugs and questions opened in the issue tracker will be answered within a day or two, and performance impacting / security related issues will be patched with high priority. Larger feature sets and enhancements will be added when development resources are available (see the [Roadmap](#roadmap) section for an outline of planned features).

lua-resty-waf is compatible with the master branch of `lua-resty-core`. The bundled version of `lua-resty-core` available in recent releases of OpenResty (>= 1.9.7.4) is compatible with lua-resty-waf; versions bundled with older OpenResty bundles are not, so users wanting to leverage `resty.core` will either need to replace the local version with the one available from the [GitHub project](https://github.com/openresty/lua-resty-core), or patch the module based off [this commit](https://github.com/openresty/lua-resty-core/commit/40445b12c0359eb82702f0097cd65948c245b6a4).

## Description

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