---

title: "NGINX ipset access module"
description: "RPM package nginx-module-ipset-access. NGINX module to control user access to sites using ipset "

---

# *ipset-access*: NGINX ipset access module


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


This document describes nginx-module-ipset-access [v1.0.5](https://github.com/GetPageSpeed/ngx_ipset_access_module/releases/tag/v1.0.5){target=_blank} 
released on Oct 11 2025.

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
3. Evaluates the client address against each configured set.  
4. Returns a configurable status (default **403 Forbidden**) when the request is blocked.
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

### `ipset_blacklist` *set1* [*set2* …*setN*]

*Context*: `server`  
Blocks requests **if the client IP appears in **any** of the listed ipset(s)**.

### `ipset_whitelist` *set1* [*set2* …*setN*]

*Context*: `server`  
Allows requests **only if the client IP appears in a listed set**. All other IPs are rejected.

### `ipset_status` *code*

*Context*: `server`  
Sets the HTTP status code returned when a request is blocked by `whitelist` or `blacklist`. Defaults to **403** if not set.  
Common choices are `403` (Forbidden) or `444` (drop without response).

### `ipset_autoadd` *setname*

*Context*: `location`  
**Honeypot functionality**: Automatically adds the client IP to the specified ipset when the location is accessed. Perfect for creating honeypot endpoints that automatically blacklist malicious bots and scanners.  
When an IP is auto‑added, the module forces the current connection to close (disables keep‑alive) so attackers cannot reuse the connection.

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
    server {
        listen 80 default_server;
        root /usr/share/nginx/html;

        # Block any IP found in "bad_guys"
        ipset_blacklist bad_guys;

        # Return 444 for blocked requests (optional)
        ipset_status 444;
    }
}
```

Because look‑ups are *live*, adding or removing IPs from `bad_guys` takes effect instantly without reloading NGINX.
## 

## Honeypot Example

Create automatic honeypot traps that add malicious IPs to blacklists:

```bash
## Create ipsets for honeypot functionality
sudo ipset create honeypot hash:ip
sudo ipset create malicious_scanners hash:ip
```

```nginx
load_module modules/ngx_http_ipset_access.so;

http {
    server {
        listen 80 default_server;
        root /usr/share/nginx/html;

        # Use honeypot sets as blacklist - trapped IPs get blocked
        ipset_blacklist honeypot malicious_scanners;
        # Optional: customize blocked status
        ipset_status 403;

        # Normal content
        location / {
            try_files $uri $uri/ =404;
        }

        # Honeypot endpoints - bots that hit these get auto-blacklisted
        location /config.php {
            ipset_autoadd honeypot;
            return 200 "Config access logged";
        }

        location /wp-admin.php {
            ipset_autoadd honeypot;
            return 200 "Admin access logged";
        }

        # Catch common exploit attempts
        location ~ ^/(phpMyAdmin|admin|eval\.php|shell\.php)$ {
            ipset_autoadd malicious_scanners;
            return 200 "Scanner detected";
        }
    }
}
```

When a bot hits `/config.php`, their IP is automatically added to the `honeypot` set and immediately blocked from all further requests. The connection is closed after adding to prevent keep‑alive reuse. No external scripts or fcgiwrap needed!
## 

## Logging & debugging

Build NGINX with `--with-debug` and set `error_log /var/log/nginx/error.log debug;` to see verbose output such as:

```text
test bad_guys 203.0.113.4 -> IPS_TEST_IS_IN_SET
Blocking 203.0.113.4 due to IPSET
```
## 

## Return codes

| Condition                           | HTTP status                         |
|-------------------------------------|-------------------------------------|
| `whitelist` and not in any set      | Default **403** (or `ipset_status`) |
| `blacklist` and present in a set    | Default **403** (or `ipset_status`) |
| Transient ipset error (safety deny) | Default **403** (or `ipset_status`) |
## 

## Limitations & Roadmap

* IPv4 only – `AF_INET6` is not yet supported.  
* Uses synchronous libipset calls; at very high request rates the kernel may be faster with `nft set` rules alone.  
* Custom return status **444** is prepared but commented; enable if you need drop‑without‑reply semantics.
## 

## 

## Dev & Test Workflow (fast iteration)

To avoid re-downloading and rebuilding NGINX on every test run, we use a prebuilt Docker base image with NGINX and Test::Nginx. Tests then compile only this module as a dynamic `.so` and load it via the harness.

Prereqs: Docker (and optionally `act` if you want to run the CI workflow locally).

Quick start:

```bash
## 1) Build the reusable base image once per NGINX version
make base-image NGINX_VERSION=release-1.27.2

## 2) Run the whole test suite (compiles only the module .so each run)
make tests NGINX_VERSION=release-1.27.2

## 3) Iterate on a single test file
make tests NGINX_VERSION=release-1.27.2 T=t/10-ipset.t
```

Details:
- The base image is defined in `Dockerfile.tests-base` and tagged `nginx-ipset-access-tests-base:<NGINX_VERSION>`.
- At test time, the runner script (`docker-run-tests.sh`) configures NGINX with `--add-dynamic-module` pointing at the repo (`/work`), runs `make modules`, then sets:
  - `TEST_NGINX_BINARY` to the prebuilt `nginx` binary
  - `TEST_NGINX_LOAD_MODULES` to the compiled `.so`

Tips:
- For logs and speed during iteration the Makefile sets:
  - `TEST_NGINX_FAST_SHUTDOWN=1`
  - `TEST_NGINX_NO_CLEAN=1` (keeps `t/servroot/`)
  - `TEST_NGINX_LOG_LEVEL=debug`
  - `TEST_NGINX_ERROR_LOG=/work/test-error.log`
- Use `T=<path>` to run an individual test file. Inspect `t/servroot/conf/nginx.conf` and `test-error.log` when debugging.

Run the CI workflow locally with `act`:

```bash
## Requires: npm i -g act (or brew install act), Docker daemon running
act -W .github/workflows/build.yml -j build --container-daemon-socket 'unix:///var/run/docker.sock'
```

This locally reproduces the GitHub Actions job that builds the base image and executes the test suite inside a container with `NET_ADMIN` capability.
## 

## 

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-ipset-access](https://github.com/GetPageSpeed/ngx_ipset_access_module){target=_blank}.