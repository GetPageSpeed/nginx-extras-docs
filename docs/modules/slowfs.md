---

title: "NGINX SlowFS Cache Module"
description: "RPM package nginx-module-slowfs. NGINX module which adds ability to cache static files."

---

# *slowfs*: NGINX SlowFS Cache Module


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
    dnf -y install nginx-module-slowfs
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-slowfs
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_slowfs_module.so;
```


This document describes nginx-module-slowfs [v1.11](https://github.com/dvershinin/ngx_slowfs_cache/releases/tag/1.11){target=_blank} 
released on Aug 23 2020.

<hr />
`ngx_slowfs_cache` is `nginx` module which allows caching of static files
(served using `root` directive). This enables one to create fast caches
for files stored on slow filesystems, for example:

- storage: network disks, cache: local disks,
- storage: 7,2K SATA drives, cache: 15K SAS drives in RAID0.


**WARNING! There is no point in using this module when cache is placed
on the same speed disk(s) as origin.**


## Sponsors
`ngx_slowfs_cache` was fully funded by [c2hosting.com](http://c2hosting.com).


## Status
This module is production-ready and it's compatible with following nginx
releases:

- 0.7.x (tested with 0.7.60 to 0.7.69),
- 0.8.x (tested with 0.8.0 to 0.8.55),
- 0.9.x (tested with 0.9.0 to 0.9.7),
- 1.0.x (tested with 1.0.0 to 1.0.15),
- 1.1.x (tested with 1.1.0 to 1.1.19),
- 1.2.x (tested with 1.2.0 to 1.2.7),
- 1.3.x (tested with 1.3.0 to 1.3.14).


## Configuration notes
`slowfs_cache_path` and `slowfs_temp_path` values should point to the same
filesystem, otherwise files will be copied twice.

`ngx_slowfs_cache` currently doesn't work when AIO is enabled.


## Configuration directives
## slowfs_cache
* **syntax**: `slowfs_cache zone_name`
* **default**: `none`
* **context**: `http`, `server`, `location`

Sets area used for caching (previously defined using `slowfs_cache_path`).
  

## slowfs_cache_key
* **syntax**: `slowfs_cache_key key`
* **default**: `none`
* **context**: `http`, `server`, `location`

Sets key for caching.


## slowfs_cache_purge
* **syntax**: `slowfs_cache_purge zone_name key`
* **default**: `none`
* **context**: `location`

Sets area and key used for purging selected pages from cache.


## slowfs_cache_path
* **syntax**: `slowfs_cache_path path [levels] keys_zone=zone_name:zone_size [inactive] [max_size]`
* **default**: `none`
* **context**: `http`

Sets cache area and its structure.


## slowfs_temp_path
* **syntax**: `slowfs_temp_path path [level1] [level2] [level3]`
* **default**: `/tmp 1 2`
* **context**: `http`
  
Sets temporary area where files are stored before they are moved to cache area.


## slowfs_cache_min_uses
* **syntax**: `slowfs_cache_min_uses number`
* **default**: `1`
* **context**: `http`, `server`, `location`

Sets number of uses after which file is copied to cache.


## slowfs_cache_valid
* **syntax**: `slowfs_cache_valid [reply_code] time`
* **default**: `none`
* **context**: `http`, `server`, `location`

Sets time for which file will be served from cache.


## slowfs_big_file_size
* **syntax**: `slowfs_big_file_size size`
* **default**: `128k`
* **context**: `http`, `server`, `location`

Sets minimum file size for `big` files. Worker processes `fork()` child process
before they start copying `big` files to avoid any service disruption. 


## Configuration variables
## $slowfs_cache_status
Represents availability of cached file.

Possible values are: `MISS`, `HIT` and `EXPIRED`.


## Sample configuration
    http {
        slowfs_cache_path  /tmp/cache levels=1:2 keys_zone=fastcache:10m;
        slowfs_temp_path   /tmp/temp 1 2;

        server {
            location / {
                root                /var/www;
                slowfs_cache        fastcache;
                slowfs_cache_key    $uri;
                slowfs_cache_valid  1d;
            }

            location ~ /purge(/.*) {
                allow               127.0.0.1;
                deny                all;
                slowfs_cache_purge  fastcache $1;
            }
       }
    }

## Testing
`ngx_slowfs_cache` comes with complete test suite based on [Test::Nginx](http://github.com/agentzh/test-nginx).

You can test it by running:

`$ prove`


## See also
- [ngx_cache_purge](http://github.com/FRiCKLE/ngx_cache_purge).

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-slowfs](https://github.com/dvershinin/ngx_slowfs_cache){target=_blank}.