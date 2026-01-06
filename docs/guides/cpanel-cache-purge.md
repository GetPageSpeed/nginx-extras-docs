---
title: "WordPress Cache Purging on cPanel with NGINX"
description: "Complete guide to setting up automatic cache purging for WordPress sites on cPanel servers using ea-nginx and the ngx_cache_purge module from GetPageSpeed."
---

# WordPress Cache Purging on cPanel with NGINX

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Instant Cache Invalidation**

    ---

    Automatically purge NGINX cache when content changes in WordPress

-   :material-shield-check:{ .lg .middle } **Secure Multi-Tenant**

    ---

    Each cPanel user's cache is completely isolated—users cannot purge each other's content

-   :material-puzzle:{ .lg .middle } **Simple Integration**

    ---

    Works with existing WordPress plugins or a few lines of custom code

</div>

## Prerequisites

- CloudLinux or CentOS/RHEL with cPanel
- `ea-nginx` installed and configured as reverse proxy
- NGINX caching enabled for your domains

## Quick Start

### 1. Install the Cache Purge Module

=== "CloudLinux with cPanel"

    ```bash
    # Install GetPageSpeed repository (auto-enables cl-ea4 repo on CloudLinux)
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm
    
    # Install the cache purge module
    dnf -y install ea-nginx-cache-purge
    ```

=== "Other RHEL-based with cPanel"

    ```bash
    # Install GetPageSpeed repository
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm
    
    # Enable the cl-ea4 repository
    dnf config-manager --set-enabled getpagespeed-extras-cl-ea4
    
    # Install the cache purge module
    dnf -y install ea-nginx-cache-purge
    ```

### 2. Configure the Purge Endpoint

Create a configuration file for each cPanel user that needs cache purging.

For user `username`, create `/etc/nginx/conf.d/users/username/cache-purge.conf`:

```nginx
# Cache purge endpoint for ngx_cache_purge module
# Matches /purge/any/path and purges the cached version of /any/path

location ~ ^/purge(/.*) {
    # Security: Only allow purge from localhost
    allow 127.0.0.1;
    allow ::1;
    deny all;
    
    # Purge using the same cache key format as cPanel's proxy config
    # Replace 'username' with the actual cPanel username
    proxy_cache_purge username "$scheme://$host$1";
}
```

!!! warning "Important: Replace `username`"
    The first argument to `proxy_cache_purge` must match the cPanel username, 
    which is used as the cache zone name in cPanel's NGINX configuration.

### 3. Reload NGINX

```bash
nginx -t && systemctl reload nginx
```

### 4. Test the Setup

```bash
# First, cache a page
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' | grep X-Cache
# Should show: X-Cache-Status: MISS (first request)
# Then: X-Cache-Status: HIT (subsequent requests)

# Purge the cached page
curl -s http://127.0.0.1/purge/sample-page/ -H 'Host: yourdomain.com'
# Shows: <html>...<h1>Successful purge</h1>...

# Verify cache was cleared
curl -sI http://127.0.0.1/sample-page/ -H 'Host: yourdomain.com' | grep X-Cache
# Should show: X-Cache-Status: MISS
```

---

## WordPress Integration

### Option A: Simple MU-Plugin (Recommended)

Create `wp-content/mu-plugins/nginx-cache-purge.php`:

