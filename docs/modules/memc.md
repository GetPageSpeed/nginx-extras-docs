---

title: "Extended version of the standard NGINX memcached module"
description: "RPM package nginx-module-memc. Extended version of the standard NGINX memcached module "

---

# *memc*: Extended version of the standard NGINX memcached module


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
    dnf -y install nginx-module-memc
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-memc
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_memc_module.so;
```


This document describes nginx-module-memc [v0.20](https://github.com/openresty/memc-nginx-module/releases/tag/v0.20){target=_blank} 
released on Dec 27 2023.

<hr />

**ngx_memc** - An extended version of the standard memcached module that supports set, add, delete, and many more memcached commands.


## Synopsis

```nginx

 # GET /foo?key=dog
 #
 # POST /foo?key=cat
 # Cat's value...
 #
 # PUT /foo?key=bird
 # Bird's value...
 #
 # DELETE /foo?key=Tiger
 location /foo {
     set $memc_key $arg_key;

     # $memc_cmd defaults to get for GET,
     #   add for POST, set for PUT, and
     #   delete for the DELETE request method.

     memc_pass 127.0.0.1:11211;
 }
```

```nginx

 # GET /bar?cmd=get&key=cat
 #
 # POST /bar?cmd=set&key=dog
 # My value for the "dog" key...
 #
 # DELETE /bar?cmd=delete&key=dog
 # GET /bar?cmd=delete&key=dog
 location /bar {
     set $memc_cmd $arg_cmd;
     set $memc_key $arg_key;
     set $memc_flags $arg_flags; # defaults to 0
     set $memc_exptime $arg_exptime; # defaults to 0

     memc_pass 127.0.0.1:11211;
 }
```

```nginx

 # GET /bar?cmd=get&key=cat
 # GET /bar?cmd=set&key=dog&val=animal&flags=1234&exptime=2
 # GET /bar?cmd=delete&key=dog
 # GET /bar?cmd=flush_all
 location /bar {
     set $memc_cmd $arg_cmd;
     set $memc_key $arg_key;
     set $memc_value $arg_val;
     set $memc_flags $arg_flags; # defaults to 0
     set $memc_exptime $arg_exptime; # defaults to 0

     memc_cmds_allowed get set add delete flush_all;

     memc_pass 127.0.0.1:11211;
 }
```

```nginx

   http {
     ...
     upstream backend {
        server 127.0.0.1:11984;
        server 127.0.0.1:11985;
     }
     server {
         location /stats {
             set $memc_cmd stats;
             memc_pass backend;
         }
         ...
     }
   }
   ...
```

```nginx

 # read the memcached flags into the Last-Modified header
 # to respond 304 to conditional GET
 location /memc {
     set $memc_key $arg_key;

     memc_pass 127.0.0.1:11984;

     memc_flags_to_last_modified on;
 }
```

```nginx

 location /memc {
     set $memc_key foo;
     set $memc_cmd get;

     # access the unix domain socket listend by memcached
     memc_pass unix:/tmp/memcached.sock;
 }
```

## Description

This module extends the standard [memcached module](http://nginx.org/en/docs/http/ngx_http_memcached_module.html) to support almost the whole [memcached ascii protocol](http://code.sixapart.com/svn/memcached/trunk/server/doc/protocol.txt).

It allows you to define a custom [REST](http://en.wikipedia.org/wiki/REST) interface to your memcached servers or access memcached in a very efficient way from within the nginx server by means of subrequests or [independent fake requests](http://github.com/srlindsay/nginx-independent-subrequest).

This module is not supposed to be merged into the Nginx core because I've used [Ragel](http://www.complang.org/ragel/) to generate the memcached response parsers (in C) for joy :)

If you are going to use this module to cache location responses out of the box, try [srcache-nginx-module](http://github.com/openresty/srcache-nginx-module) with this module to achieve that.

When used in conjunction with [lua-nginx-module](http://github.com/openresty/lua-nginx-module), it is recommended to use the [lua-resty-memcached](http://github.com/openresty/lua-resty-memcached) library instead of this module though, because the former is much more flexible and memory-efficient.


## Keep-alive connections to memcached servers

You need [HttpUpstreamKeepaliveModule](http://wiki.nginx.org/HttpUpstreamKeepaliveModule) together with this module for keep-alive TCP connections to your backend memcached servers.

Here's a sample configuration:

```nginx

   http {
     upstream backend {
       server 127.0.0.1:11211;

       # a pool with at most 1024 connections
       # and do not distinguish the servers:
       keepalive 1024;
     }

     server {
         ...
         location /memc {
             set $memc_cmd get;
             set $memc_key $arg_key;
             memc_pass backend;
         }
     }
   }
