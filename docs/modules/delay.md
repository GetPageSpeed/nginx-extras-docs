---

title: "Delay requests for a given time"
description: "RPM package nginx-module-delay. The delay module allows to delay requests for a given time. This is useful for testing, rate limiting simulation, or implementing artificial latency for specific endpoints. Based on work by Maxim Dounin."

---

# *delay*: Delay requests for a given time


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
    dnf -y install nginx-module-delay
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-delay
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_delay_module.so;
```


This document describes nginx-module-delay [v0.1.0](https://github.com/dvershinin/ngx_http_delay_module/releases/tag/0.1.0){target=_blank} 
released on Jan 06 2026.

<hr />
Delay module for nginx.

This module allows to delay requests for a given time.

Configuration directives:

    delay <time>

        Context: http, server, location
        Default: 0

        Delay requests for a given time.

Usage:

    location = /slow {
        delay 10s;
        ...
    }

Note that internal redirects (e.g. directory index ones) will trigger another
delay.

To compile nginx with delay module, use "--add-module <path>" option
to nginx configure.

Development of this module was sponsored by Openstat (http://www.openstat.com/).

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-delay](https://github.com/dvershinin/ngx_http_delay_module){target=_blank}.