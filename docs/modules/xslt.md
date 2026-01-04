---

title: "NGINX XSLT dynamic module"
description: "RPM package nginx-module-xslt. NGINX XSLT dynamic module. This filter module transforms XML responses using one or more XSLT stylesheets."

---

# *xslt*: NGINX XSLT dynamic module


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
    dnf -y install nginx-module-xslt
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-xslt
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_xslt_filter_module.so;
```


This module is built from the same source as the NGINX core.

<hr />


## Directives

You may find information about configuration directives for this module at the following links:        

*   https://nginx.org/en/docs/http/ngx_http_xslt_module.html#directives