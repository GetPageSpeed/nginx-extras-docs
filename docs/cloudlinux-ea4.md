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

## Popular Use Case: WordPress Cache Purging

The `ea-nginx-cache-purge` module enables automatic cache invalidation when WordPress content changes.

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Complete WordPress Guide**

    ---

    Step-by-step instructions for setting up cache purging with WordPress on cPanel, 
    including code examples and troubleshooting.

    [:octicons-arrow-right-24: WordPress Cache Purging Guide](guides/cpanel-cache-purge.md)

</div>

### Quick Example

```nginx
# /etc/nginx/conf.d/users/username/cache-purge.conf
location ~ ^/purge(/.*) {
    allow 127.0.0.1;
    deny all;
    proxy_cache_purge username "$scheme://$host$1";
}
```

Then in WordPress, add a simple mu-plugin:

```php
<?php
// wp-content/mu-plugins/nginx-cache-purge.php
add_action('save_post', function($post_id) {
    if (wp_is_post_revision($post_id)) return;
    $path = wp_parse_url(get_permalink($post_id), PHP_URL_PATH);
    wp_remote_get(home_url('/purge' . $path), ['sslverify' => false]);
});
```

For complete setup instructions, security considerations, and advanced features, see the 
[WordPress Cache Purging Guide](guides/cpanel-cache-purge.md)

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

