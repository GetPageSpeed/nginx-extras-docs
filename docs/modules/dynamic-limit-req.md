# *dynamic-limit-req*: NGINX module to dynamically lock IP and release it periodically


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-dynamic-limit-req
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-dynamic-limit-req
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_dynamic_limit_req_module.so;
```


This document describes nginx-module-dynamic-limit-req [v1.9.3](https://github.com/limithit/ngx_dynamic_limit_req_module/releases/tag/1.9.3){target=_blank} 
released on Jan 29 2021.

<hr />
 
## Introduction

The *ngx_dynamic_limit_req_module* module is used to dynamically lock IP and release it periodically.

## principle
The ngx_dynamic_limit_req_module module is used to limit the request processing rate per a defined key, in particular, the processing rate of requests coming from a single IP address. The limitation is done using the “leaky bucket” method.

## About
This module is an extension based on [ngx_http_limit_req_module](http://nginx.org/en/docs/http/ngx_http_limit_req_module.html).

## Donate
The developers work tirelessly to improve and develop ngx_dynamic_limit_req_module. Many hours have been put in to provide the software as it is today, but this is an extremely time-consuming process with no financial reward. If you enjoy using the software, please consider donating to the devs, so they can spend more time implementing improvements.

 ### Alipay:
![Alipay](https://github.com/limithit/shellcode/blob/master/alipay.png)

## Extend
This module can be works with [RedisPushIptables](https://github.com/limithit/RedisPushIptables),  the application layer matches then the network layer to intercept. Although network layer interception will save resources, there are also deficiencies. Assuming that only one specific interface is filtered and no other interfaces are filtered, those that do not need to be filtered will also be inaccessible. Although precise control is not possible at the network layer or the transport layer, it can be precisely controlled at the application layer. Users need to weigh which solution is more suitable for the event at the time.

## Api-count
### If you want to use the api counting function, please use [limithit-API_alerts](https://github.com/limithit/ngx_dynamic_limit_req_module/tree/limithit-API_alerts). Because not everyone needs this feature, so it doesn't merge into the trunk. Users who do not need this feature can skip this paragraph description.

``` 
git clone https://github.com/limithit/ngx_dynamic_limit_req_module.git
cd ngx_dynamic_limit_req_module
git checkout limithit-API_alerts
```
``` 
root@debian:~# redis-cli 
127.0.0.1:6379> SELECT 3
127.0.0.1:6379[3]> scan 0 match *12/Dec/2018* count 10000 
127.0.0.1:6379[3]> scan 0 match *PV count 10000
1) "0"
2) 1) "[13/Dec/2018]PV"
   2) "[12/Dec/2018]PV"
127.0.0.1:6379[3]> get [12/Dec/2018]PV
"9144"
127.0.0.1:6379[3]> get [13/Dec/2018]PV
"8066"
127.0.0.1:6379[3]> get [13/Dec/2018]UV
"214"

```

This module is compatible with following nginx releases:

Author
Gandalf zhibu1991@gmail.com

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-dynamic-limit-req](https://github.com/limithit/ngx_dynamic_limit_req_module){target=_blank}.