```php
<?php
/**
 * Plugin Name: NGINX Cache Purge
 * Description: Automatically purges NGINX cache when content changes
 * Version: 1.0.0
 */

// Purge post/page when updated
add_action('save_post', 'nginx_purge_post_cache', 10, 3);
add_action('delete_post', 'nginx_purge_post_cache', 10, 1);
add_action('trash_post', 'nginx_purge_post_cache', 10, 1);

function nginx_purge_post_cache($post_id, $post = null, $update = true) {
    // Skip revisions and autosaves
    if (wp_is_post_revision($post_id) || wp_is_post_autosave($post_id)) {
        return;
    }
    
    // Get the post URL
    $url = get_permalink($post_id);
    if (!$url) {
        return;
    }
    
    nginx_purge_url($url);
    
    // Also purge the home page and archives
    nginx_purge_url(home_url('/'));
    
    // Purge category/tag archives for this post
    if ($post) {
        $categories = get_the_category($post_id);
        foreach ($categories as $category) {
            nginx_purge_url(get_category_link($category->term_id));
        }
        
        $tags = get_the_tags($post_id);
        if ($tags) {
            foreach ($tags as $tag) {
                nginx_purge_url(get_tag_link($tag->term_id));
            }
        }
    }
}

function nginx_purge_url($url) {
    $path = wp_parse_url($url, PHP_URL_PATH) ?: '/';
    $purge_url = home_url('/purge' . $path);
    
    // Send purge request to localhost
    $response = wp_remote_get($purge_url, [
        'timeout' => 2,
        'sslverify' => false,
        'blocking' => false, // Don't wait for response
    ]);
    
    // Log for debugging (optional)
    if (defined('WP_DEBUG') && WP_DEBUG) {
        error_log("NGINX Cache Purge: $path");
    }
}

// Purge when comments are approved
add_action('comment_post', 'nginx_purge_comment_cache', 10, 3);
add_action('wp_set_comment_status', 'nginx_purge_comment_status_change', 10, 2);

function nginx_purge_comment_cache($comment_id, $approved, $commentdata) {
    if ($approved === 1) {
        $post_id = $commentdata['comment_post_ID'];
        nginx_purge_post_cache($post_id);
    }
}

function nginx_purge_comment_status_change($comment_id, $status) {
    if ($status === 'approve') {
        $comment = get_comment($comment_id);
        if ($comment) {
            nginx_purge_post_cache($comment->comment_post_ID);
        }
    }
}

// Admin bar indicator (optional)
add_action('admin_bar_menu', 'nginx_purge_admin_bar', 100);

function nginx_purge_admin_bar($wp_admin_bar) {
    if (!current_user_can('manage_options')) {
        return;
    }
    
    $wp_admin_bar->add_node([
        'id'    => 'nginx-purge',
        'title' => '🚀 Purge Cache',
        'href'  => wp_nonce_url(admin_url('admin-post.php?action=nginx_purge_all'), 'nginx_purge_all'),
        'meta'  => ['title' => 'Purge entire NGINX cache'],
    ]);
}

// Handle manual purge all
add_action('admin_post_nginx_purge_all', 'nginx_handle_purge_all');

function nginx_handle_purge_all() {
    if (!wp_verify_nonce($_GET['_wpnonce'], 'nginx_purge_all')) {
        wp_die('Security check failed');
    }
    
    if (!current_user_can('manage_options')) {
        wp_die('Unauthorized');
    }
    
    // Purge home and common pages
    nginx_purge_url(home_url('/'));
    nginx_purge_url(home_url('/blog/'));
    nginx_purge_url(home_url('/feed/'));
    
    // Redirect back with success message
    wp_redirect(add_query_arg('nginx_purged', '1', wp_get_referer()));
    exit;
}
```

This plugin:

- ✅ Automatically purges posts when edited
- ✅ Purges home page and archives
- ✅ Purges when comments are approved
- ✅ Adds "Purge Cache" button to admin bar
- ✅ Works with any WordPress theme

### Option B: WP-CLI Command

Add to your theme's `functions.php` or a custom plugin:

```php
if (defined('WP_CLI') && WP_CLI) {
    WP_CLI::add_command('nginx-purge', function($args) {
        $url = isset($args[0]) ? $args[0] : home_url('/');
        $path = wp_parse_url($url, PHP_URL_PATH) ?: '/';
        $purge_url = 'http://127.0.0.1/purge' . $path;
        
        $response = wp_remote_get($purge_url, [
            'headers' => ['Host' => wp_parse_url(home_url(), PHP_URL_HOST)],
            'sslverify' => false,
        ]);
        
        if (is_wp_error($response)) {
            WP_CLI::error($response->get_error_message());
        } else {
            WP_CLI::success("Purged: $path");
        }
    });
}
```

