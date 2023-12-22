# *pta*: Period of Time Authentication module for NGINX


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-pta
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_pta_module.so;
```


This document describes nginx-module-pta [v1.0.1](https://github.com/iij/pta/releases/tag/v1.0.1){target=_blank} 
released on Jul 04 2022.

<hr />

## Overview

PTA(Period of Time Authentication) module is a module for NGINX. Using
PTA you can control access to your contents. PTA calcurates a
encrypted query string or cookie parameter that includes an expiration
time and a path of the content.

## Usage

It's an example of nginx.conf below.

```
  worker_processes  1;
  
  events {
      worker_connections  1024;
  }
   
   
  http {
      include       mime.types;
      default_type  application/octet-stream;
   
      sendfile        on;
   
      keepalive_timeout  65;
   
      server {
          listen       80;
          server_name  localhost;
   
          pta_1st_key 0102030405060708090a0b0c0d0e0f00;
          pta_1st_iv  00000000000000000000000000000000;
          pta_2nd_key 11111111111111111111111111111111;
          pta_2nd_iv  22222222222222222222222222222222;
   
          location / {
              root   html;
              index  index.html index.htm;
          }
   
          location /foo/ {
              pta_enable on;
          }
   
          error_page   500 502 503 504  /50x.html;
          location = /50x.html {
              root   html;
          }
      }
  }
```


## pta_1st_key
- Syntax  : pta_1st_key   keystring
- Default : -
- Context : server


## pta_1st_iv
- Syntax  : pta_1st_iv   ivstring;
- Default : -
- Context : server


## pta_2nd_key
- Syntax  : pta_2nd_key   keystring;
- Default : -
- Context : server


## pta_2nd_iv
- Syntax  : pta_2nd_iv   ivstring;
- Default : -
- Context : server


## pta_enable
- Syntax  : pta_enable   on | off;
- Default : pta_enable off;
- Context : location

## pta_auth_method
- Syntax  : pta_auth_method qs | cookie | qs cookie;
- Default : pta_auth_method qs;
- Context : location


## How it works

PTA module decrypts a query string or cookie parameter starting from
`pta=...' and check CRC32, expiration time and requested URI path
embedded in it. So you need to generate PTA token and add it to a link
as query string or cookie parameter. There are some codes under the
smaples directory to generate PTA.

## format

This byte stream is encrypted with the AES AES 128 bit CBC mode.

```
  +---------------+-------------------------+----------+-----------------+
  | CRC32 (4byte) | Expiration Time (8byte) | URI Path | Padding         |
  |               | Unix Time format        |          | pkcs #7 format  |
  +---------------+-------------------------+----------+-----------------+
```

### CRC32
It's big endian. It's calculated from the Expiration Time and URI Path.
This part is used to check that AES decryption is valid.

### Expiration time
It's big endian. It's compared with the time that request is arrived
and if the time is less than or equal to the expiration time that is
contained in the PTA token the request is permitted.

### URI Path
Basically it must be identical with the path of requested content.

  e.g.
  http://example.com/index.html -> /index.html

It must be started from the slash `/'.

The asterisk character `*' means wildcard.

- The `\*' character must be only one.
  e.g. /foo/\*/bar/*.jpg isn't allowed.
  
- You can use the `*' character any part such as a part of directory
  name, file name or file name suffix.
  
- If you use the `*' character literally, you must escape it with the
  back slash.

## Query string and Cookie

pta_auth_method directive can specify the method to authenticate. 
You can choose the type of query string, cookie, or both as the method.

In case of both, query string is evaluated first, and then cookie
is done if pta parameter isn't included in query string.
When pta parameter in query string isn't valid the authentication 
fails, not fallback to ealuate cookie. Only without pta parameter
in query string cookie is evaluated.

<!--
## Local Variables:
## mode: auto-fill
## coding: utf-8-unix
## End:
-->

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-pta](https://github.com/iij/pta){target=_blank}.