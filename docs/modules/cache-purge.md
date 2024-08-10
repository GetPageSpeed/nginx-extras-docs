# *cache-purge*: NGINX Cache Purge module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-cache-purge
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-cache-purge
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_cache_purge_module.so;
```


This document describes nginx-module-cache-purge [v2.5.3](https://github.com/nginx-modules/ngx_cache_purge/releases/tag/2.5.3){target=_blank} 
released on Feb 22 2023.

<hr />
`ngx_cache_purge` is `nginx` module which adds ability to purge content from
`FastCGI`, `proxy`, `SCGI` and `uWSGI` caches. A purge operation removes the 
content with the same cache key as the purge request has.


## Sponsors
Work on the original patch was fully funded by [yo.se](http://yo.se).


## Status
This module is production-ready.


## Configuration directives (same location syntax)
## fastcgi_cache_purge
* **syntax**: `fastcgi_cache_purge on|off|<method> [purge_all] [from all|<ip> [.. <ip>]]`
* **default**: `none`
* **context**: `http`, `server`, `location`

Allow purging of selected pages from `FastCGI`'s cache.


## proxy_cache_purge
* **syntax**: `proxy_cache_purge on|off|<method> [purge_all] [from all|<ip> [.. <ip>]]`
* **default**: `none`
* **context**: `http`, `server`, `location`

Allow purging of selected pages from `proxy`'s cache.


## scgi_cache_purge
* **syntax**: `scgi_cache_purge on|off|<method> [purge_all] [from all|<ip> [.. <ip>]]`
* **default**: `none`
* **context**: `http`, `server`, `location`

Allow purging of selected pages from `SCGI`'s cache.


## uwsgi_cache_purge
* **syntax**: `uwsgi_cache_purge on|off|<method> [purge_all] [from all|<ip> [.. <ip>]]`
* **default**: `none`
* **context**: `http`, `server`, `location`

Allow purging of selected pages from `uWSGI`'s cache.


## Configuration directives (separate location syntax)
## fastcgi_cache_purge
* **syntax**: `fastcgi_cache_purge zone_name key`
* **default**: `none`
* **context**: `location`

Sets area and key used for purging selected pages from `FastCGI`'s cache.


## proxy_cache_purge
* **syntax**: `proxy_cache_purge zone_name key`
* **default**: `none`
* **context**: `location`

Sets area and key used for purging selected pages from `proxy`'s cache.


## scgi_cache_purge
* **syntax**: `scgi_cache_purge zone_name key`
* **default**: `none`
* **context**: `location`

Sets area and key used for purging selected pages from `SCGI`'s cache.


## uwsgi_cache_purge
* **syntax**: `uwsgi_cache_purge zone_name key`
* **default**: `none`
* **context**: `location`

Sets area and key used for purging selected pages from `uWSGI`'s cache.

## Configuration directives (Optional)

## cache_purge_response_type
* **syntax**: `cache_purge_response_type html|json|xml|text`
* **default**: `html`
* **context**: `http`, `server`, `location`

Sets a response type of purging result.



## Partial Keys
Sometimes it's not possible to pass the exact key cache to purge a page. For example; when the content of a cookie or the params are part of the key.
You can specify a partial key adding an asterisk at the end of the URL.

    curl -X PURGE /page*

The asterisk must be the last character of the key, so you **must** put the $uri variable at the end.



## Sample configuration (same location syntax)
    http {
        proxy_cache_path  /tmp/cache  keys_zone=tmpcache:10m;

        server {
            location / {
                proxy_pass         http://127.0.0.1:8000;
                proxy_cache        tmpcache;
                proxy_cache_key    "$uri$is_args$args";
                proxy_cache_purge  PURGE from 127.0.0.1;
            }
        }
    }


## Sample configuration (same location syntax - purge all cached files)
    http {
        proxy_cache_path  /tmp/cache  keys_zone=tmpcache:10m;

        server {
            location / {
                proxy_pass         http://127.0.0.1:8000;
                proxy_cache        tmpcache;
                proxy_cache_key    "$uri$is_args$args";
                proxy_cache_purge  PURGE purge_all from 127.0.0.1 192.168.0.0/8;
            }
        }
    }


## Sample configuration (separate location syntax)
    http {
        proxy_cache_path  /tmp/cache  keys_zone=tmpcache:10m;

        server {
            location / {
                proxy_pass         http://127.0.0.1:8000;
                proxy_cache        tmpcache;
                proxy_cache_key    "$uri$is_args$args";
            }

            location ~ /purge(/.*) {
                allow              127.0.0.1;
                deny               all;
                proxy_cache        tmpcache;
                proxy_cache_key    "$1$is_args$args";
            }
        }
    }

## Sample configuration (Optional)
    http {
        proxy_cache_path  /tmp/cache  keys_zone=tmpcache:10m;

        cache_purge_response_type text;

        server {

            cache_purge_response_type json;

            location / { #json
                proxy_pass         http://127.0.0.1:8000;
                proxy_cache        tmpcache;
                proxy_cache_key    "$uri$is_args$args";
            }

            location ~ /purge(/.*) { #xml
                allow              127.0.0.1;
                deny               all;
                proxy_cache        tmpcache;
                proxy_cache_key    "$1$is_args$args";
                cache_purge_response_type xml;
            }

            location ~ /purge2(/.*) { # json
                allow              127.0.0.1;
                deny               all;
                proxy_cache        tmpcache;
                proxy_cache_key    "$1$is_args$args";
            }
        }

        server {

            location / { #text
                proxy_pass         http://127.0.0.1:8000;
                proxy_cache        tmpcache;
                proxy_cache_key    "$uri$is_args$args";
            }

            location ~ /purge(/.*) { #text
                allow              127.0.0.1;
                deny               all;
                proxy_cache        tmpcache;
                proxy_cache_key    "$1$is_args$args";
            }

            location ~ /purge2(/.*) { #html
                allow              127.0.0.1;
                deny               all;
                proxy_cache        tmpcache;
                proxy_cache_key    "$1$is_args$args";
                cache_purge_response_type html;
            }
        }
    }



## Solve problems
* Enabling [`gzip_vary`](https://nginx.org/r/gzip_vary) can lead to different results when clearing, when enabling it, you may have problems clearing the cache. For reliable operation, you can disable [`gzip_vary`](https://nginx.org/r/gzip_vary) inside the location [#20](https://github.com/nginx-modules/ngx_cache_purge/issues/20).


## Testing
`ngx_cache_purge` comes with complete test suite based on [Test::Nginx](http://github.com/agentzh/test-nginx).

You can test it by running:

`$ prove`


## See also
- [ngx_slowfs_cache](http://github.com/FRiCKLE/ngx_slowfs_cache).
- http://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#purger
- http://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_cache_purge
- https://github.com/wandenberg/nginx-selective-cache-purge-module
- https://github.com/wandenberg/nginx-sorted-querystring-module
- https://github.com/ledgetech/ledge
- [Faking Surrogate Cache-Keys for Nginx Plus](https://www.innoq.com/en/blog/faking-surrogate-cache-keys-for-nginx-plus/) ([gist](https://gist.github.com/titpetric/2f142e89eaa0f36ba4e4383b16d61474))
- [Delete NGINX cached md5 items with a PURGE with wildcard support](https://gist.github.com/nosun/0cfb58d3164f829e2f027fd37b338ede)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-cache-purge](https://github.com/nginx-modules/ngx_cache_purge){target=_blank}.