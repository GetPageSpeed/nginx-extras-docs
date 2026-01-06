---
title: "CloudLinux EA4 Repository"
description: "Install NGINX modules for cPanel EasyApache 4 (ea-nginx) on CloudLinux. The GetPageSpeed CloudLinux EA4 repository provides pre-built modules compatible with cPanel's NGINX implementation."
---

# CloudLinux EA4 Repository

!!! success "🎉 Free Access - Limited Time Offer!"
    The CloudLinux EA4 repository is currently **free to use** — no subscription required!
    
    Install any `ea-nginx-*` module at no cost while this promotion lasts. This is a great 
    opportunity to try out our modules on your cPanel servers.

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

# Install headers-more module
dnf -y install ea-nginx-headers-more

# Install GeoIP2 module
dnf -y install ea-nginx-geoip2
```

## Available Modules

All modules from the GetPageSpeed collection are available for CloudLinux EA4. 
The package naming follows this pattern:

| Standard Package | CloudLinux EA4 Package |
|-----------------|------------------------|
| `nginx-module-cache-purge` | `ea-nginx-cache-purge` |
| `nginx-module-headers-more` | `ea-nginx-headers-more` |
| `nginx-module-geoip2` | `ea-nginx-geoip2` |
| `nginx-module-naxsi` | `ea-nginx-naxsi` |

## WordPress Cache Purging

The `ea-nginx-cache-purge` module enables automatic cache invalidation when WordPress content changes.
Combined with the **Proxy Cache Purge** plugin, you get seamless cache management.

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Complete Setup Guide**

    ---

    Step-by-step instructions for NGINX configuration and Proxy Cache Purge plugin setup.

    [:octicons-arrow-right-24: WordPress Cache Purging Guide](guides/cpanel-cache-purge.md)

</div>

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
