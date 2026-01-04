---

title: "NGINX HTTP Untar Module"
description: "RPM package nginx-module-untar. This NGINX module can serve static file content directly from tar archives. Inspired by nginx-unzip-module.  Features:   * Zero-copy: outputs content directly from archive file     (no temporary files)   * Caching parsed archive file entries: reduce archive     scan-search time   * Supported tar item types: normal file, long file name data  Configuration example:      location ~ ^/(.+?.tar)/(.*)$ {         untar_archive $document_root/$1;         untar_file $2;         untar;     }"

---

# *untar*: NGINX HTTP Untar Module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9 and 10
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023+"

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-untar
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-untar
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_untar_module.so;
```


This document describes nginx-module-untar [v1.1](https://github.com/ajax16384/ngx_http_untar_module/releases/tag/v1.1){target=_blank} 
released on Mar 21 2022.

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

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-untar](https://github.com/ajax16384/ngx_http_untar_module){target=_blank}.