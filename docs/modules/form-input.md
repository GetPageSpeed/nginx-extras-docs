---

title: "NGINX form input module"
description: "RPM package nginx-module-form-input. NGINX module that reads HTTP POST and PUT request body encoded in application/x-www-form-urlencoded and parses the arguments into NGINX variables."

---

# *form-input*: NGINX form input module


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
    dnf -y install nginx-module-form-input
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-form-input
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_form_input_module.so;
```


This document describes nginx-module-form-input [v0.12](https://github.com/calio/form-input-nginx-module/releases/tag/v0.12){target=_blank} 
released on May 15 2016.

<hr />

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


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-form-input](https://github.com/calio/form-input-nginx-module){target=_blank}.