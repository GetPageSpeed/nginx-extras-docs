---

title: "NGINX Javascript challenge module"
description: "RPM package nginx-module-js-challenge. Similar to Cloudflare's anti-DDoS feature.  Simple javascript proof-of-work based access for NGINX with virtually no overhead. "

---

# *js-challenge*: NGINX Javascript challenge module


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
    dnf -y install nginx-module-js-challenge
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-js-challenge
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_js_challenge_module.so;
```


This document describes nginx-module-js-challenge [v0.0.2](https://github.com/dvershinin/ngx_http_js_challenge_module/releases/tag/v0.0.2){target=_blank} 
released on Aug 21 2024.

A request for stable release exists. Vote up [here](https://github.com/simon987/ngx_http_js_challenge_module/issues/4).
<hr />

## ngx_http_js_challenge_module

![GitHub](https://img.shields.io/github/license/simon987/ngx_http_js_challenge_module.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/simon987/ngx_http_js_challenge_module/badge)](https://www.codefactor.io/repository/github/simon987/ngx_http_js_challenge_module)


[Demo website](https://ngx-js-demo.simon987.net/)

Simple javascript proof-of-work based access for Nginx with virtually no overhead.

Easy installation: just add `load_module /path/to/ngx_http_js_challenge_module.so;` to your
`nginx.conf` file and follow the [configuration instructions](#configuration).

<p align="center">
  <img width="600px" src="throughput.png"/>
</p>

### Configuration

**Simple configuration**
```nginx
server {
    js_challenge on;
    js_challenge_secret "change me!";

    # ...
}
```


**Advanced configuration**
```nginx
server {
    js_challenge on;
    js_challenge_secret "change me!";
    js_challenge_html /path/to/body.html;
    js_challenge_bucket_duration 3600;
    js_challenge_title "Verifying your browser...";

    location /static {
        js_challenge off;
        alias /static_files/;
    }

    location /sensitive {
        js_challenge_bucket_duration 600;
        #...
    }

    #...
}
```

* `js_challenge on|off` Toggle javascript challenges for this config block
* `js_challenge_secret "secret"` Secret for generating the challenges. DEFAULT: "changeme"
* `js_challenge_html "/path/to/file.html"` Path to html file to be inserted in the `<body>` tag of the interstitial page
* `js_challenge_title "title"` Will be inserted in the `<title>` tag of the interstitial page. DEFAULT: "Verifying your browser..."
* `js_challenge_bucket_duration time` Interval to prompt js challenge, in seconds. DEFAULT: 3600

### Known limitations / TODO

* Users with cookies disabled will be stuck in an infinite refresh loop (TODO: redirect with a known query param, if no cookie is specified but the query arg is set, display an error page)
* If nginx is behind a reverse proxy/load balancer, the same challenge will be sent to different users and/or the response cookie will be invalidated when the user is re-routed to another server. (TODO: use the x-real-ip header when available) 

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-js-challenge](https://github.com/dvershinin/ngx_http_js_challenge_module){target=_blank}.