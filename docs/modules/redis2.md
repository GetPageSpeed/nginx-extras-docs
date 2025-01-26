---

title: "NGINX upstream module for the Redis 2.0 protocol"
description: "RPM package nginx-module-redis2. NGINX upstream module for the Redis 2.0 protocol "

---

# *redis2*: NGINX upstream module for the Redis 2.0 protocol


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
    dnf -y install nginx-module-redis2
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-redis2
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_redis2_module.so;
```


This document describes nginx-module-redis2 [v0.15](https://github.com/openresty/redis2-nginx-module/releases/tag/v0.15){target=_blank} 
released on Apr 19 2018.

<hr />

ngx_redis2 - Nginx upstream module for the Redis 2.0 protocol


## Status

This module is already production ready.

## Synopsis

```nginx

 location = /foo {
     set $value 'first';
     redis2_query set one $value;
     redis2_pass 127.0.0.1:6379;
 }

 # GET /get?key=some_key
 location = /get {
     set_unescape_uri $key $arg_key;  # this requires ngx_set_misc
     redis2_query get $key;
     redis2_pass foo.com:6379;
 }

 # GET /set?key=one&val=first%20value
 location = /set {
     set_unescape_uri $key $arg_key;  # this requires ngx_set_misc
     set_unescape_uri $val $arg_val;  # this requires ngx_set_misc
     redis2_query set $key $val;
     redis2_pass foo.com:6379;
 }

 # multiple pipelined queries
 location = /foo {
     set $value 'first';
     redis2_query set one $value;
     redis2_query get one;
     redis2_query set one two;
     redis2_query get one;
     redis2_pass 127.0.0.1:6379;
 }

 location = /bar {
     # $ is not special here...
     redis2_literal_raw_query '*1\r\n$4\r\nping\r\n';
     redis2_pass 127.0.0.1:6379;
 }

 location = /bar {
     # variables can be used below and $ is special
     redis2_raw_query 'get one\r\n';
     redis2_pass 127.0.0.1:6379;
 }

 # GET /baz?get%20foo%0d%0a
 location = /baz {
     set_unescape_uri $query $query_string; # this requires the ngx_set_misc module
     redis2_raw_query $query;
     redis2_pass 127.0.0.1:6379;
 }

 location = /init {
     redis2_query del key1;
     redis2_query lpush key1 C;
     redis2_query lpush key1 B;
     redis2_query lpush key1 A;
     redis2_pass 127.0.0.1:6379;
 }

 location = /get {
     redis2_query lrange key1 0 -1;
     redis2_pass 127.0.0.1:6379;
 }
```


## Description

This is an Nginx upstream module that makes nginx talk to a [Redis](http://redis.io/) 2.x server in a non-blocking way. The full Redis 2.0 unified protocol has been implemented including the Redis pipelining support.

This module returns the raw TCP response from the Redis server. It's recommended to use my [lua-redis-parser](http://github.com/openresty/lua-redis-parser) (written in pure C) to parse these responses into lua data structure when combined with [lua-nginx-module](http://github.com/openresty/lua-nginx-module).

When used in conjunction with [lua-nginx-module](http://github.com/openresty/lua-nginx-module), it is recommended to use the [lua-resty-redis](http://github.com/openresty/lua-resty-redis) library instead of this module though, because the former is much more flexible and memory-efficient.

If you only want to use the `get` redis command, you can try out the [HttpRedisModule](http://wiki.nginx.org/HttpRedisModule). It returns the parsed content part of the Redis response because only `get` is needed to implement.

Another option is to parse the redis responses on your client side yourself.


## Directives


## redis2_query
**syntax:** *redis2_query cmd arg1 arg2 ...*

**default:** *no*

**context:** *location, location if*

Specify a Redis command by specifying its individual arguments (including the Redis command name itself) in a similar way to the `redis-cli` utility.

Multiple instances of this directive are allowed in a single location and these queries will be pipelined. For example,

```nginx

 location = /pipelined {
     redis2_query set hello world;
     redis2_query get hello;

     redis2_pass 127.0.0.1:$TEST_NGINX_REDIS_PORT;
 }
```

then `GET /pipelined` will yield two successive raw Redis responses

```nginx

 +OK
 $5
 world
