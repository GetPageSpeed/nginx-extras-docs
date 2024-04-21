# *njs*: NGINX njs dynamic modules


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

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


This document describes nginx-module-njs [v0.8.4](https://github.com/nginx/njs/releases/tag/0.8.4){target=_blank} 
released on Apr 15 2024.

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
## 
NGINX, Inc., https://nginx.com

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-njs](https://github.com/nginx/njs){target=_blank}.