# *f4fhds*: NGINX module for Adobe f4f format


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-f4fhds
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_f4fhds_module.so;
```


This document describes nginx-module-f4fhds [v0.0.1](https://github.com/GetPageSpeed/f4fhds/releases/tag/v0.0.1){target=_blank} 
released on Oct 24 2020.

<hr />

Nginx module for Adobe f4f format.

This module implements handling of HTTP Dynamic Streaming requests in the “/videoSeg1-Frag1” form — extracting the 
needed fragment from the videoSeg1.f4f file using the videoSeg1.f4x index file. This module is an alternative to the 
Adobe’s f4f module (HTTP Origin Module) for Apache.

It is open-source equivalent for commercial [ngx_http_f4f_module](http://nginx.org/en/docs/http/ngx_http_f4f_module.html#f4f_buffer_size)
module.

## Synopsis

```nginx
location /video/ {
    f4fhds;
    ...
}
```

## Limitations

* The assumption is that all files contain a single (first) segment, e.g. Seg1
* The files should reside in a local non-networked filesystem, due to use of `mmap(2)`.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-f4fhds](https://github.com/GetPageSpeed/f4fhds){target=_blank}.