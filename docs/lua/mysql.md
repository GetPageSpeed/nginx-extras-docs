---

title: "Nonblocking Lua MySQL driver library for nginx-module-lua"
description: "RPM package lua-resty-mysql: Nonblocking Lua MySQL driver library for nginx-module-lua"

---
  
# *mysql*: Nonblocking Lua MySQL driver library for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-mysql
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-mysql
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-mysql [v0.28](https://github.com/openresty/lua-resty-mysql/releases/tag/v0.28){target=_blank} 
released on May 08 2025.
    
<hr />

lua-resty-mysql - Lua MySQL client driver for ngx_lua based on the cosocket API

## Status

This library is considered production ready.

## Description

This Lua library is a MySQL client driver for the ngx_lua nginx module:

https://github.com/openresty/lua-nginx-module

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

Note that at least [ngx_lua 0.9.11](https://github.com/chaoslawful/lua-nginx-module/tags) or [ngx_openresty 1.7.4.1](http://openresty.org/#Download) is required.

Also, the [bit library](http://bitop.luajit.org/) is also required. If you're using LuaJIT 2 with ngx_lua, then the `bit` library is already available by default.

## Synopsis

```lua

    # you do not need the following line if you are using
    # the ngx_openresty bundle:
    server {
        location /test {
            content_by_lua '
                local mysql = require "resty.mysql"
                local db, err = mysql:new()
                if not db then
                    ngx.say("failed to instantiate mysql: ", err)
                    return
                end

                db:set_timeout(1000) -- 1 sec

                -- or connect to a unix domain socket file listened
                -- by a mysql server:
                --     local ok, err, errcode, sqlstate =
                --           db:connect{
                --              path = "/path/to/mysql.sock",
                --              database = "ngx_test",
                --              user = "ngx_test",
                --              password = "ngx_test" }

                local ok, err, errcode, sqlstate = db:connect{
                    host = "127.0.0.1",
                    port = 3306,
                    database = "ngx_test",
                    user = "ngx_test",
                    password = "ngx_test",
                    charset = "utf8",
                    max_packet_size = 1024 * 1024,
                }

                if not ok then
                    ngx.say("failed to connect: ", err, ": ", errcode, " ", sqlstate)
                    db:close()
                    return
                end

                ngx.say("connected to mysql.")

                local res, err, errcode, sqlstate =
                    db:query("drop table if exists cats")
                if not res then
                    ngx.say("bad result: ", err, ": ", errcode, ": ", sqlstate, ".")
                    db:close()
                    return
                end

                res, err, errcode, sqlstate =
                    db:query("create table cats "
                             .. "(id serial primary key, "
                             .. "name varchar(5))")
                if not res then
                    ngx.say("bad result: ", err, ": ", errcode, ": ", sqlstate, ".")
                    db:close()
                    return
                end

                ngx.say("table cats created.")

                res, err, errcode, sqlstate =
                    db:query("insert into cats (name) "
                             .. "values (\'Bob\'),(\'\'),(null)")
                if not res then
                    ngx.say("bad result: ", err, ": ", errcode, ": ", sqlstate, ".")
                    db:close()
                    return
                end

                ngx.say(res.affected_rows, " rows inserted into table cats ",
                        "(last insert id: ", res.insert_id, ")")

                -- run a select query, expected about 10 rows in
                -- the result set:
                res, err, errcode, sqlstate =
                    db:query("select * from cats order by id asc", 10)
                if not res then
                    ngx.say("bad result: ", err, ": ", errcode, ": ", sqlstate, ".")
                    db:close()
                    return
                end

                local cjson = require "cjson"
                ngx.say("result: ", cjson.encode(res))

                -- put it into the connection pool of size 100,
                -- with 10 seconds max idle timeout
                local ok, err = db:set_keepalive(10000, 100)
                if not ok then
                    ngx.say("failed to set keepalive: ", err)
                    db:close()
                    return
                end

                -- or just close the connection right away:
                -- local ok, err = db:close()
                -- if not ok then
                --     ngx.say("failed to close: ", err)
                --     return
                -- end
            ';
        }
    }
```

## Methods

## new
`syntax: db, err = mysql:new()`

Creates a MySQL connection object. In case of failures, returns `nil` and a string describing the error.

## connect
`syntax: ok, err, errcode, sqlstate = db:connect(options)`

Attempts to connect to the remote MySQL server.

The `options` argument is a Lua table holding the following keys:

* `host`

    the host name for the MySQL server.
* `port`

    the port that the MySQL server is listening on. Default to 3306.
* `path`

    the path of the unix socket file listened by the MySQL server.
* `database`

    the MySQL database name.
* `user`

    MySQL account name for login.
* `password`

    MySQL account password for login (in clear text).
* `charset`

    the character set used on the MySQL connection, which can be different from the default charset setting.
The following values are accepted: `big5`, `dec8`, `cp850`, `hp8`, `koi8r`, `latin1`, `latin2`,
`swe7`, `ascii`, `ujis`, `sjis`, `hebrew`, `tis620`, `euckr`, `koi8u`, `gb2312`, `greek`,
`cp1250`, `gbk`, `latin5`, `armscii8`, `utf8`, `ucs2`, `cp866`, `keybcs2`, `macce`,
`macroman`, `cp852`, `latin7`, `utf8mb4`, `cp1251`, `utf16`, `utf16le`, `cp1256`,
`cp1257`, `utf32`, `binary`, `geostd8`, `cp932`, `eucjpms`, `gb18030`.
* `max_packet_size`

    the upper limit for the reply packets sent from the MySQL server (default to 1MB).
* `ssl`

    If set to `true`, then uses SSL to connect to MySQL (default to `false`). If the MySQL
    server does not have SSL support
    (or just disabled), the error string "ssl disabled on server" will be returned.
* `ssl_verify`

    If set to `true`, then verifies the validity of the server SSL certificate (default to `false`).
    Note that you need to configure the [lua_ssl_trusted_certificate](https://github.com/openresty/lua-nginx-module#lua_ssl_trusted_certificate)
    to specify the CA (or server) certificate used by your MySQL server. You may also
    need to configure [lua_ssl_verify_depth](https://github.com/openresty/lua-nginx-module#lua_ssl_verify_depth)
    accordingly.
* `pool`

    the name for the MySQL connection pool. if omitted, an ambiguous pool name will be generated automatically with the string template `user:database:host:port` or `user:database:path`. (this option was first introduced in `v0.08`.)

* `pool_size`

    Specifies the size of the connection pool. If omitted and no `backlog` option was provided, no pool will be created. If omitted but `backlog` was provided, the pool will be created with a default size equal to the value of the [lua_socket_pool_size](https://github.com/openresty/lua-nginx-module#lua_socket_pool_size) directive. The connection pool holds up to `pool_size` alive connections ready to be reused by subsequent calls to [connect](#connect), but note that there is no upper limit to the total number of opened connections outside of the pool. If you need to restrict the total number of opened connections, specify the `backlog` option. When the connection pool would exceed its size limit, the least recently used (kept-alive) connection already in the pool will be closed to make room for the current connection. Note that the cosocket connection pool is per Nginx worker process rather than per Nginx server instance, so the size limit specified here also applies to every single Nginx worker process. Also note that the size of the connection pool cannot be changed once it has been created. Note that at least [ngx_lua 0.10.14](https://github.com/openresty/lua-nginx-module/tags) is required to use this options.

* `backlog`

    If specified, this module will limit the total number of opened connections for this pool. No more connections than `pool_size` can be opened for this pool at any time. If the connection pool is full, subsequent connect operations will be queued into a queue equal to this option's value (the "backlog" queue). If the number of queued connect operations is equal to `backlog`, subsequent connect operations will fail and return nil plus the error string `"too many waiting connect operations"`. The queued connect operations will be resumed once the number of connections in the pool is less than `pool_size`. The queued connect operation will abort once they have been queued for more than `connect_timeout`, controlled by [set_timeout](#set_timeout), and will return nil plus the error string "timeout". Note that at least [ngx_lua 0.10.14](https://github.com/openresty/lua-nginx-module/tags) is required to use this options.

* `compact_arrays`

    when this option is set to true, then the [query](#query) and [read_result](#read_result) methods will return the array-of-arrays structure for the resultset, rather than the default array-of-hashes structure.

Before actually resolving the host name and connecting to the remote backend, this method will always look up the connection pool for matched idle connections created by previous calls of this method.

## set_timeout
`syntax: db:set_timeout(time)`

Sets the timeout (in ms) protection for subsequent operations, including the `connect` method.

## set_keepalive
`syntax: ok, err = db:set_keepalive(max_idle_timeout, pool_size)`

Puts the current MySQL connection immediately into the ngx_lua cosocket connection pool.

You can specify the max idle timeout (in ms) when the connection is in the pool and the maximal size of the pool every nginx worker process.

In case of success, returns `1`. In case of errors, returns `nil` with a string describing the error.

Only call this method in the place you would have called the `close` method instead. Calling this method will immediately turn the current `resty.mysql` object into the `closed` state. Any subsequent operations other than `connect()` on the current objet will return the `closed` error.

## get_reused_times
`syntax: times, err = db:get_reused_times()`

This method returns the (successfully) reused times for the current connection. In case of error, it returns `nil` and a string describing the error.

If the current connection does not come from the built-in connection pool, then this method always returns `0`, that is, the connection has never been reused (yet). If the connection comes from the connection pool, then the return value is always non-zero. So this method can also be used to determine if the current connection comes from the pool.

## close
`syntax: ok, err = db:close()`

Closes the current mysql connection and returns the status.

In case of success, returns `1`. In case of errors, returns `nil` with a string describing the error.

## send_query
`syntax: bytes, err = db:send_query(query)`

Sends the query to the remote MySQL server without waiting for its replies.

Returns the bytes successfully sent out in success and otherwise returns `nil` and a string describing the error.

You should use the [read_result](#read_result) method to read the MySQL replies afterwards.

## read_result
`syntax: res, err, errcode, sqlstate = db:read_result()`

`syntax: res, err, errcode, sqlstate = db:read_result(nrows)`

Reads in one result returned from the MySQL server.

It returns a Lua table (`res`) describing the MySQL `OK packet` or `result set packet` for the query result.

For queries corresponding to a result set, it returns an array holding all the rows. Each row holds key-value pairs for each data fields. For instance,

```lua
    {
        { name = "Bob", age = 32, phone = ngx.null },
        { name = "Marry", age = 18, phone = "10666372"}
    }
```

For queries that do not correspond to a result set, it returns a Lua table like this:

```lua
    {
        insert_id = 0,
        server_status = 2,
        warning_count = 1,
        affected_rows = 32,
        message = nil
    }
```

If more results are following the current result, a second `err` return value will be given the string `again`. One should always check this (second) return value and if it is `again`, then she should call this method again to retrieve more results. This usually happens when the original query contains multiple statements (separated by semicolon in the same query string) or calling a MySQL procedure. See also [Multi-Resultset Support](#multi-resultset-support).

In case of errors, this method returns at most 4 values: `nil`, `err`, `errcode`, and `sqlstate`. The `err` return value contains a string describing the error, the `errcode` return value holds the MySQL error code (a numerical value), and finally, the `sqlstate` return value contains the standard SQL error code that consists of 5 characters. Note that, the `errcode` and `sqlstate` might be `nil` if MySQL does not return them.

The optional argument `nrows` can be used to specify an approximate number of rows for the result set. This value can be used
to pre-allocate space in the resulting Lua table for the result set. By default, it takes the value 4.

## query
`syntax: res, err, errcode, sqlstate = db:query(query)`

`syntax: res, err, errcode, sqlstate = db:query(query, nrows)`

This is a shortcut for combining the [send_query](#send_query) call and the first [read_result](#read_result) call.

You should always check if the `err` return value  is `again` in case of success because this method will only call [read_result](#read_result) only once for you. See also [Multi-Resultset Support](#multi-resultset-support).

## server_ver
`syntax: str = db:server_ver()`

Returns the MySQL server version string, like `"5.1.64"`.

You should only call this method after successfully connecting to a MySQL server, otherwise `nil` will be returned.

## set_compact_arrays
`syntax: db:set_compact_arrays(boolean)`

Sets whether to use the "compact-arrays" structure for the resultsets returned by subsequent queries. See the `compact_arrays` option for the `connect` method for more details.

This method was first introduced in the `v0.09` release.

## SQL Literal Quoting

It is always important to quote SQL literals properly to prevent SQL injection attacks. You can use the
[ngx.quote_sql_str](https://github.com/openresty/lua-nginx-module#ngxquote_sql_str) function provided by ngx_lua to quote values.
Here is an example:

```lua
    local name = ngx.unescape_uri(ngx.var.arg_name)
    local quoted_name = ngx.quote_sql_str(name)
    local sql = "select * from users where name = " .. quoted_name
```

## Multi-Resultset Support

For a SQL query that produces multiple result-sets, it is always your duty to check the "again" error message returned by the [query](#query) or [read_result](#read_result) method calls, and keep pulling more result sets by calling the [read_result](#read_result) method until no "again" error message returned (or some other errors happen).

Below is a trivial example for this:

```lua
    local cjson = require "cjson"
    local mysql = require "resty.mysql"

    local db = mysql:new()
    local ok, err, errcode, sqlstate = db:connect({
        host = "127.0.0.1",
        port = 3306,
        database = "world",
        user = "monty",
        password = "pass"})

    if not ok then
        ngx.log(ngx.ERR, "failed to connect: ", err, ": ", errcode, " ", sqlstate)
        return ngx.exit(500)
    end

    res, err, errcode, sqlstate = db:query("select 1; select 2; select 3;")
    if not res then
        ngx.log(ngx.ERR, "bad result #1: ", err, ": ", errcode, ": ", sqlstate, ".")
        db:close()
        return ngx.exit(500)
    end

    ngx.say("result #1: ", cjson.encode(res))

    local i = 2
    while err == "again" do
        res, err, errcode, sqlstate = db:read_result()
        if not res then
            ngx.log(ngx.ERR, "bad result #", i, ": ", err, ": ", errcode, ": ", sqlstate, ".")
            db:close()
            return ngx.exit(500)
        end

        ngx.say("result #", i, ": ", cjson.encode(res))
        i = i + 1
    end

    local ok, err = db:set_keepalive(10000, 50)
    if not ok then
        ngx.log(ngx.ERR, "failed to set keepalive: ", err)
        db:close()
        ngx.exit(500)
    end
```

This code snippet will produce the following response body data:

    result #1: [{"1":"1"}]
    result #2: [{"2":"2"}]
    result #3: [{"3":"3"}]

## Debugging

It is usually convenient to use the [lua-cjson](http://www.kyne.com.au/~mark/software/lua-cjson.php) library to encode the return values of the MySQL query methods to JSON. For example,

```lua
    local cjson = require "cjson"
    ...
    local res, err, errcode, sqlstate = db:query("select * from cats")
    if res then
        print("res: ", cjson.encode(res))
    end
```

## Automatic Error Logging

By default the underlying [ngx_lua](https://github.com/openresty/lua-nginx-module) module
does error logging when socket errors happen. If you are already doing proper error
handling in your own Lua code, then you are recommended to disable this automatic error logging by turning off [ngx_lua](https://github.com/openresty/lua-nginx-module)'s [lua_socket_log_errors](https://github.com/openresty/lua-nginx-module#lua_socket_log_errors) directive, that is,

```nginx
    lua_socket_log_errors off;
```

## Limitations

* This library cannot be used in code contexts like init_by_lua*, set_by_lua*, log_by_lua*, and
header_filter_by_lua* where the ngx_lua cosocket API is not available.
* The `resty.mysql` object instance cannot be stored in a Lua variable at the Lua module level,
because it will then be shared by all the concurrent requests handled by the same nginx
 worker process (see
https://github.com/openresty/lua-nginx-module#data-sharing-within-an-nginx-worker ) and
result in bad race conditions when concurrent requests are trying to use the same `resty.mysql` instance.
You should always initiate `resty.mysql` objects in function local
variables or in the `ngx.ctx` table. These places all have their own data copies for
each request.

## More Authentication Method Support

By default, Of all authentication method, only [Old Password Authentication(mysql_old_password)](https://dev.mysql.com/doc/internals/en/old-password-authentication.html) and [Secure Password Authentication(mysql_native_password)](https://dev.mysql.com/doc/internals/en/secure-password-authentication.html) are suppored. If the server requires [sha256_password](https://dev.mysql.com/doc/internals/en/sha256.html) or cache_sha2_password, an error like `auth plugin caching_sha2_password or sha256_password are not supported because resty.rsa is not installed` may be returned.

Need [lua-resty-rsa](https://github.com/spacewander/lua-resty-rsa) when using the `sha256_password` and `cache_sha2_password`.

## See Also
* the ngx_lua module: https://github.com/openresty/lua-nginx-module
* the MySQL wired protocol specification: http://forge.mysql.com/wiki/MySQL_Internals_ClientServer_Protocol
* the [lua-resty-memcached](https://github.com/agentzh/lua-resty-memcached) library
* the [lua-resty-redis](https://github.com/agentzh/lua-resty-redis) library
* the ngx_drizzle module: https://github.com/openresty/drizzle-nginx-module


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-mysql](https://github.com/openresty/lua-resty-mysql){target=_blank}.