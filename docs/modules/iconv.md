# *iconv*: NGINX iconv module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-iconv
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


## Copyright & License

This program is licenced under the BSD license.

Copyright (c) 2010-2016, Calio <vipcalio@gmail.com>.

Copyright (c) 2010-2016, Yichun Zhang <agentzh@gmail.com>.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of the Taobao Inc. nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## Changelog

This module's change logs are part of the OpenResty bundle's change logs. Please see
See <http://openresty.org/#Changes>


## See Also

* The [OpenResty](https://openresty.org) bundle.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-iconv](https://github.com/calio/iconv-nginx-module){target=_blank}.