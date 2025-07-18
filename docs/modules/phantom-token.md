---

title: "Phantom Token NGINX Module"
description: "RPM package nginx-module-phantom-token. NGINX module that introspects phantom access tokens according to RFC 7662 "

---

# *phantom-token*: Phantom Token NGINX Module


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
    dnf -y install nginx-module-phantom-token
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-phantom-token
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_curity_http_phantom_token_module.so;
```


This document describes nginx-module-phantom-token [v2.0.0](https://github.com/curityio/nginx_phantom_token_module/releases/tag/2.0.0){target=_blank} 
released on May 22 2025.

<hr />

[![Quality](https://img.shields.io/badge/quality-production-green)](https://curity.io/resources/code-examples/status/)
[![Availability](https://img.shields.io/badge/availability-binary-blue)](https://curity.io/resources/code-examples/status/)

NGINX module that introspects access tokens according to [RFC 7662](https://tools.ietf.org/html/rfc7662), producing a "phantom token" that can be forwarded to back-end APIs and Web services. Read more about the [Phantom Token approach](https://curity.io/resources/learn/phantom-token-pattern/).

This module, when enabled, filters incoming requests, denying access to those which do *not* have a valid OAuth access token presented in an `Authorization` header. From this header, the access_token is extracted and introspected using the configured endpoint. The Curity Identity Server replies to this request according to the standard. For an active access token, the body of the Curity Identity Server's response contains the JWT that replaces the access token in the header of the request that is forwarded by NGINX to the back-end. If the token is not valid or absent, no request to the back-end is made and the caller is given a 401, unauthorized, error. This flow is shown in the following diagram:

![NGINX / Curity integration](nginx_curity_integration.png?v=2 "Overview of how NGINX and Curity are integrated")

The initial calls by the app (web or native) are done using [OpenID Connect](http://openid.net/specs/openid-connect-core-1_0.html) (OIDC). The important part is that the token that is issued is an opaque access token. It is a GUID or UUID or a few handfuls of random bytes; there is no identity-related data in this token. It is a _phantom_ of the actual user data, hence the name -- _phantom token_. The app presents the token to the NGINX gateway according to the _Bearer Token Usage_ specficiation (i.e., [RFC 6750](https://tools.ietf.org/html/rfc6750)). This standard says that the app should send the phantom token in the `Authorization` request header. 

Once the NGINX server receives the access token, this module will kick in. Using configuration like that below, this module will interrogate the request, find the token, and make a sideways call to the Curity Identity Server. This web service request will be done using the _Token Introspection_ standard ([RFC 7662](https://tools.ietf.org/html/rfc7662)) with an `Accept` type of `application/jwt` (as defined in [RFC 7519](https://tools.ietf.org/html/rfc7519#section-10.3.1)). This will cause the Curity Identity Server to return not JSON but just a JWT. Then, the module will forward the JWT token to the back-end APIs and microservices. 

If the module is also configured to cache the results of the call to the Curity Identity Server (which it should be for production cases), the phantom token will be used as a cache key for the corresponding JWT token. This will eliminate the need for subsequent calls to the Curity Identity Server for as long as it tells the NGINX module it may cache the JWT for.

The tl;dr is a very simple API gateway that is blazing fast, highly scalable, and without any bells and whistles to get in the way. All the code is here, so it's easy to change and use with other OAuth servers even!

## Module Configuration Directives

Version 2.0 introduced a **BREAKING CHANGE** to use updated configuration directives.\
See [previous configuration instructions](https://github.com/curityio/nginx_phantom_token_module/tree/1.6.0) to configure older releases.

### Required Configuration Directives

The directives in this subsection are required; if any of these are omitted, the module will be disabled.

#### phantom_token

> **Syntax**: **`phantom_token`** `on` | `off`
>
> **Default**: *`off`*
>
> **Context**: `location`

#### phantom_token_introspection_endpoint

> **Syntax**: **`phantom_token_introspection_endpoint`** _`string`_
>
> **Default**: *`—`*
>
> **Context**: `location`


### Optional Configuration Directives

The following directives are optional and do not need to be configured.

#### phantom_token_realm

> **Syntax**: **`phantom_token_realm`** _`string`_
> 
> **Default**: *`api`*
> 
> **Context**: `location`

The name of the protected realm or scope of protection that should be used when a client does not provide an access token.

Example configuration:

```nginx
location / {
   ...
   phantom_token_realm "myGoodRealm";
}   
```

#### phantom_token_scopes

> **Syntax**: **`phantom_token_scopes`** _`string`_
>
> **Default**: *`—`*
>
> **Context**: `location`

The space-separated list of scopes that the server should inform the client are required when it does not provide an access token.

Example configuration:

```nginx
location / {
   ...
   phantom_token_scopes "scope_a scope_b scope_c";
}
```

#### phantom_token_scope

> **Syntax**: **`phantom_token_scope`** _`string`_
>
> **Default**: *`—`*
>
> **Context**: `location`

An array of scopes that the server should inform the client are required when it does not provide an access token. If `phantom_token_scopes` is also configured, that value will supersede these.
 
Example configuration:
 
```nginx
location / {
   ...
   phantom_token_scope "scope_a";
   phantom_token_scope "scope_b";
   phantom_token_scope "scope_c";
}
```

## Sample Configuration

### Loading the Module

If the module is downloaded from GitHub or compiled as a shared library (the default) and not explicitly compiled into NGINX, it will need to be loaded using the [load_module](http://nginx.org/en/docs/ngx_core_module.html#load_module) directive. This needs to be done in the _main_ part of the NGINX configuration:

```nginx
load_module modules/ngx_curity_http_phantom_token_module.so;
```

The file can be an absolute or relative path. If it is not absolute, it should be relative to the NGINX root directory.

### NGINX Parameters for the Introspection Endpoint

You must also configure the following NGINX parameters for the introspection subrequest:

```nginx
location curity {
    internal;
    proxy_pass_request_headers off;
    proxy_set_header Accept "application/jwt";
    proxy_set_header Content-Type "application/x-www-form-urlencoded";
    proxy_set_header Authorization "Basic bXlfY2xpZW50X2lkOm15X2NsaWVudF9zZWNyZXQ=";
    proxy_pass "https://curity.example.com/oauth/v2/oauth-introspect";
}
```

| Introspection Setting | Description |
| --------------------- | ----------- |
| internal | Prevent the introspection endpoint being externally available. |
| proxy_pass_request_headers | Set to off to avoid using the main request's headers in the introspection subrequest. |
| Accept header | Configure a fixed value of `application/jwt`. |
| Content-Type header | Configure a fixed value of `application/x-www-form-urlencoded`. |
| Authorization header | Configure a basic credential with the introspection client ID and client secret. |

To get the basic credential, concatenate the client ID, a colon character and the client secret, then base64 encode them. The following command provides an example.

```bash
echo -n "my_client_id:my_client_secret" | base64
```

### Simple Configuration

The following is a simple configuration that might be used in demo or development environments where the NGINX reverse proxy is on the same host as the Curity Identity Server:

```nginx
server {
    location /api {
        phantom_token on;
        phantom_token_introspection_endpoint curity;
        proxy_pass https://example.com/api;
    }
    
    location curity {
        internal;
        proxy_pass_request_headers off;
        proxy_set_header Accept "application/jwt";
        proxy_set_header Content-Type "application/x-www-form-urlencoded";
        proxy_set_header Authorization "Basic bXlfY2xpZW50X2lkOm15X2NsaWVudF9zZWNyZXQ=";
        proxy_pass "https://curity.example.com/oauth/v2/oauth-introspect";
    }
}
```

### Complex Configuration

The following is a more complex configuration where the NGINX reverse proxy is on a separate host to the Curity Identity Server:

```nginx
server {
    server_name server1.example.com;n
    location /api {
        phantom_token on;
        phantom_token_introspection_endpoint curity;
        phantom_token_realm "myGoodAPI";
        phantom_token_scopes "scope_a scope_b scope_c";
        proxy_pass https://example.com/api;
    }
    
    location curity {
        internal;
        proxy_pass_request_headers off;
        proxy_set_header Accept "application/jwt";
        proxy_set_header Content-Type "application/x-www-form-urlencoded";
        proxy_set_header Authorization "Basic bXlfY2xpZW50X2lkOm15X2NsaWVudF9zZWNyZXQ=";
        proxy_pass "https://server2.example.com:8443/oauth/v2/oauth-introspect";
    }
}

