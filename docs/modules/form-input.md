# *form-input*: NGINX form input module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-form-input
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_form_input_module.so;
```


This document describes nginx-module-form-input [v0.12](https://github.com/calio/form-input-nginx-module/releases/tag/v0.12){target=_blank} 
released on May 16 2016.

<hr />

form-input-nginx-module - NGINX module that reads HTTP POST and PUT request body encoded in "application/x-www-form-urlencoded" and parses the arguments into nginx variables.

## Description

This is a nginx module that reads HTTP POST and PUT request body encoded
in "application/x-www-form-urlencoded", and parse the arguments in
request body into nginx variables.

This module depends on the ngx_devel_kit (NDK) module.

## Usage

```nginx
set_form_input $variable;
set_form_input $variable argument;

set_form_input_multi $variable;
set_form_input_multi $variable argument;
```

example:

```nginx
#nginx.conf

location /foo {
    # ensure client_max_body_size == client_body_buffer_size
    client_max_body_size 100k;
    client_body_buffer_size 100k;

    set_form_input $data;    # read "data" field into $data
    set_form_input $foo foo; # read "foo" field into $foo
}

location /bar {
    # ensure client_max_body_size == client_body_buffer_size
    client_max_body_size 1m;
    client_body_buffer_size 1m;

    set_form_input_multi $data; # read all "data" field into $data
    set_form_input_multi $foo data; # read all "data" field into $foo

    array_join ' ' $data; # now $data is an string
    array_join ' ' $foo;  # now $foo is an string
}
```


## Limitations

* ngx_form_input will discard request bodies that are buffered
to disk files. When the client_max_body_size setting is larger than
client_body_buffer_size, request bodies that are larger
than client_body_buffer_size (but no larger than
client_max_body_size) will be buffered to disk files.
So it's important to ensure these two config settings take
the same values to avoid confustion.


## Copyright & License

Copyright (c) 2010, 2011, Jiale "calio" Zhi <vipcalio@gmail.com>.

Copyright (c) 2010-2016, Yichun "agentzh" Zhang <agentzh@gmail.com>, CloudFlare Inc.

This module is licensed under the terms of the BSD license.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
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
nginx-module-form-input](https://github.com/calio/form-input-nginx-module){target=_blank}.