```

while newlines here are actually `CR LF` (`\r\n`).


## redis2_raw_query
**syntax:** *redis2_raw_query QUERY*

**default:** *no*

**context:** *location, location if*

Specify raw Redis queries and nginx variables are recognized in the `QUERY` argument.

Only *one* Redis command is allowed in the `QUERY` argument, or you'll receive an error. If you want to specify multiple pipelined commands in a single query, use the [redis2_raw_queries](#redis2_raw_queries) directive instead.


## redis2_raw_queries
**syntax:** *redis2_raw_queries N QUERIES*

**default:** *no*

**context:** *location, location if*

Specify `N` commands in the `QUERIES` argument. Both the `N` and `QUERIES`
arguments can take Nginx variables.

Here's some examples
```nginx

 location = /pipelined {
     redis2_raw_queries 3 "flushall\r\nget key1\r\nget key2\r\n";
     redis2_pass 127.0.0.1:6379;
 }

 # GET /pipelined2?n=2&cmds=flushall%0D%0Aget%20key%0D%0A
 location = /pipelined2 {
     set_unescape_uri $n $arg_n;
     set_unescape_uri $cmds $arg_cmds;

     redis2_raw_queries $n $cmds;

     redis2_pass 127.0.0.1:6379;
 }
```
Note that in the second sample above, the [set_unescape_uri](http://github.com/openresty/set-misc-nginx-module#set_unescape_uri) directive is provided by the [set-misc-nginx-module](http://github.com/openresty/set-misc-nginx-module).


## redis2_literal_raw_query
**syntax:** *redis2_literal_raw_query QUERY*

**default:** *no*

**context:** *location, location if*

Specify a raw Redis query but Nginx variables in it will not be *not* recognized. In other words, you're free to use the dollar sign character (`$`) in your `QUERY` argument.

Only One redis command is allowed in the `QUERY` argument.


## redis2_pass
**syntax:** *redis2_pass &lt;upstream_name&gt;*

**syntax:** *redis2_pass &lt;host&gt;:&lt;port&gt;*

**default:** *no*

**context:** *location, location if*

**phase:** *content*

Specify the Redis server backend. 


## redis2_connect_timeout
**syntax:** *redis2_connect_timeout &lt;time&gt;*

**default:** *60s*

**context:** *http, server, location*

The timeout for connecting to the Redis server, in seconds by default.

It's wise to always explicitly specify the time unit to avoid confusion. Time units supported are `s`(seconds), `ms`(milliseconds), `y`(years), `M`(months), `w`(weeks), `d`(days), `h`(hours), and `m`(minutes).

This time must be less than 597 hours.


## redis2_send_timeout
**syntax:** *redis2_send_timeout &lt;time&gt;*

**default:** *60s*

**context:** *http, server, location*

The timeout for sending TCP requests to the Redis server, in seconds by default.

It's wise to always explicitly specify the time unit to avoid confusion. Time units supported are `s`(seconds), `ms`(milliseconds), `y`(years), `M`(months), `w`(weeks), `d`(days), `h`(hours), and `m`(minutes).


## redis2_read_timeout
**syntax:** *redis2_read_timeout &lt;time&gt;*

**default:** *60s*

**context:** *http, server, location*

The timeout for reading TCP responses from the redis server, in seconds by default.

It's wise to always explicitly specify the time unit to avoid confusion. Time units supported are `s`(seconds), `ms`(milliseconds), `y`(years), `M`(months), `w`(weeks), `d`(days), `h`(hours), and `m`(minutes).


## redis2_buffer_size
**syntax:** *redis2_buffer_size &lt;size&gt;*

**default:** *4k/8k*

**context:** *http, server, location*

This buffer size is used for reading Redis replies, but it's not required to be as big as the largest possible Redis reply.

This default size is the page size, may be 4k or 8k.


## redis2_next_upstream
**syntax:** *redis2_next_upstream [ error | timeout | invalid_response | off ]*

**default:** *error timeout*

**context:** *http, server, location*

Specify which failure conditions should cause the request to be forwarded to another
upstream server. Applies only when the value in [redis2_pass](#redis2_pass) is an upstream with two or more
servers.

Here's an artificial example:
```nginx

 upstream redis_cluster {
     server 127.0.0.1:6379;
     server 127.0.0.1:6380;
 }

 server {
     location = /redis {
         redis2_next_upstream error timeout invalid_response;
         redis2_query get foo;
         redis2_pass redis_cluster;
     }
 }
