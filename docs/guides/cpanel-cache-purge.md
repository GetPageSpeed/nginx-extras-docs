---
title: "WordPress Cache Purging with Varnish HTTP Purge"
description: "Set up automatic NGINX cache purging for WordPress on CloudLinux with ea-nginx using the Varnish HTTP Purge plugin and ngx_cache_purge module."
---

# WordPress Cache Purging on CloudLinux EA4

This guide shows how to set up automatic NGINX cache purging for WordPress sites on 
CloudLinux servers with cPanel's `ea-nginx`, using the **Varnish HTTP Purge** plugin.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Automatic Invalidation**

    ---

    Cache is purged automatically when you edit posts, pages, or comments

-   :material-shield-check:{ .lg .middle } **Multi-Tenant Safe**

    ---

    Each cPanel user's cache is isolated—users cannot purge each other's content

-   :material-puzzle:{ .lg .middle } **Zero Coding**

    ---

    Works out of the box with the Varnish HTTP Purge WordPress plugin

</div>

---

## Step 1: Install the Cache Purge Module

```bash
# Install GetPageSpeed repository (auto-enables cl-ea4 repo on CloudLinux)
dnf -y install https://extras.getpagespeed.com/release-latest.rpm

# Install the cache purge module
dnf -y install ea-nginx-cache-purge
```

---

## Step 2: Configure NGINX

For each cPanel user that needs cache purging, create a configuration file.

For user `username`, create `/etc/nginx/conf.d/users/username/cache-purge.conf`:

```nginx
# Enable PURGE method for cache purging
proxy_cache_purge PURGE from 127.0.0.1;
```

!!! info "Replace `username`"
    The path must match the cPanel username. Each user needs their own config file.

Reload NGINX to apply:

```bash
nginx -t && systemctl reload nginx
```

---

## Step 3: Install Varnish HTTP Purge Plugin

In WordPress admin:

1. Go to **Plugins → Add New**
2. Search for **"Varnish HTTP Purge"**
3. Click **Install Now**, then **Activate**

Or via WP-CLI:

```bash
wp plugin install varnish-http-purge --activate
```

---

## Step 4: Configure Varnish HTTP Purge

In WordPress admin:

1. Go to **Settings → Varnish HTTP Purge**
2. Set **"Set Custom IP"** to: `127.0.0.1`
3. Click **Save Settings**

![Varnish HTTP Purge Settings](../assets/vhp-settings.png){ loading=lazy }

!!! warning "Critical Setting"
    The plugin must send PURGE requests to `127.0.0.1` (localhost), not your public IP or domain.
    This ensures requests go directly to NGINX on the same server.

---

## Step 5: Verify It Works

### Test via Command Line

```bash
# 1. Cache a page (first request = MISS, second = HIT)
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' | grep X-Cache
# X-Cache-Status: MISS
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' | grep X-Cache
# X-Cache-Status: HIT

# 2. Send PURGE request
curl -sX PURGE http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com'
# <h1>Successful purge</h1>

# 3. Verify cache cleared
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' | grep X-Cache
# X-Cache-Status: MISS
```

### Test via WordPress

1. Edit any published post
2. Make a small change and click **Update**
3. The Varnish HTTP Purge plugin automatically sends PURGE requests
4. Visit the page—it should show fresh content

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                         WordPress                                │
│                                                                  │
│  ┌──────────────────┐    ┌─────────────────────────────────┐   │
│  │  Post Updated    │───▶│  Varnish HTTP Purge Plugin      │   │
│  └──────────────────┘    │                                  │   │
│                          │  wp_remote_request(              │   │
│                          │    "http://127.0.0.1/post-url/", │   │
│                          │    ['method' => 'PURGE']         │   │
│                          │  )                               │   │
│                          └──────────────┬──────────────────┘   │
└─────────────────────────────────────────┼───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX (ea-nginx)                              │
│                                                                  │
│  proxy_cache_purge PURGE from 127.0.0.1;                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Request: PURGE /post-url/ HTTP/1.1                      │   │
│  │  Host: yourdomain.com                                     │   │
│  │                                                           │   │
│  │  ngx_cache_purge module:                                 │   │
│  │  → Finds cache entry for "http://yourdomain.com/post-url/"│   │
│  │  → Deletes cached file from disk                         │   │
│  │  → Returns "Successful purge"                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Security

### Localhost-Only Access

The `from 127.0.0.1` restriction ensures only local requests can purge cache:

```nginx
proxy_cache_purge PURGE from 127.0.0.1;
```

External requests sending `PURGE` will be processed as normal requests, not purges.

### User Isolation

cPanel's NGINX configuration uses per-user cache zones:

- User `alice` has cache zone `alice`
- User `bob` has cache zone `bob`

When `alice` sends a PURGE for `/page/`, it only affects `alice`'s cache.
Bob's cached `/page/` remains untouched.

---

## Troubleshooting

### Cache Not Being Purged

1. **Verify the plugin setting:**
   - Go to **Settings → Varnish HTTP Purge**
   - Ensure **Custom IP** is set to `127.0.0.1`

2. **Check NGINX config is loaded:**
   ```bash
   nginx -T | grep cache_purge
   ```

3. **Check NGINX error log:**
   ```bash
   tail -f /var/log/nginx/error.log
   ```

### "412 Precondition Failed"

This means the URL wasn't in cache. Not an error—just nothing to purge.

### Module Not Loading

```bash
# Check if installed
rpm -q ea-nginx-cache-purge

# Check module file
ls -la /etc/nginx/modules/ngx_http_cache_purge_module.so
```

### Version Mismatch Error

```
nginx: [emerg] module ... version 1029003 instead of 1029004
```

Update the module:

```bash
dnf clean all
dnf upgrade ea-nginx-cache-purge
```

---

## Related

- [CloudLinux EA4 Repository](../cloudlinux-ea4.md)
- [cache-purge Module Reference](../modules/cache-purge.md)
- [Varnish HTTP Purge Plugin](https://wordpress.org/plugins/varnish-http-purge/)

