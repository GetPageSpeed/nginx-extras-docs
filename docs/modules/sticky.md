# *sticky*: NGINX sticky cookie module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-sticky
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_sticky_module.so;
```


This document describes nginx-module-sticky [v1.3.0](https://github.com/dvershinin/nginx-sticky-module-ng/releases/tag/v1.3.0){target=_blank} 
released on Jun 27 2022.

<hr />


modified and extended version; see Changelog.txt 

## Description

A nginx module to add a sticky cookie to be always forwarded to the same
upstream server.

When dealing with several backend servers, it's sometimes useful that one
client (browser) is always served by the same backend server
(for session persistance for example).

Using a persistance by IP (with the ip_hash upstream module) is maybe not
a good idea because there could be situations where a lot of different
browsers are coming with the same IP address (behind proxies)and the load
balancing system won't be fair.

Using a cookie to track the upstream server makes each browser unique.

When the sticky module can't apply, it switchs back to the classic Round Robin
Upstream or returns a "Bad Gateway" (depending on the no_fallback flag).

Sticky module can't apply when cookies are not supported by the browser

> Sticky module is based on a "best effort" algorithm. Its aim is not to handle
> security somehow. It's been made to ensure that normal users are always
> redirected to the same  backend server: that's all!

## Usage

    upstream {
      sticky;
      server 127.0.0.1:9000;
      server 127.0.0.1:9001;
      server 127.0.0.1:9002;
    }

	  sticky [hash=index|md5|sha1] [no_fallback]
           [name=route] [domain=.foo.bar] [path=/] [expires=1h] [secure] [httponly];
       or
	  sticky [hmac=md5|sha1 hmac_key=<foobar_key>] [no_fallback]
           [name=route] [domain=.foo.bar] [path=/] [expires=1h] [secure] [httponly];
       or
	  sticky [text=raw] [no_fallback]
           [name=route] [domain=.foo.bar] [path=/] [expires=1h] [secure] [httponly];

Server selection algorithm:
- hash:    the hash mechanism to encode upstream server. It can't be used with hmac or text.
  default: md5

    - md5|sha1: well known hash
    - index:    it's not hashed, an in-memory index is used instead, it's quicker and the overhead is shorter
    Warning: the matching against upstream servers list
    is inconsistent. So, at reload, if upstreams servers
    has changed, index values are not guaranted to
    correspond to the same server as before!
    USE IT WITH CAUTION and only if you need to!

- hmac:    the HMAC hash mechanism to encode upstream server
    It's like the hash mechanism but it uses hmac_key
    to secure the hashing. It can't be used with hash or text.
    md5|sha1: well known hash

- hmac_key: the key to use with hmac. It's mandatory when hmac is set

- no_fallback: when this flag is set, nginx will return a 502 (Bad Gateway or
              Proxy Error) if a request comes with a cookie and the
              corresponding backend is unavailable. You can set it to the
              upstream block, or set "sticky_no_fallback" in a server or
              location block.

Cookie settings:
- name:    the name of the cookie used to track the persistant upstream srv;
  default: route

- domain:  the domain in which the cookie will be valid
  default: none. Let the browser handle this.

- path:    the path in which the cookie will be valid
  default: /

- expires: the validity duration of the cookie
  default: nothing. It's a session cookie.
  restriction: must be a duration greater than one second

- secure    enable secure cookies; transferred only via https
- httponly  enable cookies not to be leaked via js


## Detail Mechanism

- see docs/sticky.{vsd,pdf}	

## Issues and Warnings:

- when using different upstream-configs with stickyness that use the same domain but 
  refer to different location - configs it might be wise to set a different path / route -  
  option on each of this upstream-configs like described here:
  https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/issue/7/leaving-cookie-path-empty-in-module

- sticky module does not work with the "backup" option of the "server" configuration item.
- sticky module might work with the nginx_http_upstream_check_module (up from version 1.2.3)
  


## Downloads

- tarballs are available via tags from the repo: https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/downloads


## Authors & Credits

- Jerome Loyet, initial module
- Markus Linnala, httponly/secure-cookies-patch
- Peter Bowey, Nginx 1.5.8 API-Change 
- Michael Chernyak for Max-Age-Patch 
- anybody who suggested a patch, created an issue on bitbucket or helped improving this module 



## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-sticky](https://github.com/dvershinin/nginx-sticky-module-ng){target=_blank}.