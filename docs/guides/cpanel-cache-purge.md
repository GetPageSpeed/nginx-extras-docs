---
title: "WordPress Cache Purging with Proxy Cache Purge"
description: "Set up automatic NGINX cache purging for WordPress on CloudLinux with ea-nginx using the Proxy Cache Purge plugin and ngx_cache_purge module."
---

# WordPress Cache Purging on CloudLinux EA4

This guide shows how to set up automatic NGINX cache purging for WordPress sites on 
CloudLinux servers with cPanel's `ea-nginx`, using the **Proxy Cache Purge** plugin.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Automatic Invalidation**

    ---

    Cache is purged automatically when you edit posts, pages, or comments

-   :material-shield-check:{ .lg .middle } **Multi-Tenant Safe**

    ---

    Each cPanel user's cache is isolated—users cannot purge each other's content

-   :material-puzzle:{ .lg .middle } **Zero Coding**

    ---

    Works out of the box with the Proxy Cache Purge WordPress plugin

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

You can enable cache purging globally for all users or per-user.

### Global Configuration (Recommended)

Create `/etc/nginx/conf.d/server-includes/cache-purge.conf`:

```nginx
# Enable PURGE method for cache purging (all users)
proxy_cache_purge PURGE from 127.0.0.1;
```

This file is automatically included in all cPanel user server blocks.

### Per-User Configuration

For user `username`, create `/etc/nginx/conf.d/users/username/cache-purge.conf`:

```nginx
# Enable PURGE method for cache purging
proxy_cache_purge PURGE from 127.0.0.1;
```

After creating the config, reload NGINX:

```bash
nginx -t && systemctl reload nginx
```

---

## Step 3: Install Proxy Cache Purge Plugin

In WordPress admin:

1. Go to **Plugins → Add New**
2. Search for **"Proxy Cache Purge"** (slug: `varnish-http-purge`)
3. Click **Install Now**, then **Activate**

Or via WP-CLI:

```bash
wp plugin install varnish-http-purge --activate
```

---

## Step 4: Configure Proxy Cache Purge

In WordPress admin:

1. Go to **Settings → Proxy Cache Purge**
2. Set **"Set Custom IP"** to: `127.0.0.1`
3. Click **Save Settings**

!!! warning "Critical Setting"
    The plugin must send PURGE requests to `127.0.0.1` (localhost), not your public IP or domain.

---

## Step 5: Add Wildcard Purge Fix

Due to NGINX's `Vary: Accept-Encoding` header, the cache stores separate variants for different 
encodings. To ensure all variants are purged, create a mu-plugin:

Create `wp-content/mu-plugins/nginx-cache-purge-fix.php`:

```php
<?php
/**
 * Plugin Name: NGINX Cache Purge Fix
 * Description: Appends wildcard to purge URLs for Vary header compatibility
 */
add_filter("vhp_purgeme_path", function($purgeme, $schema, $host, $path, $pregex, $p) {
    // Add wildcard to purge all cache variants (gzip, br, etc.)
    if (empty($pregex)) {
        $purgeme .= "*";
    }
    return $purgeme;
}, 10, 6);
```

This ensures that when a page is purged, all cached variants (gzip, brotli, uncompressed) are cleared.

---

## Step 6: Test the Setup

```bash
# 1. Cache a page (first request = MISS, second = HIT)
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' -H 'Accept-Encoding: gzip' | grep X-Cache
# X-Cache-Status: MISS
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' -H 'Accept-Encoding: gzip' | grep X-Cache
# X-Cache-Status: HIT

# 2. Purge using PURGE method with wildcard
curl -sX PURGE 'http://127.0.0.1/sample-page/*' -H 'Host: yourdomain.com'
# <h1>Successful purge</h1>

# 3. Verify cache cleared
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' -H 'Accept-Encoding: gzip' | grep X-Cache
# X-Cache-Status: MISS
```

Then test via WordPress:

1. Edit any published post
2. Make a change and click **Update**
3. The plugin automatically purges the cache
4. Visit the page—it should show fresh content

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                         WordPress                                │
│                                                                  │
│  ┌──────────────────┐    ┌─────────────────────────────────┐   │
│  │  Post Updated    │───▶│  Proxy Cache Purge Plugin       │   │
│  └──────────────────┘    │                                  │   │
│                          │  PURGE http://127.0.0.1/url/*    │   │
│                          │  Host: yourdomain.com            │   │
│                          └──────────────┬──────────────────┘   │
└─────────────────────────────────────────┼───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX (ea-nginx)                              │
│                                                                  │
│  proxy_cache_purge PURGE from 127.0.0.1;                        │
│                                                                  │
│  ngx_cache_purge module:                                        │
│  → Wildcard (*) matches all variants (gzip, br, plain)          │
│  → Deletes all cached versions from disk                        │
│  → Returns "Successful purge"                                   │
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
   - Go to **Settings → Proxy Cache Purge**
   - Ensure **Custom IP** is set to `127.0.0.1`

2. **Check the mu-plugin exists:**
   ```bash
   ls -la wp-content/mu-plugins/nginx-cache-purge-fix.php
   ```

3. **Check NGINX config is loaded:**
   ```bash
   nginx -T | grep cache_purge
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

---

## Related

- [CloudLinux EA4 Repository](../cloudlinux-ea4.md)
- [cache-purge Module Reference](../modules/cache-purge.md)
- [Proxy Cache Purge Plugin](https://wordpress.org/plugins/varnish-http-purge/)
