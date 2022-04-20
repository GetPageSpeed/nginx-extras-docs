# *njs*: NGINX njs dynamic modules


## Installation

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-njs
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_js_module.so;
```
```nginx
load_module modules/ngx_stream_js_module.so;
```


This document describes nginx-module-njs [v0.7.3](https://github.com/nginx/njs/releases/tag/0.7.3){target=_blank} 
released on Apr 12 2022.

<hr />

## NGINX JavaScript (njs)

njs is a subset of the JavaScript language that allows extending nginx
functionality. njs is created in compliance with ECMAScript 5.1 (strict mode)
with some ECMAScript 6 and later extensions. The compliance is still evolving.

The documentation is available online:

  https://nginx.org/en/docs/njs/

Additional examples and howtos can be found here:

  https://github.com/nginx/njs-examples

Please ask questions, report issues, and send patches to the mailing list:

    nginx-devel@nginx.org (https://mailman.nginx.org/mailman/listinfo/nginx-devel)

or via Github:

    https://github.com/nginx/njs

--
NGINX, Inc., https://nginx.com

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-njs](https://github.com/nginx/njs){target=_blank}.