server {
    listen 8443;
    server_name server2.example.com;
    location / {
        proxy_pass "https://curity.example.com";
    }
}
```
        
### More Advanced Configuration with Separate Servers and Caching

This module takes advantage of NGINX built-in _proxy_cache_ directive. In order to be able to cache the requests made to the introspection endpoint, except of the `proxy_cache_path` in http context and `proxy_cache` in location context, you have to add the following 3 directives in the location context of the introspection endpoint.

- `proxy_cache_methods POST;` POST requests are not cached by default.
- `proxy_cache_key $request_body;` The key of the cache is related to the _access_token_ sent in the original request. Different requests using the same _access_token_ reach the same cache.
- `proxy_ignore_headers Set-Cookie;` NGINX will not cache the response if `Set-Cookie` header is not ignored.

```nginx
http {
    proxy_cache_path /path/to/cache/cache levels=1:2 keys_zone=my_cache:10m max_size=10g
                     inactive=60m use_temp_path=off;
    server {
        server_name server1.example.com;
        location /api {
            phantom_token on;
            phantom_token_introspection_endpoint curity;
            phantom_token_scopes "scope_a scope_b scope_c";
            phantom_token_realm "myGoodAPI";
            proxy_pass https://example.com/api;
        }
        
        location curity {
            internal;            
            proxy_pass_request_headers off;
            proxy_set_header Accept "application/jwt";
            proxy_set_header Content-Type "application/x-www-form-urlencoded";
            proxy_set_header Authorization "Basic bXlfY2xpZW50X2lkOm15X2NsaWVudF9zZWNyZXQ=";

            proxy_cache_methods POST;
            proxy_cache my_cache;
            proxy_cache_key $request_body;
            proxy_ignore_headers Set-Cookie;

            proxy_pass "https://server2.example.com:8443/oauth/v2/oauth-introspect";
        }
    }
    
    server {
        listen 8443;
        server_name server2.example.com;
        location / {
            proxy_pass "https://curity.example.com";
        }
    }
}   
```

## Cacheless Configuration

It is recommended to cache the results of the call to the Curity Identity Server so that you avoid triggering an introspection request for every API request. If you wish to disable caching you should extend the default [proxy_buffer_size](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#directives) to ensure that the module can read large JWTs. Do so by updating the configuration of the introspection request as in the following example.

```nginx
http {
    server {
        server_name server1.example.com;
        location /api {
            phantom_token on;
            phantom_token_introspection_endpoint curity;
            phantom_token_scopes "scope_a scope_b scope_c";
            phantom_token_realm "myGoodAPI";
            proxy_pass https://example.com/api;
        }
        
        location curity {
            internal;
            proxy_pass_request_headers off;
            proxy_set_header Accept "application/jwt";
            proxy_set_header Content-Type "application/x-www-form-urlencoded";
            proxy_set_header Authorization "Basic bXlfY2xpZW50X2lkOm15X2NsaWVudF9zZWNyZXQ=";

            proxy_ignore_headers Set-Cookie;
            proxy_buffer_size 16k;
            proxy_buffers 4 16k;

            proxy_pass "https://server2.example.com:8443/oauth/v2/oauth-introspect";
        }
    }
    
    server {
        listen 8443;
        server_name server2.example.com;
        location / {
            proxy_pass "https://curity.example.com";
        }
    }
}   
```

## More Information

For more information about the Curity Identity Server, its capabilities, and how to use it to issue phantom tokens for microservices, visit [curity.io](https://curity.io/product/token-service/?=use-cases?tab=microservices). For background information on using the Curity Identity Server to secure API access, see our [API security resources](https://curity.io/resources/api-security).

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-phantom-token](https://github.com/curityio/nginx_phantom_token_module){target=_blank}.