```


## Connection Pool

You can use the excellent [HttpUpstreamKeepaliveModule](http://wiki.nginx.org/HttpUpstreamKeepaliveModule) with this module to provide TCP connection pool for Redis.

A sample config snippet looks like this

```nginx

 http {
     upstream backend {
       server 127.0.0.1:6379;

       # a pool with at most 1024 connections
       # and do not distinguish the servers:
       keepalive 1024;
     }

     server {
         ...
         location = /redis {
             set_unescape_uri $query $arg_query;
             redis2_query $query;
             redis2_pass backend;
         }
     }
 }
```


## Selecting Redis Databases

Redis provides the [select](http://redis.io/commands/SELECT) command to switch Redis databaess. This command is no different from other normal commands
like [get](http://redis.io/commands/GET) or [set](http://redis.io/commands/SET). So you can use them in [redis2_query](#redis2_query) directives, for
example,

```nginx
redis2_query select 8;
redis2_query get foo;
```


## Lua Interoperability

This module can be served as a non-blocking redis2 client for [lua-nginx-module](http://github.com/openresty/lua-nginx-module) (but nowadays it is recommended to use the [lua-resty-redis](http://github.com/openresty/lua-resty-redis) library instead, which is much simpler to use and more efficient most of the time).
Here's an example using a GET subrequest:

```nginx

 location = /redis {
     internal;

     # set_unescape_uri is provided by ngx_set_misc
     set_unescape_uri $query $arg_query;

     redis2_raw_query $query;
     redis2_pass 127.0.0.1:6379;
 }

 location = /main {
     content_by_lua '
         local res = ngx.location.capture("/redis",
             { args = { query = "ping\\r\\n" } }
         )
         ngx.print("[" .. res.body .. "]")
     ';
 }
```

Then accessing `/main` yields


    [+PONG\r\n]


where `\r\n` is `CRLF`. That is, this module returns the *raw* TCP responses from the remote redis server. For Lua-based application developers, they may want to utilize the [lua-redis-parser](http://github.com/openresty/lua-redis-parser) library (written in pure C) to parse such raw responses into Lua data structures.

When moving the inlined Lua code into an external `.lua` file, it's important to use the escape sequence `\r\n` directly. We used `\\r\\n` above just because the Lua code itself needs quoting when being put into an Nginx string literal.

You can also use POST/PUT subrequests to transfer the raw Redis request via request body, which does not require URI escaping and unescaping, thus saving some CPU cycles. Here's such an example:

```nginx

 location = /redis {
     internal;

     # $echo_request_body is provided by the ngx_echo module
     redis2_raw_query $echo_request_body;

     redis2_pass 127.0.0.1:6379;
 }

 location = /main {
     content_by_lua '
         local res = ngx.location.capture("/redis",
             { method = ngx.HTTP_PUT,
               body = "ping\\r\\n" }
         )
         ngx.print("[" .. res.body .. "]")
     ';
 }
```

This yeilds exactly the same output as the previous (GET) sample.

One can also use Lua to pick up a concrete Redis backend based on some complicated hashing rules. For instance,

```nginx

 upstream redis-a {
     server foo.bar.com:6379;
 }

 upstream redis-b {
     server bar.baz.com:6379;
 }

 upstream redis-c {
     server blah.blah.org:6379;
 }

 server {
     ...

     location = /redis {
         set_unescape_uri $query $arg_query;
         redis2_query $query;
         redis2_pass $arg_backend;
     }

     location = /foo {
         content_by_lua "
             -- pick up a server randomly
             local servers = {'redis-a', 'redis-b', 'redis-c'}
             local i = ngx.time() % #servers + 1;
             local srv = servers[i]

             local res = ngx.location.capture('/redis',
                 { args = {
                     query = '...',
                     backend = srv
                   }
                 }
             )
             ngx.say(res.body)
         ";
     }
 }
```


## Pipelined Redis Requests by Lua

Here's a complete example demonstrating how to use Lua to issue multiple pipelined Redis requests via this Nginx module.

First of all, we include the following in our `nginx.conf` file:

```nginx

 location = /redis2 {
     internal;

     redis2_raw_queries $args $echo_request_body;
     redis2_pass 127.0.0.1:6379;
 }

 location = /test {
     content_by_lua_file conf/test.lua;
 }
