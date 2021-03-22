# *zip*: Streaming ZIP archiver for NGINX


## Installation

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-zip
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_zip_module.so;
```


This document describes nginx-module-zip [v1.2.0](https://github.com/evanmiller/mod_zip/releases/tag/1.2.0){target=_blank} 
released on Oct 24 2020.
    
<hr />

mod_zip assembles ZIP archives dynamically. It can stream component files from
upstream servers with nginx's native proxying code, so that the process never
takes up more than a few KB of RAM at a time, even while assembling archives that
are (potentially) gigabytes in size.

mod_zip supports a number of "modern" ZIP features, including large files, UTC
timestamps, and UTF-8 filenames. It allows clients to resume large downloads using
the "Range" and "If-Range" headers, although these feature require the server
to know the file checksums (CRC-32's) in advance. See "Usage" for details.

To unzip files on the fly, check out [nginx-unzip-module](https://github.com/youzee/nginx-unzip-module).


## Tips

1. Add a header "Content-Disposition: attachment; filename=foobar.zip" in the
upstream response if you would like the client to name the file "foobar.zip"

1. To save bandwidth, add a "Last-Modified" header in the upstream response; 
mod_zip will then honor the "If-Range" header from clients.

1. To wipe the X-Archive-Files header from the response sent to the client,
use the headers_more module: http://wiki.nginx.org/NginxHttpHeadersMoreModule

1. To improve performance, ensure the backends are not returning gzipped
files. You can achieve this with `proxy_set_header Accept-Encoding "";`
in the location blocks for the component files.

Questions/patches may be directed to Evan Miller, emmiller@gmail.com.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-zip](https://github.com/evanmiller/mod_zip){target=_blank}.