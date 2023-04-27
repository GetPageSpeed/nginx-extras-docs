# *stream-sts*: Nginx stream server traffic status core module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-stream-sts
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_stream_server_traffic_status_module.so;
```


This document describes nginx-module-stream-sts [v0.1.1](https://github.com/vozlt/nginx-module-stream-sts/releases/tag/v0.1.1){target=_blank} 
released on Jul 04 2018.

<hr />

[![License](http://img.shields.io/badge/license-BSD-brightgreen.svg)](https://github.com/vozlt/nginx-module-stream-sts/blob/master/LICENSE)

Nginx stream server traffic status core module

## Screenshots
![nginx-module-sts screenshot](https://cloud.githubusercontent.com/assets/3648408/23112117/e8c56cda-f770-11e6-9c68-f57cbf4dd542.png "screenshot with deault")

## Synopsis

```Nginx
http {
    stream_server_traffic_status_zone;

    ...

    server {

        ...

        location /status {
            stream_server_traffic_status_display;
            stream_server_traffic_status_display_format html;
        }
    }
}

stream {
    server_traffic_status_zone;

    ...

    server {
        ...
    }
}
```

## Description
This is an Nginx module that provides access to stream server traffic status information.
This is a porting version of the [nginx-module-vts](https://github.com/vozlt/nginx-module-vts) to the NGINX "stream" subsystem so as to support the same features in [nginx-module-vts](https://github.com/vozlt/nginx-module-vts).
It contains the current status such as servers, upstreams, user-defined filter.
This module is the core module of two modules([nginx-module-sts](https://github.com/vozlt/nginx-module-sts), [nginx-module-stream-sts](https://github.com/vozlt/nginx-module-stream-sts)).

The functions of each module are as follows:

* [nginx-module-stream-sts](https://github.com/vozlt/nginx-module-stream-sts)
  * Support for implementing stream server stats.
  * Support for implementing stream filter.
  * Support for implementing stream limit.
  * Support for implementing stream embedded variables.
* [nginx-module-sts](https://github.com/vozlt/nginx-module-sts)
  * Support for implementing display of stream server stats.
  * Support for implementing control of stream server stats.

## See Also
* [nginx-module-sts](https://github.com/vozlt/nginx-module-sts)
* [nginx-module-vts](https://github.com/vozlt/nginx-module-vts)

## TODO

## Donation
[![License](http://img.shields.io/badge/PAYPAL-DONATE-yellow.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=PWWSYKQ9VKH38&lc=KR&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

## Author
YoungJoo.Kim(김영주) [<vozltx@gmail.com>]

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-stream-sts](https://github.com/vozlt/nginx-module-stream-sts){target=_blank}.