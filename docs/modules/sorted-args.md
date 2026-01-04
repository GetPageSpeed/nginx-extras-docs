---

title: "HTTP querystring parameters normalization for NGINX"
description: "RPM package nginx-module-sorted-args. Powerful NGINX module that normalizes HTTP request querystring parameters  by sorting them alphanumerically. "

---

# *sorted-args*: HTTP querystring parameters normalization for NGINX


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
    dnf -y install nginx-module-sorted-args
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-sorted-args
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_sorted_args.so;
```


This document describes nginx-module-sorted-args [v3.0.0](https://github.com/GetPageSpeed/ngx_http_sorted_args/releases/tag/v3.0.0){target=_blank} 
released on Dec 31 2025.

<hr />

A powerful Nginx module that normalizes HTTP request querystring parameters by sorting them alphanumerically. This module provides a consistent, canonical representation of query strings regardless of the original parameter order, making it ideal for cache key generation, request deduplication, and URL normalization.

## Overview

Different URLs with the same query parameters in different orders will produce the same normalized querystring:

- `/index.php?b=2&a=1&c=3`
- `/index.php?b=2&c=3&a=1`
- `/index.php?c=3&a=1&b=2`
- `/index.php?c=3&b=2&a=1`

All of the above will produce the same normalized querystring: `a=1&b=2&c=3`

This normalization is accessible via the `$sorted_args` variable, which can be used in cache keys, logging, and other Nginx contexts.

[![Test Build](https://github.com/dvershinin/ngx_http_sorted_args/actions/workflows/build.yml/badge.svg)](https://github.com/dvershinin/ngx_http_sorted_args/actions/workflows/build.yml)

## Features

- ✅ **Natural sorting** of query parameters by key, then by value (e.g., `item2` < `item10`)
- ✅ **Empty value stripping** — parameters like `?a=` are automatically removed
- ✅ **Blocklist mode** (`sorted_args_ignore_list`) to exclude specific parameters from the sorted output
- ✅ **Allowlist mode** (`sorted_args_allow_list`) to keep only specific parameters, dropping all others
- ✅ **Wildcard patterns** — use `utm_*` to match all UTM parameters, `*_id` for suffixes
- ✅ **Deduplication** (`sorted_args_dedupe`) — keep only first or last occurrence of duplicate keys
- ✅ **Optional `$args` overwrite** to automatically replace the original querystring with sorted args
- ✅ **Location-level configuration** with inheritance from server and main contexts
- ✅ **Efficient implementation** using Nginx's native queue sorting
- ✅ **Case-insensitive** parameter name matching for filtering
- ✅ **Duplicate detection** in filter lists

## Configuration

### Variables

#### `$sorted_args`

Returns the querystring parameters sorted alphanumerically by parameter name, then by value. Parameters are joined with `&` and maintain their original URL encoding.

**Example:**

```
Request: /page?zebra=1&apple=2&banana=3
$sorted_args: apple=2&banana=3&zebra=1
```

**Behavior:**
- Empty querystring returns an empty string
- Parameters without values (e.g., `?param`) are included as `param`
- Parameters with empty values (e.g., `?param=`) are automatically stripped
- Multiple values for the same parameter are sorted individually
- Natural sorting: `p=1`, `p=2`, `p=10` sort correctly (not `p=1`, `p=10`, `p=2`)
- Case-insensitive sorting for parameter names

### Directives

#### `sorted_args_ignore_list`

**Syntax:** `sorted_args_ignore_list pattern [pattern ...];`

**Default:** none

**Context:** `http`, `server`, `location`, `if`

**Description:**

Specifies one or more patterns to exclude from the `$sorted_args` variable (blocklist mode). This is useful for removing cache-busting parameters (like timestamps, version numbers, or tracking IDs) from cache keys while preserving other parameters.

**Pattern types:**
- `name` — exact match (case-insensitive)
- `name*` — prefix match (matches `name`, `name_foo`, `name123`, etc.)
- `*name` — suffix match (matches `foo_name`, `bar_name`, etc.)
- `*name*` — contains match (matches any parameter containing `name`)

Duplicate patterns in the list are automatically removed.

**Example:**

```nginx
location /api {
    # Filter exact names and all utm_* tracking parameters
    sorted_args_ignore_list timestamp version _ utm_* fb_*;

    proxy_cache_key "$uri$sorted_args";
    proxy_pass http://backend;
}
```

In this example, requests like `/api?user=123&timestamp=1234567890&utm_source=google&utm_medium=cpc` will produce `$sorted_args` as `user=123`, with `timestamp` and all UTM parameters filtered out.

#### `sorted_args_allow_list`

**Syntax:** `sorted_args_allow_list pattern [pattern ...];`

**Default:** none

**Context:** `http`, `server`, `location`, `if`

**Description:**

Specifies one or more patterns to **keep** in the `$sorted_args` variable (allowlist mode). All parameters NOT matching any pattern will be excluded. This is useful when you want to strictly control which query parameters are allowed through for caching.

**Pattern types:**
- `name` — exact match (case-insensitive)
- `name*` — prefix match (matches `name`, `name_foo`, `name123`, etc.)
- `*name` — suffix match (matches `foo_name`, `bar_name`, etc.)
- `*name*` — contains match (matches any parameter containing `name`)

When both `sorted_args_allow_list` and `sorted_args_ignore_list` are configured, the allowlist is applied first (keeping only allowed parameters), then the ignore list is applied to filter out any remaining unwanted parameters.

**Example:**

```nginx
location /api {
    # Only allow pagination and sorting parameters
    sorted_args_allow_list page* sort* limit;

    proxy_cache_key "$uri$sorted_args";
    proxy_pass http://backend;
}
```

In this example, a request like `/api?page=1&page_size=10&sort=asc&timestamp=123` will produce `$sorted_args` as `limit=10&page=1&page_size=10&sort=asc`. The `timestamp` parameter is dropped because it doesn't match any pattern.

#### `sorted_args_overwrite`

**Syntax:** `sorted_args_overwrite on | off;`

**Default:** `off`

**Context:** `http`, `server`, `location`, `if`

**Description:**

When enabled, this directive automatically overwrites the built-in `$args` variable with the sorted (and optionally filtered) query arguments. This is useful when you want all downstream processing (proxying, logging, redirects) to use the normalized querystring without explicitly referencing `$sorted_args`.

The overwrite happens during the rewrite phase, so all subsequent phases will see the sorted arguments in `$args`.

**Example:**

```nginx
location /api {
    sorted_args_overwrite on;
    sorted_args_ignore_list timestamp version;

    # $args is now automatically sorted and filtered
    proxy_pass http://backend$uri?$args;
}
```

In this example, a request to `/api?z=1&a=2&timestamp=123` will be proxied as `/api?a=2&z=1` — sorted and with `timestamp` filtered out.

#### `sorted_args_dedupe`

**Syntax:** `sorted_args_dedupe first | last | off;`

**Default:** `off`

**Context:** `http`, `server`, `location`, `if`

**Description:**

Controls how duplicate parameter keys are handled. When multiple parameters have the same key (e.g., `?a=1&a=2&a=3`), this directive determines which value to keep.

- `first` — keep only the first occurrence of each key
- `last` — keep only the last occurrence of each key
- `off` — keep all occurrences (default behavior)

This is useful for normalizing URLs where the same parameter might be specified multiple times, ensuring consistent cache keys.

**Example:**

```nginx
location /search {
    sorted_args_dedupe first;

    proxy_cache_key "$uri$sorted_args";
    proxy_pass http://backend;
}
```

In this example, a request like `/search?q=foo&q=bar&q=baz` will produce `$sorted_args` as `q=foo`, keeping only the first value. With `sorted_args_dedupe last`, it would produce `q=baz`.

## Usage Examples

### Basic Cache Key Normalization

Normalize cache keys regardless of parameter order:

```nginx
http {
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;

    server {
        listen 80;

        location / {
            proxy_cache my_cache;
            proxy_cache_key "$scheme$host$uri$sorted_args";
            proxy_pass http://backend;
        }
    }
}
```

### Automatic Args Overwrite

Automatically rewrite `$args` with sorted parameters for all downstream processing:

```nginx
server {
    listen 80;

    location /api {
        sorted_args_overwrite on;
        sorted_args_ignore_list timestamp _;

        # All of these now use sorted, filtered args automatically
        proxy_pass http://backend;
        # Equivalent to: proxy_pass http://backend$uri?$sorted_args;
    }
}
```

### Filtering Cache-Busting Parameters

Remove timestamp and tracking parameters from cache keys:

```nginx
location /static {
    sorted_args_ignore_list _ t timestamp v version;

    proxy_cache zone;
    proxy_cache_key "$uri$sorted_args";
    proxy_pass http://cdn;
}
```

### Allowlist Mode (Whitelist Only Specific Parameters)

When query parameters can cause heavy server-side processing, use an allowlist to strictly control which parameters are allowed through for caching:

```nginx
location /search {
    # Only these parameters affect the cache key; all others are dropped
    sorted_args_allow_list q page limit category;

    proxy_cache zone;
    proxy_cache_key "$uri$sorted_args";
    proxy_pass http://search_backend;
}
```

In this example, requests like `/search?q=nginx&page=1&debug=true&nocache=1` will be cached using only `category=&limit=&page=1&q=nginx`, effectively ignoring any cache-busting or debugging parameters.

### Combining Allowlist and Blocklist

You can use both directives together for fine-grained control. The allowlist is applied first, then the blocklist:

```nginx
location /api {
    # First, keep only these parameters
    sorted_args_allow_list user_id action page limit timestamp;

    # Then, remove timestamp from the allowed set
    sorted_args_ignore_list timestamp;

    proxy_cache zone;
    proxy_cache_key "$uri$sorted_args";
    proxy_pass http://api_backend;
}
```

### Logging Normalized Querystrings

Include sorted querystrings in access logs:

```nginx
http {
    log_format detailed '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        'args="$args" sorted_args="$sorted_args"';

    server {
        access_log /var/log/nginx/access.log detailed;
        # ...
    }
}
```

### Location-Specific Filtering

Different locations can have different filter lists:

```nginx
server {
    # Default: filter common tracking parameters
    sorted_args_ignore_list _ utm_source utm_medium utm_campaign;

    location /api {
        # API: also filter version and timestamp
        sorted_args_ignore_list _ utm_source utm_medium utm_campaign version t;
        proxy_pass http://api_backend;
    }

    location /content {
        # Content: only filter tracking
        proxy_pass http://content_backend;
    }
}
```

### Complete Example

```nginx
pid         logs/nginx.pid;
error_log   logs/error.log warn;

