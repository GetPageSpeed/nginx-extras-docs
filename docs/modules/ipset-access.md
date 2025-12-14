---

title: "NGINX ipset access module"
description: "RPM package nginx-module-ipset-access. NGINX module to control user access to sites using IPSets "

---

# *ipset-access*: NGINX ipset access module

> Requires the Enterprise plan of the GetPageSpeed NGINX Extras subscription.



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


This document describes nginx-module-ipset-access v2.0.2 
released on Dec 09 2025.

<hr />

Enterprise-grade IP-based access control for NGINX using Linux ipset. Block threats, rate-limit abusers, challenge bots, and protect your infrastructure.

[![Version](https://img.shields.io/badge/version-2.0.2-blue)](https://www.getpagespeed.com/server-setup/nginx-modules/ipset-access)
[![GetPageSpeed](https://img.shields.io/badge/GetPageSpeed-Premium-gold)](https://www.getpagespeed.com/)

> **⚠️ Commercial Software**  
> This is a closed-source premium module available exclusively through the [GetPageSpeed Repository](https://www.getpagespeed.com/repo-subscribe).
## 

## 

## ✨ Features

### Core Features
| Feature | Description |
|---------|-------------|
| **Whitelist/Blacklist** | Allow or deny based on ipset membership |
| **Multiple ipsets** | Check against multiple ipsets in one directive |
| **Live updates** | Modify ipsets without reloading NGINX |
| **Custom status codes** | Return any HTTP status when blocking |

### Performance Features
| Feature | Description |
|---------|-------------|
| **Per-thread sessions** | Thread-local libipset sessions eliminate lock contention |
| **LRU Cache** | Shared memory cache with configurable TTL |
| **Cache hit rates** | Typically 95%+ hit rate reduces kernel calls |

### Security Features
| Feature | Description |
|---------|-------------|
| **Rate limiting** | Limit requests per IP with configurable windows |
| **Auto-ban** | Automatically blacklist rate limit violators |
| **JS Challenge** | Proof-of-work challenge stops automated bots |
| **Honeypot traps** | Auto-blacklist IPs hitting trap URLs |
| **Entry timeout** | Auto-expire blacklist entries |

### Operational Features
| Feature | Description |
|---------|-------------|
| **Dry-run mode** | Test configuration without blocking |
| **Fail-open/close** | Control behavior on ipset errors |
| **Prometheus metrics** | Native `/metrics` endpoint for Grafana |
| **JSON stats** | Detailed statistics API |
| **NGINX variables** | `$ipset_result` and `$ipset_matched_set` |
## 

## 🚀 Quick Start

### 1. Create ipsets

```bash
## Create a blacklist
sudo ipset create bad_guys hash:ip timeout 86400

## Create a rate-limit ban list  
sudo ipset create ratelimited hash:ip timeout 1800

## Create a honeypot trap list
sudo ipset create honeypot hash:ip timeout 86400
```

### 2. Configure NGINX

```nginx
load_module modules/ngx_http_ipset_access_module.so;

http {
    server {
        listen 80;
        
        # Block known bad IPs
        ipset_blacklist bad_guys;
        
        # Rate limit: 100 requests per minute
        ipset_ratelimit rate=100 window=60s autoban=ratelimited;
        
        # Your content
        location / {
            root /var/www/html;
        }
        
        # Honeypot trap
        location /wp-admin.php {
            ipset_autoadd honeypot;
            return 200 "OK";
        }
        
        # Metrics endpoint
        location /metrics {
            ipset_metrics;
            allow 127.0.0.1;
            deny all;
        }
    }
}
```

### 3. Test and reload

```bash
sudo nginx -t && sudo nginx -s reload
```
## 

## 📦 Installation

This module is available exclusively through the **GetPageSpeed Premium Repository**.

### Step 1: Subscribe to GetPageSpeed Repository

Visit [GetPageSpeed Repository Subscription](https://www.getpagespeed.com/repo-subscribe) to get access.

### Step 2: Install the Repository

```bash
## RHEL/CentOS/Rocky/Alma Linux 8+
sudo dnf install https://extras.getpagespeed.com/release-latest.rpm
```

### Step 3: Install the Module

```bash
sudo dnf install nginx-module-ipset-access
```

### Step 4: Enable the Module

Add to `/etc/nginx/nginx.conf` before any `http {}` blocks:

```nginx
load_module modules/ngx_http_ipset_access_module.so;
```

### Step 5: Reload NGINX

```bash
sudo nginx -t && sudo systemctl reload nginx
```
## 

## 📖 Configuration Reference

### Access Control

#### `ipset_blacklist` *set1* [*set2* ...]

**Context:** `server`  
**Default:** —

Blocks requests if the client IP appears in **any** of the listed ipsets. Multiple ipsets are checked in order until a match is found.

```nginx
## Single set
ipset_blacklist bad_guys;

## Multiple sets (OR logic - blocked if in ANY set)
ipset_blacklist spammers hackers tor_exits;

## Disable
ipset_blacklist off;
```

#### `ipset_whitelist` *set1* [*set2* ...]

**Context:** `server`  
**Default:** —

Allows requests **only** if the client IP appears in at least one of the listed ipsets. All other IPs are rejected.

```nginx
## Only allow trusted IPs
ipset_whitelist trusted_partners office_ips;
```

#### `ipset_status` *code*

**Context:** `server`  
**Default:** `403`

HTTP status code returned when a request is blocked.

```nginx
ipset_status 403;   # Forbidden (default)
ipset_status 444;   # Close connection without response (NGINX special)
ipset_status 429;   # Too Many Requests
ipset_status 503;   # Service Unavailable
```
## 

### Caching & Performance

#### `ipset_cache_ttl` *time*

**Context:** `server`  
**Default:** `60s`

How long to cache ipset lookup results. Cached results avoid repeated kernel calls for the same IP.

```nginx
ipset_cache_ttl 30s;    # 30 seconds
ipset_cache_ttl 5m;     # 5 minutes
ipset_cache_ttl 1h;     # 1 hour
```

**Performance Impact:**
- Higher TTL = Better performance, but slower to reflect ipset changes
- Lower TTL = More responsive to ipset changes, but more kernel calls
- Recommended: `30s` to `5m` for most use cases

#### `ipset_fail_open` on|off

**Context:** `server`  
**Default:** `off`

Controls behavior when an ipset lookup fails (e.g., set doesn't exist).

```nginx
ipset_fail_open off;   # Deny on error (secure, default)
ipset_fail_open on;    # Allow on error (available but risky)
```

#### `ipset_dryrun` on|off

**Context:** `server`  
**Default:** `off`

When enabled, logs what would be blocked but doesn't actually block. Perfect for testing new rules in production.

```nginx
ipset_dryrun on;   # Log but don't block
```

Check logs for messages like:
```
ipset: DRYRUN would block 1.2.3.4 (matched: bad_guys)
```
## 

### Rate Limiting

#### `ipset_ratelimit` *parameters*

**Context:** `server`  
**Default:** —

Limits requests per IP within a time window. Can automatically add violators to an ipset.

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `rate=N` | Yes | Maximum requests per window |
| `window=TIME` | No | Time window (default: 60s) |
| `autoban=SET` | No | ipset to add violators |
| `ban_time=N` | No | Seconds until auto-expire (default: 3600) |

**Examples:**

```nginx
## Basic: 100 requests per minute
ipset_ratelimit rate=100;

## With custom window: 1000 requests per hour
ipset_ratelimit rate=1000 window=1h;

## With auto-ban: Add violators to ipset for 30 minutes
ipset_ratelimit rate=60 window=1m autoban=ratelimited ban_time=1800;

## Strict API protection
ipset_ratelimit rate=10 window=1s autoban=api_abusers ban_time=3600;
```

**How it works:**
1. Each IP gets a request counter and window start time
2. Counter increments on each request
3. When window expires, counter resets
4. If counter exceeds `rate`, returns `429 Too Many Requests`
5. If `autoban` is set, IP is added to specified ipset

**Note:** Rate limit state is stored in shared memory and survives worker restarts.
## 

### JavaScript Challenge

#### `ipset_challenge` on|off

**Context:** `server`  
**Default:** `off`

Enables JavaScript challenge mode. Browsers must solve a proof-of-work puzzle to access the site. Effective against automated bots and scrapers.

```nginx
ipset_challenge on;
```

**How it works:**
1. First request receives a challenge page (HTTP 503)
2. Browser executes JavaScript that solves a hash puzzle
3. Solution is stored in a cookie (`_ipset_verified`)
4. Subsequent requests with valid cookie pass through
5. Cookie expires after 24 hours

#### `ipset_challenge_difficulty` *level*

**Context:** `server`  
**Default:** `2`

Controls challenge difficulty (1-8). Higher = longer solve time.

| Level | Approximate Solve Time |
|-------|------------------------|
| 1 | ~100ms |
| 2 | ~500ms (default) |
| 3 | ~1 second |
| 4 | ~2 seconds |
| 5 | ~5 seconds |
| 6+ | ~10+ seconds |

```nginx
ipset_challenge on;
ipset_challenge_difficulty 3;  # ~1 second solve time
```

**Challenge Page Features:**
- Modern, responsive design
- Animated loading spinner
- Progress feedback
- Auto-redirect on success
- No external dependencies
## 

### Honeypot Auto-add

#### `ipset_autoadd` *setname* [timeout=*seconds*]

**Context:** `location`  
**Default:** —

Automatically adds client IP to specified ipset when the location is accessed. Perfect for honeypot traps.

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| *setname* | Yes | Target ipset name |
| `timeout=N` | No | Entry timeout in seconds |

**Examples:**

```nginx
## Basic: Add to honeypot set (permanent until manual removal)
location /config.php {
    ipset_autoadd honeypot;
    return 200 "OK";
}

## With timeout: Auto-expire after 24 hours
location /wp-admin.php {
    ipset_autoadd scanners timeout=86400;
    return 200 "OK";
}

## Severe: Block for 1 week
location ~ \.(sh|pl|cgi)$ {
    ipset_autoadd malicious timeout=604800;
    return 200 "OK";
}
```

**Common Honeypot Paths:**
```nginx
## WordPress traps
location ~ ^/(wp-admin\.php|wp-login\.php|xmlrpc\.php)$ {
    ipset_autoadd honeypot timeout=86400;
    return 200 "OK";
}

## Config file traps
location ~ ^/(\\.env|config\\.php|phpinfo\\.php)$ {
    ipset_autoadd honeypot timeout=86400;
    return 200 "OK";
}

## Shell/exploit traps
location ~ ^/(shell|cmd|eval|exec)\\.php$ {
    ipset_autoadd malicious timeout=604800;
    return 200 "OK";
}
```

**Note:** When an IP is auto-added, the connection's keep-alive is disabled to prevent further requests on the same connection.
## 

### Observability

#### `ipset_stats`

**Context:** `location`  
**Default:** —

Enables the JSON statistics endpoint.

```nginx
location = /_stats {
    ipset_stats;
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    deny all;
}
```

See [JSON Stats API](#-json-stats-api) for response format.

#### `ipset_metrics`

**Context:** `location`  
**Default:** —

Enables the Prometheus metrics endpoint.

```nginx
location = /metrics {
    ipset_metrics;
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    deny all;
}
```

See [Prometheus Metrics](#-prometheus-metrics) for available metrics.
## 

## 📝 NGINX Variables

The module exposes two variables for use in logging, headers, or conditionals.

### `$ipset_result`

The access decision made for this request.

| Value | Description |
|-------|-------------|
| `allow` | Request allowed |
| `deny` | Request blocked |
| `dryrun` | Would be blocked (dry-run mode) |
| `ratelimited` | Rate limit exceeded |
| `challenged` | Challenge page served |

### `$ipset_matched_set`

Name of the ipset that matched (if any). Empty if no match.

### Usage Examples

**Custom access log:**

```nginx
log_format security '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    'ipset_result="$ipset_result" '
                    'matched_set="$ipset_matched_set"';

access_log /var/log/nginx/security.log security;
```

**Add headers for debugging:**

```nginx
add_header X-IPSet-Result $ipset_result always;
add_header X-IPSet-Matched $ipset_matched_set always;
```

**Conditional logging:**

```nginx
## Only log blocked requests
map $ipset_result $loggable {
    "deny"  1;
    default 0;
}

access_log /var/log/nginx/blocked.log combined if=$loggable;
```
## 

## 📊 Prometheus Metrics

The `/metrics` endpoint returns metrics in Prometheus exposition format.

### Available Metrics

```prometheus
## HELP nginx_ipset_requests_total Total requests processed
## TYPE nginx_ipset_requests_total counter
nginx_ipset_requests_total{result="checked"} 1234567
nginx_ipset_requests_total{result="allowed"} 1234000
nginx_ipset_requests_total{result="blocked"} 500
nginx_ipset_requests_total{result="error"} 67

## HELP nginx_ipset_cache_total Cache operations
## TYPE nginx_ipset_cache_total counter
nginx_ipset_cache_total{result="hit"} 1200000
nginx_ipset_cache_total{result="miss"} 34567

## HELP nginx_ipset_cache_entries Current cache entries
## TYPE nginx_ipset_cache_entries gauge
nginx_ipset_cache_entries 5432

## HELP nginx_ipset_autoadd_total Auto-add operations
## TYPE nginx_ipset_autoadd_total counter
nginx_ipset_autoadd_total{result="success"} 42
nginx_ipset_autoadd_total{result="failed"} 3

## HELP nginx_ipset_ratelimit_total Rate limit events
## TYPE nginx_ipset_ratelimit_total counter
nginx_ipset_ratelimit_total{action="triggered"} 156
nginx_ipset_ratelimit_total{action="autobanned"} 23

## HELP nginx_ipset_challenge_total Challenge events
## TYPE nginx_ipset_challenge_total counter
nginx_ipset_challenge_total{result="issued"} 1000
nginx_ipset_challenge_total{result="passed"} 950
nginx_ipset_challenge_total{result="failed"} 50

## HELP nginx_ipset_uptime_seconds Module uptime
## TYPE nginx_ipset_uptime_seconds gauge
nginx_ipset_uptime_seconds 86400
```

### Grafana Dashboard Queries

**Request rate by result:**
```promql
rate(nginx_ipset_requests_total[5m])
```

**Block rate:**
```promql
rate(nginx_ipset_requests_total{result="blocked"}[5m])
```

**Cache hit rate:**
```promql
rate(nginx_ipset_cache_total{result="hit"}[5m]) / 
(rate(nginx_ipset_cache_total{result="hit"}[5m]) + rate(nginx_ipset_cache_total{result="miss"}[5m]))
```

**Rate limit triggers per minute:**
```promql
rate(nginx_ipset_ratelimit_total{action="triggered"}[1m]) * 60
```
## 

## 📈 JSON Stats API

The `/_stats` endpoint returns detailed statistics in JSON format.

### Response Format

```json
{
  "version": "2.0.2",
  "uptime_seconds": 86400,
  "requests": {
    "checked": 1234567,
    "allowed": 1234000,
    "blocked": 500,
    "errors": 67
  },
  "cache": {
    "hits": 1200000,
    "misses": 34567,
    "entries": 5432,
    "hit_rate": 97.20
  },
  "autoadd": {
    "success": 42,
    "failed": 3
  },
  "ratelimit": {
    "triggered": 156,
    "autobanned": 23
  },
  "challenge": {
    "issued": 1000,
    "passed": 950,
    "failed": 50
  }
}
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `version` | Module version |
| `uptime_seconds` | Seconds since module loaded |
| `requests.checked` | Total requests processed |
| `requests.allowed` | Requests that passed |
| `requests.blocked` | Requests that were blocked |
| `requests.errors` | ipset lookup errors |
| `cache.hits` | Cache hits (avoided kernel call) |
| `cache.misses` | Cache misses (required kernel call) |
| `cache.entries` | Current cached entries |
| `cache.hit_rate` | Hit rate percentage |
| `autoadd.success` | Successful honeypot additions |
| `autoadd.failed` | Failed honeypot additions |
| `ratelimit.triggered` | Rate limit violations |
| `ratelimit.autobanned` | IPs auto-added to ban list |
| `challenge.issued` | Challenge pages served |
| `challenge.passed` | Challenges solved successfully |
| `challenge.failed` | Challenge failures |
## 

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           REQUEST FLOW                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Incoming Request                                                   │
│         │                                                            │
│         ▼                                                            │
│   ┌───────────────┐                                                  │
│   │  Rate Limit   │──── Exceeded? ────▶ 429 + Auto-ban              │
│   │    Check      │                                                  │
│   └───────┬───────┘                                                  │
│           │ OK                                                       │
│           ▼                                                          │
│   ┌───────────────┐                                                  │
│   │   Challenge   │──── No cookie? ────▶ Serve JS Puzzle            │
│   │    Check      │                                                  │
│   └───────┬───────┘                                                  │
│           │ Passed                                                   │
│           ▼                                                          │
│   ┌───────────────┐     ┌─────────────┐                             │
│   │  Cache Check  │────▶│   HIT       │────▶ Use cached result      │
│   └───────┬───────┘     └─────────────┘                             │
│           │ MISS                                                     │
│           ▼                                                          │
│   ┌───────────────┐                                                  │
│   │  ipset Query  │──── Thread-local libipset session               │
│   │  (kernel)     │                                                  │
│   └───────┬───────┘                                                  │
│           │                                                          │
│           ▼                                                          │
│   ┌───────────────┐                                                  │
│   │ Store in Cache│                                                  │
│   └───────┬───────┘                                                  │
│           │                                                          │
│           ▼                                                          │
│   ┌───────────────┐                                                  │
│   │    Decision   │──── Blacklist match? ────▶ Block (403/444)      │
│   │               │──── Whitelist miss?  ────▶ Block (403/444)      │
│   └───────┬───────┘                                                  │
│           │ Allow                                                    │
│           ▼                                                          │
│   ┌───────────────┐                                                  │
│   │   Honeypot    │──── Location match? ────▶ Add to ipset          │
│   │    Check      │                                                  │
│   └───────┬───────┘                                                  │
│           │                                                          │
│           ▼                                                          │
│       Continue to                                                    │
│       Content Handler                                                │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                        SHARED MEMORY                                 │
│  ┌────────────────┬─────────────────┬─────────────────────────────┐ │
│  │     Stats      │    LRU Cache    │    Rate Limit Buckets       │ │
│  │   (counters)   │  (IP → Result)  │   (IP → Request Count)      │ │
│  └────────────────┴─────────────────┴─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Memory Layout

| Component | Location | Purpose |
|-----------|----------|---------|
| libipset session | Thread-local | Per-worker session to avoid locks |
| Lookup cache | Shared memory | LRU cache of IP→result mappings |
| Rate limit buckets | Shared memory | Per-IP request counters |
| Statistics | Shared memory | Atomic counters for metrics |
## 

## 📚 Examples

### Example 1: Basic Blacklist

```bash
## Create ipset
sudo ipset create blacklist hash:ip
sudo ipset add blacklist 1.2.3.4
```

```nginx
    server {
    listen 80;

    ipset_blacklist blacklist;

    location / {
        root /var/www/html;
    }
}
```

### Example 2: API with Rate Limiting

```nginx
server {
    listen 80;
    
    # Strict rate limiting for API
    ipset_ratelimit rate=100 window=1m autoban=api_banned ban_time=3600;
    
    # Only allow known partners
    ipset_whitelist api_partners;
    ipset_status 401;
    
    location /api/ {
        proxy_pass http://backend;
    }
}
```

### Example 3: Full Security Stack

```nginx
    server {
        listen 80 default_server;
    
    # Layer 1: Known threats
    ipset_blacklist malware_ips tor_exits datacenter_ranges;
    ipset_status 444;
    ipset_cache_ttl 5m;
    
    # Layer 2: Rate limiting
    ipset_ratelimit rate=60 window=1m autoban=ratelimited ban_time=1800;
    
    # Layer 3: Bot challenge
    ipset_challenge on;
    ipset_challenge_difficulty 2;
    
    # Real content
        location / {
        root /var/www/html;
    }
    
    # Honeypot traps
    location ~ ^/(wp-admin|phpmyadmin|admin)\.php$ {
        ipset_autoadd honeypot timeout=86400;
        return 200 "OK";
    }
    
    # Monitoring
    location = /metrics {
        ipset_metrics;
        allow 10.0.0.0/8;
        deny all;
    }
}
```

### Example 4: Dry-run Testing

```nginx
server {
    listen 80;
    
    # Test new rules without blocking
    ipset_blacklist new_threat_list;
    ipset_dryrun on;
    
    location / {
        root /var/www/html;
    }
}
```

Check logs:
```bash
tail -f /var/log/nginx/error.log | grep "DRYRUN"
```
## 

## 🔧 Troubleshooting

### Module not loading

```
nginx: [emerg] dlopen() failed
```

**Solution:** Ensure NGINX was built with `--with-compat` and the module was built against the same NGINX version.

### ipset not found

```
ipset: INVALID_SETNAME
```

**Solution:** Create the ipset before starting NGINX:
```bash
sudo ipset create myset hash:ip
```

### Permission denied

```
ipset: kernel error
```

**Solution:** NGINX worker needs `CAP_NET_ADMIN` capability:
```bash
sudo setcap cap_net_admin+ep /usr/sbin/nginx
```

### SELinux denials (RHEL/CentOS/AlmaLinux)

```
SELinux is preventing /usr/sbin/nginx from getattr access on the netlink_netfilter_socket
```

**Solution:** Install the included SELinux policy module:

```bash
cd selinux/
sudo ./install.sh
```

Or manually:
```bash
## Verify
semodule -l | grep nginx_ipset
```

The policy allows `httpd_t` (NGINX's SELinux domain) to use netlink_netfilter sockets required by libipset.

### High memory usage

**Solution:** Reduce cache TTL or limit cache size in shared memory configuration.

### Rate limiting not working

**Solution:** Ensure the ipset for auto-ban exists and has timeout support:
```bash
sudo ipset create ratelimited hash:ip timeout 3600
```
## 

## 📋 Requirements

- **NGINX** ≥ 1.22 (built with `--with-compat`)
- **Linux kernel** with ipset support (nf_tables or xt_set module)
- **libipset** library and development headers
- **Capabilities:** `CAP_NET_ADMIN` for ipset operations
## 

## 📜 License

This is proprietary software. All rights reserved.

Available exclusively through [GetPageSpeed Premium Repository](https://www.getpagespeed.com/repo-subscribe).
## 

## 👤 Author

**Danila Vershinin**  
[GetPageSpeed LLC](https://www.getpagespeed.com/)
## 

## 🆘 Support

- **Honeypot v2.0** [Using ipset-access for auto-banning bots](https://www.getpagespeed.com/server-setup/nginx/nginx-honeypot-v2)
- **Support:** Available for premium subscribers
- **Contact:** [GetPageSpeed Support](https://www.getpagespeed.com/contact-us)
## 

<p align="center">
<b>NGINX IPSet Access Module</b><br>
<i>A premium NGINX module by GetPageSpeed LLC</i><br>
<a href="https://www.getpagespeed.com/">www.getpagespeed.com</a>
</p>

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-ipset-access](https://github.com/GetPageSpeed/ngx_ipset_access_module){target=_blank}.