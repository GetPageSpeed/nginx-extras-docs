# *security-headers*: NGINX module for sending security headers


## Installation

### CentOS/RHEL 6, 7, 8 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-security-headers
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_security_headers_module.so;
```


This document describes nginx-module-security-headers [v0.0.9](https://github.com/GetPageSpeed/ngx_security_headers/releases/tag/0.0.9){target=_blank} 
released on Feb 29 2020.
    
<hr />

This NGINX module adds security headers and removes insecure headers easily. 

## Synopsis

```nginx
http {
    security_headers on;
    ...
}
```

Running `curl -IL http://example.com/` will yield additional headers:

```
HTTP/1.1 200 OK
Server: nginx
Date: Tue, 21 May 2019 16:15:46 GMT
Content-Type: text/html; charset=UTF-8
Vary: Accept-Encoding
Accept-Ranges: bytes
Connection: keep-alive
X-Frame-Options: SAMEORIGIN  <-----------
X-XSS-Protection: 1; mode=block <-----------
Referrer-Policy: no-referrer-when-downgrade <-----------
```

Running `curl -IL http://example.com/some.css` (or `some.js`) will yield *additional* security header:

```
HTTP/1.1 200 OK
...
X-Content-Type-Options: nosniff <-----------
```


## Key Features

*   Plug-n-Play: the default set of security headers can be enabled with `security_headers on;` in your NGINX configuration
*   Sends `X-Content-Type-Options` only for relevant MIME types (CSS/JS), preserving unnecessary headers from being sent for HTML documents
*   Similiarly, sends HTML-only relevant headers for relevant types and skips sending for others e.g. `X-Frame-Options` is useless for CSS
*   Plays well with conditional `GET` requests: the security headers are not included there unnecessarily
*   Does not suffer the `add_header` directive's pitfalls
*   Hides `X-Powered-By`, which often leaks PHP version information
*   Hides `Server` header altogether, not just the version information

## Configuration directives

### `security_headers`

- **syntax**: `security_headers on | off`
- **default**: `off`
- **context**: `http`, `server`, `location`

Enables or disables applying security headers. The default set includes:

* `X-Frame-Options: SAMEORIGIN`
* `X-XSS-Protection: 1; mode=block`
* `Referrer-Policy: strict-origin-when-cross-origin`
* `X-Content-Type-Options: nosniff` (for CSS and Javascript)

The values of these headers (or their inclusion) can be controlled with other `security_headers_*` directives below.

### `hide_server_tokens`

- **syntax**: `hide_server_tokens on | off`
- **default**: `off`
- **context**: `http`, `server`, `location`

Enables hiding headers which leak software information:

*   `Server`
*   `X-Powered-By`
*   `X-Page-Speed`
*   `X-Varnish`

It's worth noting that some of those headers bear functional use, e.g. [`X-Page-Speed` docs](https://www.modpagespeed.com/doc/configuration#XHeaderValue) mention:

> ... it is used to prevent infinite loops and unnecessary rewrites when PageSpeed 
> fetches resources from an origin that also uses PageSpeed

So it's best to specify `hide_server_tokens on;` in a front-facing NGINX insances, e.g.
the one being accessed by actual browsers, and not the ones consumed by Varnish or other software.

In most cases you will be just fine with `security_headers on;` and `hide_server_tokens on;`, without any adjustments.

For fine-tuning, use the header-specific directives below. 
A special value `omit` disables sending a particular header by the module (useful if you want to let your backend app to send it). 

### `security_headers_xss`

- **syntax**: `security_headers off | on | block | omit`
- **default**: `block`
- **context**: `http`, `server`, `location`

Controls `X-XSS-Protection` header. 
Special `omit` value will disable sending the header by the module. 
The `off` value is for disabling XSS protection: `X-XSS-Protection: 0`.

### `security_headers_frame`

- **syntax**: `security_headers_frame sameorigin | deny | omit`
- **default**: `sameorigin`
- **context**: `http`, `server`, `location`

Controls inclusion and value of `X-Frame-Options` header. 
Special `omit` value will disable sending the header by the module. 


### `security_headers_referrer_policy`

- **syntax**: `security_headers_referrer_policy no-referrer | no-referrer-when-downgrade | same-origin | origin 
| strict-origin | origin-when-cross-origin | strict-origin-when-cross-origin | unsafe-url | omit`
- **default**: `strict-origin-when-cross-origin`
- **context**: `http`, `server`, `location`

Controls inclusion and value of [`Referrer-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) header. 
Special `omit` value will disable sending the header by the module. 

### `security_headers_nosniff_types`

- **syntax**: `security_headers_nosniff_types <mime_type> [..]`
- **default**: `text/css text/javascript application/javascript`
- **context**: `http`, `server`, `location`

Defines MIME types, for which `X-Content-Type-Options: nosniff` is sent.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-security-headers](https://github.com/GetPageSpeed/ngx_security_headers){target=_blank}.