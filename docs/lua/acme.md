---

title: "Automatic Let's Encrypt certificate serving and Lua implementation of ACMEv2 procotol"
description: "RPM package lua-resty-acme: Automatic Let's Encrypt certificate serving and Lua implementation of ACMEv2 procotol"

---
  
# *acme*: Automatic Let's Encrypt certificate serving and Lua implementation of ACMEv2 procotol


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-acme
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-acme
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-acme [v0.15.0](https://github.com/fffonion/lua-resty-acme/releases/tag/0.15.0){target=_blank} 
released on Aug 13 2024.
    
<hr />

Automatic Let's Encrypt certificate serving (RSA + ECC) and pure Lua implementation of the ACMEv2 protocol.

`http-01` and `tls-alpn-01` challenges are supported.

![Build Status](https://github.com/fffonion/lua-resty-acme/workflows/Tests/badge.svg) ![luarocks](https://img.shields.io/luarocks/v/fffonion/lua-resty-acme?color=%232c3e67) ![opm](https://img.shields.io/opm/v/fffonion/lua-resty-acme?color=%23599059)

[简体中文](https://yooooo.us/2019/lua-resty-acme)

## Description

This library consists of two parts:

- `resty.acme.autossl`: automatic lifecycle management of Let's Encrypt certificates
- `resty.acme.client`: Lua implementation of ACME v2 protocol

Install using opm:

```shell
opm install fffonion/lua-resty-acme
```

Alternatively, to install using luarocks:

```shell
luarocks install lua-resty-acme
## manually install a luafilesystem
luarocks install luafilesystem
```

Note you will need to manually install `luafilesystem` when using LuaRocks. This is made to maintain
backward compatibility.

This library uses [an FFI-based openssl backend](https://github.com/fffonion/lua-resty-openssl),
which currently supports OpenSSL `1.1.1`, `1.1.0` and `1.0.2` series.


## Status

Production.

## Synopsis

Create account private key and fallback certs:

```shell
## create account key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out /etc/openresty/account.key
## create fallback cert and key
openssl req -newkey rsa:2048 -nodes -keyout /etc/openresty/default.key -x509 -days 365 -out /etc/openresty/default.pem
```

Use the following example config:

```lua
events {}

http {
    resolver 8.8.8.8 ipv6=off;

    lua_shared_dict acme 16m;

    # required to verify Let's Encrypt API
    lua_ssl_trusted_certificate /etc/ssl/certs/ca-certificates.crt;
    lua_ssl_verify_depth 2;

    init_by_lua_block {
        require("resty.acme.autossl").init({
            -- setting the following to true
            -- implies that you read and accepted https://letsencrypt.org/repository/
            tos_accepted = true,
            -- uncomment following for first time setup
            -- staging = true,
            -- uncomment following to enable RSA + ECC double cert
            -- domain_key_types = { 'rsa', 'ecc' },
            -- uncomment following to enable tls-alpn-01 challenge
            -- enabled_challenge_handlers = { 'http-01', 'tls-alpn-01' },
            account_key_path = "/etc/openresty/account.key",
            account_email = "youemail@youdomain.com",
            domain_whitelist = { "example.com" },
        })
    }

    init_worker_by_lua_block {
        require("resty.acme.autossl").init_worker()
    }

    server {
        listen 80;
        listen 443 ssl;
        server_name example.com;

        # fallback certs, make sure to create them before hand
        ssl_certificate /etc/openresty/default.pem;
        ssl_certificate_key /etc/openresty/default.key;

        ssl_certificate_by_lua_block {
            require("resty.acme.autossl").ssl_certificate()
        }

        location /.well-known {
            content_by_lua_block {
                require("resty.acme.autossl").serve_http_challenge()
            }
        }
    }
}
```

When testing deployment, it's recommanded to uncomment the `staging = true` to allow an
end-to-end test of your environment. This can avoid configuration failure result into too
many requests that hits [rate limiting](https://letsencrypt.org/docs/rate-limits/) on Let's Encrypt API.

By default `autossl` only creates RSA certificates. To use ECC certificates or both, uncomment
`domain_key_types = { 'rsa', 'ecc' }`. Note that multiple certificate
chain is only supported by NGINX 1.11.0 or later.

A certificate will be *queued* to create after Nginx seen request with such SNI, which might
take tens of seconds to finish. During the meantime, requests with such SNI are responsed
with the fallback certificate.

Note that `domain_whitelist` or `domain_whitelist_callback` must be set to include your domain
that you wish to server autossl, to prevent potential abuse using fake SNI in SSL handshake.

`domain_whitelist` defines a table that includes all domains should be included and the CN to be
used to create cert for. Only a single `*` is allowed as a wildcard.

```lua
domain_whitelist = { "domain1.com", "domain2.com", "domain3.com", "*.domain4.com" },
```

## Wildcard certificates

To enable this library to create wildcard certificate, the following requirements must be met:

- The wildcard domain appear exactly as `*.somedomain.com` in `domain_whitelist`.
- `dns-01` challenge is enabled and a dns provider that has `domains` matching the domain is configured.

Otherwise a non-wildcard certificate will be created as fallback.

By default, the wildcard domain `*.example.com` will appear in Common Name. When `wildcard_domain_in_san` is set to `true` however, a cert with Common Name `example.com` and Subject Alternate Name `*.example.com` will be created. Note both `*.example.com` and `example.com` should appear in `dns_provider_accounts`.

## Advanced Usage

### Use a function to include domains

`domain_whitelist_callback` defines a function that accepts domain as parameter and return
boolean to indicate if it should be included.

To match a pattern in your domain name, for example **all** subdomains under `example.com`, use:

```lua
domain_whitelist_callback = function(domain, is_new_cert_needed)
    return ngx.re.match(domain, [[\.example\.com$]], "jo")
end
```

Furthermore, since checking domain whitelist is running in certificate phase.
It's possible to use cosocket API here. Do note that this will increase the SSL handshake
latency.

```lua
domain_whitelist_callback = function(domain, is_new_cert_needed)
    -- send HTTP request
    local http = require("resty.http")
    local res, err = httpc:request_uri("http://example.com")
    -- access the storage
    local acme = require("resty.acme.autossl")
    local value, err = acme.storage:get("key")
    -- get cert from resty LRU cache
    -- cached = { pkey, cert } or nil if cert is not in cache
    local cached, staled, flags = acme.get_cert_from_cache(domain, "rsa")
    -- do something to check the domain
    -- return is_domain_included
end}),
```

`domain_whitelist_callback` function is provided with a second argument,
which indicates whether the certificate is about to be served on incoming HTTP request (false) or new certificate is about to be requested (true). This allows to use cached values on hot path (serving requests) while fetching fresh data from storage for new certificates. One may also implement different logic, e.g. do extra checks before requesting new cert.

### Define failure cooloff period

In case of certificate request failure one may want to prevent ACME client to request another certificate immediatelly. By default, the cooloff period it is set to 300 seconds (5 minutes). It may be customized with `failure_cooloff` or with `failure_cooloff_callback` function, e.g. to implement exponential backoff.

```lua
    failure_cooloff_callback = function(domain, count)
      if count == 1 then
        return 600 -- 10 minutes
      elseif count == 2 then
        return 1800 -- 30 minutes
      elseif count == 3 then
        return 3600 -- 1 hour
      elseif count == 4 then
        return 43200 -- 12 hours
      elseif count == 5 then
        return 43200 -- 12 hours
      else
        return 86400 -- 24 hours
      end
    end
```

## tls-alpn-01 challenge

tls-alpn-01 challenge is currently supported on Openresty `1.15.8.x`, `1.17.8.x` and `1.19.3.x`.

<details>
  <summary>Click to expand sample config</summary>

```lua
events {}

http {
    resolver 8.8.8.8 ipv6=off;

    lua_shared_dict acme 16m;

    # required to verify Let's Encrypt API
    lua_ssl_trusted_certificate /etc/ssl/certs/ca-certificates.crt;
    lua_ssl_verify_depth 2;

    init_by_lua_block {
        require("resty.acme.autossl").init({
            -- setting the following to true
            -- implies that you read and accepted https://letsencrypt.org/repository/
            tos_accepted = true,
            -- uncomment following for first time setup
            -- staging = true,
            -- uncomment folloing to enable RSA + ECC double cert
            -- domain_key_types = { 'rsa', 'ecc' },
            -- uncomment following to enable tls-alpn-01 challenge
            enabled_challenge_handlers = { 'http-01', 'tls-alpn-01' },
            account_key_path = "/etc/openresty/account.key",
            account_email = "youemail@youdomain.com",
            domain_whitelist = { "example.com" },
            storage_adapter = "file",
        })
    }
    init_worker_by_lua_block {
        require("resty.acme.autossl").init_worker()
    }

    server {
        listen 80;
        listen unix:/tmp/nginx-default.sock ssl;
        # listen unix:/tmp/nginx-default.sock ssl proxy_protocol;
        server_name example.com;

        # set_real_ip_from unix:;
        # real_ip_header proxy_protocol;

        # fallback certs, make sure to create them before hand
        ssl_certificate /etc/openresty/default.pem;
        ssl_certificate_key /etc/openresty/default.key;

        ssl_certificate_by_lua_block {
            require("resty.acme.autossl").ssl_certificate()
        }

        location /.well-known {
            content_by_lua_block {
                require("resty.acme.autossl").serve_http_challenge()
            }
        }
    }
}

stream {
    init_worker_by_lua_block {
        require("resty.acme.autossl").init({
            -- setting the following to true
            -- implies that you read and accepted https://letsencrypt.org/repository/
            tos_accepted = true,
            -- uncomment following for first time setup
            -- staging = true,
            -- uncomment folloing to enable RSA + ECC double cert
            -- domain_key_types = { 'rsa', 'ecc' },
            -- uncomment following to enable tls-alpn-01 challenge
            enabled_challenge_handlers = { 'http-01', 'tls-alpn-01' },
            account_key_path = "/etc/openresty/account.key",
            account_email = "youemail@youdomain.com",
            domain_whitelist = { "example.com" },
            storage_adapter = "file"
        })
        require("resty.acme.autossl").init_worker()
    }

    map $ssl_preread_alpn_protocols $backend {
        ~\bacme-tls/1\b unix:/tmp/nginx-tls-alpn.sock;
        default unix:/tmp/nginx-default.sock;
    }

    server {
            listen 443;
            listen [::]:443;

            ssl_preread on;
            proxy_pass $backend;

            # proxy_protocol on;
    }

    server {
            listen unix:/tmp/nginx-tls-alpn.sock ssl;
            # listen nix:/tmp/nginx-tls-alpn.sock ssl proxy_protocol;
            ssl_certificate certs/default.pem;
            ssl_certificate_key certs/default.key;

            # requires --with-stream_realip_module
            # set_real_ip_from unix:;

            ssl_certificate_by_lua_block {
                    require("resty.acme.autossl").serve_tls_alpn_challenge()
            }

            content_by_lua_block {
                    ngx.exit(0)
            }
    }
}
```

</details>

In the above sample config, we set a http server and two stream server.

The very front stream server listens for 443 port and route to different upstream
based on client ALPN. The tls-alpn-01 responder listens on `unix:/tmp/nginx-tls-alpn.sock`.
All normal https traffic listens on `unix:/tmp/nginx-default.sock`.

```
                                                [stream server unix:/tmp/nginx-tls-alpn.sock ssl]
                                            Y /
[stream server 443] --- ALPN is acme-tls ?
                                            N \
                                                [http server unix:/tmp/nginx-default.sock ssl]
```

- The config passed to `require("resty.acme.autossl").init` in both subsystem should be
kept same as possible.
- `tls-alpn-01` challenge handler doesn't need any third party dependency.
- You can enable `http-01` and `tls-alpn-01` challenge handlers at the same time.
- `http` and `stream` subsystem doesn't share shm, thus considering use a storage other
than `shm`. If you must use `shm`, you will need to apply
[this patch](https://github.com/fffonion/lua-resty-shdict-server/tree/master/patches).

## dns-01 challenge

DNS-01 challenge is supported on lua-resty-acme > 0.13.0. Currently, following DNS providers are supported:

- `cloudflare`: Cloudflare
- `dynv6`: Dynv6
- `dnspod-intl`: Dnspod International (only Dnspod token is supported and use `id,token` in secret field)

To read to how to extend a new DNS provider to work with `dns-01` challenge, see [DNS provider](#dns-providers).

An example config to use `dns-01` challenge would be:

```lua
require("resty.acme.autossl").init({
  -- setting the following to true
  -- implies that you read and accepted https://letsencrypt.org/repository/
  tos_accepted = true,
  -- uncomment following for first time setup
  -- staging = true,
  -- uncomment following to enable RSA + ECC double cert
  -- domain_key_types = { 'rsa', 'ecc' },
  -- do not set `http-01` or `tls-alpn-01` if you only plan to use dns-01.
  enabled_challenge_handlers = { 'dns-01' },
  account_key_path = "/etc/openresty/account.key",
  account_email = "youemail@youdomain.com",
  domain_whitelist = { "example.com", "subdomain.anotherdomain.com" },

  dns_provider_accounts = {
    {
      name = "cloudflare_prod",
      provider = "cloudflare",
      secret = "apikey of cloudflare",
      domains = { "example.com" },
    },
    {
      name = "dynv6_staging",
      provider = "dynv6",
      secret = "apikey of dynv6",
      domains = { "*.anotherdomain.com" },
    },
  },
  -- uncomment following to create anotherdomain.com in CN and *.anotherdomain.com in SAN
  -- wildcard_domain_in_san = true,
})
```

By default, this library tries up to 5 minutes for DNS propagation. If the default TTL for dns provider is longer than that, user may want to tune up `challenge_start_delay` manually to wait longer.

## resty.acme.autossl

A config table can be passed to `resty.acme.autossl.init()`, the default values are:

```lua
default_config = {
  -- accept term of service https://letsencrypt.org/repository/
  tos_accepted = false,
  -- if using the let's encrypt staging API
  staging = false,
  -- the path to account private key in PEM format
  account_key_path = nil,
  -- the account email to register
  account_email = nil,
  -- number of certificate cache, per type
  cache_size = 100,
  domain_key_paths = {
    -- the global domain RSA private key
    rsa = nil,
    -- the global domain ECC private key
    ecc = nil,
  },
  -- the private key algorithm to use, can be one or both of
  -- 'rsa' and 'ecc'
  domain_key_types = { 'rsa' },
  -- restrict registering new cert only with domain defined in this table
  domain_whitelist = nil,
  -- restrict registering new cert only with domain checked by this function
  domain_whitelist_callback = nil,
  -- interval to wait before retrying after failed certificate request
  failure_cooloff = 300,
  -- function that returns interval to wait before retrying after failed certificate request
  failure_cooloff_callback = nil,
  -- the threshold to renew a cert before it expires, in seconds
  renew_threshold = 7 * 86400,
  -- interval to check cert renewal, in seconds
  renew_check_interval = 6 * 3600,
  -- the store certificates
  storage_adapter = "shm",
  -- the storage config passed to storage adapter
  storage_config = {
    shm_name = 'acme',
  },
  -- the challenge types enabled
  enabled_challenge_handlers = { 'http-01' },
  -- time to wait before signaling ACME server to validate in seconds
  challenge_start_delay = 0,
  -- if true, the request to nginx waits until the cert has been generated and it is used right away
  blocking = false,
  -- if true, the certificate for domain not in whitelist will be deleted from storage
  enabled_delete_not_whitelisted_domain = false,
  -- the dict of dns providers, each provider should have following struct:
  -- {
  --   name = "prod_account",
  --   provider = "provider_name", -- "cloudflare" or "dynv6"
  --   secret  = "the api key or token",
  --   domains = { "example.com", "*.example.com" }, -- the list of domains that can be used with this provider
  -- }
  dns_provider_accounts = {},
  -- if enabled, wildcard domains like *.example.com will be created as SAN and CN will be example.com
  wildcard_domain_in_san = false,
}
```

If `account_key_path` is not specified, a new account key will be created
**everytime** Nginx reloads configuration. Note this may trigger **New Account**
[rate limiting](https://letsencrypt.org/docs/rate-limits/) on Let's Encrypt API.

If `domain_key_paths` is not specified, a new private key will be generated
for each certificate (4096-bits RSA and 256-bits prime256v1 ECC). Note that
generating such key will block worker and will be especially noticable on VMs
where entropy is low.

Pass config table directly to ACME client as second parameter. The following example
demonstrates how to use a CA provider other than Let's Encrypt and also set
the preferred chain.

```lua
resty.acme.autossl.init({
    tos_accepted = true,
    account_email = "example@example.com",
  }, {
    api_uri = "https://acme.otherca.com/directory",
    preferred_chain = "OtherCA PKI Root CA",
  }
)
```

See also [Storage Adapters](#storage-adapters) below.

When using distributed storage types, it's useful to bump up `challenge_start_delay` to allow
changes in storage to propogate around. When `challenge_start_delay` is set to 0, no wait
will be performed before start validating challenges.

### autossl.get_certkey

**syntax**: *certkey, err = autossl.get_certkey(domain, type?)*

Return the PEM-encoded certificate and private key for `domain` from storage. Optionally
accepts a `type` parameter which can be `"rsa"` or `"ecc"`; if omitted, `type` will default
to `"rsa"`.

## resty.acme.client

### client.new

**syntax**: *c, err = client.new(config)*

Create a ACMEv2 client.

Default values for `config` are:

```lua
default_config = {
  -- the ACME v2 API endpoint to use
  api_uri = "https://acme-v02.api.letsencrypt.org/directory",
  -- the account email to register
  account_email = nil,
  -- the account key in PEM format text
  account_key = nil,
  -- the account kid (as an URL)
  account_kid = nil,
  -- external account binding key id
  eab_kid = nil,
  -- external account binding hmac key, base64url encoded
  eab_hmac_key = nil,
  -- external account registering handler
  eab_handler = nil,
  -- storage for challenge
  storage_adapter = "shm",
  -- the storage config passed to storage adapter
  storage_config = {
    shm_name = "acme"
  },
  -- the challenge types enabled, selection of `http-01` and `tls-alpn-01`
  enabled_challenge_handlers = {"http-01"},
  -- select preferred root CA issuer's Common Name if appliable
  preferred_chain = nil,
  -- callback function that allows to wait before signaling ACME server to validate
  challenge_start_callback = nil,
  -- the dict of dns providers, each provider should have following struct:
  dns_provider_accounts = {},
}
```

If `account_kid` is omitted, user must call `client:new_account()` to register a
new account. Note that when using the same `account_key`, `client:new_account()`
will return the same `kid` that is previosuly registered.

If CA requires [External Account Binding](#external-account-binding), user can set
`eab_kid` and `eab_hmac_key` to load an existing account, or set `account_email` and
`eab_handler` to register a new account. `eab_hmac_key` must be base64 url encoded.
In later case, user must call `client:new_account()` to register a new account.
`eab_handler` must be an function that accepts account_email as parameter and
returns `eab_kid`, `eab_hmac_key` and error if any.

```lua
eab_handler = function(account_email)
  -- do something to register an account with account_email
  -- if err then
  --  return nil, nil, err
  -- end
  return eab_kid, eab_hmac_key
end
```

The following CA provider's EAB handler is supported by lua-resty-acme and user doesn't
need to implement their own `eab_handler`:

- [ZeroSSL](https://zerossl.com/)

`preferred_chain` is used to select a chain with matching Common Name in its root CA. For example,
user can use use `"ISRG Root X1"` to force use the new default chain in Let's Encrypt. When no
value is configured or the configured name is not found in any chain, the default chain will be
used.

`challenge_start_callback` is a callback function to allow the client to wait before signalling
ACME server to start validate challenge. It's useful in a distributed setup where challenges take
time to propogate. `challenge_start_callback` accepts `challenge_type` and `challenge_token`.
The client calls this function every second until it returns `true` indicating challenge should start;
if this `challenge_start_callback` is not set, no wait will be performed.

```lua
challenge_start_callback = function(challenge_type, challenge_token)
  -- do something here
  -- if we are good
  return true
end
```

See also [Storage Adapters](#storage-adapters) below.

### client:init

**syntax**: *err = client:init()*

Initialize the client, requires availability of cosocket API. This function will
login or register an account.

### client:order_certificate

**syntax**: *err = client:order_certificate(domain,...)*

Create a certificate with one or more domains. Note that wildcard domains are not
supported as it can only be verified by [dns-01](https://letsencrypt.org/docs/challenge-types/) challenge.

### client:serve_http_challenge

**syntax**: *client:serve_http_challenge()*

Serve [http-01](https://letsencrypt.org/docs/challenge-types/) challenge. A common use case will be to
put this as a content_by_* block for `/.well-known` path.

### client:serve_tls_alpn_challenge

**syntax**: *client:serve_tls_alpn_challenge()*

Serve [tls-alpn-01](https://letsencrypt.org/docs/challenge-types/) challenge. See
[this section](https://github.com/fffonion/lua-resty-acme#tls-alpn-01-challenge) on how to use this handler.


## Storage Adapters

Storage adapters are used in `autossl` or acme `client` to storage temporary or
persistent data. Depending on the deployment environment, there're currently
five storage adapters available to select from. To implement a custom storage
adapter, please refer to
[this doc](https://github.com/fffonion/lua-resty-acme/blob/master/lib/resty/acme/storage/README.md).

### file

Filesystem based storage. Sample configuration:

```lua
storage_config = {
    dir = '/etc/openresty/storage',
}
```
If `dir` is omitted, the OS temporary directory will be used.

`luafilesystem` or `luafilesystem-ffi` is needed when using the `file` storage for renewal.

### shm

Lua shared dict based storage. Note this storage is volatile between Nginx restarts
(not reloads). Sample configuration:

```lua
storage_config = {
    shm_name = 'dict_name',
}
```

### redis

Redis based storage. The default config is:

```lua
storage_config = {
    host = '127.0.0.1',
    port = 6379,
    database = 0,
    -- Redis authentication key
    auth = nil,
    ssl = false,
    ssl_verify = false,
    ssl_server_name = nil,
    -- namespace as a prefix of key
    namespace = "",
}
```

Redis >= 2.6.0 is required as this storage requires [PEXPIRE](https://redis.io/commands/pexpire).

### vault

Hashicorp [Vault](https://www.vaultproject.io/) based storage.
Only [KV V2](https://www.vaultproject.io/api/secret/kv/kv-v2.html) backend is supported.
The default config is:


```lua
storage_config = {
    host = '127.0.0.1',
    port = 8200,
    -- secrets kv prefix path
    kv_path = "acme",
    -- timeout in ms
    timeout = 2000,
    -- use HTTPS
    https = false,
    -- turn on tls verification
    tls_verify = true
    -- SNI used in request, default to host if omitted
    tls_server_name = nil,
    -- Auth Method, default to token, can be "token" or "kubernetes"
    auth_method = "token"
    -- Vault token
    token = nil,
    -- Vault's authentication path to use
    auth_path =  "kubernetes",
    -- The role to try and assign
    auth_role = nil,
    -- The path to the JWT
    jwt_path = "/var/run/secrets/kubernetes.io/serviceaccount/token",
    -- Vault namespace
    namespace = nil,
}
```

#### Support for different auth method

- Token: This is the default and allows to pass a literal "token" in the configuration
- Kubernetes: Via this method, one can utilize vault's built-in auth method for kubernetes
  What this basically this is take the service account token and validates it has been signed by Kubernetes CA.
  The major benefit here, is that config files don't expose your token anymore.

  The following configurations apply here:
  ```lua
    -- Vault's authentication path to use
    auth_path =  "kubernetes",
    -- The role to try and assign
    auth_role = nil,
    -- The path to the JWT
    jwt_path = "/var/run/secrets/kubernetes.io/serviceaccount/token",
   ```

### consul

Hashicorp [Consul](https://www.consul.io/) based storage. The default config is:


```lua
storage_config = {
    host = '127.0.0.1',
    port = 8500,
    -- kv prefix path
    kv_path = "acme",
    -- Consul ACL token
    token = nil,
    -- timeout in ms
    timeout = 2000,
}
```

### etcd

[etcd](https://etcd.io) based storage. Right now only `v3` protocol is supported, and etcd server
version should be >= v3.4.0.
The default config is:

```lua
storage_config = {
    http_host = 'http://127.0.0.1:4001',
    key_prefix = '',
    timeout = 60,
    ssl_verify = false,
}
```

Etcd storage requires [lua-resty-etcd](https://github.com/api7/lua-resty-etcd) library to installed.
It can be manually installed with `opm install api7/lua-resty-etcd` or `luarocks install lua-resty-etcd`.


## DNS providers

TO create a custom DNS provider, follow these steps:

- Create a file like `route53.lua` under `lib/resty/acme/dns_provider`
- Implement following function signature

```lua
function _M.new(token)
  -- ... 
  return self
end

function _M:post_txt_record(fqdn, content)
  return ok, err
end

function _M:delete_txt_record(fqdn)
  return ok, err
end
```

Where `token` is the apikey, `fqdn` is the DNS record name to set record, and `content` is the value of the record.


## Testing
Setup e2e test environment by running `bash t/fixtures/prepare_env.sh`.

Then run `cpanm install Test::Nginx::Socket` and then `prove -r t`.


## See Also
* [Automatic Certificate Management Environment (ACME)](https://tools.ietf.org/html/rfc8555)
* [haproxytech/haproxy-lua-acme](https://github.com/haproxytech/haproxy-lua-acme) The ACME Lua implementation used in HAProxy.
* [GUI/lua-resty-auto-ssl](https://github.com/GUI/lua-resty-auto-ssl)
* [lua-resty-openssl](https://github.com/fffonion/lua-resty-openssl)
* [Let's Encrypt API rate limits](https://letsencrypt.org/docs/rate-limits/)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-acme](https://github.com/fffonion/lua-resty-acme){target=_blank}.