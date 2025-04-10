---

title: "NGINX Headers More dynamic module"
description: "RPM package nginx-module-headers-more. Set, add, and clear arbitrary output headers in the NGINX HTTP servers. "

---

# *headers-more*: NGINX Headers More dynamic module


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
    dnf -y install nginx-module-headers-more
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-headers-more
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_headers_more_filter_module.so;
```


This document describes nginx-module-headers-more [v0.33](https://github.com/dvershinin/headers-more-nginx-module/releases/tag/v0.33){target=_blank} 
released on Jun 28 2022.

<hr />

**ngx_headers_more** - Set and clear input and output headers...more than "add"!


## Synopsis

```nginx

 # set the Server output header
 more_set_headers 'Server: my-server';

 # set and clear output headers
 location /bar {
     more_set_headers 'X-MyHeader: blah' 'X-MyHeader2: foo';
     more_set_headers -t 'text/plain text/css' 'Content-Type: text/foo';
     more_set_headers -s '400 404 500 503' -s 413 'Foo: Bar';
     more_clear_headers 'Content-Type';

     # your proxy_pass/memcached_pass/or any other config goes here...
 }

 # set output headers
 location /type {
     more_set_headers 'Content-Type: text/plain';
     # ...
 }

 # set input headers
 location /foo {
     set $my_host 'my dog';
     more_set_input_headers 'Host: $my_host';
     more_set_input_headers -t 'text/plain' 'X-Foo: bah';

     # now $host and $http_host have their new values...
     # ...
 }

 # replace input header X-Foo *only* if it already exists
 more_set_input_headers -r 'X-Foo: howdy';
```

## Description

This module allows you to add, set, or clear any output
or input header that you specify.

This is an enhanced version of the standard
[headers](http://nginx.org/en/docs/http/ngx_http_headers_module.html) module because it provides more utilities like
resetting or clearing "builtin headers" like `Content-Type`,
`Content-Length`, and `Server`.

It also allows you to specify an optional HTTP status code
criteria using the `-s` option and an optional content
type criteria using the `-t` option while modifying the
output headers with the [more_set_headers](#more_set_headers) and
[more_clear_headers](#more_clear_headers) directives. For example,

```nginx
 more_set_headers -s 404 -t 'text/html' 'X-Foo: Bar';
```

You can also specify multiple MIME types to filter out in a single `-t` option.
For example,

```nginx
more_set_headers -t 'text/html text/plain' 'X-Foo: Bar';
```

Never use other paramemters like `charset=utf-8` in the `-t` option values; they will not
work as you would expect.

Input headers can be modified as well. For example

```nginx
 location /foo {
     more_set_input_headers 'Host: foo' 'User-Agent: faked';
     # now $host, $http_host, $user_agent, and
     #   $http_user_agent all have their new values.
 }
```

The option `-t` is also available in the
[more_set_input_headers](#more_set_input_headers) and
[more_clear_input_headers](#more_clear_input_headers) directives (for request header filtering) while the `-s` option
is not allowed.

Unlike the standard [headers](http://nginx.org/en/docs/http/ngx_http_headers_module.html) module, this module's directives will by
default apply to all the status codes, including `4xx` and `5xx`.


## Directives


## more_set_headers
**syntax:** *more_set_headers [-t &lt;content-type list&gt;]... [-s &lt;status-code list&gt;]... &lt;new-header&gt;...*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

Replaces (if any) or adds (if not any) the specified output headers when the response status code matches the codes specified by the `-s` option *AND* the response content type matches the types specified by the `-t` option.

If either `-s` or `-t` is not specified or has an empty list value, then no match is required. Therefore, the following directive set the `Server` output header to the custom value for *any* status code and *any* content type:

```nginx

   more_set_headers    "Server: my_server";
```

Existing response headers with the same name are always overridden. If you want to add headers incrementally, use the standard [add_header](http://nginx.org/en/docs/http/ngx_http_headers_module.html#add_header) directive instead.

A single directive can set/add multiple output headers. For example

```nginx

   more_set_headers 'Foo: bar' 'Baz: bah';
```

Multiple occurrences of the options are allowed in a single directive. Their values will be merged together. For instance

```nginx

   more_set_headers -s 404 -s '500 503' 'Foo: bar';
```

is equivalent to

```nginx

   more_set_headers -s '404 500 503' 'Foo: bar';
```

The new header should be the one of the forms:

1. `Name: Value`
1. `Name: `
1. `Name`

The last two effectively clear the value of the header `Name`.

Nginx variables are allowed in header values. For example:

```nginx

    set $my_var "dog";
    more_set_headers "Server: $my_var";
```

But variables won't work in header keys due to performance considerations.

Multiple set/clear header directives are allowed in a single location, and they're executed sequentially.

Directives inherited from an upper level scope (say, http block or server blocks) are executed before the directives in the location block.

Note that although `more_set_headers` is allowed in *location* if blocks, it is *not* allowed in the *server* if blocks, as in

```nginx

   ?  # This is NOT allowed!
   ?  server {
   ?      if ($args ~ 'download') {
   ?          more_set_headers 'Foo: Bar';
   ?      }
   ?      ...
   ?  }
```

Behind the scene, use of this directive and its friend [more_clear_headers](#more_clear_headers) will (lazily) register an ouput header filter that modifies `r->headers_out` the way you specify.


## more_clear_headers
**syntax:** *more_clear_headers [-t &lt;content-type list&gt;]... [-s &lt;status-code list&gt;]... &lt;new-header&gt;...*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

Clears the specified output headers.

In fact,

```nginx

    more_clear_headers -s 404 -t 'text/plain' Foo Baz;
