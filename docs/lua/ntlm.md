# *ntlm*: Nginx ntlm module implemented by lua


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-ntlm
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-ntlm
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-ntlm [v0.2](https://github.com/gosp/lua-resty-ntlm/releases/tag/v0.2){target=_blank} 
released on Feb 07 2018.
    
<hr />

`Windows authentication` is always used inside company. `IIS` can enable `Windows authentication` easily. For Nginx users, some solutions aren't friendly: `Nginx Pro` provides ntlm module but it isn't free; [`reverse proxy`](https://stackoverflow.com/questions/21284935/nginx-reverse-proxy-with-windows-authentication-that-uses-ntlm) must setup other server firstly.

The project is inspired by [express-ntlm](https://github.com/einfallstoll/express-ntlm) and [PyAuthenNTLM2](https://github.com/Legrandin/PyAuthenNTLM2/). IIS will trigger windows authentication scenario for each connection. Unlike IIS, the project only trigger ntlm for first requestion. After authentication done, http header `Authorization:Bearer ` will be sent to browser, and browser should put it in each request package to avoid ntlm again. At the same time, http header: `X-Ntlm-Username` and `X-Ntlm-Domain` will be sent to upstream.

*NOTICE:* don't `set-cookie` during ntlm authentication. [(#1175)](https://github.com/openresty/lua-nginx-module/issues/1175)

## Usage
+ install [OpenResty](http://openresty.org/en/linux-packages.html) which integrates Nginx and LuaJIT
+ intall [LuaRocks](https://openresty.org/en/using-luarocks.html) because `ntlm.lua` depends on `struct`, `iconv` module
+ install `struct` module: `sudo /usr/local/openresty/luajit/bin/luarocks install struct`
+ install `iconv` module: `sudo /usr/local/openresty/luajit/bin/luarocks install lua-iconv`
+ save `ntlm.lua` into `/usr/local/openresty/site/lualib`
+ add the following code to `/usr/local/openresty/nginx/conf/nginx.conf`: 
    ```
        lua_shared_dict ntlm_cache 10m;
        keepalive_timeout  35;
        ... ...
        access_by_lua_block {
            local cache = ngx.shared.ntlm_cache
            require('ntlm').negotiate("ldap://domain.net:389", cache, 10)
            -- cache is shared DICT
            -- timeout is less than keepalive
        }
    ```
+ restart nginx service: `sudo service openresty restart`

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-ntlm](https://github.com/gosp/lua-resty-ntlm){target=_blank}.