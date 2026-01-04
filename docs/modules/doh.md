---

title: "NGINX module for serving DNS-over-HTTPS (DOH) requests"
description: "RPM package nginx-module-doh. Simple NGINX module for serving DNS-over-HTTPS (DOH) requests.  CAVEAT EMPTOR: This module is experimental, even though I have been using it successfully with both Firefox and Curl, there may be undiscovered bugs. Zone transfer is currently not officially supported."

---

# *doh*: NGINX module for serving DNS-over-HTTPS (DOH) requests


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
    dnf -y install nginx-module-doh
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-doh
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_doh_module.so;
```


This document describes nginx-module-doh [v0.1](https://github.com/dvershinin/Nginx-DOH-Module/releases/tag/0.1){target=_blank} 
released on Jan 15 2020.

<hr />
Simple Nginx module for serving DNS-over-HTTPS (DOH) requests.

CAVEAT EMPTOR: This module is experimental, even though I have been using it successfully with both Firefox and Curl, there may be undiscovered bugs. Zone transfer is currently not officially supported.

Tested with Nginx versions:
1.16.1 (stable)
1.17.6
1.17.7 (mainline).

Instructions for building installing and using Nginx modules can be found at the links below.

dynamic: https://www.nginx.com/resources/wiki/extending/converting/#compiling-dynamic

static: https://www.nginx.com/resources/wiki/extending/compiling/

I have included a config file for both building as both a dynamic and static module.

This module is only allowed to be used in an http location block.

MODULE DIRECTIVES

doh: (takes no arguments) enable DOH at this location block, default upstream DNS server address is 127.0.0.1, default port is 53, and default timeout is 5 seconds.

doh_address: (takes 1 argument) sets the address of the upstream DNS server, can be either IPv4 or IPv6.

doh_port: (takes 1 argument) sets the port to contact the upstream DNS server on (appies to both TCP and UDP connections).

doh_timeout: (takes 1 argument) sets the timeout in seconds.

EXAMPLES

simplest use case with upstream DNS server listening on 127.0.0.1 on port 53:

```nginx
location /dns-query { 
	doh;
}
```

set an upstream address of 127.0.2.1, a port of 5353, and a timeout of 2 seconds:

```nginx
location /dns-query { 
	doh;
	doh_address 127.0.2.1;
	doh_port 5353;
	doh_timeout 2;
}
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-doh](https://github.com/dvershinin/Nginx-DOH-Module){target=_blank}.