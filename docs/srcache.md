# _srcache_: Transparent subrequest-based caching layout for arbitrary NGINX locations


## Installation

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-srcache
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

    load_module modules/ngx_http_srcache_filter_module.so;

<hr />

**ngx\_srcache** - Transparent subrequest-based caching layout for
arbitrary nginx locations


# Status

This module is production ready.

# Version

This document describes srcache-nginx-module
[v0.31](https://github.com/openresty/srcache-nginx-module/tags) released
on 15 May 2016.

# Synopsis

``` nginx

 upstream my_memcached {
     server 10.62.136.7:11211;
     keepalive 10;
 }

 location = /memc {
     internal;

     memc_connect_timeout 100ms;
     memc_send_timeout 100ms;
     memc_read_timeout 100ms;
     memc_ignore_client_abort on;

     set $memc_key $query_string;
     set $memc_exptime 300;

     memc_pass my_memcached;
 }

 location /foo {
     set $key $uri$args;
     srcache_fetch GET /memc $key;
     srcache_store PUT /memc $key;
     srcache_store_statuses 200 301 302;

     # proxy_pass/fastcgi_pass/drizzle_pass/echo/etc...
     # or even static files on the disk
 }
```

``` nginx

 location = /memc2 {
     internal;

     memc_connect_timeout 100ms;
     memc_send_timeout 100ms;
     memc_read_timeout 100ms;
     memc_ignore_client_abort on;

     set_unescape_uri $memc_key $arg_key;
     set $memc_exptime $arg_exptime;

     memc_pass unix:/tmp/memcached.sock;
 }

 location /bar {
     set_escape_uri $key $uri$args;
     srcache_fetch GET /memc2 key=$key;
     srcache_store PUT /memc2 key=$key&exptime=$srcache_expire;

     # proxy_pass/fastcgi_pass/drizzle_pass/echo/etc...
     # or even static files on the disk
 }
```

``` nginx

 map $request_method $skip_fetch {
     default     0;
     POST        1;
     PUT         1;
 }

 server {
     listen 8080;

     location /api/ {
         set $key "$uri?$args";

         srcache_fetch GET /memc $key;
         srcache_store PUT /memc $key;

         srcache_methods GET PUT POST;
         srcache_fetch_skip $skip_fetch;

         # proxy_pass/drizzle_pass/content_by_lua/echo/...
     }
 }
```


# Description

This module provides a transparent caching layer for arbitrary nginx
locations (like those use an upstream or even serve static disk files).
The caching behavior is mostly compatible with
[RFC 2616](http://www.ietf.org/rfc/rfc2616.txt).

Usually,
[memc-nginx-module](https://github.com/openresty/memc-nginx-module) is
used together with this module to provide a concrete caching storage
backend. But technically, any modules that provide a REST interface can
be used as the fetching and storage subrequests used by this module.

For main requests, the [srcache\_fetch](#srcache_fetch) directive works
at the end of the access phase, so the [standard access
module](http://nginx.org/en/docs/http/ngx_http_access_module.html)'s
[allow](http://nginx.org/en/docs/http/ngx_http_access_module.html#allow)
and
[deny](http://nginx.org/en/docs/http/ngx_http_access_module.html#deny)
direcives run *before* ours, which is usually the desired behavior for
security reasons.

The workflow of this module looks like below:

![srcache flowchart](http://agentzh.org/misc/image/srcache-flowchart.png
"srcache flowchart")


## Subrequest caching

For *subrequests*, we explicitly **disallow** the use of this module
because it's too difficult to get right. There used to be an
implementation but it was buggy and I finally gave up fixing it and
abandoned it.

However, if you're using
[lua-nginx-module](https://github.com/openresty/lua-nginx-module), it's
easy to do subrequest caching in Lua all by yourself. That is, first
issue a subrequest to an
[memc-nginx-module](https://github.com/openresty/memc-nginx-module)
location to do an explicit cache lookup, if cache hit, just use the
cached data returned; otherwise, fall back to the true backend, and
finally do a cache insertion to feed the data into the cache.

Using this module for main request caching and Lua for subrequest
caching is the approach that we're taking in our business. This hybrid
solution works great in production.


## Distributed Memcached Caching

Here is a simple example demonstrating a distributed memcached caching
mechanism built atop this module. Suppose we do have three different
memcached nodes and we use simple modulo to hash our keys.

``` nginx

 http {
     upstream moon {
         server 10.62.136.54:11211;
         server unix:/tmp/memcached.sock backup;
     }

     upstream earth {
         server 10.62.136.55:11211;
     }

     upstream sun {
         server 10.62.136.56:11211;
     }

     upstream_list universe moon earth sun;

     server {
         memc_connect_timeout 100ms;
         memc_send_timeout 100ms;
         memc_read_timeout 100ms;

         location = /memc {
             internal;

             set $memc_key $query_string;
             set_hashed_upstream $backend universe $memc_key;
             set $memc_exptime 3600; # in seconds
             memc_pass $backend;
         }

         location / {
             set $key $uri;
             srcache_fetch GET /memc $key;
             srcache_store PUT /memc $key;

             # proxy_pass/fastcgi_pass/content_by_lua/drizzle_pass/...
         }
     }
 }
```

Here's what is going on in the sample above:

1.  We first define three upstreams, `moon`, `earth`, and `sun`. These
    are our three memcached servers.
2.  And then we group them together as an upstream list entity named
    `universe` with the `upstream_list` directive provided by
    [set-misc-nginx-module](https://github.com/openresty/set-misc-nginx-module).
3.  After that, we define an internal location named `/memc` for talking
    to the memcached cluster.
4.  In this `/memc` location, we first set the `$memc_key` variable with
    the query string (`$args`), and then use the
    [set\_hashed\_upstream](https://github.com/openresty/set-misc-nginx-module#set_hashed_upstream)
    directive to hash our
    [$memc\_key](https://github.com/openresty/memc-nginx-module#memc_key)
    over the upsteam list `universe`, so as to obtain a concrete
    upstream name to be assigned to the variable `$backend`.
5.  We pass this `$backend` variable into the
    [memc\_pass](https://github.com/openresty/memc-nginx-module#memc_pass)
    directive. The `$backend` variable can hold a value among `moon`,
    `earth`, and `sun`.
6.  Also, we define the memcached caching expiration time to be 3600
    seconds (i.e., an hour) by overriding the
    [$memc\_exptime](https://github.com/openresty/memc-nginx-module#memc_exptime)
    variable.
7.  In our main public location `/`, we configure the `$uri` variable as
    our cache key, and then configure [srcache\_fetch](#srcache_fetch)
    for cache lookups and [srcache\_store](#srcache_store) for cache
    updates. We're using two subrequests to our `/memc` location defined
    earlier in these two directives.

One can use
[lua-nginx-module](https://github.com/openresty/lua-nginx-module)'s
[set\_by\_lua](https://github.com/openresty/lua-nginx-module#set_by_lua)
or
[rewrite\_by\_lua](https://github.com/openresty/lua-nginx-module#rewrite_by_lua)
directives to inject custom Lua code to compute the `$backend` and/or
`$key` variables in the sample above.

One thing that should be taken care of is that memcached does have
restriction on key lengths, i.e., 250 bytes, so for keys that may be
very long, one could use the
[set\_md5](https://github.com/openresty/set-misc-nginx-module#set_md5)
directive or its friends to pre-hash the key to a fixed-length digest
before assigning it to `$memc_key` in the `/memc` location or the like.

Further, one can utilize the [srcache\_fetch\_skip](#srcache_fetch_skip)
and [srcache\_store\_skip](#srcache_store_skip) directives to control
what to cache and what not on a per-request basis, and Lua can also be
used here in a similar way. So the possibility is really unlimited.

To maximize speed, we often enable TCP (or Unix Domain Socket)
connection pool for our memcached upstreams provided by
[HttpUpstreamKeepaliveModule](http://wiki.nginx.org/HttpUpstreamKeepaliveModule),
for example,

``` nginx

 upstream moon {
     server 10.62.136.54:11211;
     server unix:/tmp/memcached.sock backup;
     keepalive 10;
 }
```

where we define a connection pool which holds up to 10 keep-alive
connections (per nginx worker process) for our `moon` upstream
(cluster).


## Caching with Redis

Redis is an alternative key-value store with many additional features.

Here is a working example by using Redis:

``` nginx

 location /api {
     default_type text/css;

     set $key $uri;
     set_escape_uri $escaped_key $key;

     srcache_fetch GET /redis $key;
     srcache_store PUT /redis2 key=$escaped_key&exptime=120;

     # fastcgi_pass/proxy_pass/drizzle_pass/postgres_pass/echo/etc
 }

 location = /redis {
     internal;

     set_md5 $redis_key $args;
     redis_pass 127.0.0.1:6379;
 }

 location = /redis2 {
     internal;

     set_unescape_uri $exptime $arg_exptime;
     set_unescape_uri $key $arg_key;
     set_md5 $key;

     redis2_query set $key $echo_request_body;
     redis2_query expire $key $exptime;
     redis2_pass 127.0.0.1:6379;
 }
```

This example makes use of the
[$echo\_request\_body](https://github.com/openresty/echo-nginx-module#echo_request_body)
variable provided by
[echo-nginx-module](https://github.com/openresty/echo-nginx-module).
Note that you need the latest version of
[echo-nginx-module](https://github.com/openresty/echo-nginx-module),
`v0.38rc2` because earlier versions may not work reliably.

Also, you need both
[HttpRedisModule](http://wiki.nginx.org/HttpRedisModule) and
[redis2-nginx-module](https://github.com/openresty/redis2-nginx-module).
The former is used in the [srcache\_fetch](#srcache_fetch) subrequest
and the latter is used in the [srcache\_store](#srcache_store)
subrequest.

The Nginx core also has a bug that could prevent
[redis2-nginx-module](https://github.com/openresty/redis2-nginx-module)'s
pipelining support from working properly in certain extreme conditions.
And the following patch fixes this:

<http://mailman.nginx.org/pipermail/nginx-devel/2012-March/002040.html>

Note that, however, if you are using the
[OpenResty](http://openresty.org/) 1.0.15.3 bundle or later, then you
already have everything that you need here in the bundle.


## Cache Key Preprocessing

It is often desired to preprocess the cache key to exclude random noises
that may hurt the cache hit rate. For example, random session IDs in the
URI arguments are usually desired to get removed.

Consider the following URI
    querystring

    SID=BC3781C3-2E02-4A11-89CF-34E5CFE8B0EF&UID=44332&L=EN&M=1&H=1&UNC=0&SRC=LK&RT=62

we want to remove the `SID` and `UID` arguments from it. It is easy to
achieve if you use
[lua-nginx-module](https://github.com/openresty/lua-nginx-module) at the
same time:

``` nginx

 location = /t {
     rewrite_by_lua '
         local args = ngx.req.get_uri_args()
         args.SID = nil
         args.UID = nil
         ngx.req.set_uri_args(args)
     ';

     echo $args;
 }
```

Here we use the
[echo](https://github.com/openresty/echo-nginx-module#echo) directive
from [echo-nginx-module](https://github.com/openresty/echo-nginx-module)
to dump out the final value of
[$args](http://nginx.org/en/docs/http/ngx_http_core_module.html#var_args)
in the end. You can replace it with your
[srcache-nginx-module](https://github.com/openresty/srcache-nginx-module)
configurations and upstream configurations instead for your case. Let's
test this /t interface with
    curl:

    $ curl 'localhost:8081/t?RT=62&SID=BC3781C3-2E02-4A11-89CF-34E5CFE8B0EF&UID=44332&L=EN&M=1&H=1&UNC=0&SRC=LK'
    M=1&UNC=0&RT=62&H=1&L=EN&SRC=LK

It is worth mentioning that, if you want to retain the order of the URI
arguments, then you can do string substitutions on the value of
[$args](http://nginx.org/en/docs/http/ngx_http_core_module.html#var_args)
directly, for example,

    location = /t {
        rewrite_by_lua '
            local args = ngx.var.args
            newargs, n, err = ngx.re.gsub(args, [[\b[SU]ID=[^&]*&?]], "", "jo")
            if n and n > 0 then
                ngx.var.args = newargs
            end
        ';
    
        echo $args;
    }

Now test it with the original curl command again, we get exactly what we
would expect:

    RT=62&L=EN&M=1&H=1&UNC=0&SRC=LK

But for caching purposes, it's good to normalize the URI argument order
so that you can increase the cache hit rate. And the hash table entry
order used by LuaJIT or Lua can be used to normalize the order as a nice
side effect.


# Directives


## srcache\_fetch

**syntax:** *srcache\_fetch \<method\> \<uri\> \<args\>?*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *post-access*

This directive registers an access phase handler that will issue an
Nginx subrequest to lookup the cache.

When the subrequest returns status code other than `200`, than a cache
miss is signaled and the control flow will continue to the later phases
including the content phase configured by
[ngx\_http\_proxy\_module](http://nginx.org/en/docs/http/ngx_http_proxy_module.html),
[ngx\_http\_fastcgi\_module](http://nginx.org/en/docs/http/ngx_http_fastcgi_module.html),
and others. If the subrequest returns `200 OK`, then a cache hit is
signaled and this module will send the subrequest's response as the
current main request's response to the client directly.

This directive will always run at the end of the access phase, such that
[ngx\_http\_access\_module](http://nginx.org/en/docs/http/ngx_http_access_module.html)'s
[allow](http://nginx.org/en/docs/http/ngx_http_access_module.html#allow)
and
[deny](http://nginx.org/en/docs/http/ngx_http_access_module.html#deny)
will always run *before* this.

You can use the [srcache\_fetch\_skip](#srcache_fetch_skip) directive to
disable cache look-up selectively.


## srcache\_fetch\_skip

**syntax:** *srcache\_fetch\_skip \<flag\>*

**default:** *srcache\_fetch\_skip 0*

**context:** *http, server, location, location if*

**phase:** *post-access*

The `<flag>` argument supports nginx variables. When this argument's
value is not empty *and* not equal to `0`, then the fetching process
will be unconditionally skipped.

For example, to skip caching requests which have a cookie named `foo`
with the value `bar`, we can write

``` nginx

 location / {
     set $key ...;
     set_by_lua $skip '
         if ngx.var.cookie_foo == "bar" then
             return 1
         end
         return 0
     ';

     srcache_fetch_skip $skip;
     srcache_store_skip $skip;

     srcache_fetch GET /memc $key;
     srcache_store GET /memc $key;

     # proxy_pass/fastcgi_pass/content_by_lua/...
 }
```

where [lua-nginx-module](https://github.com/openresty/lua-nginx-module)
is used to calculate the value of the `$skip` variable at the (earlier)
rewrite phase. Similarly, the `$key` variable can be computed by Lua
using the
[set\_by\_lua](https://github.com/openresty/lua-nginx-module#set_by_lua)
or
[rewrite\_by\_lua](https://github.com/openresty/lua-nginx-module#rewrite_by_lua)
directive too.

The standard
[map](http://nginx.org/en/docs/http/ngx_http_map_module.html#map)
directive can also be used to compute the value of the `$skip` variable
used in the sample above:

``` nginx

 map $cookie_foo $skip {
     default     0;
     bar         1;
 }
```

but your
[map](http://nginx.org/en/docs/http/ngx_http_map_module.html#map)
statement should be put into the `http` config block in your
`nginx.conf` file though.


## srcache\_store

**syntax:** *srcache\_store \<method\> \<uri\> \<args\>?*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *output-filter*

This directive registers an output filter handler that will issue an
Nginx subrequest to save the response of the current main request into a
cache backend. The status code of the subrequest will be ignored.

You can use the [srcache\_store\_skip](#srcache_store_skip) and
[srcache\_store\_max\_size](#srcache_store_max_size) directives to
disable caching for certain requests in case of a cache miss.

Since the `v0.12rc7` release, both the response status line, response
headers, and response bodies will be put into the cache. By default, the
following special response headers will not be cached:

  - Connection
  - Keep-Alive
  - Proxy-Authenticate
  - Proxy-Authorization
  - TE
  - Trailers
  - Transfer-Encoding
  - Upgrade
  - Set-Cookie

You can use the
[srcache\_store\_pass\_header](#srcache_store_pass_header) and/or
[srcache\_store\_hide\_header](#srcache_store_hide_header) directives to
control what headers to cache and what not.

The original response's data chunks get emitted as soon as they arrive.
`srcache_store` just copies and collects the data in an output filter
without postponing them from being sent downstream.

But please note that even though all the response data will be sent
immediately, the current Nginx request lifetime will not finish until
the srcache\_store subrequest completes. That means a delay in closing
the TCP connection on the server side (when HTTP keepalive is disabled,
but proper HTTP clients should close the connection actively on the
client side, which adds no extra delay or other issues at all) or
serving the next request sent on the same TCP connection (when HTTP
keepalive is in action).


## srcache\_store\_max\_size

**syntax:** *srcache\_store\_max\_size \<size\>*

**default:** *srcache\_store\_max\_size 0*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

When the response body length is exceeding this size, this module will
not try to store the response body into the cache using the subrequest
template that is specified in [srcache\_store](#srcache_store).

This is particular useful when using a cache storage backend that does
have a hard upper limit on the input data. For example, the Memcached
server has a default limit of `1 MB` by item.

When `0` is specified (the default value), there's no limit check at
all.


## srcache\_store\_skip

**syntax:** *srcache\_store\_skip \<flag\>*

**default:** *srcache\_store\_skip 0*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

The `<flag>` argument supports Nginx variables. When this argument's
value is not empty *and* not equal to `0`, then the storing process will
be unconditionally skipped.

Starting from the `v0.25` release, the `<flag>` expression (possibly
containing Nginx variables) can be evaluated up to twice: the first time
is right after the response header is being sent and when the `<flag>`
expression is not evaluated to true values it will be evaluated again
right after the end of the response body data stream is seen. Before
`v0.25`, only the first time evaluation is performed.

Here's an example using Lua to set $nocache to avoid storing URIs that
contain the string "/tmp":

``` nginx

 set_by_lua $nocache '
     if string.match(ngx.var.uri, "/tmp") then
         return 1
     end
     return 0';

 srcache_store_skip $nocache;
```


## srcache\_store\_statuses

**syntax:** *srcache\_store\_statuses \<status1\> \<status2\> ..*

**default:** *srcache\_store\_statuses 200 301 302*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

This directive controls what responses to store to the cache according
to their status code.

By default, only `200`, `301`, and `302` responses will be stored to
cache and any other responses will skip
[srcache\_store](#srcache_store).

You can specify arbitrary positive numbers for the response status code
that you'd like to cache, even including error code like `404` and
`503`. For example:

``` nginx

 srcache_store_statuses 200 201 301 302 404 503;
```

At least one argument should be given to this directive.

This directive was first introduced in the `v0.13rc2` release.


## srcache\_store\_ranges

**syntax:** *srcache\_store\_ranges on|off*

**default:** *srcache\_store\_ranges off*

**context:** *http, server, location, location if*

**phase:** *output-body-filter*

When this directive is turned on (default to `off`),
[srcache\_store](#srcache_store) will also store 206 Partial Content
responses generated by the standard `ngx_http_range_filter_module`. If
you turn this directive on, you MUST add `$http_range` to your cache
keys. For example,

``` nginx

 location / {
     set $key "$uri$args$http_range";
     srcache_fetch GET /memc $key;
     srcache_store PUT /memc $key;
 }
```

This directive was first introduced in the `v0.27` release.


## srcache\_header\_buffer\_size

**syntax:** *srcache\_header\_buffer\_size \<size\>*

**default:** *srcache\_header\_buffer\_size 4k/8k*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

This directive controles the header buffer when serializing response
headers for [srcache\_store](#srcache_store). The default size is the
page size, usually `4k` or `8k` depending on specific platforms.

Note that the buffer is not used to hold all the response headers, but
just each individual header. So the buffer is merely needed to be big
enough to hold the longest response header.

This directive was first introduced in the `v0.12rc7` release.


## srcache\_store\_hide\_header

**syntax:** *srcache\_store\_hide\_header \<header\>*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

By default, this module caches all the response headers except the
following ones:

  - Connection
  - Keep-Alive
  - Proxy-Authenticate
  - Proxy-Authorization
  - TE
  - Trailers
  - Transfer-Encoding
  - Upgrade
  - Set-Cookie

You can hide even more response headers from
[srcache\_store](#srcache_store) by listing their names
(case-insensitive) by means of this directive. For examples,

``` nginx

 srcache_store_hide_header X-Foo;
 srcache_store_hide_header Last-Modified;
```

Multiple occurrences of this directive are allowed in a single location.

This directive was first introduced in the `v0.12rc7` release.

See also [srcache\_store\_pass\_header](#srcache_store_pass_header).


## srcache\_store\_pass\_header

**syntax:** *srcache\_store\_pass\_header \<header\>*

**default:** *no*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

By default, this module caches all the response headers except the
following ones:

  - Connection
  - Keep-Alive
  - Proxy-Authenticate
  - Proxy-Authorization
  - TE
  - Trailers
  - Transfer-Encoding
  - Upgrade
  - Set-Cookie

You can force [srcache\_store](#srcache_store) to store one or more of
these response headers from [srcache\_store](#srcache_store) by listing
their names (case-insensitive) by means of this directive. For examples,

``` nginx

 srcache_store_pass_header Set-Cookie;
 srcache_store_pass_header Proxy-Autenticate;
```

Multiple occurrences of this directive are allowed in a single location.

This directive was first introduced in the `v0.12rc7` release.

See also [srcache\_store\_hide\_header](#srcache_store_hide_header).


## srcache\_methods

**syntax:** *srcache\_methods \<method\>...*

**default:** *srcache\_methods GET HEAD*

**context:** *http, server, location*

**phase:** *post-access, output-header-filter*

This directive specifies HTTP request methods that are considered by
either [srcache\_fetch](#srcache_fetch) or
[srcache\_store](#srcache_store). HTTP request methods not listed will
be skipped completely from the cache.

The following HTTP methods are allowed: `GET`, `HEAD`, `POST`, `PUT`,
and `DELETE`. The `GET` and `HEAD` methods are always implicitly
included in the list regardless of their presence in this directive.

Note that since the `v0.17` release `HEAD` requests are always skipped
by [srcache\_store](#srcache_store) because their responses never carry
a response body.

This directive was first introduced in the `v0.12rc7` release.


## srcache\_ignore\_content\_encoding

**syntax:** *srcache\_ignore\_content\_encoding on|off*

**default:** *srcache\_ignore\_content\_encoding off*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

When this directive is turned `off` (which is the default), non-empty
`Content-Encoding` response header will cause
[srcache\_store](#srcache_store) skip storing the whole response into
the cache and issue a warning into nginx's `error.log` file like
    this:

    [warn] 12500#0: *1 srcache_store skipped due to response header "Content-Encoding: gzip"
                (maybe you forgot to disable compression on the backend?)

Turning on this directive will ignore the `Content-Encoding` response
header and store the response as usual (and also without warning).

It's recommended to always disable gzip/deflate compression on your
backend server by specifying the following line in your `nginx.conf`
file:

``` nginx

 proxy_set_header  Accept-Encoding  "";
```

This directive was first introduced in the `v0.12rc7` release.


## srcache\_request\_cache\_control

**syntax:** *srcache\_request\_cache\_control on|off*

**default:** *srcache\_request\_cache\_control off*

**context:** *http, server, location*

**phase:** *post-access, output-header-filter*

When this directive is turned `on`, the request headers `Cache-Control`
and `Pragma` will be honored by this module in the following ways:

1.  [srcache\_fetch](#srcache_fetch), i.e., the cache lookup operation,
    will be skipped when request headers `Cache-Control: no-cache`
    and/or `Pragma: no-cache` are present.
2.  [srcache\_store](#srcache_store), i.e., the cache store operation,
    will be skipped when the request header `Cache-Control: no-store` is
    specified.

Turning off this directive will disable this functionality and is
considered safer for busy sites mainly relying on cache for speed.

This directive was first introduced in the `v0.12rc7` release.

See also
[srcache\_response\_cache\_control](#srcache_response_cache_control).


## srcache\_response\_cache\_control

**syntax:** *srcache\_response\_cache\_control on|off*

**default:** *srcache\_response\_cache\_control on*

**context:** *http, server, location*

**phase:** *output-header-filter*

When this directive is turned `on`, the response headers `Cache-Control`
and `Expires` will be honored by this module in the following ways:

  - `Cache-Control: private` skips [srcache\_store](#srcache_store),
  - `Cache-Control: no-store` skips [srcache\_store](#srcache_store),
  - `Cache-Control: no-cache` skips [srcache\_store](#srcache_store),
  - `Cache-Control: max-age=0` skips [srcache\_store](#srcache_store),
  - and `Expires: <date-no-more-recently-than-now>` skips
    [srcache\_store](#srcache_store).

This directive takes priority over the
[srcache\_store\_no\_store](#srcache_store_no_store),
[srcache\_store\_no\_cache](#srcache_store_no_cache), and
[srcache\_store\_private](#srcache_store_private) directives.

This directive was first introduced in the `v0.12rc7` release.

See also
[srcache\_request\_cache\_control](#srcache_request_cache_control).


## srcache\_store\_no\_store

**syntax:** *srcache\_store\_no\_store on|off*

**default:** *srcache\_store\_no\_store off*

**context:** *http, server, location*

**phase:** *output-header-filter*

Turning this directive on will force responses with the header
`Cache-Control: no-store` to be stored into the cache when
[srcache\_response\_cache\_control](#srcache_response_cache_control) is
turned `on` *and* other conditions are met. Default to `off`.

This directive was first introduced in the `v0.12rc7` release.


## srcache\_store\_no\_cache

**syntax:** *srcache\_store\_no\_cache on|off*

**default:** *srcache\_store\_no\_cache off*

**context:** *http, server, location*

**phase:** *output-header-filter*

Turning this directive on will force responses with the header
`Cache-Control: no-cache` to be stored into the cache when
[srcache\_response\_cache\_control](#srcache_response_cache_control) is
turned `on` *and* other conditions are met. Default to `off`.

This directive was first introduced in the `v0.12rc7` release.


## srcache\_store\_private

**syntax:** *srcache\_store\_private on|off*

**default:** *srcache\_store\_private off*

**context:** *http, server, location*

**phase:** *output-header-filter*

Turning this directive on will force responses with the header
`Cache-Control: private` to be stored into the cache when
[srcache\_response\_cache\_control](#srcache_response_cache_control) is
turned `on` *and* other conditions are met. Default to `off`.

This directive was first introduced in the `v0.12rc7` release.


## srcache\_default\_expire

**syntax:** *srcache\_default\_expire \<time\>*

**default:** *srcache\_default\_expire 60s*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

This directive controls the default expiration time period that is
allowed for the [$srcache\_expire](#srcache_expire) variable value when
neither `Cache-Control: max-age=N` nor `Expires` are specified in the
response headers.

The `<time>` argument values are in seconds by default. But it's wise to
always explicitly specify the time unit to avoid confusion. Time units
supported are "s"(seconds), "ms"(milliseconds), "y"(years), "M"(months),
"w"(weeks), "d"(days), "h"(hours), and "m"(minutes). For example,

``` nginx

 srcache_default_expire 30m; # 30 minutes
```

This time must be less than 597 hours.

The semantics of a zero expiration time depends on the actual cache
backend storage you are currently using, which is agnostic to this
module. In the case of memcached, for example, zero expiration times
mean that the item will never expire.

This directive was first introduced in the `v0.12rc7` release.


## srcache\_max\_expire

**syntax:** *srcache\_max\_expire \<time\>*

**default:** *srcache\_max\_expire 0*

**context:** *http, server, location, location if*

**phase:** *output-header-filter*

This directive controls the maximal expiration time period that is
allowed for the [$srcache\_expire](#srcache_expire) variable value. This
setting takes priority over other calculating methods.

The `<time>` argument values are in seconds by default. But it's wise to
always explicitly specify the time unit to avoid confusion. Time units
supported are "s"(seconds), "ms"(milliseconds), "y"(years), "M"(months),
"w"(weeks), "d"(days), "h"(hours), and "m"(minutes). For example,

``` nginx

 srcache_max_expire 2h;  # 2 hours
```

This time must be less than 597 hours.

When `0` is specified, which is the default setting, then there will be
*no* limit at all.

This directive was first introduced in the `v0.12rc7` release.


# Variables


## $srcache\_expire

**type:** *integer*

**cacheable:** *no*

**writable:** *no*

This Nginx variable gives the recommended expiration time period (in
seconds) for the current response being stored into the cache. The
algorithm of computing the value is as follows:

1.  When the response header `Cache-Control: max-age=N` is specified,
    then `N` will be used as the expiration time,
2.  otherwise if the response header `Expires` is specified, then the
    expiration time will be obtained by subtracting the current time
    stamp from the time specified in the `Expires` header,
3.  when neither `Cache-Control: max-age=N` nor `Expires` headers are
    specified, use the value specified in the
    [srcache\_default\_expire](#srcache_default_expire) directive.

The final value of this variable will be the value specified by the
[srcache\_max\_expire](#srcache_max_expire) directive if the value
obtained in the algorithm above exceeds the maximal value (if any).

You don't have to use this variable for the expiration time.

This variable was first introduced in the `v0.12rc7` release.


## $srcache\_fetch\_status

**type:** *string*

**cacheable:** *no*

**writable:** *no*

This Nginx variable is evaluated to the status of the "fetch" phase for
the caching system. Three values are possible, `HIT`, `MISS`, and
`BYPASS`.

When the "fetch" subrequest returns status code other than `200` or its
response data is not well-formed, then this variable is evaluated to the
value `MISS`.

The value of this variable is only meaningful after the `access` request
processing phase, or `BYPASS` is always given.

This variable was first introduced in the `v0.14` release.


## $srcache\_store\_status

**type:** *string*

**cacheable:** *no*

**writable:** *no*

This Nginx variable gives the current caching status for the "store"
phase. Two possible values, `STORE` and `BYPASS` can be obtained.

Because the responses for the "store" subrequest are always discarded,
so the value of this variable will always be `STORE` as long as the
"store" subrequest is actually issued.

The value of this variable is only meaningful at least when the request
headers of the current (main) request are being sent. The final result
can only be obtained after all the response body has been sent if the
`Content-Length` response header is not specified for the main request.

This variable was first introduced in the `v0.14` release.


# Known Issues

  - On certain systems, enabling aio and/or sendfile may stop
    [srcache\_store](#srcache_store) from working. You can disable them
    in the locations configured by [srcache\_store](#srcache_store).
  - The [srcache\_store](#srcache_store) directive can not be used to
    capture the responses generated by
    [echo-nginx-module](https://github.com/openresty/echo-nginx-module)'s
    subrequest directivees like
    [echo\_subrequest\_async](https://github.com/openresty/echo-nginx-module#echo_subrequest_async)
    and
    [echo\_location](https://github.com/openresty/echo-nginx-module#echo_location).
    You are recommended to use HttpLuaModule to initiate and capture
    subrequests, which should work with
    [srcache\_store](#srcache_store).


# Caveats

  - It is recommended to disable your backend server's gzip compression
    and use nginx's
    [ngx\_http\_gzip\_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html)
    to do the job. In case of
    [ngx\_http\_proxy\_module](http://nginx.org/en/docs/http/ngx_http_proxy_module.html),
    you can use the following configure setting to disable backend gzip
    compression:

<!-- end list -->

``` nginx

 proxy_set_header  Accept-Encoding  "";
```

  - Do *not* use
    [ngx\_http\_rewrite\_module](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html)'s
    [if](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html#if)
    directive in the same location as this module's, because
    "[if](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html#if)
    is evil". Instead, use
    [ngx\_http\_map\_module](http://nginx.org/en/docs/http/ngx_http_map_module.html)
    or [lua-nginx-module](https://github.com/openresty/lua-nginx-module)
    combined with this module's
    [srcache\_store\_skip](#srcache_store_skip) and/or
    [srcache\_fetch\_skip](#srcache_fetch_skip) directives. For example:

<!-- end list -->

``` nginx

 map $request_method $skip_fetch {
     default     0;
     POST        1;
     PUT         1;
 }

 server {
     listen 8080;

     location /api/ {
         set $key "$uri?$args";

         srcache_fetch GET /memc $key;
         srcache_store PUT /memc $key;

         srcache_methods GET PUT POST;
         srcache_fetch_skip $skip_fetch;

         # proxy_pass/drizzle_pass/content_by_lua/echo/...
     }
 }
```


# Trouble Shooting

To debug issues, you should always check your Nginx `error.log` file
first. If no error messages are printed, you need to enable the Nginx
debugging logs to get more details, as explained in [debugging
log](http://nginx.org/en/docs/debugging_log.html).

Several common pitfalls for beginners:

  - The original response carries a `Cache-Control` header that
    explicitly disables caching and you do not configure directives like
    [srcache\_response\_cache\_control](#srcache_response_cache_control).
  - The original response is already gzip compressed, which is not
    cached by default (see
    [srcache\_ignore\_content\_encoding](#srcache_ignore_content_encoding)).
  - Memcached might return `CLIENT_ERROR bad command line format` when
    using a too long key (250 chars as of version 1.4.25). It is thus
    safer to use `set_md5 $key $uri$args;` instead of `set $key
    $uri$args;`. The `set_md5` directive (and more) is available from
    [OpenResty's set-misc
    module](https://github.com/openresty/set-misc-nginx-module).
  - Nginx might return `client intended to send too large body` when
    trying to store objects larger than 1m to the storage backend, in
    which case nginx `client_max_body_size` must be set to a higher
    value.
  - Memcached might fail to store objects larger than 1m, causing errors
    like `srcache_store subrequest failed status=502`. Since version
    1.4.2, memcached supports a command-line `-I` option to override the
    default size of each slab page. Please read its manpage for more
    information.


# Community


## English Mailing List

The [openresty-en](https://groups.google.com/group/openresty-en) mailing
list is for English speakers.


## Chinese Mailing List

The [openresty](https://groups.google.com/group/openresty) mailing list
is for Chinese speakers.


# Bugs and Patches

Please submit bug reports, wishlists, or patches by

1.  creating a ticket on the [GitHub Issue
    Tracker](https://github.com/openresty/srcache-nginx-module/issues),
2.  or posting to the [OpenResty community](#community).


# Source Repository

Available on github at
[openresty/srcache-nginx-module](https://github.com/openresty/srcache-nginx-module).


# Test Suite

This module comes with a Perl-driven test suite. The [test
cases](https://github.com/openresty/srcache-nginx-module/tree/master/test/t)
are
[declarative](https://github.com/openresty/srcache-nginx-module/blob/master/test/t/main-req.t)
too. Thanks to the
[Test::Nginx](http://search.cpan.org/perldoc?Test::Base) module in the
Perl world.

To run it on your side:

``` bash

 $ PATH=/path/to/your/nginx-with-srcache-module:$PATH prove -r t
```

You need to terminate any Nginx processes before running the test suite
if you have changed the Nginx server binary.

Because a single nginx server (by default, `localhost:1984`) is used
across all the test scripts (`.t` files), it's meaningless to run the
test suite in parallel by specifying `-jN` when invoking the `prove`
utility.

Some parts of the test suite requires modules
[ngx\_http\_rewrite\_module](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html),
[echo-nginx-module](https://github.com/openresty/echo-nginx-module),
[rds-json-nginx-module](https://github.com/openresty/rds-json-nginx-module),
and
[drizzle-nginx-module](https://github.com/openresty/drizzle-nginx-module)
to be enabled as well when building Nginx.


# TODO

  - add gzip compression and decompression support.
  - add new nginx variable `$srcache_key` and new directives
    `srcache_key_ignore_args`, `srcache_key_filter_args`, and
    `srcache_key_sort_args`.


# Getting involved

You'll be very welcomed to submit patches to the author or just ask for
a commit bit to the source repository on GitHub.


# Author

Yichun "agentzh" Zhang (章亦春) <agentzh@gmail.com>, CloudFlare Inc.


# Copyright & License

Copyright (c) 2010-2016, Yichun "agentzh" Zhang (章亦春)
<agentzh@gmail.com>, CloudFlare Inc.

This module is licensed under the terms of the BSD license.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  - Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  - Redistributions in binary form must reproduce the above copyright
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

[Back to
    TOC](#table-of-contents)

# See Also

  - [memc-nginx-module](https://github.com/openresty/memc-nginx-module)
  - [lua-nginx-module](https://github.com/openresty/lua-nginx-module)
  - [set-misc-nginx-module](https://github.com/openresty/set-misc-nginx-module)
  - The [openresty bundle](http://openresty.org)


## GitHub

You may find additional configuration tips and documentation in the [GitHub repository for 
nginx-module-srcache](https://github.com/openresty/srcache-nginx-module).