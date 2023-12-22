# *dav-ext*: NGINX WebDAV PROPFIND,OPTIONS,LOCK,UNLOCK support


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-dav-ext
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_dav_ext_module.so;
```


This document describes nginx-module-dav-ext [v3.0.0](https://github.com/arut/nginx-dav-ext-module/releases/tag/v3.0.0){target=_blank} 
released on Dec 17 2018.

<hr />
nginx-dav-ext-module
====================

[nginx](http://nginx.org) [WebDAV](https://tools.ietf.org/html/rfc4918) PROPFIND,OPTIONS,LOCK,UNLOCK support.

About
-----

The standard [ngxhhttpddavmmodule](http://nginx.org/en/docs/http/ngx_http_dav_module.html) provides partial [WebDAV](https://tools.ietf.org/html/rfc4918) implementation and only supports GET,HEAD,PUT,DELETE,MKCOL,COPY,MOVE methods.

For full [WebDAV](https://tools.ietf.org/html/rfc4918) support in [nginx](http://nginx.org) you need to enable the standard [ngxhhttpddavmmodule](http://nginx.org/en/docs/http/ngx_http_dav_module.html) as well as this module for the missing methods.

Build
-----

Building [nginx](http://nginx.org) with the module:

``` {.sourceCode .bash}
## static module
$ ./configure --with-http_dav_module --add-module=/path/to/nginx-dav-ext-module

## dynamic module
$ ./configure --with-http_dav_module --add-dynamic-module=/path/to/nginx-dav-ext-module
```

Trying to compile [nginx](http://nginx.org) with this module but without [ngxhhttpddavmmodule](http://nginx.org/en/docs/http/ngx_http_dav_module.html) will result in compilation error.

Requirements
------------

-   [nginx](http://nginx.org) version \>= 1.13.4
-   `libxml2` + `libxslt`

The `libxslt` library is technically redundant and is only required since this combination is supported by [nginx](http://nginx.org) for the xslt module. Using builtin nginx mechanisms for linking against third-party libraries brings certain compatibility benefits. However this redundancy can be easily eliminated in the `config` file.

Testing
-------

The module tests require standard [nginxttests](http://hg.nginx.org/nginx-tests) and Perl `HTTP::DAV` library.

``` {.sourceCode .bash}
$ export PERL5LIB=/path/to/nginx-tests/lib
$ export TEST_NGINX_BINARY=/path/to/nginx
$ prove t
```

Locking
-------

-   Only the exclusive write locks are supported, which is the only type of locks described in the [WebDAV](https://tools.ietf.org/html/rfc4918) specification.
-   All currently held locks are kept in a list. Checking if an object is constrained by a lock requires O(n) operations. A huge number of simultaneously held locks may degrade performance. Thus it is not recommended to have a large lock timeout which would increase the number of locks.

Directives
----------

### dav\_ext\_methods

|---|---|
|*Syntax:*|`dav_ext_methods [PROPFIND] [OPTIONS] [LOCK] [UNLOCK]`|
|*Context:*|http, server, location|

Enables support for the specified WebDAV methods in the current scope.

### dav\_ext\_lock\_zone

|---|---|
|*Syntax:*|`dav_ext_lock_zone zone=NAME:SIZE [timeout=TIMEOUT]`|
|*Context:*|http|

Defines a shared zone for WebDAV locks with specified NAME and SIZE. Also, defines a lock expiration TIMEOUT. Default lock timeout value is 1 minute.

### dav\_ext\_lock

|---|---|
|*Syntax:*|`dav_ext_lock zone=NAME`|
|*Context:*|http, server, location|

Enables WebDAV locking in the specified scope. Locks are stored in the shared zone specified by NAME. This zone must be defined with the `dav_ext_lock_zone` directive.

Note that even though this directive enables locking capabilities in the current scope, HTTP methods LOCK and UNLOCK should also be explicitly specified in the `dav_ext_methods`.

Example 1
---------

Simple lockless example:

    location / {
        root /data/www;

        dav_methods PUT DELETE MKCOL COPY MOVE;
        dav_ext_methods PROPFIND OPTIONS;
    }

Example 2
---------

WebDAV with locking:

    http {
        dav_ext_lock_zone zone=foo:10m;

        ...

        server {
            ...

            location / {
                root /data/www;

                dav_methods PUT DELETE MKCOL COPY MOVE;
                dav_ext_methods PROPFIND OPTIONS LOCK UNLOCK;
                dav_ext_lock zone=foo;
            }
        }
    }

Example 3
---------

WebDAV with locking which works with MacOS client:

    http {
        dav_ext_lock_zone zone=foo:10m;

        ...

        server {
            ...

            location / {
                root /data/www;

                # enable creating directories without trailing slash
                set $x $uri$request_method;
                if ($x ~ [^/]MKCOL$) {
                    rewrite ^(.*)$ $1/;
                }

                dav_methods PUT DELETE MKCOL COPY MOVE;
                dav_ext_methods PROPFIND OPTIONS LOCK UNLOCK;
                dav_ext_lock zone=foo;
            }
        }
    }

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-dav-ext](https://github.com/arut/nginx-dav-ext-module){target=_blank}.