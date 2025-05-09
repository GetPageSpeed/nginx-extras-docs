# NGINX-MOD

As you may know, [our repository](https://www.getpagespeed.com/redhat){target=_blank} holds the latest stable NGINX and a vast array of dynamic modules for it. 

However, some performance-oriented folks are always looking for speeding up what's already fast - that is NGINX itself. 

There are some open-source patches for it, mainly by Cloudflare to improve things further. 
To save trouble for many people relying on a manual compilation, we build this better patched NGINX as a package that is compatible with all the NGINX modules we have! 
Its official name is NGINX-MOD.

NGINX-MOD is based on the latest *stable* NGINX with the following additions:

* **Seamless HTTP/3 Support**: Experience faster and more reliable web connections with the cutting-edge HTTP/3 protocol.
* **Enhanced HTTP/2 HPACK Compression**: Boost your website’s performance through optimized header compression, ensuring quicker data transfer.
* **Dynamic TLS Record Management**: Improve both security and speed with dynamically handled TLS records, adapting to your site’s needs in real-time.
* **Advanced Rate Limiting**: Gain precise control over traffic with the extended `ngx_http_limit_req_module`, allowing you to set request limits on an hourly, daily, weekly, or yearly basis.
* **Active Health Monitoring**: Maintain high uptime and reliability with real-time health checks of your upstream servers. [Learn More](https://github.com/yaoweibin/nginx_upstream_check_module)
* **Enhanced Security Features**: Protect your server information by disabling the display of the NGINX software name in both the Server: header and error pages.
* **Secure SSL Proxying with `CONNECT` Method**: Handle and proxy SSL requests using the `CONNECT` method, ensuring secure and efficient data transmission.
* **Dark Mode Support**: Automatic Dark Mode Support for NGINX error pages.

Upgrade to GetPageSpeed today and take full advantage of these advanced NGINX-MOD features to optimize your website’s performance, security, and reliability!

More on those patches in the documentation below.

## How to install NGINX-MOD

=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm
    dnf -y install dnf-plugins-core
    dnf config-manager --disable getpagespeed-extras-mainline
    dnf config-manager --enable getpagespeed-extras-nginx-mod
    dnf -y install nginx
    systemctl enable --now nginx
    ```

=== "CentOS/RHEL 7"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm
    yum -y install yum-utils
    yum-config-manager --disable getpagespeed-extras-mainline
    yum-config-manager --enable getpagespeed-extras-nginx-mod
    yum -y install nginx
    systemctl enable --now nginx
    ``` 
 
=== "Amazon Linux 2"

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    amazon-linux-extras install epel
    yum -y install yum-utils
    yum-config-manager --disable getpagespeed-extras-mainline
    yum-config-manager --enable getpagespeed-extras-nginx-mod
    yum -y install nginx
    systemctl enable --now nginx
    ```

## How to switch to NGINX-MOD from our regular NGINX

If you were using our regular NGINX build, you can run a series of commands to upgrade to NGINX-MOD without affecting installed modules or configuration:

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm yum-utils
yum-config-manager --disable getpagespeed-extras-mainline
yum-config-manager --enable getpagespeed-extras-nginx-mod
yum -y update nginx
# importantly, we must re-enable the nginx service after switching packages:
systemctl enable --now nginx
```


## Modules for NGINX-MOD

NGINX-MOD is fully compatible with over 50 NGINX module packages in our base repository.
So you can install them as usual, for example:

    yum -y install nginx-module-pagespeed

## Active Health Checks

### Key Features of Active Health Checks

- **Multi-Protocol Support**: HTTP, TCP, SSL Hello, MySQL, AJP, FastCGI.  
- **Customizable Checks**: Interval, timeout, success/failure thresholds.  
- **Status Dashboard**: Real-time monitoring via HTML, CSV, or JSON.  
- **Dynamic Adjustments**: Mark servers up/down based on health checks.  

### Configuration Basics for Active Health Checks

#### Example: HTTP Health Check

```nginx
http {
  upstream backend {
    server 192.168.1.10:80; 
    server 192.168.1.11:80;
    
    # Health check configuration
    check interval=5s rise=2 fall=3 timeout=4s type=http;
    check_http_send "GET /health HTTP/1.1\r\nHost: example.com\r\n\r\n";
    check_http_expect_alive http_2xx http_3xx;
  }

  server {
    listen 80;
    location / {
      proxy_pass http://backend;
    }

    # Health status dashboard (restricted access)
    location /status {
      check_status html;
      allow 10.0.0.0/8;  # Authorized IPs
      deny all;
      access_log off;
    }
  }
}
```  

#### Explanation:  

- **`check`**:  
  - `interval=5s`: Check every 5 seconds.  
  - `rise=2`: Mark server "up" after 2 consecutive successes.  
  - `fall=3`: Mark server "down" after 3 consecutive failures.  
  - `type=http`: Use HTTP checks.  
- **`check_http_send`**: Custom HTTP request sent to upstream servers.  
- **`check_http_expect_alive`**: Treat HTTP 2xx/3xx responses as healthy.  
- **`check_status`**: Exposes a dashboard at `/status` in HTML format.  

### Active Health Checks Directives Reference  

####  Core Directives  
| Directive | Syntax | Default | Description |  
|-----------|--------|---------|-------------|  
| **`check`** | `interval=ms [fall=count] [rise=count] [timeout=ms] [type=protocol] [default_down=true\|false] [port=number]` | `interval=30s fall=5 rise=2 timeout=1s type=tcp default_down=true` | Configures health check parameters. |  
| **`check_http_send`** | `"HTTP_REQUEST"` | `"GET / HTTP/1.0\r\n\r\n"` | Custom HTTP request for `type=http` checks. |  
| **`check_http_expect_alive`** | `http_2xx \| http_3xx \| ...` | `http_2xx \| http_3xx` | HTTP status codes indicating a healthy server. |  

#### Advanced Directives  
| Directive | Purpose |  
|-----------|---------|  
| **`check_keepalive_requests`** | Number of requests per connection (default: `1`). |  
| **`check_fastcgi_param`** | Custom FastCGI parameters for `type=fastcgi` checks. |  
| **`check_shm_size`** | Shared memory size for health checks (default: `1M`). |  

---

### Active Health Check Types  

#### 1. **`type=http`**  
- **Usage**:  
  ```nginx
  check type=http;
  check_http_send "HEAD /health HTTP/1.1\r\nHost: example.com\r\n\r\n";
  check_http_expect_alive http_200 http_302;
  ```  
- **Response Codes**: Configure acceptable statuses (e.g., `http_2xx`).  

#### 2. **`type=tcp`**  
- Simple TCP connection check:  
  ```nginx
  check interval=10s type=tcp;
  ```  

#### 3. **`type=mysql`**  
- Validates MySQL server availability:  
  ```nginx
  check type=mysql port=3306;
  ```  

#### 4. **`type=fastcgi`**  
- Custom FastCGI parameters:  
  ```nginx
  check type=fastcgi;
  check_fastcgi_param "REQUEST_METHOD" "GET";
  check_fastcgi_param "SCRIPT_FILENAME" "index.php";
  ```  

---

### Status Page Setup  

#### Endpoint Configuration  
```nginx
location /status {
  check_status [html|csv|json];  # Default: html
  allow 192.168.1.0/24;         # Restrict access
  deny all;
}
```  

#### Query Parameters  
- **`format`**: Override output format (e.g., `/status?format=json`).  
- **`status`**: Filter servers by status (e.g., `/status?status=down`).  

#### Sample Outputs  
- **HTML**: Interactive table with server status.  
- **JSON**: Machine-readable format for automation.  
- **CSV**: Simplified comma-separated values.  

---

### Troubleshooting & Best Practices for Active Health Checks

#### Common Issues  
1. **Shared Memory Exhausted**:  
   - **Fix**: Increase `check_shm_size` in the `http` block:  
     ```nginx
     http {
       check_shm_size 10M;  # Default: 1M
     }
     ```  

2. **False Positives/Negatives**:  
   - Adjust `rise`/`fall` thresholds and validate `check_http_send` requests.  

3. **Timeout Errors**:  
   - Increase `timeout` if upstream servers respond slowly.  

#### Security Tips  
- Restrict access to the `/status` endpoint using `allow`/`deny`.  
- Use HTTPS for the status page if sensitive data is exposed.  

Active checks work seamlessly with `ip_hash`, `least_conn`, and third-party modules like `sticky` or `fair`.  

## ngx_http_limit_req_module patch

Some NGINX users seek to define rate-limiting of once in a day for specific resources. This is not possible with stock NGINX.
Our patch allows for a more fine-grained rate limit configuration. Examples:

    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/h; # 1 request per hour
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/d; # 1 request per day
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/w; # 1 request per week
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/M; # 1 request per month
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/Y; # 1 request per year

It is important to note, that your defined zone memory size should allow retaining old IP entries before the defined rate will apply.

For example, you have defined a `10m` zone and `1r/d` for a particular resource. `10m` can store around 160,000 IP addresses.
So if someone visits your rate-limited resource, *and your traffic to it exceed 160K unique visitors within 24 hrs*, then the same visitor can theoretically not be rate-limited within the same day, because information about his IP address will be evicted from memory after enough visitors visited the resource.

This note applies to the stock module's configuration as well, but less so.

So the rules of thumb are:

* You likely need to  increase memory zone, if your traffic is sufficient to be able to evict old IP addresses "too early"
* This is more appropriate for rate-limiting specific resources, not the whole website

## What is HPACK Patch

HPACK patch implements [full HPACK](https://blog.cloudflare.com/hpack-the-silent-killer-feature-of-http-2/) in NGINX. In short, this allows for compressing HTTP headers

## What is the `CONNECT` method support

NGINX-MOD provides support for the `CONNECT` method request. This method is mainly used 
to tunnel SSL requests through proxy servers. 

To enable and configure, please refer to the [`proxy_connect` directives](https://github.com/dvershinin/ngx_http_proxy_connect_module?tab=readme-ov-file#directives). 

## Configuration Directives of NGINX-MOD

There are some configuration directives in this build, which are not otherwise available in regular builds. Let's document them here.

The following set of configuration directives are added by [dynamic TLS records](https://blog.cloudflare.com/optimizing-tls-over-tcp-to-reduce-latency/) patch. 

### `ssl_dyn_rec_enable on|off`

Whether to enable dynamic TLS records.

### `ssl_dyn_rec_size_lo`

The TLS record size to start with. Defaults to 1369 bytes (designed to fit the entire record in a single TCP segment: 1369 = 1500 - 40 (IPv6) - 20 (TCP) - 10 (Time) - 61 (Max TLS overhead))
ssl_dyn_rec_size_hi: the TLS record size to grow to. Defaults to 4229 bytes (designed to fit the entire record in 3 TCP segments)

### `ssl_dyn_rec_threshold`

The number of records to send before changing the record size.

Because we build with the latest OpenSSL:

### `ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3];`

Not a new directive. But since we build with the most recent stable OpenSSL, it allows for `TLSv1.3` value to be used.

## Hiding software information

By default, NGINX only supports `server_tokens off;` which still yields `nginx` in the `Server:` header and in error pages.
With NGINX-MOD, you can specify a new value `none`, which will cause NGINX to stop emission of its presence on the server:

    server_tokens none;

## Verification

To verify how you benefit from NGINX-MOD, you can run some tests.

### Check HTTP/2 headers compression

```
yum install nghttp2
h2load https://example.com -n 2 | tail -6 |head -1
```

Example output:

> traffic: 71.46KB (73170) total, 637B (637) headers (space savings 78.68%), 70.61KB (72304) data

If you see 50% or more space savings, then it means that full HPACK compression is utilized.

## How to switch back to stable NGINX

Going back to the stable package while preserving existing configuration:

```
yum-config-manager --disable getpagespeed-extras-nginx-mod
MOD_PKGS=$(rpm -qa --queryformat '%{NAME}\n' | grep nginx-mod | grep -v nginx-module)
rpm --erase --justdb --nodeps ${MOD_PKGS}
STABLE_PKGS=$(echo ${MOD_PKGS} | sed 's@nginx-mod@nginx@g')
yum -y install ${STABLE_PKGS}
yum history sync
# importantly, we must re-enable the nginx service after switching packages:
systemctl enable --now nginx
```

These commands will disable the NGINX-MOD repository and replace any `nginx-mod*` packages with their equivalents from the base repository, thus downgrading to stable NGINX.

## Compatibility notes

* NGINX-MOD is presently not compatible with the Plesk control panel