```

is exactly equivalent to

```nginx

    more_set_headers -s 404 -t 'text/plain' "Foo: " "Baz: ";
```

or

```nginx

    more_set_headers -s 404 -t 'text/plain' Foo Baz
```

See [more_set_headers](#more_set_headers) for more details.

The wildcard character, `*`, can also be used at the end of the header name to specify a pattern. For example, the following directive
effectively clears *any* output headers starting by "`X-Hidden-`":

```nginx

 more_clear_headers 'X-Hidden-*';
```

The `*` wildcard support was first introduced in [v0.09](#v009).


## more_set_input_headers
**syntax:** *more_set_input_headers [-r] [-t &lt;content-type list&gt;]... &lt;new-header&gt;...*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *rewrite tail*

Very much like [more_set_headers](#more_set_headers) except that it operates on input headers (or request headers) and it only supports the `-t` option.

Note that using the `-t` option in this directive means filtering by the `Content-Type` *request* header, rather than the response header.

Behind the scene, use of this directive and its friend [more_clear_input_headers](#more_clear_input_headers) will (lazily)
register a `rewrite phase` handler that modifies `r->headers_in` the way you specify. Note that it always run at the *end* of
the `rewrite` phase so that it runs *after* the standard [rewrite module](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html)
and works in subrequests as well.

If the `-r` option is specified, then the headers will be replaced to the new values *only if* they already exist.


## more_clear_input_headers
**syntax:** *more_clear_input_headers [-t &lt;content-type list&gt;]... &lt;new-header&gt;...*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *rewrite tail*

Clears the specified input headers.

In fact,

```nginx

    more_clear_input_headers -t 'text/plain' Foo Baz;
```

is exactly equivalent to

```nginx

    more_set_input_headers -t 'text/plain' "Foo: " "Baz: ";
```

or

```nginx

    more_set_input_headers -t 'text/plain' Foo Baz
```

To remove request headers "Foo" and "Baz" for all incoming requests regardless of the content type, we can write

```nginx

    more_clear_input_headers "Foo" "Baz";
```

See [more_set_input_headers](#more_set_input_headers) for more details.

The wildcard character, `*`, can also be used at the end of the header name to specify a pattern. For example, the following directive
effectively clears *any* input headers starting by "`X-Hidden-`":

```nginx

     more_clear_input_headers 'X-Hidden-*';
```


## Limitations

* Unlike the standard [headers](http://nginx.org/en/docs/http/ngx_http_headers_module.html) module, this module does not automatically take care of the constraint among the `Expires`, `Cache-Control`, and `Last-Modified` headers. You have to get them right yourself or use the [headers](http://nginx.org/en/docs/http/ngx_http_headers_module.html) module together with this module.
* You cannot remove the `Connection` response header using this module because the `Connection` response header is generated by the standard `ngx_http_header_filter_module` in the Nginx core, whose output header filter runs always *after* the filter of this module. The only way to actually remove the `Connection` header is to patch the Nginx core, that is, editing the C function `ngx_http_header_filter` in the `src/http/ngx_http_header_filter_module.c` file.


## Changes

The changes of every release of this module can be obtained from the OpenResty bundle's change logs:

<http://openresty.org/#Changes>


## Test Suite

This module comes with a Perl-driven test suite. The [test cases](https://github.com/openresty/headers-more-nginx-module/tree/master/t/) are
[declarative](https://github.com/openresty/headers-more-nginx-module/blob/master/t/sanity.t) too. Thanks to the [Test::Nginx](http://search.cpan.org/perldoc?Test::Nginx) module in the Perl world.

To run it on your side:

```bash

 $ PATH=/path/to/your/nginx-with-headers-more-module:$PATH prove -r t
```

To run the test suite with valgrind's memcheck, use the following commands:

```bash

 $ export PATH=/path/to/your/nginx-with-headers-more-module:$PATH
 $ TEST_NGINX_USE_VALGRIND=1 prove -r t
```

You need to terminate any Nginx processes before running the test suite if you have changed the Nginx server binary.

Because a single nginx server (by default, `localhost:1984`) is used across all the test scripts (`.t` files), it's meaningless to run the test suite in parallel by specifying `-jN` when invoking the `prove` utility.

Some parts of the test suite requires modules [proxy](http://nginx.org/en/docs/http/ngx_http_proxy_module.html), [rewrite](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html), and [echo](https://github.com/openresty/echo-nginx-module) to be enabled as well when building Nginx.


## See Also

* The original thread on the Nginx mailing list that inspires this module's development: ["A question about add_header replication"](http://forum.nginx.org/read.php?2,11206,11738).
* The orginal announcement thread on the Nginx mailing list: ["The "headers_more" module: Set and clear output headers...more than 'add'!"](http://forum.nginx.org/read.php?2,23460).
* The original [blog post](http://agentzh.blogspot.com/2009/11/headers-more-module-scripting-input-and.html) about this module's initial development.
* The [echo module](https://github.com/openresty/echo-nginx-module) for Nginx module's automated testing.
* The standard [headers](http://nginx.org/en/docs/http/ngx_http_headers_module.html) module.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-headers-more](https://github.com/dvershinin/headers-more-nginx-module){target=_blank}.