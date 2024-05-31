# NGINX-MOD

As you may know, [our repository](https://www.getpagespeed.com/redhat){target=_blank} holds the latest stable NGINX and a vast array of dynamic modules for it. 

However, some performance-oriented folks are always looking for speeding up what's already fast - that is NGINX itself. 

There are some open-source patches for it, mainly by Cloudflare to improve things further. 
To save trouble for many people relying on a manual compilation, we build this better patched NGINX as a package that is compatible with all the NGINX modules we have! 
Its official name is NGINX-MOD.

NGINX-MOD is based on the latest *stable* NGINX with the following additions:

* Latest OpenSSL 1.1.x (allows for TLS 1.3 to be configured)
* Patch for HTTP/2 HPACK (performance)
* Patch for dynamic TLS records (performance)
* Patch that allows ngx_http_limit_req_module to support rates of an hour, minute, day, week, and year
* [Active Health Checks](https://github.com/yaoweibin/nginx_upstream_check_module)
* Patch allowing to disable emission of NGINX software name in both the `Server:` header and error pages
* Patch allowing `CONNECT` request method

More on those patches in the documentation below.

## How to install NGINX-MOD

```bash
sudo yum -y install https://extras.getpagespeed.com/release-latest.rpm yum-utils
sudo yum-config-manager --disable getpagespeed-extras-mainline
sudo yum-config-manager --enable getpagespeed-extras-nginx-mod
sudo yum -y install nginx
sudo systemctl enable --now nginx
```

## How to switch to NGINX-MOD from our regular NGINX

If you were using our regular NGINX build, you can run a series of commands to upgrade to NGINX-MOD without affecting installed modules or configuration:

```bash
sudo yum -y install https://extras.getpagespeed.com/release-latest.rpm yum-utils
sudo yum-config-manager --disable getpagespeed-extras-mainline
sudo yum-config-manager --enable getpagespeed-extras-nginx-mod
sudo yum -y update nginx
# importantly, we must re-enable the nginx service after switching packages:
sudo systemctl enable --now nginx
```


## Modules for NGINX-MOD

NGINX-MOD is fully compatible with over 50 NGINX module packages in our base repository.
So you can install them as usual, for example:

    sudo yum -y install nginx-module-pagespeed

## Active Health Checks

Please refer [here](https://github.com/yaoweibin/nginx_upstream_check_module) for additional documentation.

## ngx_http_limit_req_module patch

Some NGINX users seek to define rate-limiting of once in a day for specific resources. This is not possible with stock NGINX.
Our patch allows for a more fine-grained rate limit configuration. Examples:

    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/h; # 1 request per hour
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/d; # 1 request per day
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/w; # 1 request per week
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/M; # 1 request per month
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/Y; # 1 request per year

It is important to note, that your defined zone memory size should allow retaining old IP entries before the defined rate will apply.

For example: you have defined a `10m` zone and `1r/d` for a particular resource. `10m` can store around 160,000 IP addresses.
So if someone visits your rate-limited resource, *and your traffic to it exceed 160K unique visitors within 24 hrs*, then the same visitor can theoretically not be rate-limited within the same day, because information about his IP address will be evicted from memory after enough visitors visited the resource.

This note applies to the stock module's configuration as well, but less so.

So the rules of thumb are:

* You likely need to  increase memory zone, if your traffic is sufficient to be able to evict old IP addresses "too early"
* This is more appropriate for rate-limiting specific resources, not the whole website

## What is HPACK Patch

HPACK patch implements [full HPACK](https://blog.cloudflare.com/hpack-the-silent-killer-feature-of-http-2/) in NGINX. In short, this allows for compressing HTTP headers

## What is the `CONNECT` patch

This patch allows `CONNECT` request method. To configure your NGINX to handle such requests, install the supplementary module:

    sudo yum -y install nginx-mod-module-proxy-connect

Documentation of this module [can be found here](https://github.com/dvershinin/ngx_http_proxy_connect_module). 

## Configuration Directives of NGINX-MOD

There are some configuration directives in this build, which are not otherwise available in regular builds. Let's document them here.

The following set of configuration directives are added by [dynamic TLS records](https://blog.cloudflare.com/optimizing-tls-over-tcp-to-reduce-latency/) patch. 

### `ssl_dyn_rec_enable on|off`

Whether to enable dynamic TLS records.

### `ssl_dyn_rec_size_lo`

The TLS record size to start with. Defaults to 1369 bytes (designed to fit the entire record in a single TCP segment: 1369 = 1500 - 40 (IPv6) - 20 (TCP) - 10 (Time) - 61 (Max TLS overhead))
ssl_dyn_rec_size_hi: the TLS record size to grow to. Defaults to 4229 bytes (designed to fit the entire record in 3 TCP segments)

### `ssl_dyn_rec_threshold`

The number of records to send before changing the record size.

Because we build with latest OpenSSL:

### `ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3];`

Not a new directive. But since we build with the most recent stable OpenSSL, it allows for `TLSv1.3` value to be used.

## Hiding software information

By default, NGINX only supports `server_tokens off;` which still yields `nginx` in the `Server:` header and in error pages.
With NGINX-MOD, you can specify a new value `none`, which will cause NGINX to stop emission of its presence on the server:

    server_tokens none;

## Verification

To verify how you benefit from NGINX-MOD, you can run some tests.

### Check HTTP/2 headers compression

```
yum install nghttp2
h2load https://example.com -n 2 | tail -6 |head -1
```

Example output:

> traffic: 71.46KB (73170) total, 637B (637) headers (space savings 78.68%), 70.61KB (72304) data

If you see 50% or more space savings, then it means that full HPACK compression is utilized.

## How to switch back to stable NGINX

Going back to the stable package while preserving existing configuration:

```
yum-config-manager --disable getpagespeed-extras-nginx-mod
MOD_PKGS=$(rpm -qa --queryformat '%{NAME}\n' | grep nginx-mod | grep -v nginx-module)
rpm --erase --justdb --nodeps ${MOD_PKGS}
STABLE_PKGS=$(echo ${MOD_PKGS} | sed 's@nginx-mod@nginx@g')
yum -y install ${STABLE_PKGS}
yum history sync
# importantly, we must re-enable the nginx service after switching packages:
sudo systemctl enable --now nginx
```

These commands will disable the NGINX-MOD repository and replace any `nginx-mod*` packages with their equivalents from the base repository, thus downgrading to stable NGINX.

## Compatibility notes

* NGINX-MOD is presently not compatible with the Plesk control panel
