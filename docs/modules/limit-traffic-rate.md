---

title: "NGINX Limiting rate by given variables"
description: "RPM package nginx-module-limit-traffic-rate. NGINX Limiting rate by given variables. "

---

# *limit-traffic-rate*: NGINX Limiting rate by given variables


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
    dnf -y install nginx-module-limit-traffic-rate
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-limit-traffic-rate
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_limit_traffic_rate_filter_module.so;
```


This document describes nginx-module-limit-traffic-rate [v1.0.0](https://github.com/dvershinin/ngx_http_limit_traffic_ratefilter_module/releases/tag/v1.0.0){target=_blank} 
released on Dec 30 2024.

<hr />

## Notes

Nginx directive `limit_rate` could limit connection's speed, and `limit_conn` could limit connection number by given variable. If the client is a browser, it only open one connection to the server. The speed will be limited to `limit_rate`, unless the client is a multi-thread download tool.

`ngx_http_limit_traffic_ratefilter_module` provides a method to limit the total download rate by client IP or download URL, even there are several connections. The limit condition could be defined by the following directive.

To install, compile nginx with this ./configure option:

    --add-module=path/to/this/directory

The limit_traffic_rate module need to use a share memory pool.

## Directive syntax is same to limit_zone

```nginx
http {
    #limit_traffic_rate_zone   rate $request_uri 32m;
    limit_traffic_rate_zone   rate $remote_addr 32m;

    server {
        location /download/ {
            limit_traffic_rate  rate 20k;
        }
    }
}
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-limit-traffic-rate](https://github.com/dvershinin/ngx_http_limit_traffic_ratefilter_module){target=_blank}.