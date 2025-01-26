---

title: "Send mail with NGINX"
description: "RPM package lua-resty-smtp: Send mail with NGINX"

---
  
# *smtp*: Send mail with NGINX


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-smtp
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-smtp
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-smtp [v0.0.3](https://github.com/duhoobo/lua-resty-smtp/releases/tag/v0.0.3){target=_blank} 
released on Mar 06 2015.
    
<hr />

I must be crazy trying to send mail with Nginx. 



## Purpose

To make Nginx a bridge between HTTP and SMTP.

Using `lua-resty-smtp` in your lua code under Nginx, you just need to issue a 
HTTP request with your handy HTTP client (`curl`, `wget`, `urllib2` from Python
etc.), in order to send a mail to your SMTP server.



## Features

* Based on module `socket.smtp` from [LuaScoket 2.0.2](http://w3.impa.br/~diego/software/luasocket/home.html), 
and API-compatible with it also

* SSL connection supported (lua-nginx-lua >= v0.9.11 needed)



## APIs

`lua-resty-smtp` is API-compatible with `socket.smtp` from [LuaSocket 2.0.2](http://w3.impa.br/~diego/software/luasocket/home.html),
and you can check [SMTP](http://w3.impa.br/~diego/software/luasocket/smtp.html)
for detailed reference of it.


And to support SSL connection to SMTP server, optional parameter `ssl` is added:

* `ssl`: should be a table with following fields:

    * `enable` - boolean - whether or not use SSL connection to SMTP server,
    default `false`;

    * `verify_cert` - boolean - whether or not to perform SSL verification,
    default `false`. When set to `true`, the server certificate will be verified
    according to the CA certificate specified by the
    [`lua_ssl_trusted_cerfificate`](http://wiki.nginx.org/HttpLuaModule#lua_ssl_trusted_certificate)
    directive.



## Extra filters

In addtion to the low-level filters provided by LuaSocket, two more filters is
provided:

* `mime.ew`: used to encode non-ASCII string into the 
[Encoded-Word](http://en.wikipedia.org/wiki/MIME#Encoded-Word) format (not
support _Q-encoding_ yet);

* `mime.unew`: used to decode string in Encoded-Word format (not implemented);



## Example

    local config = require("config")
    local smtp = require("resty.smtp")
    local mime = require("resty.smtp.mime")
    local ltn12 = require("resty.smtp.ltn12")

    -- ...
    -- Suppose your mail data in table `args` and default settings 
    -- in table `config.mail`
    -- ...

    local mesgt = { 
        headers= {
            subject= mime.ew(args.subject or config.mail.SUBJECT, nil, 
                             { charset= "utf-8" }), 
            ["content-transfer-encoding"]= "BASE64",
            ["content-type"]= "text/plain; charset='utf-8'",
        },
    
        body= mime.b64(args.body)
    }   
    
    local ret, err = smtp.send {
        from= args.from or config.mail.FROM,
        rcpt= rcpts,
        user= args.user or config.mail.USER,
        password= args.password or config.mail.PASSWORD,
        server= args.server or config.mail.SERVER,
        domain= args.domain or config.mail.DOMAIN,
        source= smtp.message(mesgt),
    }   



## Performance

Your SMTP server is the bottleneck. :)



## Known Issues

* Only work with LuaJIT 2.x now, because the codebase relies on `pcall`
  massively and lua-nginx-module does not work well with standard Lua 5.1 VM 
  under this situation. See [Known Issues](http://wiki.nginx.org/HttpLuaModule#Lua_Coroutine_Yielding.2FResuming)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-smtp](https://github.com/duhoobo/lua-resty-smtp){target=_blank}.