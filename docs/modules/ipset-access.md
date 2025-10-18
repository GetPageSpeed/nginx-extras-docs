---

title: "NGINX ipset access module"
description: "RPM package nginx-module-ipset-access. NGINX module to control user access to sites using ipset "

---

# *ipset-access*: NGINX ipset access module


## Installation

> Requires the Enterprise plan of the GetPageSpeed NGINX Extras subscription.

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9 and 10
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023+"

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-ipset-access
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-ipset-access
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_ipset_access.so;
```


This document describes nginx-module-ipset-access [v1.0.4](https://github.com/GetPageSpeed/nginx_ipset_access_module/releases/tag/v1.0.4){target=_blank} 
released on Sep 20 2025.

<hr />

A high‑performance NGINX module that lets you **whitelist** or **blacklist** client IP addresses using the Linux **ipset** kernel facility.  
All look‑ups are made in userspace via `libipset` and cached *per worker thread* to minimise overhead.
## 

## Features

* **Zero‑runtime overhead** – IPSet sessions are initialised once and cached with thread‑local storage.  
* **Whitelist & Blacklist modes** – block everything except the listed sets, or allow everything except the listed sets.  
* **Dynamic updates** – modifying an `ipset` does **not** require an NGINX reload.  
* **Native RPM packages** for RHEL / Alma / Rocky and derivatives via GetPageSpeed repository.
## 

## How it works

```text
┌ Client ──► NGINX worker
│             │
│             ├─► Thread‑local ipset session (libipset)
│             │      ├─ Test client IP against one or more sets
│             │      └─ Cache session handle for reuse
│             │
└─────────────┴── Allow / Deny based on match & mode
```

The module:

1. Initialises `libipset` once per worker process.  
2. Caches a session handle in POSIX thread‑specific data (`pthread_setspecific`).  
3. Evaluates the client’s IPv4 address (`AF_INET`) against each configured set.  
4. Returns **403 Forbidden** (or custom code *444* when `blacklist` mode is selected and the IP matches).
## 

## 

## Quick installation (RPM‑based distributions)

```bash
sudo dnf --assumeyes install https://extras.getpagespeed.com/release-latest.rpm
sudo dnf --assumeyes install nginx-module-ipset-access
```

> **Tip:** The package is signed; make sure you have `gpgcheck=1` enabled.

Enable the module in **`/etc/nginx/nginx.conf`** **before** any `http {}` blocks:

```nginx
load_module modules/ngx_http_ipset_access.so;
```

Reload NGINX to apply:

```bash
sudo systemctl reload nginx
```
## 

## Clone NGINX and the module
git clone https://github.com/nginx/nginx.git
git clone https://example.com/ngx_ipset_access.git

cd nginx
./auto/configure   --with-compat   --add-dynamic-module=../ngx_ipset_access
make -j$(nproc)
sudo make install
```

The build produces `objs/ngx_http_ipset_access.so`; copy it to your NGINX *modules* directory and add `load_module` as shown above.
## 

## Configuration Directives

### `blacklist` *set1* [*set2* …*setN*]

*Context*: `http`, `server`  
Blocks requests **if the client IP appears in **any** of the listed ipset(s)**.

### `whitelist` *set1* [*set2* …*setN*]

*Context*: `http`, `server`  
Allows requests **only if the client IP appears in a listed set**. All other IPs are rejected.

### `off`

Either directive accepts the literal word `off` to disable processing for the current context:

```nginx
server {
    listen 80;
    blacklist off;   # no ipset filtering in this virtual‑host
}
```
## 

## Example usage

```bash
## Create an ipset of blocked addresses
sudo ipset create bad_guys hash:ip
sudo ipset add bad_guys 203.0.113.4
sudo ipset add bad_guys 198.51.100.23
```

```nginx
load_module modules/ngx_http_ipset_access.so;

http {
    # Block any IP found in "bad_guys"
    blacklist bad_guys;

    server {
        listen 80 default_server;
        root /usr/share/nginx/html;
    }
}
```

Because look‑ups are *live*, adding or removing IPs from `bad_guys` takes effect instantly without reloading NGINX.
## 

## Logging & debugging

Build NGINX with `--with-debug` and set `error_log /var/log/nginx/error.log debug;` to see verbose output such as:

```text
test bad_guys 203.0.113.4 -> IPS_TEST_IS_IN_SET
Blocking 203.0.113.4 due to IPSET
```
## 

## Return codes

| Mode        | IP match result        | HTTP status |
|-------------|------------------------|-------------|
| `whitelist` | Not in any set         | **403** |
| `blacklist` | In a configured set    | **403** (module can be patched to 444) |
| Any         | Error contacting ipset | **403** (treated as deny for safety) |
## 

## Limitations & Roadmap

* IPv4 only – `AF_INET6` is not yet supported.  
* Uses synchronous libipset calls; at very high request rates the kernel may be faster with `nft set` rules alone.  
* Custom return status **444** is prepared but commented; enable if you need drop‑without‑reply semantics.
## 

## 

## 

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-ipset-access](https://github.com/GetPageSpeed/nginx_ipset_access_module){target=_blank}.