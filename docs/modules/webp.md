# *webp*: NGINX WebP module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-webp
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_webp_module.so;
```


This document describes nginx-module-webp [v0.1.1.5](https://github.com/dvershinin/ngx_webp/releases/tag/0.1.1.5){target=_blank} 
released on Dec 30 2019.

<hr />

Webp is new (and smaller) image format. This module will convert jpg/png image on fly and send webp response.

## Status

Under development. To be continued.

## Configuration directives

### `webp`

- **syntax**: `webp`
- **context**: `location`

Enables or disables module.

### Example

location ~ "\.jpg" {
webp;
}

$ curl -SLIXGET -H "accept:image/webp" http://127.0.0.1/1.jpg

HTTP/1.1 200 OK

Server: nginx/1.13.12

Date: Wed, 25 Apr 2018 10:16:45 GMT

Content-Length: 223980

Last-Modified: Wed, 25 Apr 2018 10:16:45 GMT

Connection: keep-alive

Content-Type: image/webp



$ curl -SLIXGET -H "accept:image/*" http://127.0.0.1/1.jpg

HTTP/1.1 200 OK

Server: nginx/1.13.12

Date: Wed, 25 Apr 2018 10:17:53 GMT

Content-Length: 325991

Last-Modified: Wed, 18 Apr 2018 19:55:14 GMT

Connection: keep-alive

Content-Type: image/jpeg

### Notice
As webp convertion takes some CPU usage I recommend to use some kind of caching of nginx responses, like Varnish.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-webp](https://github.com/dvershinin/ngx_webp){target=_blank}.