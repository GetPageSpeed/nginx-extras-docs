---

title: "String substitutions module for nginx"
description: "RPM package nginx-module-substitutions. nginx_substitutions_filter is a filter module which can do both regular expression and fixed string substitutions on response bodies.  This module is quite different from the Nginx's native Substitution Module.  It scans the output chains buffer and matches string line by line, just like Apache's mod_substitute  For any issues, see bug tracker at https://github.com/yaoweibin/ngx_http_substitutions_filter_module/issues and reference commit b8a71eacc7f986ba091282ab8b1bbbc6ae1807e0 if requested, not the version of the package. "

---

# *substitutions*: String substitutions module for nginx


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
    dnf -y install nginx-module-substitutions
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-substitutions
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_subs_filter_module.so;
```


This document describes nginx-module-substitutions [v0.6.6](https://github.com/dvershinin/ngx_http_substitutions_filter_module/releases/tag/v0.6.6){target=_blank} 
released on Dec 30 2021.

<hr />
nginx_substitutions_filter
    *Note: this module is not distributed with the Nginx source.
    Installation instructions can be found below.*

  Description
    nginx_substitutions_filter is a filter module which can do both regular
    expression and fixed string substitutions on response bodies. This
    module is quite different from the Nginx's native Substitution Module.
    It scans the output chains buffer and matches string line by line, just
    like Apache's mod_substitute
    (<http://httpd.apache.org/docs/trunk/mod/mod_substitute.html>).

  Example
    location / {

        subs_filter_types text/html text/css text/xml;
        subs_filter st(\d*).example.com $1.example.com ir;
        subs_filter a.example.com s.example.com;
        subs_filter http://$host https://$host;
    }

  Directives
    *   subs_filter_types

    *   subs_filter

   subs_filter_types
    syntax: *subs_filter_types mime-type [mime-types] *

    default: *subs_filter_types text/html*

    context: *http, server, location*

    *subs_filter_types* is used to specify which content types should be
    checked for *subs_filter*, in addition to *text/html*. The default is
    only *text/html*.

    This module just works with plain text. If the response is compressed,
    it can't uncompress the response and will ignore this response. This
    module can be compatible with gzip filter module. But it will not work
    with proxy compressed response. You can disable the compressed response
    like this:

    proxy_set_header Accept-Encoding "";

   subs_filter
    syntax: *subs_filter source_str destination_str [gior] *

    default: *none*

    context: *http, server, location*

    *subs_filter* allows replacing source string(regular expression or
    fixed) in the nginx response with destination string. The variables 
    in matching text is only avaiable under fixed string mode, which means 
    the matching text could not contain variables if it is a regular 
    expression. Substitution text may contain variables. More than one 
    substitution rules per location is supported. 
    The meaning of the third flags are:

    *   *g*(default): Replace all the match strings.

    *   *i*: Perform a case-insensitive match.

    *   *o*: Just replace the first one.

    *   *r*: The pattern is treated as a regular expression, default is
        fixed string.

   subs_filter_bypass
    syntax: *subs_filter_bypass $variable1 ...*

    default: *none*

    context: *http, server, location*

    You can sepcify several variables with this directive. If at least one
    of the variable is not empty and is not equal to '0', this substitution
    filter will be disabled.

  Installation
    To install, get the source with subversion:

    git clone
    git://github.com/yaoweibin/ngx_http_substitutions_filter_module.git

    and then compile nginx with the following option:

    ./configure --add-module=/path/to/module

  Known issue
    *   Can't substitute the response header.

  CHANGES
    Changes with nginx_substitutions_filter 0.6.4 2014-02-15

    *   Now non-200 response will work

    *   added the subs_filter_bypass directive

    Changes with nginx_substitutions_filter 0.6.2 2012-08-26

    *   fixed a bug of buffer overlap

    *   fixed a bug with last zero buffer

    Changes with nginx_substitutions_filter 0.6.0 2012-06-30

    *   refactor this module

    Changes with nginx_substitutions_filter 0.5.2 2010-08-11

    *   do many optimizing for this module

    *   fix a bug of buffer overlap

    *   fix a segment fault bug when output chain return NGX_AGAIN.

    *   fix a bug about last buffer with no linefeed. This may cause segment
        fault. Thanks for Josef Fröhle

    Changes with nginx_substitutions_filter 0.5 2010-04-15

    *   refactor the source structure, create branches of dev

    *   fix a bug of small chunk of buffers causing lose content

    *   fix the bug of last_buf and the nginx's compatibility above 0.8.25

    *   fix a bug with unwanted capture config error in fix string
        substitution

    *   add feature of regex captures

    Changes with nginx_substitutions_filter 0.4 2009-12-23

    *   fix many bugs

    Changes with nginx_substitutions_filter 0.3 2009-02-04

    *   Initial public release

  Reporting a bug
    Questions/patches may be directed to Weibin Yao, yaoweibin@gmail.com.

  Copyright & License
    This module is licensed under the BSD license.

    Copyright (C) 2014 by Weibin Yao <yaoweibin@gmail.com>.

    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    *
          Redistributions of source code must retain the above copyright

        notice, this list of conditions and the following disclaimer.

    *
          Redistributions in binary form must reproduce the above copyright

        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
    IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
    TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-substitutions](https://github.com/dvershinin/ngx_http_substitutions_filter_module){target=_blank}.