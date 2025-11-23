---

title: "NGINX pipelog module"
description: "RPM package nginx-module-pipelog. An NGINX module for sending HTTP access logs to an external program via pipe. "

---

# *pipelog*: NGINX pipelog module


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
    dnf -y install nginx-module-pipelog
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-pipelog
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_pipelog_module.so;
```


This document describes nginx-module-pipelog [v1.0.4](https://github.com/pandax381/ngx_http_pipelog_module/releases/tag/v1.0.4){target=_blank} 
released on Dec 19 2022.

<hr />

This module allows to send HTTP access log to an external program via pipe.

## Directives

***pipelog_format***
  
    pipelog_format name [escape=default|json|none] string ...

  * syntax is same as log_format of HttpLogModule.
  * default value is *combined*.

***pipelog***

    pipelog command [format [nonblocking] [if=condition]];
 
    pipelog off;
    
  * default value is *off*.
  * command does not need the pipe symbol `|` prefix.

## Example

      pipelog_format main '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
      
      pipelog "cat >> /var/log/nginx/access.log" main;

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-pipelog](https://github.com/pandax381/ngx_http_pipelog_module){target=_blank}.