```


## How it works

It implements the memcached TCP protocol all by itself, based upon the `upstream` mechanism. Everything involving I/O is non-blocking.

The module itself does not keep TCP connections to the upstream memcached servers across requests, just like other upstream modules. For a working solution, see section [Keep-alive connections to memcached servers](#keep-alive-connections-to-memcached-servers).


## Memcached commands supported

The memcached storage commands [set](#set-memc_key-memc_flags-memc_exptime-memc_value), [add](#add-memc_key-memc_flags-memc_exptime-memc_value), [replace](#replace-memc_key-memc_flags-memc_exptime-memc_value), [prepend](#prepend-memc_key-memc_flags-memc_exptime-memc_value), and [append](#append-memc_key-memc_flags-memc_exptime-memc_value) uses the `$memc_key` as the key, `$memc_exptime` as the expiration time (or delay) (defaults to 0), `$memc_flags` as the flags (defaults to 0), to build the corresponding memcached queries.

If `$memc_value` is not defined at all, then the request body will be used as the value of the `$memc_value` except for the [incr](#incr-memc_key-memc_value) and [decr](#decr-memc_key-memc_value) commands. Note that if `$memc_value` is defined as an empty string (`""`), that empty string will still be used as the value as is.

The following memcached commands have been implemented and tested (with their parameters marked by corresponding
nginx variables defined by this module):


## get $memc_key

Retrieves the value using a key.

```nginx

   location /foo {
       set $memc_cmd 'get';
       set $memc_key 'my_key';

       memc_pass 127.0.0.1:11211;

       add_header X-Memc-Flags $memc_flags;
   }
```

Returns `200 OK` with the value put into the response body if the key is found, or `404 Not Found` otherwise. The `flags` number will be set into the `$memc_flags` variable so it's often desired to put that info into the response headers by means of the standard [add_header directive](http://nginx.org/en/docs/http/ngx_http_headers_module.html#add_header).

It returns `502` for `ERROR`, `CLIENT_ERROR`, or `SERVER_ERROR`.


## set $memc_key $memc_flags $memc_exptime $memc_value

To use the request body as the memcached value, just avoid setting the `$memc_value` variable:

```nginx

   # POST /foo
   # my value...
   location /foo {
       set $memc_cmd 'set';
       set $memc_key 'my_key';
       set $memc_flags 12345;
       set $memc_exptime 24;

       memc_pass 127.0.0.1:11211;
   }
```

Or let the `$memc_value` hold the value:

```nginx

   location /foo {
       set $memc_cmd 'set';
       set $memc_key 'my_key';
       set $memc_flags 12345;
       set $memc_exptime 24;
       set $memc_value 'my_value';

       memc_pass 127.0.0.1:11211;
   }
```

Returns `201 Created` if the upstream memcached server replies `STORED`, `200` for `NOT_STORED`, `404` for `NOT_FOUND`, `502` for `ERROR`, `CLIENT_ERROR`, or `SERVER_ERROR`.

The original memcached responses are returned as the response body except for `404 NOT FOUND`.


## add $memc_key $memc_flags $memc_exptime $memc_value

Similar to the [set command](#set-memc_key-memc_flags-memc_exptime-memc_value).


## replace $memc_key $memc_flags $memc_exptime $memc_value

Similar to the [set command](#set-memc_key-memc_flags-memc_exptime-memc_value).


## append $memc_key $memc_flags $memc_exptime $memc_value

Similar to the [set command](#set-memc_key-memc_flags-memc_exptime-memc_value).

Note that at least memcached version 1.2.2 does not support the "append" and "prepend" commands. At least 1.2.4 and later versions seem to supports these two commands.


## prepend $memc_key $memc_flags $memc_exptime $memc_value

Similar to the [append command](#append-memc_key-memc_flags-memc_exptime-memc_value).


## delete $memc_key

Deletes the memcached entry using a key.

```nginx

   location /foo
       set $memc_cmd delete;
       set $memc_key my_key;

       memc_pass 127.0.0.1:11211;
   }
