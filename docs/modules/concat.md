# _concat_: HTTP Concatenation module for NGINX


## Installation

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-concat
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_concat_module.so;
```


This document describes nginx-module-concat [v1.2.3](https://github.com/dvershinin/nginx-http-concat/releases/tag/1.2.3){target=_blank} 
released on Jan 15 2020.
    
<hr />

## Introduction 

This is a module that is distributed with
[tengine](http://tengine.taobao.org) which is a distribution of
[Nginx](http://nginx.org) that is used by the e-commerce/auction site
[Taobao.com](http://en.wikipedia.org/wiki/Taobao). This distribution
contains some modules that are new on the Nginx scene. The
`ngx_http_concat` module is one of them.

The module is inspired by Apache's
[`modconcat`](http://code.google.com/p/modconcat). It follows the same
pattern for enabling the concatenation. It uses two `?`, like this: 

    http://example.com/??style1.css,style2.css,foo/style3.css
    
If a **third** `?` is present it's treated as **version string**. Like
this:

    http://example.com/??style1.css,style2.css,foo/style3.css?v=102234

## Configuration example

    location /static/css/ {
        concat on;
        concat_max_files 20;
    }
        
    location /static/js/ {
        concat on;
        concat_max_files 30;
    }

## Module directives

**concat** `on` | `off`

**default:** `concat off`

**context:** `http, server, location`

It enables the concatenation in a given context.

<br/>
<br/>

**concat_types** `MIME types`

**default:** `concat_types: text/css application/x-javascript`

**context:** `http, server, location`

Defines the [MIME types](http://en.wikipedia.org/wiki/MIME_type) which
can be concatenated in a given context.

<br/>
<br/>

**concat_unique** `on` | `off`

**default:** `concat_unique on`

**context:** `http, server, location`

Defines if only files of a given MIME type can concatenated or if
several MIME types can be concatenated. For example if set to `off`
then in a given context you can concatenate Javascript and CSS files.

Note that the default value is `on`, meaning that only files with same
MIME type are concatenated in a given context. So if you have CSS and
JS you cannot do something like this:

    http://example.com/static/??foo.css,bar/foobaz.js
    
In order to do that you **must** set `concat_unique off`. This applies
to any other type of files that you decide to concatenate by adding
the respective MIME type via `concat_types`,

<br/>
<br/>

**concat\_max\_files** `number`p

**default:** `concat_max_files 10`

**context:** `http, server, location`

Defines the **maximum** number of files that can be concatenated in a
given context. Note that a given URI cannot be bigger than the page
size of your platform. On Linux you can get the page size issuing:

    getconf PAGESIZE
    
Usually is 4k. So if you try to concatenate a lot of files together in
a given context you might hit this barrier. To overcome that OS
defined limitation you must use
the [`large_client_header_buffers`](http://wiki.nginx.org/NginxHttpCoreModule#large_client_header_buffers)
directive. Set it to the value you need.

<br/>
<br/>

**concat_delimiter**: string

**default**: NONE

**context**: `http, server, locatione`

Defines the **delimiter** between two files.
If the config is **concat_delimiter "\n"**,a '\n' would be inserted betwen 1.js and 2.js when
visted http://example.com/??1.js,2.js

<br/>
<br/>

**concat_ignore_file_error**: `on` | `off`

**default**: off

**context**: `http, server, location`

Whether to ignore 404 and 403 or not.

<br/>
<br/>

## Tagging releases 

Perusio is maintaing a tagged release
at http://github.com/alibaba/nginx-http-concat
in synch with the [Tengine](http://tengine.taobao.org)
releases. Refer there for the latest uncommitted tags.
 
## Other tengine modules on Github

 + [footer filter](https://github.com/alibaba/nginx-http-footer-filter):
   allows to add some extra data (markup or not) at the end of a
   request body. It's pratical for things like adding time stamps or
   other miscellaneous stuff without having to tweak your application.
   
 + [http slice](https://github.com/alibaba/nginx-http-slice): allows
   to serve a file by slices. A sort of reverse byte-range. Useful for
   serving large files while not hogging the network.

## Other builds

 1. As referred at the outset this module is part of the
    [`tengine`](http://tengine.taobao.org) Nginx distribution. So you
    might want to save yourself some work and just build it from
    scratch using `tengine` in lieu if the official Nginx source.

 2. If you fancy a bleeding edge Nginx package (from the dev releases)
    for Debian made to measure then you might be interested in Perusio's HA/HP
    [debian](http://debian.perusio.net/unstable) Nginx
    package with built-in support for nginx-http-concat.
    Instructions for using the repository and making the
    package live happily inside a stable distribution installation are
    [provided](http://debian.perusio.net).
        
## Acknowledgments

Thanks to [Joshua Zhu](http://blog.zhuzhaoyuan.com) and the Taobao
platform engineering team for releasing `tengine`. Also for being kind
enough to clarify things regarding this module on the
[Nginx mailing list](http://mailman.nginx.org/pipermail/nginx/2011-December/030830.html).

## License

Copyright (C) 2010-2012 Alibaba Group Holding Limited

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
 
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
    
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-concat](https://github.com/dvershinin/nginx-http-concat){target=_blank}.