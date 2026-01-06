---

title: "Redirect server name within the same request"
description: "RPM package nginx-module-server-redirect. The server redirect module redirects server name in the same request. This allows internal routing between virtual servers without external redirects, useful for complex multi-server configurations."

---

# *server-redirect*: Redirect server name within the same request


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
    dnf -y install nginx-module-server-redirect
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-server-redirect
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_server_redirect_module.so;
```


This document describes nginx-module-server-redirect [v0.1.2](https://github.com/dvershinin/ngx_http_server_redirect_module/releases/tag/0.1.2){target=_blank} 
released on Jan 06 2026.

<hr />

## 

## Description

The `ngx_http_server_redirect_module` is a custom nginx module designed to facilitate dynamic server redirection based on configurable rules. It allows users to redirect incoming requests to different servers conditionally.

## Synopsis

### Basic Redirection
Redirect all requests to `newserver.com` unconditionally.

```nginx
http {
    server {
        listen 80;
        server_name example.com;

        server_redirect newserver.com;

        location / {
            proxy_pass http://newserver.com;
        }
    }

    server {
        listen 80;
        server_name newserver.com;

        # You can get original host from this variable.
        add_header x-original-host $server_redirect_original_host;

        location / {
            proxy_pass http://upstream.com;
        }
    }
}
```

### Conditional Redirection

Redirect requests based on the presence of a specific header.

```nginx
http {
    server {
        listen 80;
        server_name example.com;

        # Redirect if request has 'X-Redirect' header and value is not 0 or empty.
        server_redirect newserver.com if=$http_x_redirect;

        # You can use ngx_http_var_module to generate judgment variables based on conditions.
        # https://git.hanada.info/hanada/ngx_http_var_module
        # var $is_ipv6 if_find $remote_addr :;
        # server_redirect newserver.com if=$is_ipv6;

        # This module takes effect after the real_ip module,
        # Therefore, the real_ip module's directives will take effect on the server before server redirect.
        # real_ip_header x-client-ip;

        location / {
            proxy_pass http://newserver.com;
        }
    }

    server {
        listen 80;
        server_name newserver.com;

        # You can get original host from this variable.
        add_header x-original-host $server_redirect_original_host;

        location / {
            proxy_pass http://upstream.com;
        }
    }
}
```

### Schedule Redirection

Redirect the current request to another server from the first request path.
If request `http://example.com/newserver.com/test?arg=1`, it will be redirect to `http:///newserver.com/test?arg=1`. This process is internal and no 302 redirection will occur.
```nginx
http {
    server {
        listen 80;
        server_name example.com;

        # Enable schedule redirection.
        schedule_redirect on;

        # Requests will not arrive here unless the first path in the request path does not exist or the host in the first path is invalid.
        return 400 "request path invalid";
    }

    server {
        listen 80;
        server_name newserver.com;

        # You can get original host from this variable.
        add_header x-original-host $server_redirect_original_host;

        location / {
            proxy_pass http://upstream.com;
        }
    }
}
```


## Configuration

### Directive: `server_redirect`

**Syntax:** *server_redirect target_host [if=condition]*

**Default:** *-*

**Context:** *server*

Redirect the current request to another server. The target server must have the same listening port as the current server. 

The target host should be a specific host name just like the host in the request header. Even if the target server you want to redirect to is a wildcard domain name or a regular expression.

If the target server cannot be found, it will be redirected to the default server.

The if parameter enables conditional redirection. A request will not be redirected if the condition evaluates to “0” or an empty string. In addition, you can also use the form of `if!=` to make negative judgments.

Here is an example:

```nginx
server_redirect newserver.com if=$http_server_redirect;
```

This example redirects requests to `newserver.com` if the `Server-Redirect` header has value and value is not 0.

### Directive: `schedule_redirect`

**Syntax:** *schedule_redirect on | off*

**Default:** *schedule_redirect off*

**Context:** *server*

Redirect the current request to another server from the first request path.

If enabled, when accessing http://a.com/b.com/, the request will be redirected to http://b.com/. If the target server cannot be found, it will be redirected to the default server.

When server_redirect directive exists and meets the redirection conditions, server_redirect will be executed first.

If the request path does not have the first path (such as the home page), no redirection will be made.

After redirection, even $request_uri will be cleared of the first path. You can only find the original request path in the request line variable $request.

### Variable: `$server_redirect_original_host`

Keeps the original value of variable $host before redirection occurs.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-server-redirect](https://github.com/dvershinin/ngx_http_server_redirect_module){target=_blank}.