```

Returns `200 OK` if deleted successfully, `404 Not Found` for `NOT_FOUND`, or `502` for `ERROR`, `CLIENT_ERROR`, or `SERVER_ERROR`.

The original memcached responses are returned as the response body except for `404 NOT FOUND`.


## delete $memc_key $memc_exptime

Similar to the [delete $memc_key](#delete-memc_key) command except it accepts an optional `expiration` time specified by the `$memc_exptime` variable.

This command is no longer available in the latest memcached version 1.4.4.


## incr $memc_key $memc_value

Increments the existing value of `$memc_key` by the amount specified by `$memc_value`:

```nginx

   location /foo {
       set $memc_cmd incr;
       set $memc_key my_key;
       set $memc_value 2;
       memc_pass 127.0.0.1:11211;
   }
```

In the preceding example, every time we access `/foo` will cause the value of `my_key` increments by `2`.

Returns `200 OK` with the new value associated with that key as the response body if successful, or `404 Not Found` if the key is not found.

It returns `502` for `ERROR`, `CLIENT_ERROR`, or `SERVER_ERROR`.


## decr $memc_key $memc_value

Similar to [incr $memc_key $memc_value](#incr-memc_key-memc_value).


## flush_all

Mark all the keys on the memcached server as expired:

```nginx

   location /foo {
       set $memc_cmd flush_all;
       memc_pass 127.0.0.1:11211;
   }
```


## flush_all $memc_exptime

Just like [flush_all](#flush_all) but also accepts an expiration time specified by the `$memc_exptime` variable.


## stats

Causes the memcached server to output general-purpose statistics and settings

```nginx

   location /foo {
       set $memc_cmd stats;
       memc_pass 127.0.0.1:11211;
   }
```

Returns `200 OK` if the request succeeds, or 502 for `ERROR`, `CLIENT_ERROR`, or `SERVER_ERROR`.

The raw `stats` command output from the upstream memcached server will be put into the response body. 


## Directives

All the standard [memcached module](http://nginx.org/en/docs/http/ngx_http_memcached_module.html) directives in nginx 0.8.28 are directly inherited, with the `memcached_` prefixes replaced by `memc_`. For example, the `memcached_pass` directive is spelled `memc_pass`.

Here we only document the most important two directives (the latter is a new directive introduced by this module).


## memc_pass

**syntax:** *memc_pass &lt;memcached server IP address&gt;:&lt;memcached server port&gt;*

**syntax:** *memc_pass &lt;memcached server hostname&gt;:&lt;memcached server port&gt;*

**syntax:** *memc_pass &lt;upstream_backend_name&gt;*

**syntax:** *memc_pass unix:&lt;path_to_unix_domain_socket&gt;*

**default:** *none*

**context:** *http, server, location, if*

**phase:** *content*

Specify the memcached server backend.


## memc_cmds_allowed
**syntax:** *memc_cmds_allowed &lt;cmd&gt;...*

**default:** *none*

**context:** *http, server, location, if*

Lists memcached commands that are allowed to access. By default, all the memcached commands supported by this module are accessible.
An example is

```nginx

    location /foo {
        set $memc_cmd $arg_cmd;
        set $memc_key $arg_key;
        set $memc_value $arg_val;

        memc_pass 127.0.0.1:11211;

        memc_cmds_allowed get;
    }
