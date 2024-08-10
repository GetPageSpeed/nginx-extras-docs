# *iconv*: NGINX iconv module


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
    yum -y install nginx-module-iconv
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-iconv
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_iconv_module.so;
```


This document describes nginx-module-iconv [v0.14](https://github.com/calio/iconv-nginx-module/releases/tag/v0.14){target=_blank} 
released on May 15 2016.

<hr />
<!---
Don't edit this file manually! Instead you should generate it by using:
    wiki2markdown.pl doc/manpage.wiki
-->

## Name

iconv-nginx-module

## Description

This is a nginx module that uses libiconv to convert characters of different
encoding. It brings the 'set_iconv' command to nginx.

This module depends on the ngx_devel_kit(NDK) module.

## Usage

## set_iconv

**syntax:** *set_iconv &lt;destination_variable&gt; &lt;from_variable&gt; from=&lt;from_encoding&gt; to=&lt;to_encoding&gt;*

**default:** *none*

**phase:** *rewrite*


## iconv_buffer_size

**syntax:** *iconv_buffer_size &lt;size&gt;*

**default:** *iconv_buffer_size &lt;pagesize&gt;*


## iconv_filter

**syntax:** *iconv_filter from=&lt;from_encoding&gt; to=&lt;to_encoding&gt;*

**default:** *none*

**phase:** *output-filter*

Here is a basic example:

```nginx

 #nginx.conf

 location /foo {
     set $src '你好'; #in UTF-8
     set_iconv $dst $src from=utf8 to=gbk; #now $dst holds 你好 in GBK
 }

 #everything generated from /foo will be converted from utf8 to gbk
 location /bar {
     iconv_filter from=utf-8 to=gbk;
     iconv_buffer_size 1k;
     #content handler here
 }
```


## Changelog

This module's change logs are part of the OpenResty bundle's change logs. Please see
See <http://openresty.org/#Changes>


## See Also

* The [OpenResty](https://openresty.org) bundle.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-iconv](https://github.com/calio/iconv-nginx-module){target=_blank}.