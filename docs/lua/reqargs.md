---

title: "Read application/x-www-form-urlencoded, multipart/form-data, and application/json request args"
description: "RPM package lua-resty-reqargs: Read application/x-www-form-urlencoded, multipart/form-data, and application/json request args"

---
  
# *reqargs*: Read application/x-www-form-urlencoded, multipart/form-data, and application/json request args


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-reqargs
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-reqargs
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-reqargs [v1.4](https://github.com/bungle/lua-resty-reqargs/releases/tag/v1.4){target=_blank} 
released on Jan 07 2017.
    
<hr />

Helper to Retrieve `application/x-www-form-urlencoded`, `multipart/form-data`, and `application/json` Request Arguments.

## Synopsis

```lua
local get, post, files = require "resty.reqargs"()
if not get then
    error(post)
end
-- Use get, post, and files...
```

## API

This module has only one function, and that function is loaded with require:

```lua
local reqargs = require "resty.reqargs"
```

### get, post, files regargs(options)

When you call the function (`reqargs`) you can pass it `options`. These
options override whatever you may have defined in your Nginx configuration
(or the defaults). You may use the following options:

```lua
{
    tmp_dir          = "/tmp",
    timeout          = 1000,
    chunk_size       = 4096,
    max_get_args     = 100,
    mas_post_args    = 100,
    max_line_size    = 512,
    max_file_uploads = 10
}
```

This function will return three (3) return values, and they are called
`get`, `post`,  and `files`. These are Lua tables containing the data
that was (HTTP) requested. `get` contains HTTP request GET arguments
retrieved with [ngx.req.get_uri_args](https://github.com/openresty/lua-nginx-module#ngxreqget_uri_args).
`post` contains either HTTP request POST arguments retrieved with
[ngx.req.get_post_args](https://github.com/openresty/lua-nginx-module#ngxreqget_post_args),
or in case of `application/json` (as a content type header for the request),
it will read the request body and decode the JSON, and the `post` will
then contain the decoded JSON structure presented as Lua tables. The
last return value `files` contains all the files uploaded. The `files`
return value will only contain data when there are actually files uploaded
and that the request content type is set to `multipart/form-data`. `files`
has the same structure as `get` and `post` for the keys, but the values
are presented as a Lua tables, that look like this (think about PHP's `$_FILES`):

```lua
{
    -- The name of the file upload form field (same as the key)
    name = "photo",
    -- The name of the file that the user selected for the upload
    file = "cat.jpg",
    -- The mimetype of the uploaded file
    type = "image/jpeg"
    -- The file size of the uploaded file (in bytes)
    size = 123465
    -- The location where the uploaded file was streamed
    temp = "/tmp/????"
}
```

In case of error, this function will return `nil`, `error message`.

## Nginx Configuration Variables

You can configure several aspects of `lua-resty-reqargs` directly from
the Nginx configuration, here are the configuration values that you may
use, and their default values:

```nginx
## the default is the system temp dir
set $reqargs_tmp_dir           /tmp;
## see https://github.com/openresty/lua-resty-upload
set $reqargs_timeout           1000;
## see https://github.com/openresty/lua-resty-upload
set $reqargs_chunk_size        4096;
## see https://github.com/openresty/lua-nginx-module#ngxreqget_uri_args
set $reqargs_max_get_args      100;
## see https://github.com/openresty/lua-nginx-module#ngxreqget_post_args
set $reqargs_max_post_args     100;
## see https://github.com/openresty/lua-resty-upload
set $reqargs_max_line_size     512;  
## the default is unlimited
set $reqargs_max_file_uploads  10;
```

## Changes

The changes of every release of this module is recorded in [Changes.md](https://github.com/bungle/lua-resty-reqargs/blob/master/Changes.md) file.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-reqargs](https://github.com/bungle/lua-resty-reqargs){target=_blank}.