```

Basically we use URI query args to pass the number of Redis requests and request body to pass the pipelined Redis request string.

And then we create the `conf/test.lua` file (whose path is relative to the server root of Nginx) to include the following Lua code:

```lua

 -- conf/test.lua
 local parser = require "redis.parser"

 local reqs = {
     {"set", "foo", "hello world"},
     {"get", "foo"}
 }

 local raw_reqs = {}
 for i, req in ipairs(reqs) do
     table.insert(raw_reqs, parser.build_query(req))
 end

 local res = ngx.location.capture("/redis2?" .. #reqs,
     { body = table.concat(raw_reqs, "") })

 if res.status ~= 200 or not res.body then
     ngx.log(ngx.ERR, "failed to query redis")
     ngx.exit(500)
 end

 local replies = parser.parse_replies(res.body, #reqs)
 for i, reply in ipairs(replies) do
     ngx.say(reply[1])
 end
```

Here we assume that your Redis server is listening on the default port (6379) of the localhost. We also make use of the [lua-redis-parser](http://github.com/openresty/lua-redis-parser) library to construct raw Redis queries for us and also use it to parse the replies.

Accessing the `/test` location via HTTP clients like `curl` yields the following output


    OK
    hello world


A more realistic setting is to use a proper upstream definition for our Redis backend and enable TCP connection pool via the [keepalive](http://wiki.nginx.org/HttpUpstreamKeepaliveModule#keepalive) directive in it.


## Redis Publish/Subscribe Support

This module has limited support for Redis publish/subscribe feature. It cannot be fully supported due to the stateless nature of REST and HTTP model.

Consider the following example:

```nginx

 location = /redis {
     redis2_raw_queries 2 "subscribe /foo/bar\r\n";
     redis2_pass 127.0.0.1:6379;
 }
```

And then publish a message for the key `/foo/bar` in the `redis-cli` command line. And then you'll receive two multi-bulk replies from the `/redis` location.

You can surely parse the replies with the [lua-redis-parser](http://github.com/openresty/lua-redis-parser) library if you're using Lua to access this module's location.


## Limitations For Redis Publish/Subscribe

If you want to use the [Redis pub/sub](http://redis.io/topics/pubsub) feature with this module, then you must note the following limitations:

* You cannot use [HttpUpstreamKeepaliveModule](http://wiki.nginx.org/HttpUpstreamKeepaliveModule) with this Redis upstream. Only short Redis connections will work.
* There may be some race conditions that produce the harmless `Redis server returned extra bytes` warnings in your nginx's error.log. Such warnings might be rare but just be prepared for it.
* You should tune the various timeout settings provided by this module like [redis2_connect_timeout](#redis2_connect_timeout) and [redis2_read_timeout](#redis2_read_timeout).

If you cannot stand these limitations, then you are highly recommended to switch to the [lua-resty-redis](https://github.com/openresty/lua-resty-redis) library for [lua-nginx-module](http://github.com/openresty/lua-nginx-module).


## Performance Tuning

* When you're using this module, please ensure you're using a TCP connection pool (provided by [HttpUpstreamKeepaliveModule](http://wiki.nginx.org/HttpUpstreamKeepaliveModule)) and Redis pipelining wherever possible. These features will significantly improve performance.
* Using multiple instance of Redis servers on your multi-core machines also help a lot due to the sequential processing nature of a single Redis server instance.
* When you're benchmarking performance using something like `ab` or `http_load`, please ensure that your error log level is high enough (like `warn`) to prevent Nginx workers spend too much cycles on flushing the `error.log` file, which is always non-buffered and blocking and thus very expensive.


## SEE ALSO
* The [Redis](http://redis.io/) server homepage.
* The Redis wire protocol: <http://redis.io/topics/protocol>
* a redis response parser and a request constructor for Lua: [lua-redis-parser](http://github.com/openresty/lua-redis-parser).
* [lua-nginx-module](http://github.com/openresty/lua-nginx-module)
* The [ngx_openresty bundle](http://openresty.org).
* The [lua-resty-redis](https://github.com/openresty/lua-resty-redis) library based on the [lua-nginx-module](http://github.com/openresty/lua-nginx-module) cosocket API.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-redis2](https://github.com/openresty/redis2-nginx-module){target=_blank}.