---

title: "NGINX HTTP rDNS module"
description: "RPM package nginx-module-rdns. This module allows to make a reverse DNS (rDNS) lookup for incoming connection and provides simple access control of incoming hostname by allow/deny rules (similar to HttpAccessModule allow/deny directives; regular expressions are supported).  Module works with the DNS server defined by the standard resolver directive. This module uses nginx core resolver cache when resolving DNS lookup, for a maximum of 30 seconds or DNS response TTL. "

---

# *[BETA!] rdns*: NGINX HTTP rDNS module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9 and 10
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023+"

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-rdns
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-rdns
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_rdns_module.so;
```


This document describes nginx-module-rdns [v0](https://github.com/dvershinin/nginx-http-rdns/releases/tag/v0){target=_blank} 
released on Jun 08 2020.

Production stability is *not guaranteed*.
<hr />

## Summary

This module allows to make a reverse DNS (rDNS) lookup for incoming
connection and provides simple access control of incoming hostname
by allow/deny rules (similar to HttpAccessModule allow/deny
directives; regular expressions are supported). Module works with
the DNS server defined by the standard resolver directive.
This module uses nginx core resolver cache when resolving DNS lookup,
for a maximum of 30 seconds or DNS response TTL.

## Example

    location / {
        resolver 127.0.0.1;

        rdns_deny badone\.example\.com;

        if ($http_user_agent ~* FooAgent) {
            rdns on;
        }

        if ($rdns_hostname ~* (foo\.example\.com)) {
            set $myvar foo;
        }

        #...
    }

In the example above, nginx will make a reverse DNS request (through
the 127.0.0.1 DNS server) for each request having the "FooAgent"
user agent. Requests from badone.example.com will be forbidden.
The $rdns_hostname variable will have the rDNS request result or
"not found" (in case it's not found or any error occured) for any
requests made by FooAgent. For other user agents, $rdns_hostname
will have a special value "-".


## Directives

### rdns

* Syntax: rdns on | off | double
* Default: -
* Context: http, server, location, if-in-server, if-in-location
* Phase: rewrite
* Variables: rdns_hostname

Enables/disables rDNS lookups.

* on     - enable rDNS lookup in this context.
* double - enable double DNS lookup in this context. If the reverse
           lookup (rDNS request) succeeded, module performs a forward
           lookup (DNS request) for its result. If this forward
           lookup has failed or none of the forward lookup IP
           addresses have matched the original address,
           $rdns_hostname is set to "not found".
* off    - disable rDNS lookup in this context.

The $rdns_hostname variable may have:

* result of lookup;
* special value "not found" if not found or error occurred during
  request;
* special value "-" if lookup disabled.

After performing a lookup, module restarts request handling pipeline
to make new $rdns_hostname variable value visible to other directives.

Notice on server/location "if":

Internally, in server's or location's "if", module works through
rewrite module codes. When any enabling directive (rdns on|double) is
executed for the first time, it enables DNS lookup and makes a break
(to prevent executing further directives in this "if"). After the
lookup is done, directives in "if" using rewrite module codes are
executed for the second time, without any breaks. Disabling directive
(rdns off) makes no breaks.

Core module resolver should be defined to use this directive.


### rdns_allow

* Syntax: rdns_allow regex
* Default: -
* Context: http, server, location
* Phase: access
* Variables: -

Grants access for domain matched by regular expression.


### rdns_deny

* Syntax: rdns_deny regex
* Default: -
* Context: http, server, location
* Phase: access
* Variables: -

Forbids access for domain matched by regular expression.


## Notice on access lists

The rdns_allow and rdns_deny directives define a new access list for
the context in which they are used.

Access list inheritance in contexts works only if child context
doesn't define own rules.


## Warning on named locations

Making rDNS requests in named locations isn't supported and may
invoke a loop. For example:

    server {
        rdns on;

        location / {
            echo_exec @foo;
        }

        location @foo {
            #...
        }
    }

Being in a named location and restarting request handling pipeline,
nginx continue its request handling in usual (unnamed) location.
That's why this example will make a loop if you don't disable the
module in your named location. The correct config for this example
should be as follows:

    server {
        rdns on;

        location / {
            echo_exec @foo;
        }

        location @foo {
            rdns off;
            #...
        }
    }


## Links

* The source code on GitHub:
  https://github.com/flant/nginx-http-rdns
* The module homepage (in Russian):
  http://flant.ru/projects/nginx-http-rdns

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-rdns](https://github.com/dvershinin/nginx-http-rdns){target=_blank}.