---

title: "A web application firewall module for NGINX"
description: "RPM package nginx-module-waf. A web application firewall module for NGINX. "

---

# *waf*: A web application firewall module for NGINX


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
    dnf -y install nginx-module-waf
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-waf
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_waf_module.so;
```


This document describes nginx-module-waf [v6.1.10](https://github.com/ADD-SP/ngx_waf/releases/tag/v6.1.10){target=_blank} 
released on Jan 25 2025.

<hr />

<p align="center">
    <img src="https://cdn.jsdelivr.net/gh/ADD-SP/ngx_waf@master/assets/logo.png" width=200 height=200/>
</p>

[![test](https://github.com/ADD-SP/ngx_waf/workflows/test/badge.svg)](https://github.com/ADD-SP/ngx_waf/actions?query=workflow%3Atest)

[![Notification](https://img.shields.io/badge/Notification-Telegram%20Channel-blue)](https://t.me/ngx_waf)
[![Discussion EN](https://img.shields.io/badge/Discussion%20EN-Telegram%20Group-blue)](https://t.me/group_ngx_waf)
[![Discussion CN](https://img.shields.io/badge/Discussion%20CN-Telegram%20Group-blue)](https://t.me/group_ngx_waf_cn)

English | [简体中文](README-ZH-CN.md)

Handy, High performance Nginx firewall module.

## Why ngx_waf

* Basic protection: such as black and white list of IPs or IP range, uri black and white list, and request body black list, etc.
* Easy to use: configuration files and rule files are easy to write and readable.
* High performance: Efficient algorithms and caching.
* Advanced protection: [ModSecurity](https://github.com/SpiderLabs/ModSecurity) compatible, you can use [OWASP(Open Web Application Security Project®) ModSecurity Core Rule Set](https://owasp.org/www-project-modsecurity-core-rule-set/).
* Friendly crawler verification: Supports verifying Google, Bing, Baidu and Yandex crawlers and allowing them automatically to avoid false positives.
* Captcha: Supports three kinds of captchas: hCaptcha, reCAPTCHAv2 and reCAPTCHAv3.

## Features

* [ModSecurity](https://github.com/SpiderLabs/ModSecurity) compatible. This feature is only available in the latest `Current` version.
* Rules that are compatible with [ModSecurity](https://github.com/SpiderLabs/ModSecurity).
* Anti SQL injection (powered by [libinjection](https://github.com/libinjection/libinjection)).
* Anti XSS (powered by [libinjection](https://github.com/libinjection/libinjection)).
* IPV4 and IPV6 support.
* Support for enabling CAPTCHAs, including [hCaptcha](https://www.hcaptcha.com/), [reCAPTCHAv2](https://developers.google.com/recaptcha) and [reCAPTCHAv3](https://developers.google.com/recaptcha). This feature is only available in the latest `Current` version.
* Support authentication-friendly crawlers (based on user agent and IP identification) to avoid blocking of these crawlers (e.g. GoogleBot). This feature is only available in the latest `Current` version.
* Anti Challenge Collapsar, it can automatically block malicious IP.
* Exceptional allow on specific IP address.
* Block the specified IP address.
* Block the specified request body.
* Exceptional allow on specific URL.
* Block the specified URL.
* Block the specified query string.
* Block the specified UserAgent.
* Block the specified Cookie.
* Exceptional allow on specific Referer.
* Block the specified Referer.

## Docs

* Recommended link: [https://docs.addesp.com/ngx_waf/](https://docs.addesp.com/ngx_waf/)
* Alternate link 1: [https://add-sp.github.io/ngx_waf-docs/](https://add-sp.github.io/ngx_waf-docs/)
* Alternate link 2: [https://ngx-waf-docs.pages.dev/](https://ngx-waf-docs.pages.dev/)

## Contact

* Telegram Channel: [https://t.me/ngx_waf](https://t.me/ngx_waf)
* Telegram Group (English): [https://t.me/group_ngx_waf](https://t.me/group_ngx_waf)
* Telegram Group (Chinese): [https://t.me/group_ngx_waf_cn](https://t.me/group_ngx_waf_cn)

## Sponsor

Hope you can help promote this project. The more stars got, the better this project is. :)

## Test Suite

This module comes with a Perl-driven test suite. The test cases are declarative too. 
Thanks to the [Test::Nginx](http://search.cpan.org/perldoc?Test::Nginx) module in the Perl world.

To run it on your side:

```shell
## It will take a lot of time, but it only needs to be run once.
cpan Test::Nginx

## You need to specify a temporary directory.
## If the directory does not exist it will be created automatically.
## If the directory already exists it will be **removed** first and then created.
export MODULE_TEST_PATH=/path/to/temp/dir

## You need to specify the absolute path to the dynamic module if you have it installed, 
## otherwise you do not need to run this line.
export MODULE_PATH=/path/to/ngx_http_waf_module.so

cd ./test/test-nginx
sh ./init.sh
sh ./start.sh ./t/*.t
```

Some parts of the test suite requires standard modules proxy, rewrite and SSI to be enabled as well when building Nginx.

## Thanks

* [ModSecurity](https://github.com/SpiderLabs/ModSecurity): An open source, cross platform web application firewall (WAF) engine.
* [uthash](https://github.com/troydhanson/uthash): C macros for hash tables and more.
* [libcurl](https://curl.se/libcurl/): The multiprotocol file transfer library .
* [cJSON](https://github.com/DaveGamble/cJSON): Ultralightweight JSON parser in ANSI C.
* [libinjection](https://github.com/libinjection/libinjection): SQL / SQLI tokenizer parser analyzer.
* [libsodium](https://github.com/jedisct1/libsodium): A modern, portable, easy to use crypto library.
* [test-nginx](https://github.com/openresty/test-nginx): Data-driven test scaffold for Nginx C module and OpenResty Lua library development.
* [lastversion](https://github.com/dvershinin/lastversion): A command line tool that helps you download or install a specific version of a project.
* [ngx_lua_waf](https://github.com/loveshell/ngx_lua_waf): A web application firewall based on the lua-nginx-module (openresty).
* [nginx-book](https://github.com/taobao/nginx-book): The Chinese language development guide for nginx.
* [nginx-development-guide](https://github.com/baishancloud/nginx-development-guide): The Chinese language development guide for nginx.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-waf](https://github.com/ADD-SP/ngx_waf){target=_blank}.