```


## memc_flags_to_last_modified
**syntax:** *memc_flags_to_last_modified on|off*

**default:** *off*

**context:** *http, server, location, if*

Read the memcached flags as epoch seconds and set it as the value of the `Last-Modified` header. For conditional GET, it will signal nginx to return `304 Not Modified` response to save bandwidth.


## memc_connect_timeout
**syntax:** *memc_connect_timeout &lt;time&gt;*

**default:** *60s*

**context:** *http, server, location*

The timeout for connecting to the memcached server, in seconds by default.

It's wise to always explicitly specify the time unit to avoid confusion. Time units supported are "s"(seconds), "ms"(milliseconds), "y"(years), "M"(months), "w"(weeks), "d"(days), "h"(hours), and "m"(minutes).

This time must be less than 597 hours.


## memc_send_timeout
**syntax:** *memc_send_timeout &lt;time&gt;*

**default:** *60s*

**context:** *http, server, location*

The timeout for sending TCP requests to the memcached server, in seconds by default.

It is wise to always explicitly specify the time unit to avoid confusion. Time units supported are "s"(seconds), "ms"(milliseconds), "y"(years), "M"(months), "w"(weeks), "d"(days), "h"(hours), and "m"(minutes).

This time must be less than 597 hours.


## memc_read_timeout
**syntax:** *memc_read_timeout &lt;time&gt;*

**default:** *60s*

**context:** *http, server, location*

The timeout for reading TCP responses from the memcached server, in seconds by default.

It's wise to always explicitly specify the time unit to avoid confusion. Time units supported are "s"(seconds), "ms"(milliseconds), "y"(years), "M"(months), "w"(weeks), "d"(days), "h"(hours), and "m"(minutes).

This time must be less than 597 hours.


## memc_buffer_size
**syntax:** *memc_buffer_size &lt;size&gt;*

**default:** *4k/8k*

**context:** *http, server, location*

This buffer size is used for the memory buffer to hold

* the complete response for memcached commands other than `get`,
* the complete response header (i.e., the first line of the response) for the `get` memcached command.

This default size is the page size, may be `4k` or `8k`.


## memc_ignore_client_abort
**syntax:** *memc_ignore_client_abort on|off*

**default:** *off*

**context:** *location*

Determines whether the connection with a memcache server should be closed when a client closes a connection without waiting for a response.

This directive was first added in the `v0.14` release.


## Changes

The changes of every release of this module can be obtained from the OpenResty bundle's change logs:

<http://openresty.org/#Changes>


## Test Suite

This module comes with a Perl-driven test suite. The [test cases](http://github.com/openresty/memc-nginx-module/tree/master/t/) are
[declarative](http://github.com/openresty/memc-nginx-module/blob/master/t/storage.t) too. Thanks to the [Test::Base](http://search.cpan.org/perldoc?Test::Base) module in the Perl world.

To run it on your side:

```bash

 $ PATH=/path/to/your/nginx-with-memc-module:$PATH prove -r t
```

You need to terminate any Nginx processes before running the test suite if you have changed the Nginx server binary.

Either [LWP::UserAgent](http://search.cpan.org/perldoc?LWP::UserAgent) or [IO::Socket](http://search.cpan.org/perldoc?IO::Socket) is used by the [test scaffold](http://github.com/openresty/memc-nginx-module/blob/master/test/lib/Test/Nginx/LWP.pm).

Because a single nginx server (by default, `localhost:1984`) is used across all the test scripts (`.t` files), it's meaningless to run the test suite in parallel by specifying `-jN` when invoking the `prove` utility.

You should also keep a memcached server listening on the `11211` port at localhost before running the test suite.

Some parts of the test suite requires modules [rewrite](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html) and [echo](http://github.com/openresty/echo-nginx-module) to be enabled as well when building Nginx.


## See Also

* The original announcement email on the nginx mailing list: [ngx_memc: "an extended version of ngx_memcached that supports set, add, delete, and many more commands"](http://forum.nginx.org/read.php?2,28359)
* My slides demonstrating various ngx_memc usage: <http://agentzh.org/misc/slides/nginx-conf-scripting/nginx-conf-scripting.html#34> (use the arrow or pageup/pagedown keys on the keyboard to swith pages)
* The latest [memcached TCP protocol](http://code.sixapart.com/svn/memcached/trunk/server/doc/protocol.txt).
* The [ngx_srcache](http://github.com/openresty/srcache-nginx-module) module
* The [lua-resty-memcached](https://github.com/openresty/lua-resty-memcached) library based on the [lua-nginx-module](http://github.com/openresty/lua-nginx-module) cosocket API.
* The standard [memcached](http://nginx.org/en/docs/http/ngx_http_memcached_module.html) module.
* The [echo module](http://github.com/openresty/echo-nginx-module) for Nginx module's automated testing.
* The standard [headers](http://nginx.org/en/docs/http/ngx_http_headers_module.html) module and the 3rd-parth [headers-more](http://github.com/openresty/headers-more-nginx-module) module.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-memc](https://github.com/openresty/memc-nginx-module){target=_blank}.