Usage:

```bash
# Purge a specific URL
wp nginx-purge https://example.com/my-post/

# Purge home page
wp nginx-purge
```

---

## Understanding Cache Isolation

### How cPanel Keeps Users Separate

```
┌─────────────────────────────────────────────────────────────┐
│                     cPanel NGINX                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  user1       │  │  user2       │  │  user3       │       │
│  │  Cache Zone  │  │  Cache Zone  │  │  Cache Zone  │       │
│  │              │  │              │  │              │       │
│  │ site1.com    │  │ site2.com    │  │ site3.com    │       │
│  │ site1b.com   │  │ another.com  │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  Each user has their own isolated cache zone                │
│  proxy_cache_purge only affects the zone specified          │
└─────────────────────────────────────────────────────────────┘
```

- **Each cPanel user** has their own cache zone (named after their username)
- **Each domain** within a user's account shares that user's cache zone
- **Cache keys** include the hostname, so `site1.com/page` and `site1b.com/page` are cached separately
- **Purge requests** from `site1.com` cannot affect `site2.com`'s cache

### Why `/purge/` is Required

cPanel uses **variable cache zones** (`proxy_cache $CPANEL_PROXY_CACHE`) to dynamically assign cache zones based on the username. The `ngx_cache_purge` module's "same-location syntax" (`proxy_cache_purge PURGE from ...`) doesn't support variable cache zones.

The `/purge/` location workaround:

1. Uses an explicit cache zone name (the username)
2. Restricts access to localhost only
3. Provides a clean, predictable API for cache invalidation

---

## Troubleshooting

### Cache Not Being Purged

1. **Check if caching is active:**
   ```bash
   curl -sI http://127.0.0.1/page/ -H 'Host: domain.com' | grep X-Cache
   ```
   You should see `X-Cache-Status: HIT`. If you see `MISS` every time, caching isn't working.

2. **Verify the cache zone name:**
   ```bash
   # Find your cache zone name (should match cPanel username)
   grep -r "proxy_cache_path" /etc/nginx/
   ```

3. **Check NGINX error log:**
   ```bash
   tail -f /var/log/nginx/error.log
   ```

### 403 Forbidden on Purge

The purge endpoint only allows localhost. Make sure WordPress is sending requests to `127.0.0.1`, not the public IP.

### 404 Not Found on Purge

1. Check that the cache-purge config file exists:
   ```bash
   ls -la /etc/nginx/conf.d/users/USERNAME/cache-purge.conf
   ```

2. Verify NGINX loaded the config:
   ```bash
   nginx -T | grep purge
   ```

### Module Not Loading

```bash
# Check if module is installed
rpm -q ea-nginx-cache-purge

# Check if module is loaded
nginx -V 2>&1 | grep -i purge

# Verify module file exists
ls -la /usr/lib64/nginx/modules/ngx_http_cache_purge_module.so
```

---

## Advanced: Wildcard Purging

The `ngx_cache_purge` module supports partial/wildcard purging. Add `*` to purge all URLs matching a prefix:

```bash
# Purge all cached pages under /blog/
curl -s http://127.0.0.1/purge/blog/* -H 'Host: domain.com'

# Purge everything for the domain
curl -s 'http://127.0.0.1/purge/*' -H 'Host: domain.com'
```

!!! warning "Performance Note"
    Wildcard purging scans the entire cache directory, which can be slow for large caches.

---

## Related Resources

- [CloudLinux EA4 Repository](../cloudlinux-ea4.md) - Repository setup for CloudLinux cPanel servers
- [cache-purge Module Reference](../modules/cache-purge.md) - Full module documentation
- [ngx_cache_purge on GitHub](https://github.com/nginx-modules/ngx_cache_purge) - Module source code


