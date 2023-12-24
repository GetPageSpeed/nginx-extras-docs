# *cors*: It's the implement of CORS on nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-cors
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-cors
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-cors [v0.2.1](https://github.com/detailyang/lua-resty-cors/releases/tag/0.2.1){target=_blank} 
released on Oct 17 2016.
    
<hr />
lua-resty-cors

## lua-resty-cors
It's the implement of [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS) on OpenResty and 
It backports the [nginx-http-cors](https://github.com/x-v8/ngx_http_cors_filter) to OpenResty

## Status
![lua-resty-cors](https://travis-ci.org/detailyang/lua-resty-cors.svg?branch=master)

Experimental

## Usage
It shoule be placed on the nginx output header phase. In OpenResty it should be header_filter_by_lua\*. The config shoule be like as the following:

````bash

http {
      header_filter_by_lua_block {
        local cors = require('lib.resty.cors');

        cors.allow_host([==[.*\.google\.com]==])
        cors.allow_host([==[.*\.facebook\.com]==])
        cors.expose_header('x-custom-field1')
        cors.expose_header('x-custom-field2')
        cors.allow_method('GET')
        cors.allow_method('POST')
        cors.allow_method('PUT')
        cors.allow_method('DELETE')
        cors.allow_header('x-custom-field1')
        cors.allow_header('x-custom-field2')
        cors.max_age(7200)
        cors.allow_credentials(false)
        
        cors.run()
    }
}
````

## API

## allow_host
`syntax: cors.allow_host(host)`

This will match the host from cors request then be added to the header Access-Control-Allow-Origin like as the following:

````bash
Request:
Origin: https://www.google.com

Response:
Access-Control-Allow-Origin: http://www.google.com
````

## expose_header
`syntax: cors.expose_header(header)`

This will be added to the header Access-Control-Expose-Headers like as the following:

````bash
Request:
Origin: https://www.google.com

Response:
Access-Control-Expose-Headers: x-custom-field1,x-custom-field2
````

## allow_method
`syntax: cors.allow_method(method)`

This will be added to the header Access-Control-Allow-Methods like as the following:

````bash
Request:
Origin: https://www.google.com

Response:
Access-Control-Allow-Methods:GET,POST,PUT
````

## allow_header
`syntax: cors.allow_header(header)`

This will be added to the header Access-Control-Allow-Headers like as the following:

````bash
Request:
Origin: https://www.google.com

Response:
Access-Control-Allow-Headers:x-custom-field1,x-custom-field2
````

## max_age
`syntax: cors.max_age(age)`

This will be added to the header Access-Control-Max-Age like as the following:

````bash
Request:
Origin: https://www.google.com

Response:
Access-Control-Max-Age: 7200
````

## Allow-Credentials
`syntax: cors.allow_credentials(true or false)`

This will be added to the header Access-Control-Allow-Credentials like as the following:

````bash
Request:
Origin: https://www.google.com

Response:
Access-Control-Allow-Credentials: true
````

## run
`syntax: cors.run()`

This is the entry for lua-resty-cors to run


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-cors](https://github.com/detailyang/lua-resty-cors){target=_blank}.