---
title: "Country Blocking with GeoIP2"
description: "Block or allow traffic by country using NGINX and MaxMind GeoIP2 database. Complete setup guide for RHEL, CentOS, Rocky Linux, and AlmaLinux."
---

# :material-earth: Country Blocking with GeoIP2

<p class="subtitle" style="font-size: 1.3rem; opacity: 0.9; margin-top: -0.5rem;">
Control access by country with MaxMind's accurate geolocation database.
</p>

---

<div class="grid cards" markdown>

-   :material-shield-lock:{ .lg .middle } **Block Bad Actors**

    ---

    Stop attacks from high-risk countries before they reach your app

-   :material-scale-balance:{ .lg .middle } **Compliance Ready**

    ---

    Enforce geographic restrictions for GDPR, licensing, or legal requirements

-   :material-speedometer:{ .lg .middle } **Zero Overhead**

    ---

    In-memory database lookup—no external API calls or latency

-   :material-check-all:{ .lg .middle } **Accurate Data**

    ---

    MaxMind GeoIP2 databases with 99.8% country accuracy

</div>

---

## :material-clipboard-list: Prerequisites

You'll need a **free MaxMind account** to download GeoIP2 databases:

1. Sign up at [maxmind.com/en/geolite2/signup](https://www.maxmind.com/en/geolite2/signup)
2. Generate a license key in your account
3. Save it for the automated update setup

---

## :material-clock-fast: Quick Setup

### Step 1: Install GeoIP2 Module

```bash
# Install GetPageSpeed repository
dnf -y install https://extras.getpagespeed.com/release-latest.rpm

# Install GeoIP2 module and automatic database updater
dnf -y install nginx-module-geoip2 geoipupdate
```

Enable in `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_geoip2_module.so;
```

---

### Step 2: Configure Database Updates

Edit `/etc/GeoIP.conf`:

```ini
AccountID YOUR_ACCOUNT_ID
LicenseKey YOUR_LICENSE_KEY
EditionIDs GeoLite2-Country GeoLite2-City
```

Download the databases:

```bash
geoipupdate
```

Enable automatic weekly updates:

```bash
systemctl enable --now geoipupdate.timer
```

---

### Step 3: Configure NGINX

Add to your `http` block in `/etc/nginx/nginx.conf`:

```nginx
# Load GeoIP2 databases
geoip2 /usr/share/GeoIP/GeoLite2-Country.mmdb {
    auto_reload 60m;
    $geoip2_country_code country iso_code;
    $geoip2_country_name country names en;
}
```

---

### Step 4: Block Countries

=== "Block Specific Countries"

    ```nginx
    # Block Russia, China, North Korea
    map $geoip2_country_code $blocked_country {
        default 0;
        RU 1;
        CN 1;
        KP 1;
    }

    server {
        # ... your server config ...
        
        if ($blocked_country) {
            return 403;
        }
    }
    ```

=== "Allow Only Specific Countries"

    ```nginx
    # Only allow US, UK, Canada, Australia
    map $geoip2_country_code $allowed_country {
        default 0;
        US 1;
        GB 1;
        CA 1;
        AU 1;
    }

    server {
        # ... your server config ...
        
        if ($allowed_country = 0) {
            return 403;
        }
    }
    ```

=== "Custom Error Page"

    ```nginx
    map $geoip2_country_code $blocked_country {
        default 0;
        RU 1;
        CN 1;
    }

    server {
        error_page 403 /geo-blocked.html;
        
        location = /geo-blocked.html {
            internal;
            root /var/www/error-pages;
        }
        
        if ($blocked_country) {
            return 403;
        }
    }
    ```

Reload NGINX:

```bash
nginx -t && systemctl reload nginx
```

---

## :material-test-tube: Testing

```bash
# Test with a known IP
curl -H 'X-Forwarded-For: 8.8.8.8' https://example.com
# Should work (Google DNS - US)

curl -H 'X-Forwarded-For: 77.88.8.8' https://example.com
# Should be blocked (Yandex DNS - Russia, if RU is blocked)
```

!!! warning "Testing Locally"
    Local/private IPs return empty country codes. Test with real public IPs.

---

## :material-cog: Advanced Usage

### Use Real Client IP Behind Proxy/CDN

```nginx
geoip2 /usr/share/GeoIP/GeoLite2-Country.mmdb {
    $geoip2_country_code source=$http_x_forwarded_for country iso_code;
}
```

### Different Rules for Different Paths

```nginx
# Block everywhere except API
location / {
    if ($blocked_country) {
        return 403;
    }
    # ... normal config ...
}

location /api/ {
    # API accessible from anywhere
    # ... api config ...
}
```

### Log Country Information

```nginx
log_format geo '$remote_addr - $geoip2_country_code - $request';
access_log /var/log/nginx/geo.log geo;
```

### Rate Limit by Country

```nginx
# Stricter limits for high-risk countries
map $geoip2_country_code $limit_key {
    default $binary_remote_addr;
    RU $binary_remote_addr$geoip2_country_code;
    CN $binary_remote_addr$geoip2_country_code;
}

limit_req_zone $limit_key zone=geo_limit:10m rate=10r/s;
```

---

## :material-format-list-bulleted: Common Country Codes

| Code | Country | Code | Country |
|------|---------|------|---------|
| US | United States | DE | Germany |
| GB | United Kingdom | FR | France |
| CA | Canada | AU | Australia |
| CN | China | RU | Russia |
| IN | India | BR | Brazil |
| JP | Japan | KR | South Korea |
| KP | North Korea | IR | Iran |

Full list: [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

---

## :material-wrench: Troubleshooting

??? question "Country always empty"

    - Check database path exists: `ls -la /usr/share/GeoIP/`
    - Verify module loaded: `nginx -V 2>&1 | grep geoip2`
    - Check IP isn't private/localhost

??? question "Wrong country detected"

    - Update database: `geoipupdate`
    - Check if behind CDN/proxy (use `X-Forwarded-For`)
    - MaxMind accuracy: ~99.8% for countries

??? question "Database not updating"

    - Check timer: `systemctl status geoipupdate.timer`
    - Verify credentials in `/etc/GeoIP.conf`
    - Run manually: `geoipupdate -v`

---

## :material-link-variant: Related

<div class="grid cards" markdown>

-   :material-package-variant:{ .lg .middle } **GeoIP2 Module**

    ---

    Complete directive reference

    [:octicons-arrow-right-24: Documentation](../modules/geoip2.md)

-   :material-security:{ .lg .middle } **ModSecurity WAF**

    ---

    Full web application firewall

    [:octicons-arrow-right-24: Documentation](../modules/security.md)

-   :material-shield-alert:{ .lg .middle } **Rate Limiting**

    ---

    Protect against abuse

    [:octicons-arrow-right-24: Documentation](../modules/dynamic-limit-req.md)

</div>

