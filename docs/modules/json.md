---

title: "NGINX JSON module"
description: "RPM package nginx-module-json. Dumps json variable $json into string variable $string"

---

# *[BETA!] json*: NGINX JSON module


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
    dnf -y install nginx-module-json
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-json
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_json_module.so;
```


This document describes nginx-module-json [v0](https://github.com/dvershinin/ngx_http_json_module/releases/tag/v0){target=_blank} 
released on Dec 16 2023.

Production stability is *not guaranteed*.
<hr />

### Directives:

    Syntax:	 json_load $json string;
    Default: ——
    Context: http, server, location

Loads string (may contains variables) into (json) variable $json.

    Syntax:	 json_dump $string $json [name ...];
    Default: ——
    Context: http, server, location

Dumps (json) variable $json into (string) variable $string (may point path by names).

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-json](https://github.com/dvershinin/ngx_http_json_module){target=_blank}.