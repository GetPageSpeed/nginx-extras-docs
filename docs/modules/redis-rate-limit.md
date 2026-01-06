---

title: "Redis backed rate limit module for Nginx"
description: "RPM package nginx-module-redis-rate-limit. A Redis backed rate limit module for NGINX web servers."

---

# *redis-rate-limit*: Redis backed rate limit module for Nginx


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
    dnf -y install nginx-module-redis-rate-limit
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-redis-rate-limit
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_rate_limit_module.so;
```


This document describes nginx-module-redis-rate-limit [v1.0.0](https://github.com/weserv/rate-limit-nginx-module/releases/tag/v1.0.0){target=_blank} 
released on Jul 16 2022.

<hr />

[![CI status](https://github.com/weserv/rate-limit-nginx-module/workflows/CI/badge.svg)](https://github.com/weserv/rate-limit-nginx-module/actions)

A Redis backed rate limit module for Nginx web servers.

This implementation is based on the following [Redis module](https://redis.io/topics/modules-intro):

* [redis-rate-limiter](https://github.com/onsigntv/redis-rate-limiter)

Which offers a straightforward implementation of the fairly sophisticated [generic cell rate algorithm](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm), in 130 lines of C, without external dependencies.
 

## Synopsis

```nginx
upstream redis {
   server 127.0.0.1:6379;

   # Or: server unix:/var/run/redis/redis.sock;

   # a pool with at most 1024 connections
   keepalive 1024;
}

geo $limit {
    default 1;
    10.0.0.0/8 0;
    192.168.0.0/24 0;
}

map $limit $limit_key {
    0 "";
    1 $remote_addr;
}

rate_limit_status 429;

location = /limit {
    rate_limit $limit_key requests=15 period=1m burst=20;
    rate_limit_pass redis;
}

location = /limit_b {
    rate_limit $limit_key requests=20 period=1m burst=25;
    rate_limit_prefix b;
    rate_limit_pass redis;
}

location = /quota {
    rate_limit $limit_key requests=15 period=1m burst=20;
    rate_limit_quantity 0;
    rate_limit_pass redis;
    rate_limit_headers on;
}
```

## Here we assume you would install you nginx under /opt/nginx/.
./configure --prefix=/opt/nginx \
            --add-module=rate-limit-nginx-module/

make -j$(nproc)
make install
```

## Test suite

The following dependencies are required to run the test suite:

* Nginx version >= 1.9.11

* Perl modules:
    * [Test::Nginx](https://metacpan.org/pod/Test::Nginx::Socket)

* Nginx modules:
	* ngx_http_rate_limit_module (i.e., this module)

* Redis modules:
    * [redis-rate-limiter](https://github.com/onsigntv/redis-rate-limiter)

* Applications:
	* redis: listening on the default port, 6379.

To run the whole test suite in the default testing mode:
```bash
cd /path/to/rate-limit-nginx-module
export PATH=/path/to/your/nginx/sbin:$PATH
prove -I/path/to/test-nginx/lib -r t
```

To run specific test files:
```bash
cd /path/to/rate-limit-nginx-module
export PATH=/path/to/your/nginx/sbin:$PATH
prove -I/path/to/test-nginx/lib t/sanity.t
```

To run a specific test block in a particular test file, add the line 
`--- ONLY` to the test block you want to run, and then use the `prove` 
utility to run that `.t` file.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-redis-rate-limit](https://github.com/weserv/rate-limit-nginx-module){target=_blank}.