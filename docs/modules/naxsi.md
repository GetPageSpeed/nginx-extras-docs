---

title: "NGINX Anti XSS & SQL Injection module"
description: "RPM package nginx-module-naxsi. NAXSI is an open-source, high performance, low rules maintenance WAF for NGINX.  This module, by default, reads a small subset of simple (and readable) rules containing 99% of known patterns involved in website vulnerabilities. For example, <, | or drop are not supposed to be part of a URI.  Being very simple, those patterns may match legitimate queries, it is the Naxsi's administrator duty to add specific rules that will whitelist legitimate behaviours. The administrator can either add whitelists manually by analyzing nginx's error log, or (recommended) start the project with an intensive auto-learning phase that will automatically generate whitelisting rules regarding a website's behaviour.  In short, Naxsi behaves like a DROP-by-default firewall, the only task is to add required ACCEPT rules for the target website to work properly. "

---

# *naxsi*: NGINX Anti XSS & SQL Injection module


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
    dnf -y install nginx-module-naxsi
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-naxsi
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_naxsi_module.so;
```


This document describes nginx-module-naxsi [v1.6](https://github.com/dvershinin/naxsi/releases/tag/1.6){target=_blank} 
released on Nov 28 2023.

<hr />
![naxsi](logo.png)

## What is Naxsi?

NAXSI means [Nginx]( http://nginx.org/ ) Anti [XSS]( https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29 ) & [SQL Injection]( https://www.owasp.org/index.php/SQL_injection ). 

Technically, it is a third party nginx module, available as a package for
many UNIX-like platforms. This module, by default, reads a small subset of
simple (and readable) rules containing 99% of known patterns involved in
website vulnerabilities. For example, `<`, `|` or `drop` are not supposed
to be part of a URI.

Being very simple, those patterns may match legitimate queries, it is
the Naxsi's administrator duty to add specific rules that will whitelist
legitimate behaviours. The administrator can either add whitelists manually
by analyzing nginx's error log, or (recommended) start the project with an
intensive auto-learning phase that will automatically generate whitelisting
rules regarding a website's behaviour.

In short, Naxsi behaves like a DROP-by-default firewall, the only task
is to add required ACCEPT rules for the target website to work properly.

## Why is it different?

Contrary to most Web Application Firewalls, Naxsi doesn't rely on a
signature base like an antivirus, and thus cannot be circumvented by an
"unknown" attack pattern.
Naxsi is [Free software]( https://www.gnu.org/licenses/gpl.html ) (as in freedom)
and free (as in free beer) to use.

## What does it run on?
Naxsi should be compatible with any nginx version.

It depends on `libpcre` for its regexp support, and is reported to work great on NetBSD, FreeBSD, OpenBSD, Debian, Ubuntu and CentOS.

## Why using this repository

*The original project is (unofficially) abandoned*, but you can fully ask for support here as i'm willing to keep the project working as last remaining developer.

## Documentation

[docs](docs/index)

## Support

You can ask for support regarding NAXSI here or on the original repository https://github.com/nbs-system/naxsi

## Future plans

- Bring back nxapi via py3
- Creation of a simple tool to create rules and test them

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-naxsi](https://github.com/dvershinin/naxsi){target=_blank}.