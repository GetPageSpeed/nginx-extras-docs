---

title: "Encrypt and decrypt NGINX variable values"
description: "RPM package nginx-module-encrypted-session. NGINX module to encrypt and decrypt NGINX variable values. "

---

# *encrypted-session*: Encrypt and decrypt NGINX variable values


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
    dnf -y install nginx-module-encrypted-session
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-encrypted-session
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_encrypted_session_module.so;
```


This document describes nginx-module-encrypted-session [v0.9](https://github.com/openresty/encrypted-session-nginx-module/releases/tag/v0.09){target=_blank} 
released on Nov 18 2021.

<hr />

encrypted-session-nginx-module - encrypt and decrypt nginx variable values

installation instructions.

## Status

This module is production ready.

## Synopsis

```nginx
## key must be of 32 bytes long
encrypted_session_key "abcdefghijklmnopqrstuvwxyz123456";

## iv must not be longer than 16 bytes
## default: "deadbeefdeadbeef" (w/o quotes)
encrypted_session_iv "1234567812345678";

## default: 1d (1 day)
encrypted_session_expires 3600; # in sec

location /encrypt {
    set $raw 'text to encrypted'; # from the ngx_rewrite module
    set_encrypt_session $session $raw;
    set_encode_base32 $session; # from the ngx_set_misc module

    add_header Set-Cookie 'my_login=$session';  # from the ngx_headers module

    # your content handler goes here...
}

location /decrypt {
    set_decode_base32 $session $cookie_my_login; # from the ngx_set_misc module
    set_decrypt_session $raw $session;

    if ($raw = '') {
        # bad session
    }

    # your content handler goes here...
}
```

## Description

This module provides encryption and decryption support for
nginx variables based on AES-256 with Mac.

This module is usually used with the [ngx_set_misc module](http://github.com/agentzh/set-misc-nginx-module)
and the standard rewrite module's directives.

This module can be used to implement simple user login and ACL.

Usually, you just decrypt data in nginx level, and pass the unencrypted
data to your FastCGI/HTTP backend, as in

```nginx
location /blah {
    set_decrypt_session $raw_text $encrypted;

    # this directive is from the ngx_set_misc module
    set_escape_uri $escaped_raw_text $raw_text;

    fastcgi_param QUERY_STRING "uid=$uid";
    fastcgi_pass unix:/path/to/my/php/or/python/fastcgi.sock;
}
```

Lua web applications running directly on [ngx_lua](https://github.com/openresty/lua-nginx-module) can call
this module's directives directly from within Lua code:

```lua
local raw_text = ndk.set_var.set_decrypt_session(encrypted_text)
```


## Directives


## encrypted_session_key
**syntax:** *encrypted_session_key &lt;key&gt;*

**default:** *no*

**context:** *http, server, server if, location, location if*

Sets the key for the cipher (must be 32 bytes long). For example,

```nginx
encrypted_session_key "abcdefghijklmnopqrstuvwxyz123456";
```


## encrypted_session_iv
**syntax:** *encrypted_session_iv &lt;iv&gt;*

**default:** *encrypted_session_iv "deadbeefdeadbeef";*

**context:** *http, server, server if, location, location if*

Sets the initial vector used for the cipher (must be *no longer* than 16 bytes).

For example,

```nginx
encrypted_session_iv "12345678";
```


## encrypted_session_expires
**syntax:** *encrypted_session_expires &lt;time&gt;*

**default:** *encrypted_session_expires 1d;*

**context:** *http, server, server if, location, location if*

Sets expiration time difference (in seconds by default).

For example, consider the following configuration:

```nginx
encypted_session_expires 1d;
```

When your session is being generated, ngx_encrypted_session will plant
an expiration time (1 day in the future in this example) into the
encrypted session string, such that when the session is being decrypted
later, the server can pull the expiration time out of the session and
compare it with the server's current system time. No matter how you
transfer and store your session, like using cookies, or URI query arguments,
or whatever.

People may confuse this setting with the expiration date of HTTP
cookies. This directive simply controls when the session gets expired;
it knows nothing about HTTP cookies. Even if the end user intercepted
this session from cookie by himself and uses it later manually, the
server will still reject it when the expiration time gets passed.


## set_encrypt_session
**syntax:** *set_encrypt_session $target &lt;value&gt;*

**default:** *no*

**context:** *http, server, server if, location, location if*

Encrypts the string value specified by the `value` argument and saves the result into
the variable specified by `$target`.

For example,

```nginx
set_encrypt_session $res $value;
```

will encrypts the value in the variable $value into the target variable `$res`.

The `value` argument can also be an nginx string value, for example,

```nginx
set_encrypt_session $res "my value = $value";
```

The resulting data can later be decrypted via the [set_decrypt_session](#set_decrypt_session) directive.


## set_decrypt_session
**syntax:** *set_decrypt_session $target &lt;value&gt;*

**default:** *no*

**context:** *http, server, server if, location, location if*

Similar to [set_encrypt_session](#set_encrypt_session), but performs the inverse operation, that is,
to decrypt things.


## See Also
* [NDK](http://github.com/simpl-it/ngx_devel_kit)
* [ngx_set_misc module](http://github.com/agentzh/set-misc-nginx-module)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-encrypted-session](https://github.com/openresty/encrypted-session-nginx-module){target=_blank}.