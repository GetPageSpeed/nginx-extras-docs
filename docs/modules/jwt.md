---

title: "NGINX JWT Module"
description: "RPM package nginx-module-jwt. NGINX module to check for a valid JWT. "

---

# *jwt*: NGINX JWT Module


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
    dnf -y install nginx-module-jwt
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-jwt
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_auth_jwt_module.so;
```


This document describes nginx-module-jwt [v3.4.3](https://github.com/max-lt/nginx-jwt-module/releases/tag/v3.4.3){target=_blank} 
released on Mar 14 2025.

<hr />
[github-license-url]: /blob/master/LICENSE
[action-docker-url]: https://github.com/max-lt/nginx-jwt-module/actions/workflows/docker.yml
[github-container-url]: https://github.com/max-lt/nginx-jwt-module/pkgs/container/nginx-jwt-module

## Nginx jwt auth module
[![License](https://img.shields.io/github/license/maxx-t/nginx-jwt-module.svg)][github-license-url]

This is an NGINX module to check for a valid JWT, this module intend to be as light as possible and to remain simple:
 - Docker image based on the [official nginx Dockerfile](https://github.com/nginxinc/docker-nginx) (alpine).
 - Light image (~400KB more than the official one).

### Module Configuration:

#### Example Configuration:
```nginx
## nginx.conf
load_module /usr/lib/nginx/modules/ngx_http_auth_jwt_module.so;

http {
    server {
        auth_jwt_key "0123456789abcdef" hex; # Your key as hex string
        auth_jwt     off;

        # Default auth method is "Authentication" header
        location /secured-by-auth-header/ {
            auth_jwt on;
        }

        # But you can use a cookie instead
        location /secured-by-cookie/ {
            auth_jwt $cookie_MyCookieName;
        }

        # JWT keys are inherited from the previous configuration level
        # but you can have different keys for different locations
        location /secured-by-auth-header-too/ {
            auth_jwt_key "another-secret"; # Your key as utf8 string
            auth_jwt on;
        }

        location /secured-by-rsa-key/ {
            auth_jwt_key /etc/keys/rsa-public.pem file; # Your key from a PEM file
            auth_jwt on;
        }

        location /not-secure/ {}
    }
}
```

Note: don't forget to [load](http://nginx.org/en/docs/ngx_core_module.html#load_module) the module in the main context: 
```nginx
load_module /usr/lib/nginx/modules/ngx_http_auth_jwt_module.so;
```

### Directives:

#### auth_jwt

    Syntax:	 auth_jwt $variable | on | off;
    Default: auth_jwt off;
    Context: http, server, location

Enables validation of JWT.

The `auth_jwt $variable` value can be used to set a custom way to get the JWT, for example to get it from a cookie instead of the default `Authentication` header: ` auth_jwt $cookie_MyCookieName;`

<hr>

#### auth_jwt_key

    Syntax:	 auth_jwt_key value [encoding];
    Default: ——
    Context: http, server, location

Specifies the key for validating JWT signature (must be hexadecimal).<br>
The *encoding* option may be `hex | utf8 | base64 | file` (default is `utf8`).<br>
The `file` option requires the *value* to be a valid file path (pointing to a PEM encoded key).

<hr>

#### auth_jwt_alg

    Syntax:	 auth_jwt_alg any | HS256 | HS384 | HS512 | RS256 | RS384 | RS512 | ES256 | ES384 | ES512;
    Default: auth_jwt_alg any;
    Context: http, server, location

Specifies which algorithm the server expects to receive in the JWT.

<hr>

#### auth_jwt_require

    Syntax:	 auth_jwt_require $value ... [error=401 | 403];
    Default: ——
    Context: http, server, location

Specifies additional checks for JWT validation. The authentication will succeed only if all the values are not empty and are not equal to “0”.

These directives are inherited from the previous configuration level if and only if there are no auth_jwt_require directives defined on the current level.

If any of the checks fails, the 401 error code is returned. The optional error parameter allows redefining the error code to 403.

Example:
```nginx
## server.conf

map $jwt_claim_role $jwt_has_admin_role {
    \"admin\"  1;
}

map $jwt_claim_scope $jwt_has_restricted_scope {
    \"restricted\"  1;
}

server {
  # ...

  location /auth-require {
    auth_jwt_require $jwt_has_admin_role error=403;
    # ...
  }

  location /auth-compound-require {
    auth_jwt_require $jwt_has_admin_role $jwt_has_restricted_scope error=403;
    # ...
  }
}
```

> Note that as `$jwt_claim_` returns a JSON-encoded value, so we have to check `\"value\"` (and not  `value`)

### Embedded Variables:
The ngx_http_auth_jwt_module module supports embedded variables:
- $jwt_header_*name* returns the specified header value
- $jwt_claim_*name* returns the specified claim value
- $jwt_headers returns headers
- $jwt_payload returns payload

> Note that as all returned values are JSON-encoded, so string will be surrounded by `"` character

### Image:
Image is generated with Github Actions (see [nginx-jwt-module:latest][github-container-url])

```
docker pull ghcr.io/max-lt/nginx-jwt-module:latest
```

#### Simply create your image from Github's generated one
```dockerfile
FROM ghcr.io/max-lt/nginx-jwt-module:latest

## Copy your nginx conf
## Don't forget to include this module in your configuration
## load_module /usr/lib/nginx/modules/ngx_http_auth_jwt_module.so;
COPY my-nginx-conf /etc/nginx

EXPOSE 8000

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
```

#### Or use the provided one directly
```bash
docker run -p 80:80 \
  -v ./nginx.conf:/etc/nginx/nginx.conf \
  ghcr.io/max-lt/nginx-jwt-module
```

## or
docker build -f Dockerfile -t jwt-nginx .
```

### Test:

#### Default usage:
```bash
make test # Will build a test image and run the test suite
```

### Example configurations:

In this section, we will see some examples of how to use this module.

#### Redirect to login page if JWT is invalid:
```nginx
load_module /usr/lib/nginx/modules/ngx_http_auth_jwt_module.so;

## ...

http {
    server {
        listen 80;
        server_name _;

        auth_jwt_key "0123456789abcdef" hex; # Your key as hex string
        auth_jwt     off;

        location @login_err_redirect {
            return 302 $scheme://$host:$server_port/login?redirect=$request_uri;
        }

        location /secure/ {
            auth_jwt on;
            error_page 401 = @login_err_redirect;
        }

        location / {
            return 200 "OK";
        }
    }
}
```

Trying `curl -i http://localhost/secure/path?param=value` will return a 302 redirect to `/login?redirect=/secure/path?param=value` if the JWT is invalid.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-jwt](https://github.com/max-lt/nginx-jwt-module){target=_blank}.