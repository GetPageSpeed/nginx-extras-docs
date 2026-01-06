---
title: "CloudLinux EA4 Repository"
description: "Install NGINX modules for cPanel EasyApache 4 (ea-nginx) on CloudLinux. The GetPageSpeed CloudLinux EA4 repository provides pre-built modules compatible with cPanel's NGINX implementation."
---

# CloudLinux EA4 Repository

GetPageSpeed provides a dedicated repository for **CloudLinux with cPanel EasyApache 4**, 
enabling easy installation of NGINX modules that are fully compatible with cPanel's `ea-nginx`.

## Why CloudLinux EA4?

cPanel's EasyApache 4 uses a custom-built NGINX (`ea-nginx`) that differs from standard NGINX distributions:

- **Custom paths**: Modules are installed to `/etc/nginx/modules/` instead of `/usr/lib64/nginx/modules/`
- **Custom configuration**: Module configs go to `/etc/nginx/conf.d/modules/`
- **ABI compatibility**: Modules must be built against the exact `ea-nginx` version

Our CloudLinux EA4 repository (**cl-ea4**) provides modules specifically built for this environment, 
ensuring perfect compatibility with your cPanel server.

## Installation

### Step 1: Install the GetPageSpeed Repository

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
```

On CloudLinux systems with cPanel detected, the `cl-ea4` repository is **automatically enabled**.

### Step 2: Install Modules

All EA4-compatible modules use the `ea-nginx-` prefix instead of `nginx-module-`:

```bash
# Install cache-purge module
dnf -y install ea-nginx-cache-purge

# Install brotli compression
dnf -y install ea-nginx-brotli

# Install headers-more module
dnf -y install ea-nginx-headers-more
```

### Step 3: Enable Modules

After installation, modules are automatically loaded via configs in `/etc/nginx/conf.d/modules/`.
Simply reload NGINX:

```bash
systemctl reload nginx
```

## Available Modules

All modules from the GetPageSpeed collection are available for CloudLinux EA4. 
The package naming follows this pattern:

| Standard Package | CloudLinux EA4 Package |
|-----------------|------------------------|
| `nginx-module-cache-purge` | `ea-nginx-cache-purge` |
| `nginx-module-brotli` | `ea-nginx-brotli` |
| `nginx-module-headers-more` | `ea-nginx-headers-more` |
| `nginx-module-geoip2` | `ea-nginx-geoip2` |

## Cache Purging with WordPress

The `ea-nginx-cache-purge` module enables cache purging from WordPress and other applications.

### Configuration

For each cPanel user that needs cache purging, create a configuration file.
For example, for user `username`, create `/etc/nginx/conf.d/users/username/cache-purge.conf`:

```nginx
# Cache purge endpoint for ngx_cache_purge module
# Uses "separate location syntax" - required for cPanel's variable cache zones
#
# SECURITY: 
# - Only localhost can access /purge/
# - Each user has their own cache zone, isolated from other users

location ~ ^/purge(/.*) {
    allow 127.0.0.1;
    allow ::1;
    deny all;
    
    # Use the same cache key format as cPanel's cpanel-proxy.conf
    # Replace 'username' with the actual cPanel username (cache zone name)
    proxy_cache_purge username "$scheme://$host$1";
}
```

!!! note "Cache Zone Name"
    Replace `username` in `proxy_cache_purge username` with the actual cPanel username. 
    Each user has their own cache zone named after their username.

### How It Works

1. WordPress (or any application) sends a request to `/purge/path/to/page`
2. NGINX matches the `/purge/` location
3. The `proxy_cache_purge` directive removes the cached entry for `/path/to/page`
4. Response: "Successful purge" with the cache key

### Testing Cache Purge

```bash
# First, cache a page
curl -sI http://127.0.0.1/test-page.html -H 'Host: example.com' | grep X-Cache-Status
# Should show: X-Cache-Status: HIT (after second request)

# Purge the cached page
curl -s http://127.0.0.1/purge/test-page.html -H 'Host: example.com'
# Shows: Successful purge

# Verify cache was cleared
curl -sI http://127.0.0.1/test-page.html -H 'Host: example.com' | grep X-Cache-Status  
# Should show: X-Cache-Status: MISS
```

### Security

Each cPanel user has their own isolated cache zone:

- **Localhost only**: The `/purge/` location only allows requests from `127.0.0.1` and `::1`
- **User isolation**: Each user's cache zone is separate - users cannot purge each other's cache
- **Domain-based keys**: Cache keys include the domain name, so different domains are isolated

### WordPress Integration

For WordPress cache purging, you can use a simple mu-plugin. Create 
`wp-content/mu-plugins/nginx-cache-purge.php`:

```php
<?php
/**
 * Plugin Name: NGINX Cache Purge
 * Description: Purges NGINX cache when posts are updated
 */

add_action('save_post', function($post_id) {
    if (wp_is_post_revision($post_id)) return;
    
    $url = get_permalink($post_id);
    $path = wp_parse_url($url, PHP_URL_PATH);
    $purge_url = home_url('/purge' . $path);
    
    wp_remote_get($purge_url, ['sslverify' => false]);
});
```

This automatically purges the cache when any post or page is updated

## Version Compatibility

Modules are automatically rebuilt when `ea-nginx` is updated. The package version format ensures 
you always get the correct module for your NGINX version:

```
ea-nginx-cache-purge-1.29.4+2.5.5-1.gps.el9
                      │      │
                      │      └── Module upstream version (2.5.5)
                      └── ea-nginx version (1.29.4)
```

## Repository Details

| Property | Value |
|----------|-------|
| Repository ID | `getpagespeed-extras-cl-ea4` |
| Base URL | `https://extras.getpagespeed.com/redhat/$releasever/cl-ea4/$basearch/` |
| GPG Key | `/etc/pki/rpm-gpg/RPM-GPG-KEY-GETPAGESPEED` |

## Manual Repository Configuration

If you need to manually enable the repository:

```bash
dnf config-manager --set-enabled getpagespeed-extras-cl-ea4
```

Or edit `/etc/yum.repos.d/getpagespeed-extras.repo` and set `enabled=1` under the 
`[getpagespeed-extras-cl-ea4]` section.

## Troubleshooting

### Module Version Mismatch

If you see an error like:

```
nginx: [emerg] module "/etc/nginx/modules/ngx_http_cache_purge_module.so" version 1029003 instead of 1029004
```

This means the module was built for a different `ea-nginx` version. Solution:

```bash
dnf clean all
dnf upgrade ea-nginx-cache-purge
```

### Repository Not Found

If the `cl-ea4` repository is not available:

1. Ensure you have the latest `getpagespeed-extras-release`:
   ```bash
   dnf upgrade getpagespeed-extras-release
   ```

2. The repository is automatically enabled on CloudLinux with cPanel. If not detected:
   ```bash
   dnf config-manager --set-enabled getpagespeed-extras-cl-ea4
   ```

## Support

For issues with CloudLinux EA4 packages:

- [GetPageSpeed Support](https://www.getpagespeed.com/support)
- [GitHub Issues](https://github.com/GetPageSpeed/nginx-extras/issues)

