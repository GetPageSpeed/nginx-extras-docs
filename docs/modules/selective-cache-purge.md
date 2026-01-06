---

title: "Nginx module for the key-value store"
description: "RPM package nginx-module-selective-cache-purge. This nginx module creates variables with values taken from key-value pairs."

---

# *selective-cache-purge*: Nginx module for the key-value store


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
    dnf -y install nginx-module-selective-cache-purge
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-selective-cache-purge
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_keyval_module.so;
```


This document describes nginx-module-selective-cache-purge [v0.3.0](https://github.com/kjdev/nginx-keyval/releases/tag/0.3.0){target=_blank} 
released on Apr 01 2024.

<hr />

This nginx module creates variables with values taken from key-value pairs.

> This module is heavily inspired by the nginx original
> [http_keyval_module](https://nginx.org/en/docs/http/ngx_http_keyval_module.html).

## Dependency

Using the Redis store.

- [hiredis](https://github.com/redis/hiredis)

### Docker

``` sh
$ docker build -t nginx-keyval .
$ : "app.conf: Create nginx configuration"
$ docker run -p 80:80 -v $PWD/app.conf:/etc/nginx/http.d/default.conf nginx-keyval
```

> Github package: ghcr.io/kjdev/nginx-keyval

## Configuration: `ngx_http_keyval_module`

### Example

```nginx
http {
  keyval_zone zone=one:32k;
  keyval $arg_text $text zone=one;
  ...
  server {
    ...
    location / {
      return 200 $text;
    }
  }
}
```

### Directives

```
Syntax: keyval key $variable zone=name;
Default: -
Context: http
```

Creates a new `$variable` whose value is looked up by the `key`
in the key-value database.

The database is stored in shared memory or Redis as specified
by the zone parameter.

In `key`, you can use a mix of variables and text or just variables.

> For example:
> - `$remote_addr:$http_user_agent`
> - `'$remote_addr    $http_user_agent   $host "a random text"'`

```
Syntax: keyval_zone zone=name:size [timeout=time] [ttl=time];
Default: -
Context: http
```

Sets the `name` and `size` of the shared memory zone that
keeps the key-value database.

The optional `timeout` or `ttl` parameter sets the time to live
which key-value pairs are removed (default value is `0` seconds).

```
Syntax: keyval_zone_redis zone=name [hostname=name] [port=number] [database=number] [connect_timeout=time] [ttl=time];
Default: -
Context: http
```

> Using the Redis store

Sets the `name` of the Redis zone that keeps the key-value database.

The optional `hostname` parameter sets the Redis hostname
(default value is `127.0.0.1`).

The optional `port` parameter sets the Redis port
(default value is `6379`).

The optional `database` parameter sets the Redis database number
(default value is `0`).

The optional `connect_timeout` parameter sets the Redis connection
timeout seconds (default value is `3`).

The optional `ttl` parameter sets the time to live
which key-value pairs are removed (default value is `0` seconds).

## Configuration: `ngx_stream_keyval_module`

### Example

```nginx
stream {
  keyval_zone zone=one:32k;
  keyval $ssl_server_name $name zone=one;

  server {
    listen 12345 ssl;
    proxy_pass $name;
    ssl_certificate /usr/share/nginx/conf/cert.pem;
    ssl_certificate_key /usr/share/nginx/conf/cert.key;
  }
}
```

### Directives

```
Syntax: keyval key $variable zone=name;
Default: -
Context: http
```

Creates a new `$variable` whose value is looked up by the `key`
in the key-value database.

The database is stored in shared memory or Redis as specified
by the zone parameter.

```
Syntax: keyval_zone zone=name:size [timeout=time] [ttl=time];
Default: -
Context: http
```

Sets the `name` and `size` of the shared memory zone that
keeps the key-value database.

The optional `timeout` or `ttl` parameter sets the time to live which key-value pairs are removed (default value is 0 seconds).

```
Syntax: keyval_zone_redis zone=name [hostname=name] [port=number] [database=number] [connect_timeout=time] [ttl=time];
Default: -
Context: http
```

> Using the Redis store

Sets the `name` of the Redis zone that keeps the key-value database.

The optional `hostname` parameter sets the Redis hostname
(default value is `127.0.0.1`).

The optional `port` parameter sets the Redis port
(default value is `6379`).

The optional `database` parameter sets the Redis database number
(default value is `0`).

The optional `connect_timeout` parameter sets the Redis connection
timeout seconds (default value is `3`).

The optional `ttl` parameter sets the time to live
which key-value pairs are removed (default value is `0` seconds).

## Example

- [OpenID Connect Authentication](example/README.md)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-selective-cache-purge](https://github.com/kjdev/nginx-keyval){target=_blank}.