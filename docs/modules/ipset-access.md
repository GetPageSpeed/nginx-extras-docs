---

title: "NGINX ipset access module"
description: "RPM package nginx-module-ipset-access. NGINX module to control user access to sites using ipset "

---

# *ipset-access*: NGINX ipset access module


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
    dnf -y install nginx-module-ipset-access
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-ipset-access
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_ipset_access.so;
```


This document describes nginx-module-ipset-access [v1.0.3](https://github.com/GetPageSpeed/nginx_ipset_access_module/releases/tag/v1.0.3){target=_blank} 
released on Feb 21 2025.

<hr />
== ngx_http_ipset_access

An nginx module for using netfilter ipsets as a black/white list.
In comparison to standard nginx access module this allows for dynamic list updating, without nginx reload/restart.

== Installation

* Get youself a linux server with root access
* Get nginx source code, unpack etc.
* Install libipset, libssl-dev, pcre and other nginx requirements
* Configure nginx with this module:
    ./configure --add-module=/path/to/ngx_http_ipset_access
* Compile, install
* Create yout ipset and add some 'offending' ips to it:
    sudo ipset -N myblacklist iphash
    sudo ipset -A myblacklist 127.0.0.1
* Start nginx
* Profit!

== Installation as dynamic module

Alternatively, you can compile a dynamic module for nginx with:
    ./configure --add-dynamic-module=/path/to/ngx_http_ipset_access --with-compat

After compilation, locate `objs/ngx_http_ipset_access.so`.

To load the compiled module into nginx, add the following at the top of nginx.conf:
    load_module /path/to/ngx_http_ipset_access.so;

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-ipset-access](https://github.com/GetPageSpeed/nginx_ipset_access_module){target=_blank}.