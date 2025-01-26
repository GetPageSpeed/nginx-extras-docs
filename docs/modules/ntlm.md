---

title: "NTLM NGINX Module"
description: "RPM package nginx-module-ntlm. NGINX NTLM module allows proxying requests with NTLM Authentication "

---

# *ntlm*: NTLM NGINX Module


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
    dnf -y install nginx-module-ntlm
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-ntlm
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_upstream_ntlm_module.so;
```


This document describes nginx-module-ntlm [v1.19.4](https://github.com/dvershinin/nginx-ntlm-module/releases/tag/v1.19.4){target=_blank} 
released on May 04 2024.

<hr />

The NTLM module allows proxying requests with [NTLM Authentication](https://en.wikipedia.org/wiki/Integrated_Windows_Authentication). The upstream connection is bound to the client connection once the client sends a request with the "Authorization" header field value starting with "Negotiate" or "NTLM". Further client requests will be proxied through the same upstream connection, keeping the authentication context.

## How to use

> Syntax:  ntlm [connections];  
> Default: ntlm 100;  
> Context: upstream 


```nginx
upstream http_backend {
    server 127.0.0.1:8080;

    ntlm;
}

server {
    ...

    location /http/ {
        proxy_pass http://http_backend;
        # next 2 settings are required for the keepalive to work properly
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

The connections parameter sets the maximum number of connections to the upstream servers that are preserved in the cache.

> Syntax:  ntlm_timeout timeout;  
> Default: ntlm_timeout 60s;  
> Context: upstream  

Sets the timeout during which an idle connection to an upstream server will stay open.

## Tests

In order to run the tests you need nodejs and perl installed on your system

```bash
## install the backend packages
npm install -C t/backend

## instal the test framework
cpan Test::Nginx

## set the path to your nginx location
export PATH=/opt/local/nginx/sbin:$PATH

prove -r t
```


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-ntlm](https://github.com/dvershinin/nginx-ntlm-module){target=_blank}.