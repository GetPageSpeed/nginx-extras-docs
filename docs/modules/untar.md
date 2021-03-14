# _untar_: NGINX HTTP Untar Module


## Installation

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-untar
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_untar_module.so;
```


This document describes nginx-module-untar [v1.0](https://github.com/ajax16384/ngx_http_untar_module/releases/tag/v1.0){target=_blank} 
released on Mar 01 2020.
    
<hr />
This [nginx](https://nginx.org/) module can serve static file content directly from tar archives.
Inspired by [nginx-unzip-module](https://github.com/youzee/nginx-unzip-module).

## Features
* Zero-copy: outputs content directly from archive file (no temporary files)
* Caching parsed archive file entries: reduce archive scan-search time
* Supported tar item types: normal file, long file name data

## Configuration example
```nginx
  location ~ ^/(.+?\.tar)/(.*)$ {
      untar_archive "$document_root/$1";
      untar_file "$2";
      untar;
  }
```
## Module directives
***
**untar_archive** `string`

**context:** `http, server, location`

Specifies tar archive name.
***
**untar_file** `string`

**context:** `http, server, location`

Specifies file to be extracted from **untar_archive**.
***
**untar**

**context:** `location`

Invokes untar of **untar_file** from **untar_archive**
***
## Known limitations
* only GET,HEAD verbs supported
* no archive entries listing
* base tar format support (only normal files: no symlink, sparse e.t.c)

## TODO
* Limit cache archive descriptors, free expired archive descriptors
* Add tar item checksum to ETag

## GitHub

You may find additional configuration tips and documentation in the [GitHub repository for 
nginx-module-untar](https://github.com/ajax16384/ngx_http_untar_module){target=_blank}.