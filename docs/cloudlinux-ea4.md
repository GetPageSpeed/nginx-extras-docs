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

The `ea-nginx-cache-purge` module enables cache purging directly from WordPress, 
compatible with the popular [Varnish HTTP Purge](https://wordpress.org/plugins/varnish-http-purge/) plugin.

### Configuration

Add the following to your NGINX configuration to enable PURGE method support.
Create `/etc/nginx/conf.d/includes-optional/cpanel-proxy-vendors/cache-purge.conf`:

```nginx
# Enable PURGE method for cache purging
# Works with varnish-http-purge WordPress plugin
# Security: PURGE only allowed from localhost
proxy_cache_purge PURGE from 127.0.0.1;
```

This configuration:

- Enables the HTTP `PURGE` method for cache invalidation
- Restricts purge requests to localhost only (127.0.0.1)
- Works within cPanel's `ea-nginx` proxy cache infrastructure

### Security

Each cPanel user has their own isolated cache zone. When WordPress sends a PURGE request:

1. The request goes to `127.0.0.1` (localhost)
2. NGINX matches it to the user's server block
3. Only that user's cache zone is affected

Users **cannot purge each other's cache** because:

- PURGE is only allowed from localhost
- Each server block uses a separate cache zone
- The cache key includes the domain name

### WordPress Integration

The [Varnish HTTP Purge](https://wordpress.org/plugins/varnish-http-purge/) plugin works out of the box:

1. Install and activate the plugin
2. No configuration needed - it automatically sends PURGE requests to localhost
3. When you update a post, the cached version is automatically purged

## Version Compatibility

Modules are automatically rebuilt when `ea-nginx` is updated. The package version format ensures 
you always get the correct module for your NGINX version:

```
ea-nginx-cache-purge-1.29.4+2.5.4-1.gps.el9
                      │      │
                      │      └── Module upstream version (2.5.4)
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

