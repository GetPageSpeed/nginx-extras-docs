---

title: "Streaming reader and parser for http file uploading based on nginx-module-lua cosocket"
description: "RPM package lua-resty-upload: Streaming reader and parser for http file uploading based on nginx-module-lua cosocket"

---
  
# *upload*: Streaming reader and parser for http file uploading based on nginx-module-lua cosocket


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-upload
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-upload
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-upload [v0.11](https://github.com/openresty/lua-resty-upload/releases/tag/v0.11){target=_blank} 
released on Jan 19 2023.
    
<hr />

lua-resty-upload - Streaming reader and parser for HTTP file uploading based on ngx_lua cosocket

## Status

This library is considered production ready.

## Description

This Lua library is a streaming file uploading API for the ngx_lua nginx module:

http://wiki.nginx.org/HttpLuaModule

The multipart/form-data MIME type is supported.

The API of this library just returns tokens one by one. The user just needs to call the `read` method repeatedly until a nil token type is returned. For each token returned from the `read` method, just check the first return value for the current token type. The token type can be `header`, `body`, and `part end`. Each `multipart/form-data` form field parsed consists of several `header` tokens holding each field header, several `body` tokens holding each body data chunk, and a `part end` flag indicating the field end.

This is how streaming reading works. Even for giga bytes of file data input, the memory used in the lua land can be small and constant, as long as the user does not accumulate the input data chunks herself.

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

Note that at least [ngx_lua 0.7.9](https://github.com/chaoslawful/lua-nginx-module/tags) or [OpenResty 1.2.4.14](http://openresty.org/#Download) is required.

## Synopsis

```lua
    server {
        location /test {
            content_by_lua '
                local upload = require "resty.upload"
                local cjson = require "cjson"

                local chunk_size = 5 -- should be set to 4096 or 8192
                                     -- for real-world settings

                local form, err = upload:new(chunk_size)
                if not form then
                    ngx.log(ngx.ERR, "failed to new upload: ", err)
                    ngx.exit(500)
                end

                form:set_timeout(1000) -- 1 sec

                while true do
                    local typ, res, err = form:read()
                    if not typ then
                        ngx.say("failed to read: ", err)
                        return
                    end

                    ngx.say("read: ", cjson.encode({typ, res}))

                    if typ == "eof" then
                        break
                    end
                end

                local typ, res, err = form:read()
                ngx.say("read: ", cjson.encode({typ, res}))
            ';
        }
    }
```

A typical output of the /test location defined above is:

    read: ["header",["Content-Disposition","form-data; name=\"file1\"; filename=\"a.txt\"","Content-Disposition: form-data; name=\"file1\"; filename=\"a.txt\""]]
    read: ["header",["Content-Type","text\/plain","Content-Type: text\/plain"]]
    read: ["body","Hello"]
    read: ["body",", wor"]
    read: ["body","ld"]
    read: ["part_end"]
    read: ["header",["Content-Disposition","form-data; name=\"test\"","Content-Disposition: form-data; name=\"test\""]]
    read: ["body","value"]
    read: ["body","\r\n"]
    read: ["part_end"]
    read: ["eof"]
    read: ["eof"]

You can use the [lua-resty-string](https://github.com/agentzh/lua-resty-string) library to compute SHA-1 and MD5 digest of the file data incrementally. Here is such an example:

```lua
    local resty_sha1 = require "resty.sha1"
    local upload = require "resty.upload"

    local chunk_size = 4096
    local form = upload:new(chunk_size)
    local sha1 = resty_sha1:new()
    local file
    while true do
        local typ, res, err = form:read()

        if not typ then
             ngx.say("failed to read: ", err)
             return
        end

        if typ == "header" then
            local file_name = my_get_file_name(res)
            if file_name then
                file = io.open(file_name, "w+")
                if not file then
                    ngx.say("failed to open file ", file_name)
                    return
                end
            end

         elseif typ == "body" then
            if file then
                file:write(res)
                sha1:update(res)
            end

        elseif typ == "part_end" then
            file:close()
            file = nil
            local sha1_sum = sha1:final()
            sha1:reset()
            my_save_sha1_sum(sha1_sum)

        elseif typ == "eof" then
            break

        else
            -- do nothing
        end
    end
```

If you want to compute MD5 sums for the uploaded files, just use the
resty.md5 module shipped by the [lua-resty-string](https://github.com/agentzh/lua-resty-string) library. It has
a similar API as resty.sha1.

For big file uploading, it is important not to buffer all the data in memory.
That is, you should never accumulate data chunks either in a huge Lua string or
in a huge Lua table. You must write the data chunk into files as soon as possible and
throw away the data chunk immediately (to let the Lua GC free it up).

Instead of writing the data chunk into files (as shown in the example above),
you can also write the data chunks to upstream cosocket connections if you do
not want to save the data on local file systems.

## Usage

```lua
local upload = require "resty.upload"
local form, err = upload:new(self, chunk_size, max_line_size, preserve_body)
```
`chunk_size` defaults to 4096. It is the size used to read data from the socket.

`max_line_size` defaults to 512. It is the size limit to read the chunked body header.

By Default, `lua-resty-upload` will consume the request body. For proxy mode this means upstream will not see the body. When `preserve_body` is set to true, the request body will be preserved. Note that this option is not free. When enabled, it will double the memory usage of `resty.upload`.

## See Also
* the [ngx_lua module](http://wiki.nginx.org/HttpLuaModule)
* the [lua-resty-string](https://github.com/agentzh/lua-resty-string) library
* the [lua-resty-memcached](https://github.com/agentzh/lua-resty-memcached) library
* the [lua-resty-redis](https://github.com/agentzh/lua-resty-redis) library
* the [lua-resty-mysql](https://github.com/agentzh/lua-resty-mysql) library


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-upload](https://github.com/openresty/lua-resty-upload){target=_blank}.