worker_processes  auto;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" "$http_user_agent" '
                    'args="$args" sorted_args="$sorted_args"';

    access_log  logs/access.log  main;

    proxy_cache_path /tmp/cache
                     levels=1:2
                     keys_zone=zone:10m
                     inactive=10d
                     max_size=100m;

    server {
        listen       8080;
        server_name  localhost;

        # Filter tracking and cache-busting parameters
        location /filtered {
            sorted_args_ignore_list v _ time timestamp;

            proxy_set_header Host "backend";
            proxy_pass http://localhost:8081;

            proxy_cache zone;
            proxy_cache_key "$uri$sorted_args";
            proxy_cache_valid 200 1m;
        }

        # Use sorted args without filtering
        location / {
            proxy_pass http://localhost:8081;

            proxy_cache zone;
            proxy_cache_key "$uri$sorted_args";
            proxy_cache_valid 200 10m;
        }
    }

    # Backend server for testing
    server {
        listen       8081;

        location / {
            return 200 "args: $args\nsorted_args: $sorted_args\n";
        }
    }
}
```

## How It Works

1. **Parameter Extraction**: The module parses the querystring from `r->args`, splitting on `&` and `=`
2. **Queue Building**: Each parameter is stored in a queue structure with its key, value, and complete key-value pair
3. **Sorting**: Parameters are sorted using a natural comparison function:
   - Primary sort: parameter name (case-insensitive, natural order)
   - Secondary sort: complete parameter string (key=value, natural order)
   - Natural order means embedded numbers are compared numerically: `item2` < `item10`
4. **Empty Value Stripping**: Parameters with `=` but no value (like `?a=`) are removed
5. **Allowlist Filtering**: If `sorted_args_allow_list` is configured, only parameters matching patterns are kept
6. **Blocklist Filtering**: Parameters matching patterns in `sorted_args_ignore_list` are excluded
7. **Deduplication**: If `sorted_args_dedupe` is enabled, only first or last occurrence of each key is kept
8. **Reconstruction**: The sorted, filtered parameters are joined with `&` to form the final string

## Testing

This project uses [Test::Nginx](https://metacpan.org/pod/Test::Nginx::Socket) for its test suite, running inside Docker for reproducible builds.

### Prerequisites

- Docker

### Running Tests

Run the full test suite:

```bash
make tests
```

Run a specific test file:

```bash
make tests T=t/sorted_args.t
```

Disable HUP mode for debugging (slower but more isolated):

```bash
make tests HUP=0
```

Use a different Nginx version:

```bash
make tests NGINX_VERSION=release-1.26.2
```

Open an interactive shell in the test container for debugging:

```bash
make shell
```

### Test Coverage

The test suite verifies:
- ✅ Basic sorting functionality
- ✅ Natural/numeric sorting (e.g., `p=1`, `p=2`, `p=10` in correct order)
- ✅ Array-like parameters (e.g., `c[]=1&c[]=2`)
- ✅ Blocklist filtering (`sorted_args_ignore_list`)
- ✅ Allowlist filtering (`sorted_args_allow_list`)
- ✅ Combined allowlist and blocklist usage
- ✅ Wildcard patterns: prefix (`utm_*`), suffix (`*_id`), contains (`*token*`)
- ✅ Deduplication: `sorted_args_dedupe first` and `last`
- ✅ Empty querystring handling
- ✅ Empty value stripping (`?a=&b=2` → `b=2`)
- ✅ Cache key usage
- ✅ Location-level configuration inheritance
- ✅ `sorted_args_overwrite` directive
- ✅ Case-insensitive parameter matching (both allowlist and blocklist)
- ✅ Parameters without values vs empty values
- ✅ Duplicate parameter handling
- ✅ Special character preservation
- ✅ Malformed query strings (consecutive ampersands)
- ✅ Parameters with multiple equals signs
- ✅ E2E: `$args` is modified before cache key evaluation (REWRITE phase timing)
- ✅ E2E: Reordered params produce identical cache keys
- ✅ E2E: Rewrite directives see overwritten `$args`

## Performance Considerations

- The sorted querystring is computed once per request and cached in the request context
- Sorting uses Nginx's efficient queue-based algorithm
- Filtering uses case-insensitive string comparison
- Memory allocation is done from the request pool, so no explicit cleanup is needed

## Limitations

- Parameter values are not decoded/encoded; original encoding is preserved
- Filtering is case-insensitive for parameter names but preserves original case in output
- Parameters with empty values (e.g., `?a=`) are always stripped; use `?a` (no equals) for flags

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-sorted-args](https://github.com/GetPageSpeed/ngx_http_sorted_args){target=_blank}.