---

title: "FFI-based OpenSSL binding for nginx-module-lua"
description: "RPM package lua-resty-openssl: FFI-based OpenSSL binding for nginx-module-lua"

---
  
# *openssl*: FFI-based OpenSSL binding for nginx-module-lua


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-openssl
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-openssl
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-openssl [v1.6.1](https://github.com/fffonion/lua-resty-openssl/releases/tag/1.6.1){target=_blank} 
released on Apr 16 2025.
    
<hr />

FFI-based OpenSSL binding for LuaJIT, supporting OpenSSL 3.x, 1.1 series.

OpenSSL 1.1.0, 1.0.2 and BoringSSL support has been dropped, but are still available at the [0.x branch](https://github.com/fffonion/lua-resty-openssl/tree/0.x).

![Build Status](https://github.com/fffonion/lua-resty-openssl/workflows/Tests/badge.svg) ![luarocks](https://img.shields.io/luarocks/v/fffonion/lua-resty-openssl?color=%232c3e67) ![opm](https://img.shields.io/opm/v/fffonion/lua-resty-openssl?color=%23599059)


## Description

`lua-resty-openssl` is a FFI-based OpenSSL binding library, currently
supports OpenSSL `3.x` and `1.1.1` series.

## Status

Production.

## Synopsis

This library is greatly inspired by [luaossl](https://github.com/wahern/luaossl), while uses the
naming conversion closer to original OpenSSL API.
For example, a function called `X509_set_pubkey` in OpenSSL C API will expect to exist
as `resty.openssl.x509:set_pubkey`.
*CamelCase*s are replaced to *underscore_case*s, for exmaple `X509_set_serialNumber` becomes
`resty.openssl.x509:set_serial_number`. Another difference than `luaossl` is that errors are never thrown
using `error()` but instead return as last parameter.

Each Lua table returned by `new()` contains a cdata object `ctx`. User are not supposed to manully setting
`ffi.gc` or calling corresponding destructor of the `ctx` struct (like `*_free` functions).

## resty.openssl

This meta module provides a version sanity check against linked OpenSSL library.

### openssl.load_library

**syntax**: *name, err = openssl.load_library()*

Try to load OpenSSL shared libraries. This function tries couple of known patterns
the library could be named and return the name of `crypto` library if it's being
successfully loaded and error if any.

When running inside `resty` CLI or OpenResty with SSL enabled, calling this function
is not necessary.

### openssl.load_modules

**syntax**: *openssl.load_modules()*

Load all available sub modules into current module:

```lua
  bn = require("resty.openssl.bn"),
  cipher = require("resty.openssl.cipher"),
  digest = require("resty.openssl.digest"),
  hmac = require("resty.openssl.hmac"),
  kdf = require("resty.openssl.kdf"),
  pkey = require("resty.openssl.pkey"),
  objects = require("resty.openssl.objects"),
  rand = require("resty.openssl.rand"),
  version = require("resty.openssl.version"),
  x509 = require("resty.openssl.x509"),
  altname = require("resty.openssl.x509.altname"),
  chain = require("resty.openssl.x509.chain"),
  csr = require("resty.openssl.x509.csr"),
  crl = require("resty.openssl.x509.crl"),
  extension = require("resty.openssl.x509.extension"),
  extensions = require("resty.openssl.x509.extensions"),
  name = require("resty.openssl.x509.name"),
  store = require("resty.openssl.x509.store"),
  ssl = require("resty.openssl.ssl"),
  ssl_ctx = require("resty.openssl.ssl_ctx"),
```

Starting OpenSSL 3.0, [`provider`](#restyopensslprovider) and [`mac`](#restyopensslmac)
[`ctx`](#restyopensslctx)
is also available.

### openssl.luaossl_compat

**syntax**: *openssl.luaossl_compat()*

Provides `luaossl` flavored API which uses *camelCase* naming; user can expect drop in replacement.

For example, `pkey:get_parameters` is mapped to `pkey:getParameters`.

Note that not all `luaossl` API has been implemented, please check readme for source of truth.

### openssl.get_fips_mode

**syntax**: *enabled = openssl.get_fips_mode()*

Returns a boolean indicating if FIPS mode is enabled.

### openssl.set_fips_mode

**syntax**: *ok, err = openssl.set_fips_mode(enabled)*

Toggle FIPS mode on or off.

lua-resty-openssl supports following modes:

**OpenSSL 1.0.2 series with fips 2.0 module**

Compile the module per [security policy](https://www.openssl.org/docs/fips/SecurityPolicy-2.0.2.pdf),

**OpenSSL 3.0.0 fips provider**

Refer to https://wiki.openssl.org/index.php/OpenSSL_3.0 Section 7
Compile the provider per guide, install the fipsmodule.cnf that
matches hash of FIPS provider fips.so.

On OpenSSL 3.0 or later, this function also turns on and off default
properties for EVP functions. When turned on, all applications using
EVP_* API will be redirected to FIPS-compliant implementations and
have no access to non-FIPS-compliant algorithms.

Calling this function is equivalent of loading `fips` provider and
call [openssl.set_default_properties("fips=yes")](#opensslset_default_properties).

If fips provider is loaded but default properties are not set, use following
to explictly fetch FIPS implementation.
```lua
local provider = require "resty.openssl.provider"
assert(provider.load("fips"))
local cipher = require "resty.openssl.cipher"
local c = assert(cipher.new("aes256"))
print(c:get_provider_name()) -- prints "default"
local c = assert(cipher.new("aes256", "fips=yes"))
print(c:get_provider_name()) -- prints "fips"
```

### openssl.get_fips_version_text

**syntax**: *text, err = openssl.get_fips_version_text()*

Returns the version text of the FIPS module, only available on OpenSSL 3.x.

### openssl.set_default_properties

**syntax**: *ok, err = openssl.set_default_properties(props)*

Sets the default properties for all future EVP algorithm fetches, implicit as well as explicit. See "ALGORITHM FETCHING" in crypto(7) for information about implicit and explicit fetching.

### openssl.list_cipher_algorithms

**syntax**: *ret = openssl.list_cipher_algorithms(hide_provider?)*

Return available cipher algorithms in an array. Set `hide_provider` to `true` to
hide provider name from the result.

### openssl.list_digest_algorithms

**syntax**: *ret = openssl.list_digest_algorithms(hide_provider?)*

Return available digest algorithms in an array. Set `hide_provider` to `true` to
hide provider name from the result.

### openssl.list_mac_algorithms

**syntax**: *ret = openssl.list_mac_algorithms(hide_provider?)*

Return available MAC algorithms in an array. Set `hide_provider` to `true` to
hide provider name from the result.

### openssl.list_kdf_algorithms

**syntax**: *ret = openssl.list_kdf_algorithms(hide_provider?)*

Return available KDF algorithms in an array. Set `hide_provider` to `true` to
hide provider name from the result.

### openssl.list_ssl_ciphers

**syntax**: *cipher_string, err = openssl.list_ssl_ciphers(cipher_list?, ciphersuites?, protocol?)*

Return default SSL ciphers as a string. `cipher_list` (prior TLSv1.3) and
`ciphersuites` (TLSv1.3) can be used to expand the cipher settings matches
`protocol`.

```lua
openssl.list_ssl_ciphers()
openssl.list_ssl_ciphers("ECDHE-ECDSA-AES128-SHA")
openssl.list_ssl_ciphers("ECDHE-ECDSA-AES128-SHA", nil, "TLSv1.2")
openssl.list_ssl_ciphers("ECDHE-ECDSA-AES128-SHA", "TLS_CHACHA20_POLY1305_SHA256", "TLSv1.3")
```

## resty.openssl.ctx

A module to provide OSSL_LIB_CTX context switches.

  OSSL_LIB_CTX is an internal OpenSSL library context type. Applications may allocate their own, but may also use NULL to use a default context with functions that take an OSSL_LIB_CTX argument.

See [OSSL_LIB_CTX.3](#https://www.openssl.org/docs/manmaster/man3/OSSL_LIB_CTX.html) for deeper
reading.

The context is currently effective following modules:

- [cipher](#restyopensslcipher)
- [digest](#restyopenssldigest)
- [kdf](#restyopensslkdf)
- [mac](#restyopensslmac)
- [pkcs12.encode](#pkcs12encode)
- [pkey](#restyopensslpkey)
- [provider](#restyopensslprovider)
- [rand](#restyopensslrand)
- [x509](#restyopensslx509), [x509.csr](#restyopensslx509csr), [x509.crl](#restyopensslx509crl) and some [x509.store](#restyopensslx509store) functions

This module is only available on OpenSSL 3.0 or later.
 
### ctx.new

**syntax**: *ok, err = ctx.new(request_context_only?, conf_file?)*

Create a new context and use as default context for this module. When
`request_context_only` is set to true, the context is only used inside current
request's context. `conf_file` can optionally specify an OpenSSL conf file
to create the context.

The created context is automatically freed with its given lifecycle.

```lua
-- initialize a AES cipher instance from given provider implementation only
-- for current request, without interfering other part of code
-- or future requests from using the same algorithm.
assert(require("resty.openssl.ctx").new(true))
local p = assert(require("resty.openssl.provider").load("myprovider"))
local c = require("resty.openssl.cipher").new("aes256")
print(c:encrypt(string.rep("0", 32), string.rep("0", 16), "🦢"))
-- don't need to release provider and ctx, they are GC'ed automatically
```

### ctx.free

**syntax**: *ctx.free(request_context_only?)*

Free the context that was previously created by [ctx.new](#ctxnew).

## resty.openssl.err

A module to provide error messages.

### err.format_error

**syntax**: *msg = err.format_error(ctx_msg?, return_code?, all_errors?)*

**syntax**: *msg = err.format_all_errors(ctx_msg?, return_code?)*

Return the latest error message from the last error code. Errors are formatted as:

    [ctx_msg]: code: [return_code]: error:[error code]:[library name]:[func name]:[reason string]:[file name]:[line number]:

On OpenSSL prior to 3.x, errors are formatted as:

    [ctx_msg]: code: [return_code]: [file name]:[line number]:error:[error code]:[library name]:[func name]:[reason string]:


If `all_errors` is set to `true`, all errors no just the latest one will be returned in a single string. All errors thrown
by this library internally only thrown the latest error.

For example:

```lua
local f = io.open("t/fixtures/ec_key_encrypted.pem"):read("*a")
local privkey, err = require("resty.openssl.pkey").new(f, {
    format = "PEM",
    type = "pr",
    passphrase = "wrongpasswrod",
})
ngx.say(err)
-- pkey.new:load_key: error:4800065:PEM routines:PEM_do_header:bad decrypt:crypto/pem/pem_lib.c:467:
```

### err.get_last_error_code

**syntax**: *code = err.get_last_error_code()*

Return the last error code.

### err.get_lib_error_string

**syntax**: *lib_error_message = err.get_lib_error_string(code?)*

Return the library name of the last error code as string. If `code` is set, return the library name
corresponding to provided error code instead.

### err.get_reason_error_string

**syntax**: *reason_error_message = err.get_reason_error_string(code?)*

Return the reason of the last error code as string. If `code` is set, return the reason
corresponding to provided error code instead.

## resty.openssl.version

A module to provide version info.

## resty.openssl.provider

Module to interact with providers. This module only work on OpenSSL >= 3.0.0.

### provider.load

**syntax**: *pro, err = provider.load(name, try?)*

Load provider with `name`. If `try` is set to true, OpenSSL will not disable the
fall-back providers if the provider cannot be loaded and initialized. If the provider
loads successfully, however, the fall-back providers are disabled.

By default this functions loads provider into the default context, meaning it will affect
other applications in the same process using the default context as well. If such behaviour
is not desired, consider using [ctx](#restyopensslctx) to load
provider only to limited scope.

### provider.istype

**syntax**: *ok = pkey.provider(table)*

Returns `true` if table is an instance of `provider`. Returns `false` otherwise.

### provider.is_available

**syntax**: *ok, err = provider.is_available(name)*

Checks if a named provider is available for use.

### provider.set_default_search_path

**syntax**: *ok, err = provider.set_default_search_path(name)*

Specifies the default search path that is to be used for looking for providers.

### provider:unload

**syntax**: *ok, err = pro:unload(name)*

Unload a provider that is previously loaded by `provider.load`.

### provider:self_test

**syntax**: *ok, err = pro:self_test(name)*

Runs a provider's self tests on demand. If the self tests fail then the provider
will fail to provide any further services and algorithms.

### provider:get_params

**syntax**: *ok, err = pro:get_params(key1, key2?...)*

Returns one or more provider parameter values.

```lua
local pro = require "resty.openssl.provider"

local p = pro.load("default")

local name = assert(p:get_params("name"))
print(name)
-- outputs "OpenSSL Default Provider"

local result = assert(p:get_params("name", "version", "buildinfo", "status"))
print(require("cjson").encode(result))
-- outputs '{"buildinfo":"3.0.0-alpha7","name":"OpenSSL Default Provider","status":1,"version":"3.0.0"}'
```

## resty.openssl.pkey

Module to interact with private keys and public keys (EVP_PKEY).

Each key type may only support part of operations:

Key Type | Load existing key | Key generation | Encrypt/Decrypt | Sign/Verify | Key Exchange |
---------|----------|----------------|-----------------|-------------|---------- |
RSA| Y | Y | Y | Y | |
DH | Y | Y | | | Y |
EC | Y | Y | | Y (ECDSA) | Y (ECDH) |
Ed25519 | Y | Y | | Y (PureEdDSA) | |
X25519 | Y | Y | | | Y (ECDH) |
Ed448 | Y | Y | | Y (PureEdDSA) | |
X448 | Y | Y | | | Y (ECDH) |

Direct support of encryption and decryption for EC and ECX does not exist, but
processes like ECIES is possible with [pkey:derive](#pkeyderive),
[kdf](#restyopensslkdf) and [cipher](#restyopensslcipher)

### pkey.new

#### Load existing key

**syntax**: *pk, err = pkey.new(string, opts?)*

Supports loading a private or public key in PEM, DER or JWK format passed as first argument `string`.

The second parameter `opts` accepts an optional table to constraint the behaviour of key loading.

- `opts.format`: set explictly to `"PEM"`, `"DER"`, `"JWK"` to load specific format or set to `"*"` for auto detect
- `opts.type`: set explictly to `"pr"` for privatekey, `"pu"` for public key; set to `"*"` for auto detect

When loading a PEM encoded RSA key, it can either be a PKCS#8 encoded
`SubjectPublicKeyInfo`/`PrivateKeyInfo` or a PKCS#1 encoded `RSAPublicKey`/`RSAPrivateKey`.

When loading a encrypted PEM encoded key, the `passphrase` to decrypt it can either be set
in `opts.passphrase` or `opts.passphrase_cb`:

```lua
pkey.new(pem_or_der_text, {
  format = "*", -- choice of "PEM", "DER", "JWK" or "*" for auto detect
  type = "*", -- choice of "pr" for privatekey, "pu" for public key and "*" for auto detect
  passphrase = "secret password", -- the PEM encryption passphrase
  passphrase_cb = function()
    return "secret password"
  end, -- the PEM encryption passphrase callback function
}

```

When loading JWK, there are couple of caveats:
- Make sure the encoded JSON text is passed in, it must have been base64 decoded.
- When using OpenSSL 1.1.1 or lua-resty-openssl earlier than 1.6.0, constraint `type`
on JWK key is only supported on OpenSSL 3.x and lua-resty-openssl 1.6.0.
Otherwise the parameters in provided JSON will decide if a private or public key is loaded, 
specifying `type` will result in an error; also public key part for `OKP` keys (the `x` parameter)
is not honored and derived from private key part (the `d` parameter) if it's specified.
- Only key type of `RSA`, `P-256`, `P-384` and `P-512` `EC`,
`Ed25519`, `X25519`, `Ed448` and `X448` `OKP` keys are supported.
- Signatures and verification must use `ecdsa_use_raw` option to work with JWS standards
for EC keys. See [pkey:sign](#pkeysign) and [pkey.verify](#pkeyverify) for detail.
- When running outside of OpenResty, needs to install a JSON library (`cjson` or `dkjson`)
and `basexx`.

#### Key generation

**syntax**: *pk, err = pkey.new(config?)*

Generate a new public key or private key.

To generate RSA key, `config` table can have `bits` and `exp` field to control key generation.
When `config` is emitted, this function generates a 2048 bit RSA key with `exponent` of 65537,
which is equivalent to:
  
```lua
local key, err = pkey.new({
  type = 'RSA',
  bits = 2048,
  exp = 65537
})
```

To generate EC or DH key, please refer to [pkey.paramgen](#pkeyparamgen) for possible values of
`config` table. For example:

```lua
local key, err = pkey.new({
  type = 'EC',
  curve = 'prime256v1',
})
```

It's also possible to pass a PEM-encoded EC or DH parameters to `config.param` for key generation:

```lua
local dhparam = pkey.paramgen({
  type = 'DH',
  group = 'dh_1024_160'
})
-- OR
-- local dhparam = io.read("dhparams.pem"):read("*a")

local key, err = pkey.new({
  type = 'DH',
  param = dhparam,
}) 
```

It's also possible to pass raw pkeyopt control strings in `config` table as used in the `genpkey` CLI program.
See [openssl-genpkey(1)](https://www.openssl.org/docs/man3.0/man1/openssl-genpkey.html) for a list of options.

For example:

```lua
pkey.new({
  type = 'RSA',
  bits = 2048,
  exp = 65537,
})
-- is same as
pkey.new({
  type = 'RSA',
  exp = 65537,
  "rsa_keygen_bits:4096",
})

```

#### Key composition

**syntax**: *pk, err = pkey.new(config?)*

Compose a public or private key using existing parameters. To see
list of parameters for each key, refer to [pkey:set_parameters](#pkeyset_parameters).

Only `type` and `params` should exist in `config` table, all other keys will be ignored.

```lua
local private_bn = require "resty.openssl.bn".new("7F48282CCA4C1A65D589C06DBE9C42AE50FBFFDF3A18CBB48498E1DE47F11BE1A3486CD8FA950D68F111970F922279D8", 16)
local p_384, err = assert(require("resty.openssl.pkey").new({
    type = "EC",
    params = {
        private = private_bn,
        group = "secp384r1",
    }
}))
```

### pkey.istype

**syntax**: *ok = pkey.istype(table)*

Returns `true` if table is an instance of `pkey`. Returns `false` otherwise.

### pkey.paramgen

**syntax**: *pem_txt, err = pk.paramgen(config)*

Generate parameters for EC or DH key and output as PEM-encoded text.

For EC key:

 Parameter | Description
-----------|-------------
type | `"EC"`
curve | EC curves. If omitted, default to `"prime192v1"`. To see list of supported EC curves, use `openssl ecparam -list_curves`.

For DH key:
  
 Parameter | Description
-----------|-------------
type | `"DH"`
bits | Generate a new DH parameter with `bits` long prime. If omitted, default to `2048`. Starting OpenSSL 3.0, only bits equal to 2048 is allowed.
group | Use predefined groups instead of generating new one. `bit` will be ignored if `group` is set.

Possible values for `group` are:
- [RFC7919](https://tools.ietf.org/html/rfc7919#appendix-A.1) `"ffdhe2048"`, `"ffdhe3072"`,
`"ffdhe4096"`, `"ffdhe6144"`, `"ffdhe8192"`
- [RFC5114](https://tools.ietf.org/html/rfc5114#section-2) `"dh_1024_160"`, `"dh_2048_224"`, `"dh_2048_256"`
- [RFC3526](https://tools.ietf.org/html/rfc3526#page-3) `"modp_1536"`, `"modp_2048"`,
`"modp_3072"`, `"modp_4096"`, `"modp_6144"`, `"modp_8192"`
  
```lua
local pem, err = pkey.paramgen({
  type = 'EC',
  curve = 'prime192v1',
})

local pem, err = pkey.paramgen({
  type = 'DH',
  group = 'ffdhe4096',
})
```

It's also possible to pass raw pkeyopt control strings in `config` table as used in the `genpkey` CLI program.
See [openssl-genpkey(1)](https://www.openssl.org/docs/man3.0/man1/openssl-genpkey.html) for a list of options.

### pkey:get_provider_name

**syntax**: *name = pkey:get_provider_name()*

Returns the provider name of `pkey`.

This function is available since OpenSSL 3.0.

## pkey:gettable_params, pkey:settable_params, pkey:get_param, pkey:set_params

Query settable or gettable params and set or get params.
See [Generic EVP parameter getter/setter](#generic-evp-parameter-gettersetter).

### pkey:get_parameters

**syntax**: *parameters, err = pk:get_parameters()*

Returns a table containing the `parameters` of pkey instance.

### pkey:set_parameters

**syntax**: *ok, err = pk:set_parameters(params)*

Set the parameters of the pkey from a table `params`.
If the parameter is not set in the `params` table,
it remains untouched in the pkey instance.

```lua
local pk, err = require("resty.openssl.pkey").new()
local parameters, err = pk:get_parameters()
local e = parameters.e
ngx.say(e:to_number())
-- outputs 65537

local ok, err = pk:set_parameters({
  e = require("resty.openssl.bn").from_hex("100001")
})

local ok, err = pk:set_parameters(parameters)
```

Parameters for RSA key:

 Parameter | Description | Type
-----------|-------------|------
n | modulus common to both public and private key | [bn](#restyopensslbn)
e | public exponent | [bn](#restyopensslbn)
d | private exponent | [bn](#restyopensslbn)
p | first factor of **n** | [bn](#restyopensslbn)
q | second factor of **n** | [bn](#restyopensslbn)
dmp1 | `d mod (p - 1)`, exponent1 | [bn](#restyopensslbn)
dmq1 | `d mod (q - 1)`, exponent2 | [bn](#restyopensslbn)
iqmp | `(InverseQ)(q) = 1 mod p`, coefficient | [bn](#restyopensslbn)

Parameters for EC key:

 Parameter | Description | Type
-----------|-------------|-----
private | private key | [bn](#restyopensslbn)
public | public key | [bn](#restyopensslbn)
x | x coordinate of the public key| [bn](#restyopensslbn)
y | y coordinate of the public key| [bn](#restyopensslbn)
group | the named curve group | [NID] as a number, when passed in as `set_parameters()`, it's also possible to use the text representation. This is different from `luaossl` where a `EC_GROUP` instance is returned.

It's not possible to set `x`, `y` with `public` at same time as `x` and `y` is basically another representation
of `public`. Also currently it's only possible to set `x` and `y` at same time.

Parameters for DH key:

 Parameter | Description | Type
-----------|-------------|-----
private | private key | [bn](#restyopensslbn)
public | public key | [bn](#restyopensslbn)
p | prime modulus | [bn](#restyopensslbn)
q | reference position | [bn](#restyopensslbn)
g | base generator | [bn](#restyopensslbn)


Parameters for Curve25519 and Curve448 keys:

 Parameter | Description | Type
-----------|-------------|-----
private | raw private key represented as bytes | string
public | raw public key represented as bytes | string

### pkey:is_private

**syntax**: *ok = pk:is_private()*

Checks whether `pk` is a private key. Returns true if it's a private key, returns false if
it's a public key.

### pkey:get_key_type

**syntax**: *obj, err = pk:get_key_type(nid_only?)*

Returns a ASN1_OBJECT of key type of the private key as a table.

Starting from lua-resty-openssl 1.6.0, an optional argument `nid_only` can be set to `true`
to only return the numeric NID of the key.

```lua
local pkey, err = require("resty.openssl.pkey").new({type="X448"})

ngx.say(require("cjson").encode(pkey:get_key_type()))
-- outputs '{"ln":"X448","nid":1035,"sn":"X448","id":"1.3.101.111"}'
ngx.say(pkey:get_key_type(true))
-- outputs 1035
```

### pkey:get_size

**syntax**: *size, err = pk:get_size()*

Returns the maximum suitable size for the output buffers for almost all
operations that can be done with pkey.

For RSA key, this is the size of the modulus.
For EC, Ed25519 and Ed448 keys, this is the size of the private key.
For DH key, this is the size of the prime modulus.

### pkey:get_default_digest_type

**syntax**: *obj, err = pk:get_default_digest_type()*

Returns a ASN1_OBJECT of key type of the private key as a table. An additional field `mandatory` is also
returned in the table, if `mandatory` is true then other digests can not be used.

```lua
local pkey, err = require("resty.openssl.pkey").new()

ngx.say(require("cjson").encode(pkey:get_default_digest_type()))
-- outputs '{"ln":"sha256","nid":672,"id":"2.16.840.1.101.3.4.2.1","mandatory":false,"sn":"SHA256"}'
```

### pkey:sign

**syntax**: *signature, err = pk:sign(digest)*

**syntax**: *signature, err = pk:sign(message, md_alg?, padding?, opts?)*

Perform a digest signing using the private key defined in `pkey`
instance. The first parameter must be a [resty.openssl.digest](#restyopenssldigest)
instance or a string. Returns the signed text and error if any.

When passing a [digest](#restyopenssldigest) instance as first parameter, it should not
have been called [final()](#digestfinal), user should only use [update()](#digestupdate).
This mode only supports RSA and EC keys.

When passing a string as first parameter, `md_alg` parameter will specify the name
to use when signing. When `md_alg` is undefined, for RSA and EC keys, this function does SHA256
by default. For Ed25519 or Ed448 keys, this function does a PureEdDSA signing,
no message digest should be specified and will not be used.

For RSA key, it's also possible to specify `padding` scheme with following choices:

```lua
  pkey.PADDINGS = {
    RSA_PKCS1_PADDING       = 1,
    RSA_SSLV23_PADDING      = 2,
    RSA_NO_PADDING          = 3,
    RSA_PKCS1_OAEP_PADDING  = 4,
    RSA_X931_PADDING        = 5, -- sign only
    RSA_PKCS1_PSS_PADDING   = 6, -- sign and verify only
  }
```

When `padding` is `RSA_PKCS1_PSS_PADDING`, it's
possible to specify PSS salt length by setting `opts.pss_saltlen`.

For EC key, this function does a ECDSA signing.
Note that OpenSSL does not support EC digital signature (ECDSA) with the
obsolete MD5 hash algorithm and will return error on this combination. See
[EVP_DigestSign(3)](https://www.openssl.org/docs/manmaster/man3/EVP_DigestSign.html)
for a list of algorithms and associated public key algorithms. Normally, the ECDSA signature
is encoded in ASN.1 DER format. If the `opts` table contains a `ecdsa_use_raw` field with
a true value, a binary with just the concatenation of binary representation `pr` and `ps` is returned.
This is useful for example to send the signature as JWS.

`opts` is a table that accepts additional parameters with following choices:

```
{
  pss_saltlen, -- For PSS mode only this option specifies the salt length.
  mgf1_md, -- For PSS and OAEP padding sets the MGF1 digest. If the MGF1 digest is not explicitly set in PSS mode then the signing digest is used.
  oaep_md, -- The digest used for the OAEP hash function. If not explicitly set then SHA1 is used.
}
```

It's also possible to pass raw pkeyopt control strings as used in the `pkeyutl` CLI program. This lets user pass in options that
are not explictly supported as parameters above.
See [openssl-pkeyutl(1)](https://www.openssl.org/docs/manmaster/man1/openssl-pkeyutl.html) for a list of options.

```lua
pk:sign(message, nil, pk.PADDINGS.RSA_PKCS1_OAEP_PADDING, {
  oaep_md = "sha256",
})
-- is same as
pk:sign(message, nil, nil, {
  "rsa_padding_mode:oaep",
  "rsa_oaep_md:sha256",
})
-- in pkeyutl CLI the above is equivalent to: `openssl pkeyutl -sign -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256
```

To sign a message without doing message digest, please check [pkey:sign_raw](#pkeysign_raw).

### pkey:verify

**syntax**: *ok, err = pk:verify(signature, digest)*

**syntax**: *ok, err = pk:verify(signature, message, md_alg?, padding?, opts?)*

Verify a signture (which can be the string returned by [pkey:sign](#pkey-sign)). The second
argument must be a [resty.openssl.digest](#restyopenssldigest) instance that uses
the same digest algorithm as used in `sign` or a string. `ok` returns `true` if verficiation is
successful and `false` otherwise. Note when verfication failed `err` will not be set when used
with OpenSSL 1.1.1 or lower.

When passing [digest](#restyopenssldigest) instances as second parameter, it should not
have been called [final()](#digestfinal), user should only use [update()](#digestupdate).
This mode only supports RSA and EC keys.

When passing a string as second parameter, `md_alg` parameter will specify the name
to use when verifying. When `md_alg` is undefined, for RSA and EC keys, this function does SHA256
by default. For Ed25519 or Ed448 keys, this function does a PureEdDSA verification,
no message digest should be specified and will not be used.

When key is a RSA key, the function accepts an optional argument `padding` which choices
of values are same as those in [pkey:sign](#pkeysign). When `padding` is `RSA_PKCS1_PSS_PADDING`, it's
possible to specify PSS salt length by setting `opts.pss_saltlen`.

For EC key, this function does a ECDSA verification. Normally, the ECDSA signature
should be encoded in ASN.1 DER format. If the `opts` table contains a `ecdsa_use_raw` field with
a true value, this library treat `signature` as concatenation of binary representation `pr` and `ps`.
This is useful for example to verify the signature as JWS.

`opts` is a table that accepts additional parameters which choices
of values are same as those in [pkey:sign](#pkeysign).


```lua
-- RSA and EC keys
local pk, err = require("resty.openssl.pkey").new()
local digest, err = require("resty.openssl.digest").new("SHA256")
digest:update("dog")
-- WRONG:
-- digest:final("dog")
local signature, err = pk:sign(digest)
-- uses SHA256 by default
local signature, err = pk:sign("dog")
ngx.say(ngx.encode_base64(signature))
-- uses SHA256 and PSS padding
local signature_pss, err = pk:sign("dog", "sha256", pk.PADDINGS.RSA_PKCS1_PSS_PADDING)

digest, err = require("resty.openssl.digest").new("SHA256")
digest:update("dog")
local ok, err = pk:verify(signature, digest)
-- uses SHA256 by default
local ok, err = pk:verify(signature, "dog")
-- uses SHA256 and PSS padding
local ok, err = pk:verify(signature_pss, "dog", "sha256", pk.PADDINGS.RSA_PKCS1_PSS_PADDING)

-- Ed25519 and Ed448 keys
local pk, err = require("resty.openssl.pkey").new({
  type = "Ed25519",
})
local signature, err = pk:sign("23333")
ngx.say(ngx.encode_base64(signature))

```

To verify a message without doing message digest, please check [pkey:verify_raw](#pkeyverify_raw) and [pkey:verify_recover](#pkeyverify_recover).

### pkey:encrypt

**syntax**: *cipher_txt, err = pk:encrypt(txt, padding?, opts?)*

Encrypts plain text `txt` with `pkey` instance, which must loaded a public key.

The optional second argument `padding` has same meaning as in [pkey:sign](#pkeysign).
If omitted, `padding` is default to `pkey.PADDINGS.RSA_PKCS1_PADDING`.

The third optional argument `opts` has same meaning as in [pkey:sign](#pkeysign).


### pkey:decrypt

**syntax**: *txt, err = pk:decrypt(cipher_txt, padding?, opts?)*

Decrypts cipher text `cipher_txt` with pkey instance, which must loaded a private key.

The optional second argument `padding` has same meaning as in [pkey:sign](#pkeysign).
If omitted, `padding` is default to `pkey.PADDINGS.RSA_PKCS1_PADDING`.

The third optional argument `opts` has same meaning as in [pkey:sign](#pkeysign).

```lua
local pkey = require("resty.openssl.pkey")
local privkey, err = pkey.new()
local pub_pem = privkey:to_PEM("public")
local pubkey, err = pkey.new(pub_pem)
local s, err = pubkey:encrypt("🦢", pkey.PADDINGS.RSA_PKCS1_PADDING)
ngx.say(#s)
-- outputs 256
local decrypted, err = privkey:decrypt(s)
ngx.say(decrypted)
-- outputs "🦢"
```

### pkey:sign_raw

**syntax**: *signature, err = pk:sign_raw(txt, padding?, opts?)*

Signs the cipher text `cipher_txt` with pkey instance, which must loaded a private key.

The optional second argument `padding` has same meaning as in [pkey:sign](#pkeysign).
If omitted, `padding` is default to `pkey.PADDINGS.RSA_PKCS1_PADDING`.

The third optional argument `opts` has same meaning as in [pkey:sign](#pkeysign).

This function may also be called "private encrypt" in some implementations like NodeJS or PHP.
Do note as the function names suggested, this function is not secure to be regarded as an encryption.
When developing new applications, user should use [pkey:sign](#pkeysign) for signing with digest, or 
[pkey:encrypt](#pkeyencrypt) for encryption.

See [examples/raw-sign-and-recover.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/raw-sign-and-recover.lua)
for an example.

### pkey:verify_raw

**syntax**: *ok, err = pk:verify_raw(signature, data, md_alg, padding?, opts?)*

Verify the cipher text `signature` with the message `data` with pkey instance, which must loaded a public key. Set the message digest to `md_alg` but doesn't do message digest
automatically, in other words, this function assumes `data` has already been hashed with `md_alg`.

When `md_alg` is undefined, for RSA and EC keys, this function does SHA256 by default. For Ed25519 or Ed448 keys, no default value is set.

The optinal fourth argument `padding` has same meaning as in [pkey:sign](#pkeysign).
If omitted, `padding` is default to `pkey.PADDINGS.RSA_PKCS1_PADDING`.

The fifth optional argument `opts` has same meaning as in [pkey:sign](#pkeysign).

See [examples/raw-sign-and-recover.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/raw-sign-and-recover.lua)
for an example.

### pkey:verify_recover

**syntax**: *txt, err = pk:verify_recover(signature, padding?, opts?)*

Verify the cipher text `signature` with pkey instance, which must loaded a public key, and also
returns the original text being signed. This operation is only supported by RSA key.

The optional second argument `padding` has same meaning as in [pkey:sign](#pkeysign).
If omitted, `padding` is default to `pkey.PADDINGS.RSA_PKCS1_PADDING`.

The third optional argument `opts` has same meaning as in [pkey:sign](#pkeysign).

This function may also be called "public decrypt" in some implementations like NodeJS or PHP.

See [examples/raw-sign-and-recover.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/raw-sign-and-recover.lua)
for an example.

### pkey:derive

**syntax**: *txt, err = pk:derive(peer_key)*

Derive public key algorithm shared secret `peer_key`, which must be a [pkey](#restyopensslpkey)
instance.

See [examples/x25519-dh.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/x25519-dh.lua)
for an example on how key exchange works for X25519 keys with DH algorithm.

### pkey:tostring

**syntax**: *txt, err = pk:tostring(private_or_public?, fmt?, is_pkcs1?)*

Outputs private key or public key of pkey instance in PEM-formatted text.
The first argument must be a choice of `public`, `PublicKey`, `private`, `PrivateKey` or nil.

The second argument `fmt` can be `PEM`, `DER`, `JWK` or nil.
If both arguments are omitted, this functions returns the `PEM` representation of public key.

If `is_pkcs1` is set to true, the output is encoded using a PKCS#1 RSAPublicKey structure;
`PKCS#1` encoding is currently supported for RSA key in PEM format. Writing out a PKCS#1
encoded RSA key is currently not supported when using with OpenSSL 3.0.

### pkey:to_PEM

**syntax**: *pem, err = pk:to_PEM(private_or_public?, is_pkcs1?)*

Equivalent to `pkey:tostring(private_or_public, "PEM", is_pkcs1)`.

## resty.openssl.bn

Module to expose BIGNUM structure. Note bignum is a big integer, no float operations
(like square root) are supported.

### bn.new

**syntax**: *b, err = bn.new(number?)*

**syntax**: *b, err = bn.new(string?, base?)*

Creates a `bn` instance. The first argument can be:

- `nil` to creates an empty bn instance.
- A Lua number to initialize the bn instance.
- A string to initialize the bn instance. The second argument `base` specifies the base of the string,
and can take value from (compatible with Ruby OpenSSL.BN API):
  - `10` or omitted, for decimal string (`"23333"`)
  - `16`, for hex encoded string (`"5b25"`)
  - `2`, for binary string (`"\x5b\x25"`)
  - `0`, for MPI formated string (`"\x00\x00\x00\x02\x5b\x25"`)

MPI is a format that consists of the number's length in bytes represented as a 4-byte big-endian number, and the number itself in big-endian format, where the most significant bit signals a negative number (the representation of numbers with the MSB set is prefixed with null byte).

### bn.dup

**syntax**: *b, err = bn.dup(bn_ptr_cdata)*

Duplicates a `BIGNUM*` to create a new `bn` instance.

### bn.istype

**syntax**: *ok = bn.istype(table)*

Returns `true` if table is an instance of `bn`. Returns `false` otherwise.

### bn.set

**syntax**: *b, err = bn:set(number)*

**syntax**: *b, err = bn:set(string, base?)*

Reuse the existing bn instance and reset its value with given number or string.
Refer to [bn.new](#bnnew) for the type of arguments supported.

### bn.from_binary, bn:to_binary

**syntax**: *bn, err = bn.from_binary(bin)*

**syntax**: *bin, err = bn:to_binary(padto?)*

Creates a `bn` instance from binary string.

Exports the BIGNUM value in binary string.

`bn:to_binary` accepts an optional number argument `padto` that can be
used to pad leading zeros to the output to a specific length.

```lua
local to_hex = require "resty.string".to_hex
local b, err = require("resty.openssl.bn").from_binary("\x5b\x25")
local bin, err = b:to_binary()
ngx.say(to_hex(bin))
-- outputs "5b25
```

### bn.from_mpi, bn:to_mpi

**syntax**: *bn, err = bn.from_mpi(bin)*

**syntax**: *bin, err = bn:to_mpi()*

Creates a `bn` instance from MPI formatted binary string.

Exports the BIGNUM value in MPI formatted binary string.


```lua
local to_hex = require "resty.string".to_hex
local b, err = require("resty.openssl.bn").from_mpi("\x00\x00\x00\x02\x5b\x25")
local bin, err = b:to_mpi()
ngx.say(to_hex(bin))
-- outputs "000000025b25
```

### bn.from_hex, bn:to_hex

**syntax**: *bn, err = bn.from_hex(hex)*

**syntax**: *hex, err = bn:to_hex()*

Creates a `bn` instance from hex encoded string. Note that the leading `0x` should not be
included. A leading `-` indicating the sign may be included.

Exports the `bn` instance to hex encoded string.

```lua
local bn = require("resty.openssl.bn")
local b = bn.from_hex("5B25")
local hex, err = b:to_hex()
ngx.say(hex)
-- outputs "5B25"
```

### bn.from_dec, bn:to_dec

**syntax**: *bn, err = bn.from_dec(dec)*

**syntax**: *dec, err = bn:to_dec()*

Creates a `bn` instance from decimal string. A leading `-` indicating the sign may be included.

Exports the `bn` instance to decimal string.

```lua
local bn = require("resty.openssl.bn")
local b = bn.from_dec("23333")
local dec, err = b:to_dec()
ngx.say(dec)
-- outputs "23333"
```

### bn:to_number

**syntax**: *n, err = bn:to_number()*

**syntax**: *n, err = bn:tonumber()*

Export the lowest 32 bits or 64 bits part (based on the ABI) of `bn` instance
to a number. This is useful when user wants to perform bitwise operations.

```lua
local bn = require("resty.openssl.bn")
local b = bn.from_dec("23333")
local n, err = b:to_number()
ngx.say(n)
-- outputs 23333
ngx.say(type(n))
-- outputs "number"
```

### bn.generate_prime

**syntax**: *bn, err = bn.generate_prime(bits, safe)*

Generates a pseudo-random prime number of bit length `bits`.

If `safe` is true, it will be a safe prime (i.e. a prime p so that (p-1)/2 is also prime).

The PRNG must be seeded prior to calling BN_generate_prime_ex().
The prime number generation has a negligible error probability.

### bn:__metamethods

Various mathematical operations can be performed as if it's a number.

```lua
local bn = require("resty.openssl.bn")
local a = bn.new(123456)
local b = bn.new(222)
 -- the following returns a bn
local r
r = -a
r = a + b
r = a - b
r = a * b
r = a / b -- equal to bn:idiv, returns floor division
r = a % b
-- all operations can be performed between number and bignum
r = a + 222
r = 222 + a
-- the following returns a bool
local bool
bool = a < b
bool = a >= b
-- compare between number will not work
-- WRONG: bool = a < 222
```

### bn:add, bn:sub, bn:mul, bn:div, bn:exp, bn:mod, bn:gcd

**syntax**: *r = a:op(b)*

**syntax**: *r = bn.op(a, b)*

Perform mathematical operations `op`.

- `add`: add
- `sub`: subtract
- `mul`: multiply
- `div`, `idiv`: floor division (division with rounding down to nearest integer)
- `exp`, `pow`: the `b`-th power of `a`, this function is faster than repeated `a * a * ...`.
- `mod`: modulo
- `gcd`: the greatest common divider of `a` and `b`.

Note that `add`, `sub`, `mul`, `div`, `mod` is also available with `+, -, *, /, %` operaters.
See [above section](#bn__metamethods) for examples.

```lua
local bn = require("resty.openssl.bn")
local a = bn.new(123456)
local b = bn.new(9876)
local r
-- the followings are equal
r = a:add(b)
r = bn.add(a, b)
r = a:add(9876)
r = bn.add(a, 9876)
r = bn.add(123456, b)
r = bn.add(123456, 9876)
```

### bn:sqr

**syntax**: *r = a:sqr()*

**syntax**: *r = bn.sqr(a)*

Computes the 2-th power of `a`. This function is faster than `r = a * a`.

### bn:mod_add, bn:mod_sub, bn:mod_mul, bn:mod_exp

**syntax**: *r = a:op(b, m)*

**syntax**: *r = bn.op(a, b, m)*

Perform modulo mathematical operations `op`.

- `mod_add`: adds `a` to `b` modulo `m`
- `mod_sub`: substracts `b` from `a` modulo `m`
- `mod_mul`: multiplies `a` by `b` and finds the non-negative remainder respective to modulus `m`
- `mod_exp`, `mod_pow`: computes `a` to the `b`-th power modulo `m` (r=a^b % m). This function uses less
time and space than `exp`. Do not call this function when `m` is even and any of the parameters
have the `BN_FLG_CONSTTIME` flag set.

```lua
local bn = require("resty.openssl.bn")
local a = bn.new(123456)
local b = bn.new(9876)
local r
-- the followings are equal
r = a:mod_add(b, 3)
r = bn.mod_add(a, b, 3)
r = a:mod_add(9876, 3)
r = bn.mod_add(a, 9876, 3)
r = bn.mod_add(123456, b, 3)
r = bn.mod_add(123456, 9876, 3)
```

### bn:mod_sqr

**syntax**: *r = a:mod_sqr(m)*

**syntax**: *r = bn.mod_sqr(a, m)*

Takes the square of `a` modulo `m`.

### bn:lshift, bn:rshift

**syntax**: *r = bn:lshift(bit)*

**syntax**: *r = bn.lshift(a, bit)*

**syntax**: *r = bn:rshift(bit)*

**syntax**: *r = bn.rshift(a, bit)*

Bit shift `a` to `bit` bits.

### bn:is_zero, bn:is_one, bn:is_odd, bn:is_word

**syntax**: *ok = bn:is_zero()*

**syntax**: *ok = bn:is_one()*

**syntax**: *ok = bn:is_odd()*

**syntax**: *ok, err = bn:is_word(n)*

Checks if `bn` is `0`, `1`, and odd number or a number `n` respectively.

### bn:is_prime

**syntax**: *ok, err = bn:is_prime(nchecks?)*

Checks if `bn` is a prime number. Returns `true` if it is prime with an
error probability of less than 0.25^`nchecks` and error if any. If omitted,
`nchecks` is set to 0 which means to select number of iterations basedon the
size of the number

> This function perform a Miller-Rabin probabilistic primality test with nchecks iterations. If nchecks == BN_prime_checks (0), a number of iterations is used that yields a false positive rate of at most 2^-64 for random input. The error rate depends on the size of the prime and goes down for bigger primes. The rate is 2^-80 starting at 308 bits, 2^-112 at 852 bits, 2^-128 at 1080 bits, 2^-192 at 3747 bits and 2^-256 at 6394 bits.

> When the source of the prime is not random or not trusted, the number of checks needs to be much higher to reach the same level of assurance: It should equal half of the targeted security level in bits (rounded up to the next integer if necessary). For instance, to reach the 128 bit security level, nchecks should be set to 64.

See also [BN_is_prime(3)](https://www.openssl.org/docs/manmaster/man3/BN_is_prime.html).

## resty.openssl.cipher

Module to interact with symmetric cryptography (EVP_CIPHER).

### cipher.new

**syntax**: *d, err = cipher.new(cipher_name, properties?)*

Creates a cipher instance. `cipher_name` is a case-insensitive string of cipher algorithm name.
To view a list of cipher algorithms implemented, use
[openssl.list_cipher_algorithms](#openssllist_cipher_algorithms)
or `openssl list -cipher-algorithms`

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### cipher.istype

**syntax**: *ok = cipher.istype(table)*

Returns `true` if table is an instance of `cipher`. Returns `false` otherwise.

### cipher.set_buffer_size

**syntax**: *ok = cipher.set_buffer_size(sz)*

Resize the internal buffer size used by all cipher instance. The default buffer size is 1024 bytes.

If you are expecting to pass input text larger than 1024 bytes at one time to `update()`, `encrypt()`
or `decrypt()`, setting the buffer to larger than the expected input size will improve performance
by let more code to be JIT-able.

Avoid call this function at hotpath, as this re-allocate the buffer every time it's called.

### cipher:get_provider_name

**syntax**: *name = cipher:get_provider_name()*

Returns the provider name of `cipher`.

This function is available since OpenSSL 3.0.

## cipher:gettable_params, cipher:settable_params, cipher:get_param, cipher:set_params

Query settable or gettable params and set or get params.
See [Generic EVP parameter getter/setter](#generic-evp-parameter-gettersetter).

### cipher:encrypt

**syntax**: *s, err = cipher:encrypt(key, iv?, s, no_padding?, aead_aad?)*

Encrypt the text `s` with key `key` and IV `iv`. Returns the encrypted text in raw binary string
and error if any.
Optionally accepts a boolean `no_padding` which tells the cipher to enable or disable padding and default
to `false` (enable padding). If `no_padding` is `true`, the length of `s` must then be a multiple of the
block size or an error will occur.

When using GCM or CCM mode or `chacha20-poly1305` cipher, it's also possible to pass
the Additional Authenticated Data (AAD) as the fifth argument.

This function is a shorthand of `cipher:init`, `cipher:set_aead_aad` (if appliable) then `cipher:final`.

### cipher:decrypt

**syntax**: *s, err = cipher:decrypt(key, iv?, s, no_padding?, aead_aad?, aead_tag?)*

Decrypt the text `s` with key `key` and IV `iv`. Returns the decrypted text in raw binary string
and error if any.
Optionally accepts a boolean `no_padding` which tells the cipher to enable or disable padding and default
to `false` (enable padding). If `no_padding` is `true`, the length of `s` must then be a multiple of the
block size or an error will occur; also, padding in the decrypted text will not be removed.

When using GCM or CCM mode or `chacha20-poly1305` cipher, it's also possible to pas
the Additional Authenticated Data (AAD) as the fifth argument and authentication tag
as the sixth argument.

This function is a shorthand of `cipher:init`, `cipher:set_aead_aad` (if appliable),
`cipher:set_aead_tag` (if appliable) then `cipher:final`.

### cipher:init

**syntax**: *ok, err = cipher:init(key, iv?, opts?)*

Initialize the cipher with key `key` and IV `iv`. The optional third argument is a table consists of:

```lua
{
    is_encrypt = false,
    no_padding = false,
}
```

Calling function is needed before [cipher:update](#restycipherupdate) and
[cipher:final](#restycipherfinal) if the cipher is not being initialized already. But not
[cipher:encrypt](#restycipherencrypt) and [cipher:decrypt](#restycipherdecrypt).

If you wish to reuse `cipher` instance multiple times, calling this function is necessary
to clear the internal state of the cipher. The shorthand functions
[cipher:encrypt](#restycipherencrypt) and [cipher:decrypt](#restycipherdecrypt)
already take care of initialization and reset.

### cipher:update

**syntax**: *s, err = cipher:update(partial, ...)*

Updates the cipher with one or more strings. If the cipher has larger than block size of data to flush,
the function will return a non-empty string as first argument. This function can be used in a streaming
fashion to encrypt or decrypt continous data stream.

### cipher:update_aead_aad

**syntax**: *ok, err = cipher:update_aead_aad(aad)*

Provides AAD data to the cipher, this function can be called more than one times.

### cipher:get_aead_tag

**syntax**: *tag, err = cipher:get_aead_tag(size?)*

Gets the authentication tag from cipher with length specified as `size`. If omitted, a tag with length
of half of the block size will be returned. The size cannot exceed block size.

This function can only be called after encryption is finished.

### cipher:set_aead_tag

**syntax**: *ok, err = cipher:set_aead_tag(tag)*

Set the authentication tag of cipher with `tag`.

This function can only be called before decryption starts.

### cipher:final

**syntax**: *s, err = cipher:final(partial?)*

Returns the encrypted or decrypted text in raw binary string, optionally accept one string to encrypt or decrypt.

```lua
-- encryption
local c, err = require("resty.openssl.cipher").new("aes256")
c:init(string.rep("0", 32), string.rep("0", 16), {
    is_encrypt = true,
})
c:update("🦢")
local cipher, err = c:final()
ngx.say(ngx.encode_base64(cipher))
-- outputs "vGJRHufPYrbbnYYC0+BnwQ=="
-- OR:
local c, err = require("resty.openssl.cipher").new("aes256")
local cipher, err = c:encrypt(string.rep("0", 32), string.rep("0", 16), "🦢")
ngx.say(ngx.encode_base64(cipher))
-- outputs "vGJRHufPYrbbnYYC0+BnwQ=="

-- decryption
local encrypted = ngx.decode_base64("vGJRHufPYrbbnYYC0+BnwQ==")
local c, err = require("resty.openssl.cipher").new("aes256")
c:init(string.rep("0", 32), string.rep("0", 16), {
    is_encrypt = false,
})
c:update(encrypted)
local cipher, err = c:final()
ngx.say(cipher)
-- outputs "🦢"
-- OR:
local c, err = require("resty.openssl.cipher").new("aes256")
local cipher, err = c:decrypt(string.rep("0", 32), string.rep("0", 16), encrypted)
ngx.say(cipher)
-- outputs "🦢"
```

**Note:** in some implementations like `libsodium` or Java, AEAD ciphers append the `tag` (or `MAC`)
at the end of encrypted ciphertext. In such case, user will need to manually cut off the `tag`
with correct size(usually 16 bytes) and pass in the ciphertext and `tag` seperately.

See [examples/aes-gcm-aead.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/aes-gcm-aead.lua)
for an example to use AEAD modes with authentication.

### cipher:derive

**syntax**: *key, iv, err = cipher:derive(key, salt?, count?, md?)*

Derive a key and IV (if appliable) from given material that can be used in current cipher. This function
is useful mainly to work with keys that were already derived from same algorithm. Newer applications should
use a more modern algorithm such as PBKDF2 provided by [kdf.derive](#kdfderive).

`count` is the iteration count to perform. If it's omitted, it's set to `1`. Note the recent version of
`openssl enc` cli tool automatically use PBKDF2 if `-iter` is set to larger than 1,
while this function will not. To use PBKDF2 to derive a key, please refer to [kdf.derive](#kdfderive).

`md` is the message digest name to use, it can take one of the values `md2`, `md5`, `sha` or `sha1`.
If it's omitted, it's default to `sha1`.

```lua
local cipher = require("resty.openssl.cipher").new("aes-128-cfb")
local key, iv, err = cipher:derive("x")
-- equivalent to `openssl enc -aes-128-cfb -pass pass:x -nosalt -P -md sha1`
```

## resty.openssl.digest

Module to interact with message digest (EVP_MD_CTX).

### digest.new

**syntax**: *d, err = digest.new(digest_name?, properties?)*

Creates a digest instance. `digest_name` is a case-insensitive string of digest algorithm name.
To view a list of digest algorithms implemented, use 
[openssl.list_digest_algorithms](#openssllist_digest_algorithms) or
`openssl list -digest-algorithms`.

If `digest_name` is omitted, it's default to `sha1`. Specially, the digest_name `"null"`
represents a "null" message digest that does nothing: i.e. the hash it returns is of zero length.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### digest.istype

**syntax**: *ok = digest.istype(table)*

Returns `true` if table is an instance of `digest`. Returns `false` otherwise.

### digest:get_provider_name

**syntax**: *name = digest:get_provider_name()*

Returns the provider name of `digest`.

This function is available since OpenSSL 3.0.

## digest:gettable_params, digest:settable_params, digest:get_param, digest:set_params

Query settable or gettable params and set or get params.
See [Generic EVP parameter getter/setter](#generic-evp-parameter-gettersetter).

### digest:update

**syntax**: *ok, err = digest:update(partial, ...)*

Updates the digest with one or more strings.

### digest:final

**syntax**: *str, err = digest:final(partial?)*

Returns the digest in raw binary string, optionally accept one string to digest.

```lua
local d, err = require("resty.openssl.digest").new("sha256")
d:update("🦢")
local digest, err = d:final()
ngx.say(ngx.encode_base64(digest))
-- outputs "tWW/2P/uOa/yIV1gRJySJLsHq1xwg0E1RWCvEUDlla0="
-- OR:
local d, err = require("resty.openssl.digest").new("sha256")
local digest, err = d:final("🦢")
ngx.say(ngx.encode_base64(digest))
-- outputs "tWW/2P/uOa/yIV1gRJySJLsHq1xwg0E1RWCvEUDlla0="
```

### digest:reset

**syntax**: *ok, err = digest:reset()*

Reset the internal state of `digest` instance as it's just created by [digest.new](#digestnew).
It calls [EVP_DigestInit_ex](https://www.openssl.org/docs/manmaster/man3/EVP_DigestInit_ex.html) under
the hood.

User must call this before reusing the same `digest` instance.

## resty.openssl.hmac

Module to interact with hash-based message authentication code (HMAC_CTX).

Use of this module is deprecated since OpenSSL 3.0, please use [resty.openssl.mac](#restyopensslmac)
instead.

### hmac.new

**syntax**: *h, err = hmac.new(key, digest_name?)*

Creates a hmac instance. `digest_name` is a case-insensitive string of digest algorithm name.
To view a list of digest algorithms implemented, use
[openssl.list_digest_algorithms](#openssllist_digest_algorithms) or
`openssl list -digest-algorithms`.

If `digest_name` is omitted, it's default to `sha1`.

### hmac.istype

**syntax**: *ok = hmac.istype(table)*

Returns `true` if table is an instance of `hmac`. Returns `false` otherwise.

### hmac:update

**syntax**: *ok, err = hmac:update(partial, ...)*

Updates the HMAC with one or more strings.

### hmac:final

**syntax**: *str, err = hmac:final(partial?)*

Returns the HMAC in raw binary string, optionally accept one string to digest.

```lua
local d, err = require("resty.openssl.hmac").new("goose", "sha256")
d:update("🦢")
local hmac, err = d:final()
ngx.say(ngx.encode_base64(hmac))
-- outputs "k2UcrRp25tj1Spff89mJF3fAVQ0lodq/tJT53EYXp0c="
-- OR:
local d, err = require("resty.openssl.hmac").new("goose", "sha256")
local hmac, err = d:final("🦢")
ngx.say(ngx.encode_base64(hmac))
-- outputs "k2UcrRp25tj1Spff89mJF3fAVQ0lodq/tJT53EYXp0c="
```

### hmac:reset

**syntax**: *ok, err = hmac:reset()*

Reset the internal state of `hmac` instance as it's just created by [hmac.new](#hmacnew).
It calls [HMAC_Init_ex](https://www.openssl.org/docs/manmaster/man3/HMAC_Init_ex.html) under
the hood.

User must call this before reusing the same `hmac` instance.

## resty.openssl.mac

Module to interact with message authentication code (EVP_MAC).

### mac.new

**syntax**: *h, err = mac.new(key, mac, cipher?, digest?, properties?)*

Creates a mac instance. `mac` is a case-insensitive string of MAC algorithm name.
To view a list of digest algorithms implemented, use
[openssl.list_mac_algorithms](#openssllist_mac_algorithms) or
`openssl list -mac-algorithms`.

At least one of `cipher` or `digest` must be specified.

`cipher` is a case-insensitive string of digest algorithm name.
To view a list of digest algorithms implemented, use
[openssl.list_cipher_algorithms](#openssllist_cipher_algorithms) or
`openssl list -cipher-algorithms`.
`digest` is a case-insensitive string of digest algorithm name.
To view a list of digest algorithms implemented, use
[openssl.list_digest_algorithms](#openssllist_digest_algorithms) or
`openssl list -digest-algorithms`.
`properties` parameter can be used to explictly select provider to fetch algorithms.

### mac.istype

**syntax**: *ok = mac.istype(table)*

Returns `true` if table is an instance of `mac`. Returns `false` otherwise.

### mac:get_provider_name

**syntax**: *name = mac:get_provider_name()*

Returns the provider name of `mac`.

This function is available since OpenSSL 3.0.

## mac:gettable_params, mac:settable_params, mac:get_param, mac:set_params

Query settable or gettable params and set or get params.
See [Generic EVP parameter getter/setter](#generic-evp-parameter-gettersetter).

### mac:update

**syntax**: *ok, err = mac:update(partial, ...)*

Updates the MAC with one or more strings.

### mac:final

**syntax**: *str, err = mac:final(partial?)*

Returns the MAC in raw binary string, optionally accept one string to digest.

```lua
local d, err = require("resty.openssl.mac").new("goose", "HMAC", nil, "sha256")
d:update("🦢")
local mac, err = d:final()
ngx.say(ngx.encode_base64(mac))
-- outputs "k2UcrRp25tj1Spff89mJF3fAVQ0lodq/tJT53EYXp0c="
-- OR:
local d, err = require("resty.openssl.mac").new("goose", "HMAC", nil, "sha256")
local hmac, err = d:final("🦢")
ngx.say(ngx.encode_base64(mac))
-- outputs "k2UcrRp25tj1Spff89mJF3fAVQ0lodq/tJT53EYXp0c="
```

### mac:reset

**syntax**: *ok, err = mac:reset()*

Reset the internal state of `mac` instance as it's just created by [mac.new](#macnew).
It calls [EVP_MAC_Init](https://www.openssl.org/docs/manmaster/man3/EVP_MAC_init.html) under
the hood.

User must call this before reusing the same `mac` instance.

## resty.openssl.kdf

Module to interact with KDF (key derivation function).

### kdf.derive (legacy)

**syntax**: *key, err = kdf.derive(options)*

Use of this module is deprecated since OpenSSL 3.0, please use [kdf.new](#kdfnew)
instead.

Derive a key from given material. Various KDFs are supported based on OpenSSL version:

`PBKDF2`([RFC 2898], [NIST SP 800-132]), `HKDF`([RFC 5869]), `TLS1-PRF`([RFC 2246], [RFC 5246] and [NIST SP 800-135 r1]) and `scrypt`([RFC 7914]) is available.


`options` is a table that contains:

| Key | Type | Description | Required or default |
| ------------   | ---- | ----------- | ------ |
| type   | number | Type of KDF function to use, one of `kdf.PBKDF2`, `kdf.SCRYPT`, `kdf.TLS1_PRF` or `kdf.HKDF` | **required** |
| outlen   | number | Desired key length to derive | **required** |
| pass    | string | Initial key material to derive from | (empty string) |
| salt    | string | Add some salt | (empty string) |
| md    | string | Message digest method name to use, not effective for `scrypt` type | `"sha1"` |
| properties | string | Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms. | |
| pbkdf2_iter     | number | PBKDF2 iteration count. RFC 2898 suggests an iteration count of at least 1000. Any value less than 1 is treated as a single iteration.  | `1` |
| hkdf_key     | string | HKDF key  | **required** |
| hkdf_mode     | number | HKDF mode to use, one of `kdf.HKDEF_MODE_EXTRACT_AND_EXPAND`, `kdf.HKDEF_MODE_EXTRACT_ONLY` or `kdf.HKDEF_MODE_EXPAND_ONLY`. To learn about mode, please refer to [EVP_PKEY_CTX_set1_hkdf_key(3)](https://www.openssl.org/docs/manmaster/man3/EVP_PKEY_CTX_set1_hkdf_key.html). Note with `kdf.HKDEF_MODE_EXTRACT_ONLY`, `outlen` is ignored and the output will be fixed size of `HMAC-<md>`.  | `kdf.HKDEF_MODE_EXTRACT_AND_EXPAND`|
| hkdf_info     | string | HKDF info value  | (empty string) |
| tls1_prf_secret     | string | TLS1-PRF secret  | **required** |
| tls1_prf_seed     | string | TLS1-PRF seed  | **required** |
| scrypt_maxmem     | number | Scrypt maximum memory usage in bytes  |`32 * 1024 * 1024` |
| scrypt_N     | number | Scrypt CPU/memory cost parameter, must be a power of 2 | **required** |
| scrypt_r     | number | Scrypt blocksize parameter (8 is commonly used) | **required** |
| scrypt_p     | number | Scrypt parallelization parameter | **required** |

```lua
local kdf = require("resty.openssl.kdf")
local key, err = kdf.derive({
    type = kdf.PBKDF2,
    outlen = 16,
    pass = "1234567",
    md = "md5",
    pbkdf2_iter = 1000,
})
ngx.say(ngx.encode_base64(key))
-- outputs "cDRFLQ7NWt+AP4i0TdBzog=="

key, err = kdf.derive({
    type = kdf.SCRYPT,
    outlen = 16,
    pass = "1234567",
    scrypt_N = 1024,
    scrypt_r = 8,
    scrypt_p = 16,
})
ngx.say(ngx.encode_base64(key))
-- outputs "9giFtxace5sESmRb8qxuOw=="
```

### kdf.new

**syntax**: *k, err = kdf.new(kdf_name?, properties?)*

Creates a kdf instance. `kdf_name` is a case-insensitive string of kdf algorithm name.
To view a list of kdf algorithms implemented, use
[openssl.list_kdf_algorithms](#openssllist_kdf_algorithms) or
`openssl list -kdf-algorithms`.

This function is available since OpenSSL 3.0.

This function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### kdf.istype

**syntax**: *ok = kdf.istype(table)*

Returns `true` if table is an instance of `kdf`. Returns `false` otherwise.

This function is available since OpenSSL 3.0.

### kdf:get_provider_name

**syntax**: *name = kdf:get_provider_name()*

Returns the provider name of `kdf`.

This function is available since OpenSSL 3.0.

## kdf:gettable_params, kdf:settable_params, kdf:get_param, kdf:set_params

Query settable or gettable params and set or get params.
See [Generic EVP parameter getter/setter](#generic-evp-parameter-gettersetter).

This function is available since OpenSSL 3.0.

### kdf:derive

**syntax**: *ok, err = kdf:derive(outlen, options?, options_count?)*

Derive a key with length of `outlen` with `options`. Certain algorithms output fixed
length of key where `outlen` should be unset.

`options` is a table map holding parameters passing to `kdf`. To view the list of parameters
acceptable by selecter algorithm and provider, use `kdf:settable_params`.

Optionally, if length of `options` is known, user can provide its length through `options_count`
to gain better performance where `options` table is relatively large.

```lua
local k = assert(kdf.new("PBKDF2"))
key = assert(k:derive(16, {
    pass = "1234567",
    iter = 1000,
    digest = "md5",
    salt = "",
}))
ngx.say(ngx.encode_base64(key))
-- outputs "cDRFLQ7NWt+AP4i0TdBzog=="
assert(k:reset())
-- kdf instance is reusable, user can set common parameters
-- through set_params and don't need to repeat in derive()
assert(k:set_params({
    iter = 1000,
    digest = "md5",
    salt = "",
}))
key = assert(k:derive(16, {
    pass = "1234567",
}))
ngx.say(ngx.encode_base64(key))
-- outputs "cDRFLQ7NWt+AP4i0TdBzog=="

local k = assert(kdf.new("HKDF"))
key = assert(k:derive(16, {
    digest = "md5",
    key = "secret",
    salt = "salt",
    info = "some info",
    mode = kdf.HKDEF_MODE_EXPAND_ONLY,
    -- as HKDF also accepts mode as string, use the literal below also works
    -- mode = "EXPAND_ONLY"
}))
```

This function is available since OpenSSL 3.0.

### kdf:reset

**syntax**: *ok, err = kdf:reset()*

Reset the internal state of `kdf` instance as it's just created by [kdf.new](#kdfnew).

User must call this before reusing the same `kdf` instance.

## resty.openssl.objects

Helpfer module on ASN1_OBJECT.

### objects.obj2table

**syntax**: *tbl = objects.bytes(asn1_obj)*

Convert a ASN1_OBJECT pointer to a Lua table where

```
{
  id: OID of the object,
  nid: NID of the object,
  sn: short name of the object,
  ln: long name of the object,
}
```

### objects.nid2table

**syntax**: *tbl, err = objects.nid2table(nid)*

Convert a [NID] to a Lua table, returns the same format as
[objects.obj2table](#objectsobj2table)

### objects.txt2nid

**syntax**: *nid, err = objects.txt2nid(txt)*

Convert a text representation to [NID]. 

## resty.openssl.pkcs12

Module to interact with PKCS#12 format.

### pkcs12.encode

**syntax**: *der, err = pkcs12.encode(data, passphrase?, properties?)*

Encode data in `data` to a PKCS#12 text.

`data` is a table that contains:

| Key | Type | Description | Required or default |
| ------------   | ---- | ----------- | ------ |
| key   | [pkey](#restyopensslpkey) | Private key | **required** |
| cert   | [x509](#restyopensslx509) | Certificate | **required** |
| cacerts   | A list of [x509](#restyopensslx509) as Lua table | Additional certificates | `[]` |
| friendly_name | string | The name used for the supplied certificate and key | `""` |
| nid_key | number or string | The [NID] or text to specify algorithm to encrypt key | `"PBE-SHA1-RC2-4"` if compiled with RC2, otherwise `"PBE-SHA1-3DES"`; on OpenSSL 3.0 and later `PBES2 with PBKDF2 and AES-256-CBC`. |
| nid_cert | number or string | The [NID] or text to specify algorithm to encrypt cert | `"PBE-SHA1-3DES"`; on OpenSSL 3.0 and later `PBES2 with PBKDF2 and AES-256-CBC` |
| iter | number | Key iterration count | `PKCS12_DEFAULT_ITER` (2048) |
| mac_iter | number | MAC iterration count | 1 |

`passphrase` is the string for encryption. If omitted, an empty string will be used.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

Note in OpenSSL 3.0 `RC2` has been moved to **legacy** provider. In order to encode p12 data with RC2
encryption, you need to [load the legacy provider](#providerload) first.

```lua
local pro = require "resty.openssl.provider"
local legacy_provider = assert(pro.load("legacy"))
local p12, err = pkcs12.encode({ key = key, cert = cert})
assert(legacy_provider:unload())
```

### pkcs12.decode

**syntax**: *data, err = pkcs12.decode(p12, passphrase?)*

Decode a PKCS#12 text to Lua table `data`. Similar to the `data` table passed to [pkcs12.encode](#pkcs12encode),
but onle `cert`, `key`, `cacerts` and `friendly_name` are returned.

`passphrase` is the string for encryption. If omitted, an empty string will be used.

Note in OpenSSL 3.0 `RC2` has been moved to **legacy** provider. In order to decode p12 data with RC2
encryption, you need to [load the legacy provider](#providerload) first.

## resty.openssl.rand

Module to interact with random number generator.

### rand.bytes

**syntax**: *str, err = rand.bytes(length, private?, strength?)*

Generate random bytes with length of `length`. If `private` is set to true, a
private PRNG instance is used so that a compromise of the "public" PRNG instance
will not affect the secrecy of these private values.

The bytes generated will have a security strength of at least `strength` bits.

## resty.openssl.x509

Module to interact with X.509 certificates.

### x509.new

**syntax**: *crt, err = x509.new(txt?, fmt?, properties?)*

Creates a `x509` instance. `txt` can be **PEM** or **DER** formatted text;
`fmt` is a choice of `PEM`, `DER` to load specific format, or `*` for auto detect.

When `txt` is omitted, `new()` creates an empty `x509` instance.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### x509.dup

**syntax**: *x509, err = x509.dup(x509_ptr_cdata)*

Duplicates a `X509*` to create a new `x509` instance.

### x509.istype

**syntax**: *ok = x509.istype(table)*

Returns `true` if table is an instance of `x509`. Returns `false` otherwise.

### x509:digest

**syntax**: *d, err = x509:digest(digest_name?, properties?)*

Returns a digest of the DER representation of the X509 certificate object in raw binary text.

`digest_name` is a case-insensitive string of digest algorithm name.
To view a list of digest algorithms implemented, use
[openssl.list_digest_algorithms](#openssllist_digest_algorithms) or
`openssl list -digest-algorithms`.

If `digest_name` is omitted, it's default to `sha1`.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### x509:pubkey_digest

**syntax**: *d, err = x509:pubkey_digest(digest_name?, properties?)*

Returns a digest of the DER representation of the pubkey in the X509 object in raw binary text.

`digest_name` is a case-insensitive string of digest algorithm name.
To view a list of digest algorithms implemented, use
[openssl.list_digest_algorithms](#openssllist_digest_algorithms) or
`openssl list -digest-algorithms`.

If `digest_name` is omitted, it's default to `sha1`.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### x509:check_private_key

**syntax**: *match, err = x509:check_private_key(pkey)*

Checks the consistency of private key `pkey` with the public key in current X509 object.

Returns a boolean indicating if it's a match and err describing the reason.

Note this function also checks if k itself is indeed a private key or not.

### x509:get_\*, x509:set_\*

**syntax**: *ok, err = x509:set_**attribute**(instance)*

**syntax**: *instance, err = x509:get_**attribute**()*

Setters and getters for x509 attributes share the same syntax.

| Attribute name | Type | Description |
| ------------   | ---- | ----------- |
| issuer_name   | [x509.name](#restyopensslx509name) | Issuer of the certificate |
| not_before    | number | Unix timestamp when certificate is not valid before |
| not_after     | number | Unix timestamp when certificate is not valid after |
| pubkey        | [pkey](#restyopensslpkey)   | Public key of the certificate |
| serial_number | [bn](#restyopensslbn) | Serial number of the certficate |
| subject_name  | [x509.name](#restyopensslx509name) | Subject of the certificate |
| version       | number | Version of the certificate, value is one less than version. For example, `2` represents `version 3` |

Additionally, getters and setters for extensions are also available:

| Extension name | Type | Description |
| ------------   | ---- | ----------- |
| subject_alt_name   | [x509.altname](#restyopensslx509altname) | [Subject Alternative Name](https://tools.ietf.org/html/rfc5280#section-4.2.1.6) of the certificate, SANs are usually used to define "additional Common Names"  |
| issuer_alt_name    | [x509.altname](#restyopensslx509altname) | [Issuer Alternative Name](https://tools.ietf.org/html/rfc5280#section-4.2.1.7) of the certificate |
| basic_constraints  | table, { ca = bool, pathlen = int} | [Basic Constriants](https://tools.ietf.org/html/rfc5280#section-4.2.1.9) of the certificate  |
| info_access        | [x509.extension.info_access](#restyopensslx509extensioninfo_access) | [Authority Information Access](https://tools.ietf.org/html/rfc5280#section-4.2.2.1) of the certificate, contains information like OCSP reponder URL. |
| crl_distribution_points | [x509.extension.dist_points](#restyopensslx509extensiondist_points) | [CRL Distribution Points](https://tools.ietf.org/html/rfc5280#section-4.2.1.13) of the certificate, contains information like Certificate Revocation List(CRL) URLs. |

For all extensions, `get_{extension}_critical` and `set_{extension}_critical` is also supported to
access the `critical` flag of the extension.

If the attribute is not found, getter will return `nil, nil`.

```lua
local x509, err = require("resty.openssl.x509").new()
err = x509:set_not_before(ngx.time())
local not_before, err = x509:get_not_before()
ngx.say(not_before)
-- outputs 1571875065

err = x509:set_basic_constraints_critical(true)
```

If type is a table, setter requires a table with case-insensitive keys to set;
getter returns the value of the given case-insensitive key or a table of all keys if no key provided.

```lua
local x509, err = require("resty.openssl.x509").new()
err = x509:set_basic_constraints({
  cA = false,
  pathlen = 0,
})

ngx.say(x509:get_basic_constraints("pathlen"))
-- outputs 0

ngx.say(x509:get_basic_constraints())
-- outputs '{"ca":false,"pathlen":0}'
```

Note that user may also access the certain extension by [x509:get_extension](#x509get_extension) and
[x509:set_extension](#x509set_extension), while the later two function returns or requires
[extension](#restyopensslx509extension) instead. User may use getter and setters listed here if modification
of current extensions is needed; use [x509:get_extension](#x509get_extension) or
[x509:set_extension](#x509set_extension) if user are adding or replacing the whole extension or
getters/setters are not implemented. If the getter returned a type of `x509.*` instance, it can be
converted to a [extension](#restyopensslx509extension) instance by [extension:from_data](#extensionfrom_data),
and thus used by [x509:get_extension](#x509get_extension) and [x509:set_extension](#x509set_extension) 

### x509:get_lifetime

**syntax**: *not_before, not_after, err = x509:get_lifetime()*

A shortcut of `x509:get_not_before` plus `x509:get_not_after`

### x509:set_lifetime

**syntax**: *ok, err = x509:set_lifetime(not_before, not_after)*

A shortcut of `x509:set_not_before`
plus `x509:set_not_after`.

### x509:get_signature_name, x509:get_signature_nid, x509:get_signature_digest_name

**syntax**: *sn, err = x509:get_signature_name()*

**syntax**: *nid, err = x509:get_signature_nid()*

**syntax**: *sn, err = x509:get_signature_digest_name()*

Return the [NID] or the short name (SN) of the signature of the certificate.

`x509:get_signature_digest_name` returns the short name of the digest algorithm
used to sign the certificate.

### x509:get_extension

**syntax**: *extension, pos, err = x509:get_extension(nid_or_txt, last_pos?)*

Get X.509 `extension` matching the given [NID] to certificate, returns a
[resty.openssl.x509.extension](#restyopensslx509extension) instance and the found position.

If `last_pos` is defined, the function searchs from that position; otherwise it
finds from beginning. Index is 1-based.

```lua
local ext, pos, err = x509:get_extension("keyUsage")
ngx.say(ext:text())
-- outputs "Digital Signature, Key Encipherment"

local ext, pos, err = x509:get_extension("subjectKeyIdentifier")
ngx.say(ext:text())
-- outputs "3D:42:13:57:8F:79:BE:30:7D:86:A9:AC:67:50:E5:56:3E:0E:AF:4F"
```

### x509:add_extension

**syntax**: *ok, err = x509:add_extension(extension)*

Adds an X.509 `extension` to certificate, the first argument must be a
[resty.openssl.x509.extension](#restyopensslx509extension) instance.

```lua
local extension, err = require("resty.openssl.x509.extension").new(
  "keyUsage", "critical,keyCertSign,cRLSign"
)
local x509, err = require("resty.openssl.x509").new()
local ok, err = x509:add_extension(extension)
```

### x509:set_extension

**syntax**: *ok, err = x509:set_extension(extension, last_pos?)*

Adds an X.509 `extension` to certificate, the first argument must be a
[resty.openssl.x509.extension](#restyopensslx509extension) instance.
The difference from [x509:add_extension](#x509add_extension) is that
in this function if a `extension` with same type already exists,
the old extension will be replaced.

If `last_pos` is defined, the function replaces the same extension from that position;
otherwise it finds from beginning. Index is 1-based. Returns `nil, nil` if not found.

Note this function is not thread-safe.

### x509:get_extension_critical

**syntax**: *ok, err = x509:get_extension_critical(nid_or_txt)*

Get critical flag of the X.509 `extension` matching the given [NID] from certificate.

### x509:set_extension_critical

**syntax**: *ok, err = x509:set_extension_critical(nid_or_txt, crit?)*

Set critical flag of the X.509 `extension` matching the given [NID] to certificate.

### x509:get_ocsp_url

**syntax**: *url_or_urls, err = x509:get_ocsp_url(return_all?)*

Get OCSP URL(s) of the X.509 object. If `return_all` is set to true, returns a table
containing all OCSP URLs; otherwise returns a string with first OCSP URL found.
Returns `nil` if the extension is not found.

### x509:get_crl_url

**syntax**: *url_or_urls, err = x509:get_crl_url(return_all?)*

Get CRL URL(s) of the X.509 object. If `return_all` is set to true, returns a table
containing all CRL URLs; otherwise returns a string with first CRL URL found.
Returns `nil` if the extension is not found.

### x509:sign

**syntax**: *ok, err = x509:sign(pkey, digest?)*

Sign the certificate using the private key specified by `pkey`, which must be a 
[resty.openssl.pkey](#restyopensslpkey) that stores private key. Optionally accept `digest`
parameter to set digest method, whichmust be a [resty.openssl.digest](#restyopenssldigest) instance.
Returns a boolean indicating if signing is successful and error if any.

### x509:verify

**syntax**: *ok, err = x509:verify(pkey)*

Verify the certificate signature using the public key specified by `pkey`, which
must be a [resty.openssl.pkey](#restyopensslpkey). Returns a boolean indicating if
verification is successful and error if any.

### x509:tostring

**syntax**: *str, err = x509:tostring(fmt?)*

Outputs certificate in PEM-formatted text or DER-formatted binary.
The first argument can be a choice of `PEM` or `DER`; when omitted, this function outputs PEM by default.

### x509:to_PEM

**syntax**: *pem, err = x509:to_PEM()*

Outputs the certificate in PEM-formatted text.

## resty.openssl.x509.csr

Module to interact with certificate signing request (X509_REQ).

See [examples/csr.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/csr.lua)
for an example to generate CSR.

### csr.new

**syntax**: *csr, err = csr.new(txt?, fmt?, properties?)*

Create an empty `csr` instance. `txt` can be **PEM** or **DER** formatted text;
`fmt` is a choice of `PEM`, `DER` to load specific format, or `*` for auto detect.

When `txt` is omitted, `new()` creates an empty `csr` instance.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### csr.istype

**syntax**: *ok = csr.istype(table)*

Returns `true` if table is an instance of `csr`. Returns `false` otherwise.

### csr:check_private_key

**syntax**: *match, err = csr:check_private_key(pkey)*

Checks the consistency of private key `pkey` with the public key in current CSR object.

Returns a boolean indicating if it's a match and err describing the reason.

Note this function also checks if k itself is indeed a private key or not.

### csr:get_\*, csr:set_\*

**syntax**: *ok, err = csr:set_**attribute**(instance)*

**syntax**: *instance, err = csr:get_**attribute**()*

Setters and getters for x509 attributes share the same syntax.

| Attribute name | Type | Description |
| ------------   | ---- | ----------- |
| pubkey        | [pkey](#restyopensslpkey)   | Public key of the certificate request |
| subject_name  | [x509.name](#restyopensslx509name) | Subject of the certificate request |
| version       | number | Version of the certificate request, value is one less than version. For example, `2` represents `version 3` |

Additionally, getters and setters for extensions are also available:

| Extension name | Type | Description |
| ------------   | ---- | ----------- |
| subject_alt_name   | [x509.altname](#restyopensslx509altname) | [Subject Alternative Name](https://tools.ietf.org/html/rfc5280#section-4.2.1.6) of the certificate request, SANs are usually used to define "additional Common Names"  |

For all extensions, `get_{extension}_critical` and `set_{extension}_critical` is also supported to
access the `critical` flag of the extension.

If the attribute is not found, getter will return `nil, nil`.

```lua
local csr, err = require("resty.openssl.csr").new()
err = csr:set_version(3)
local version, err = csr:get_version()
ngx.say(version)
-- outputs 3
```

Note that user may also access the certain extension by [csr:get_extension](#csrget_extension) and
[csr:set_extension](#csrset_extension), while the later two function returns or requires
[extension](#restyopensslx509extension) instead. User may use getter and setters listed here if modification
of current extensions is needed; use [csr:get_extension](#csrget_extension) or
[csr:set_extension](#csrset_extension) if user are adding or replacing the whole extension or
getters/setters are not implemented. If the getter returned a type of `x509.*` instance, it can be
converted to a [extension](#restyopensslx509extension) instance by [extension:from_data](#extensionfrom_data),
and thus used by [csr:get_extension](#csrget_extension) and [csr:set_extension](#csrset_extension) 

### csr:set_subject_alt

Same as [csr:set_subject_alt_name](#csrget_-csrset_), this function is deprecated to align
with naming convension with other functions.

### csr:get_signature_name, csr:get_signature_nid, csr:get_signature_digest_name

**syntax**: *sn, err = csr:get_signature_name()*

**syntax**: *nid, err = csr:get_signature_nid()*

**syntax**: *sn, err = csr:get_signature_digest_name()*

Return the [NID] or the short name (SN) of the signature of the certificate request.

`csr:get_signature_digest_name` returns the short name of the digest algorithm
used to sign the certificate.

### csr:get_extension

**syntax**: *extension, pos, err = csr:get_extension(nid_or_txt, pos?)*

Get X.509 `extension` matching the given [NID] to certificate, returns a
[resty.openssl.x509.extension](#restyopensslx509extension) instance and the found position.

If `last_pos` is defined, the function searchs from that position; otherwise it
finds from beginning. Index is 1-based.

```lua
local ext, pos, err = csr:get_extension("basicConstraints")
```

### csr:get_extensions

**syntax**: *extensions, err = csr:get_extensions()*

Return all extensions as a [resty.openssl.x509.extensions](#restyopensslx509extensions) instance.

### csr:add_extension

**syntax**: *ok, err = csr:add_extension(extension)*

Adds an X.509 `extension` to csr, the first argument must be a
[resty.openssl.x509.extension](#restyopensslx509extension) instance.

### csr:set_extension

**syntax**: *ok, err = csr:set_extension(extension)*

Adds an X.509 `extension` to csr, the first argument must be a
[resty.openssl.x509.extension](#restyopensslx509extension) instance.
The difference from [csr:add_extension](#csradd_extension) is that
in this function if a `extension` with same type already exists,
the old extension will be replaced.

Note this function is not thread-safe.

### csr:get_extension_critical

**syntax**: *ok, err = csr:get_extension_critical(nid_or_txt)*

Get critical flag of the X.509 `extension` matching the given [NID] from csr.

### csr:set_extension_critical

**syntax**: *ok, err = csr:set_extension_critical(nid_or_txt, crit?)*

Set critical flag of the X.509 `extension` matching the given [NID] to csr.

### csr:sign

**syntax**: *ok, err = csr:sign(pkey, digest?)*

Sign the certificate request using the private key specified by `pkey`, which must be a 
[resty.openssl.pkey](#restyopensslpkey) that stores private key. Optionally accept `digest`
parameter to set digest method, whichmust be a [resty.openssl.digest](#restyopenssldigest) instance.
Returns a boolean indicating if signing is successful and error if any.

### csr:verify

**syntax**: *ok, err = csr:verify(pkey)*

Verify the CSR signature using the public key specified by `pkey`, which
must be a [resty.openssl.pkey](#restyopensslpkey). Returns a boolean indicating if
verification is successful and error if any.

### csr:tostring

**syntax**: *str, err = csr:tostring(fmt?)*

Outputs certificate request in PEM-formatted text or DER-formatted binary.
The first argument can be a choice of `PEM` or `DER`; when omitted, this function outputs PEM by default.

### csr:to_PEM

**syntax**: *pem, err = csr:to_PEM(?)*

Outputs CSR in PEM-formatted text.

## resty.openssl.x509.crl

Module to interact with X509_CRL(certificate revocation list).

### crl.new

**syntax**: *crt, err = crl.new(txt?, fmt?, properties?)*

Creates a `crl` instance. `txt` can be **PEM** or **DER** formatted text;
`fmt` is a choice of `PEM`, `DER` to load specific format, or `*` for auto detect.

When `txt` is omitted, `new()` creates an empty `crl` instance.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### crl.dup

**syntax**: *crl, err = crl.dup(crl_ptr_cdata)*

Duplicates a `X509_CRL*` to create a new `crl` instance.

### crl.istype

**syntax**: *ok = crl.istype(table)*

Returns `true` if table is an instance of `crl`. Returns `false` otherwise.

### crl:get_\*, crl:set_\*

**syntax**: *ok, err = crl:set_**attribute**(instance)*

**syntax**: *instance, err = crl:get_**attribute**()*

Setters and getters for crl attributes share the same syntax.

| Attribute name | Type | Description |
| ------------   | ---- | ----------- |
| issuer_name   | [x509.name](#restyopensslx509name) | Issuer of the CRL |
| last_update    | number | Unix timestamp when CRL is not valid before |
| next_update     | number | Unix timestamp when CRL is not valid after |
| version       | number | Version of the certificate, value is one less than version. For example, `2` represents `version 3` |

Additionally, getters and setters for extensions are also available:

| Extension name | Type | Description |
| ------------   | ---- | ----------- |

For all extensions, `get_{extension}_critical` and `set_{extension}_critical` is also supported to
access the `critical` flag of the extension.

If the attribute is not found, getter will return `nil, nil`.

```lua
local crl, err = require("resty.openssl.crl").new()
err = crl:set_next_update(ngx.time())
local not_before, err = crl:get_next_update()
ngx.say(not_before)
-- outputs 1571875065
```

Note that user may also access the certain extension by [crl:get_extension](#crlget_extension) and
[crl:set_extension](#crlset_extension), while the later two function returns or requires
[extension](#restyopensslcrlextension) instead. User may use getter and setters listed here if modification
of current extensions is needed; use [crl:get_extension](#crlget_extension) or
[crl:set_extension](#crlset_extension) if user are adding or replacing the whole extension or
getters/setters are not implemented. If the getter returned a type of `crl.*` instance, it can be
converted to a [extension](#restyopensslcrlextension) instance by [extension:from_data](#extensionfrom_data),
and thus used by [crl:get_extension](#crlget_extension) and [crl:set_extension](#crlset_extension) 

### crl:get_signature_name, crl:get_signature_nid, crl:get_signature_digest_name

**syntax**: *sn, err = crl:get_signature_name()*

**syntax**: *nid, err = crl:get_signature_nid()*

**syntax**: *sn, err = crl:get_signature_digest_name()*

Return the [NID] or the short name (SN) of the signature of the CRL.

`crl:get_signature_digest_name` returns the short name of the digest algorithm
used to sign the certificate.

### crl:get_by_serial

**syntax**: *found_revoked, err = crl:get_by_serial(serial)*

Find if given `serial` is in the CRL, `serial` can be [bn](#resty.openssl.bn) instance, or
a hexadecimal string. Returns a table if found where:

```
{
  serial_number: serial number of the revoked cert in hexadecimal string,
  revoked_date: revoked date of the cert as unix timestamp
}
```

Returns `false` if not found; specially if a serial number is removed from CRL, then
`false, "not revoked (removeFromCRL)"` is returned.

### crl:get_extension

**syntax**: *extension, pos, err = crl:get_extension(nid_or_txt, last_pos?)*

Get X.509 `extension` matching the given [NID] to CRL, returns a
[resty.openssl.x509.extension](#restyopensslx509extension) instance and the found position.

If `last_pos` is defined, the function searchs from that position; otherwise it
finds from beginning. Index is 1-based.

### crl:add_extension

**syntax**: *ok, err = crl:add_extension(extension)*

Adds an X.509 `extension` to CRL, the first argument must be a
[resty.openssl.x509.extension](#restyopensslx509extension) instance.

### crl:set_extension

**syntax**: *ok, err = crl:set_extension(extension, last_pos?)*

Adds an X.509 `extension` to CRL, the first argument must be a
[resty.openssl.x509.extension](#restyopensslx509extension) instance.
The difference from [crl:add_extension](#crladd_extension) is that
in this function if a `extension` with same type already exists,
the old extension will be replaced.

If `last_pos` is defined, the function replaces the same extension from that position;
otherwise it finds from beginning. Index is 1-based. Returns `nil, nil` if not found.

Note this function is not thread-safe.

### crl:get_extension_critical

**syntax**: *ok, err = crl:get_extension_critical(nid_or_txt)*

Get critical flag of the X.509 `extension` matching the given [NID] from CRL.

### crl:set_extension_critical

**syntax**: *ok, err = crl:set_extension_critical(nid_or_txt, crit?)*

Set critical flag of the X.509 `extension` matching the given [NID] to CRL.

### crl:add_revoked

**syntax**: *ok, err = crl:add_revoked(revoked)*

Adds a [resty.openssl.x509.revoked](#restyopensslx509revoked) instance to the CRL.

### crl:sign

**syntax**: *ok, err = crl:sign(pkey, digest?)*

Sign the CRL using the private key specified by `pkey`, which must be a 
[resty.openssl.pkey](#restyopensslpkey) that stores private key. Optionally accept `digest`
parameter to set digest method, whichmust be a [resty.openssl.digest](#restyopenssldigest) instance.
Returns a boolean indicating if signing is successful and error if any.

### crl:verify

**syntax**: *ok, err = crl:verify(pkey)*

Verify the CRL signature using the public key specified by `pkey`, which
must be a [resty.openssl.pkey](#restyopensslpkey). Returns a boolean indicating if
verification is successful and error if any.

### crl:tostring

**syntax**: *str, err = crl:tostring(fmt?)*

Outputs CRL in PEM-formatted text or DER-formatted binary.
The first argument can be a choice of `PEM` or `DER`; when omitted, this function outputs PEM by default.

### crl:text

**syntax**: *str, err = crl:text()*

Outputs CRL in a human-readable format.

### crl:to_PEM

**syntax**: *pem, err = crl:to_PEM()*

Outputs the CRL in PEM-formatted text.

### crl:__metamethods

**syntax**: *for i, revoked in ipairs(crl)*

**syntax**: *len = #crl*

**syntax**: *revoked = crl[i]*

Access the revoked list as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag; otherwise use `all`, `each`, `index` and `count`
instead.

See also [functions for stack-like objects](#functions-for-stack-like-objects).

Each returned object is a table where:

```
{
  serial_number: serial number of the revoked cert in hexadecimal string,
  revoked_date: revoked date of the cert as unix timestamp
}
```

```lua
local f = io.open("t/fixtures/TrustAsiaEVTLSProCAG2.crl"):read("*a")
local crl = assert(require("resty.openssl.x509.crl").new(f))

for _, obj in ipairs(crl) do
  ngx.say(require("cjson").encode(obj))
end
-- outputs '{"revocation_date":1577753344,"serial_number":"09159859CAC0C90203BB34C5A012C2A3"}'
```

## resty.openssl.x509.name

Module to interact with X.509 names.

### name.new

**syntax**: *name, err = name.new()*

Creates an empty `name` instance.

### name.dup

**syntax**: *name, err = name.dup(name_ptr_cdata)*

Duplicates a `X509_NAME*` to create a new `name` instance.

### name.istype

**syntax**: *ok = name.istype(table)*

Returns `true` if table is an instance of `name`. Returns `false` otherwise.

### name:add

**syntax**: *name, err = name:add(nid_text, txt)*

Adds an ASN.1 object to `name`. First arguments in the *text representation* of [NID].
Second argument is the plain text value for the ASN.1 object.

Returns the name instance itself on success, or `nil` and an error on failure.

This function can be called multiple times in a chained fashion.

```lua
local name, err = require("resty.openssl.x509.name").new()
local _, err = name:add("CN", "example.com")

_, err = name
    :add("C", "US")
    :add("ST", "California")
    :add("L", "San Francisco")

```

### name:find

**syntax**: *obj, pos, err = name:find(nid_text, last_pos?)*

Finds the ASN.1 object with the given *text representation* of [NID] from the
postition of `last_pos`. By omitting the `last_pos` parameter, `find` finds from the beginning.

Returns the object in a table as same format as decribed [here](#name__metamethods), the position
of the found object and error if any. Index is 1-based. Returns `nil, nil` if not found.

```lua
local name, err = require("resty.openssl.x509.name").new()
local _, err = name:add("CN", "example.com")
                    :add("CN", "example2.com")

local obj, pos, err = name:find("CN")
ngx.say(obj.blob, " at ", pos)
-- outputs "example.com at 1"
local obj, pos, err = name:find("2.5.4.3", 1)
ngx.say(obj.blob, " at ", pos)
-- outputs "example2.com at 2"
```

### name:tostring

**syntax**: *txt = name:tostring()*

Outputs name in a text representation.

```lua
local name, err = require("resty.openssl.x509.name").new()
local _, err = name:add("CN", "example.com")
                    :add("CN", "example2.com")

ngx.say(name:tostring())
-- outputs "CN=example.com/CN=example2.com"
```

### name:__metamethods

**syntax**: *for k, obj in pairs(name)*

**syntax**: *len = #name*

**syntax**: *k, v = name[i]*

Access the underlying objects as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag; otherwise use `all`, `each`, `index` and `count`
instead.

See also [functions for stack-like objects](#functions-for-stack-like-objects).

Each returned object is a table where:

```
{
  id: OID of the object,
  nid: NID of the object,
  sn: short name of the object,
  ln: long name of the object,
  blob: value of the object,
}
```

```lua
local name, err = require("resty.openssl.x509.name").new()
local _, err = name:add("CN", "example.com")

for k, obj in pairs(name) do
  ngx.say(k, ":", require("cjson").encode(obj))
end
-- outputs 'CN: {"sn":"CN","id":"2.5.4.3","nid":13,"blob":"3.example.com","ln":"commonName"}'
```

## resty.openssl.x509.altname

Module to interact with GENERAL_NAMES, an extension to X.509 names.

### altname.new

**syntax**: *altname, err = altname.new()*

Creates an empty `altname` instance.

### altname.dup

**syntax**: *altname, err = altname.dup(altname_ptr_cdata)*

Duplicates a `STACK_OF(GENERAL_NAMES)` to create a new `altname` instance. The function creates a new
stack but won't duplicates elements in the stack.

### altname.istype

**syntax**: *altname = digest.istype(table)*

Returns `true` if table is an instance of `altname`. Returns `false` otherwise.

### altname:add

**syntax**: *altname, err = altname:add(key, value)*

Adds a name to altname stack, first argument is case-insensitive and can be one of

    RFC822Name
    RFC822
    Email
    UniformResourceIdentifier
    URI
    DNSName
    DNS
    IP
    IPAddress

This function can be called multiple times in a chained fashion.

### altname:tostring

**syntax**: *txt = altname:tostring()*

Outputs altname in a text representation.

```lua
local altname, err = require("resty.openssl.x509.altname").new()

_, err = altname
    :add("DNS", "2.example.com")
    :add("DnS", "3.example.com")

ngx.say(altname:tostring())
-- outputs "DNS=2.example.com/DNS=3.example.com"
```

### altname:__metamethods

**syntax**: *for k, obj in pairs(altname)*

**syntax**: *len = #altname*

**syntax**: *k, v = altname[i]*

Access the underlying objects as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag; otherwise use `all`, `each`, `index` and `count`
instead.

See also [functions for stack-like objects](#functions-for-stack-like-objects).

Only the following types are decoded, other types are decoded as `"TYPE:<unsupported>"`:

    RFC822Name / Email
    URI
    DNS
    DirName

## resty.openssl.x509.extension

Module to interact with every X.509 extensions.

This module is particular useful to create extensions not supported by
`x509.*` modules or custom extensions.

### extension.new

**syntax**: *ext, err = extension.new(name, value, data?)*

Creates a new `extension` instance. `name` and `value` are strings in OpenSSL
[arbitrary extension format](https://www.openssl.org/docs/manmaster/man5/x509v3_config.html).

`data` can be a table, string or nil. Where `data` is a table, the following key will be looked up:

```lua
data = {
  issuer = resty.openssl.x509 instance,
  subject = resty.openssl.x509 instance,
  request = resty.openssl.x509.csr instance,
  crl = resty.openssl.x509.crl instance,
  issuer_pkey = resty.openssl.pkey instance, -- >= OpenSSL 3.0
}
```

From OpenSSL 3.0, `issuer_pkey` can be specified as a fallback source for
generating the authority key identifier extension when `issuer` is same as `subject`.

When `data` is a string, it's the full nconf string. Using section lookup from `value` to
`data` is also supported.

<details>
<summary>Example usages:</summary>

```lua
local extension = require("resty.openssl.x509.extension")
-- extendedKeyUsage=serverAuth,clientAuth
local ext, err = extension.new("extendedKeyUsage", "serverAuth,clientAuth")
-- crlDistributionPoints=URI:http://myhost.com/myca.crl
ext, err = extension.new("crlDistributionPoints", "URI:http://myhost.com/myca.crl")
-- with section lookup
ext, err = extension.new(
  "crlDistributionPoints", "crldp1_section",
  [[
  [crldp1_section]
  fullname=URI:http://myhost.com/myca.crl
  CRLissuer=dirName:issuer_sect
  reasons=keyCompromise, CACompromise

  [issuer_sect]
  C=UK
  O=Organisation
  CN=Some Name
  ]]
)
-- combine section lookup with other value
ext, err = extension.new(
"certificatePolicies", "ia5org,1.2.3.4,1.5.6.7.8,@polsect",
  [[
  [polsect]
  policyIdentifier = 1.3.5.8
  CPS.1="http://my.host.name/"
  CPS.2="http://my.your.name/"
  userNotice.1=@notice

  [notice]
  explicitText="Explicit Text Here"
  organization="Organisation Name"
  noticeNumbers=1,2,3,4
 ]]
))
-- subjectKeyIdentifier=hash
local x509, err = require("resty.openssl.x509").new()
ext, err =  extension.new("subjectKeyIdentifier", "hash", {
    subject = x509
})
```
</details>

See [examples/tls-alpn-01.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/tls-alpn-01.lua)
for an example to create extension with an unknown nid.

### extension.dup

**syntax**: *ext, err = extension.dup(extension_ptr_cdata)*

Creates a new `extension` instance from `X509_EXTENSION*` pointer.

### extension.from_der

**syntax**: *ext, ok = extension.from_der(der, nid_or_txt, crit?)*

Creates a new `extension` instance. `der` is the ASN.1 encoded string to be
set for the extension.

`nid_or_txt` is a number or text representation of [NID] and
`crit` is the critical flag of the extension.

See [examples/tls-alpn-01.lua](https://github.com/fffonion/lua-resty-openssl/blob/master/examples/tls-alpn-01.lua)
for an example to create extension with an unknown nid.

### extension:to_der

**syntax**: *der, ok = extension:to_der()*

Returns the ASN.1 encoded (DER) value of the extension.

`nid_or_txt` is a number or text representation of [NID]. Note `DER` is a binary
encoding format. Consider using [extension:text](#extensiontext) for human readable
or printable output.

### extension.from_data

**syntax**: *ext, ok = extension.from_data(table, nid_or_txt, crit?)*

Creates a new `extension` instance. `table` can be instance of:

- [x509.altname](#restyopensslx509altname)
- [x509.extension.info_access](#restyopensslx509extensioninfo_access)
- [x509.extension.dist_points](#restyopensslx509extensiondist_points)

`nid_or_txt` is a number or text representation of [NID] and
`crit` is the critical flag of the extension.

### extension.to_data

**syntax**: *ext, ok = extension:to_data(nid_or_txt)*

Convert the `extension` to another wrapper instance. Currently supported following:

- [x509.altname](#restyopensslx509altname)

`nid_or_txt` is a number or text representation of [NID].

### extension.istype

**syntax**: *ok = extension.istype(table)*

Returns `true` if table is an instance of `extension`. Returns `false` otherwise.

### extension:get_extension_critical

**syntax**: *crit, err = extension:get_extension_critical()*

Returns `true` if extension is critical. Returns `false` otherwise.

### extension:set_extension_critical

**syntax**: *ok, err = extension:set_extension_critical(crit)*

Set the critical flag of the extension.

### extension:get_object

**syntax**: *obj = extension:get_object()*

Returns the name of extension as ASN.1 Object. User can further use helper functions in
[resty.openssl.objects](#restyopensslobjects) to print human readable texts.

### extension:text

**syntax**: *txt, err = extension:text()*

Returns the text representation of extension. This functions calls `X509V3_EXT_print` under the hood,
and fallback to `ASN1_STRING_print` if the former failed. It thus has exact same output with that
of `openssl x509 -text`.

```lua
local objects = require "resty.openssl.objects"
ngx.say(cjson.encode(objects.obj2table(extension:get_object())))
-- outputs '{"ln":"X509v3 Subject Key Identifier","nid":82,"sn":"subjectKeyIdentifier","id":"2.5.29.14"}'
ngx.say(extension:text())
-- outputs "C9:C2:53:61:66:9D:5F:AB:25:F4:26:CD:0F:38:9A:A8:49:EA:48:A9"
```

### extension:tostring

**syntax**: *txt, err = extension:tostring()*

Same as [extension:text](#extensiontext).

## resty.openssl.x509.extension.dist_points

Module to interact with CRL Distribution Points(DIST_POINT stack).

### dist_points.new

**syntax**: *dp, err = dist_points.new()*

Creates a new `dist_points` instance.

### dist_points.dup

**syntax**: *dp, err = dist_points.dup(dist_points_ptr_cdata)*

Duplicates a `STACK_OF(DIST_POINT)` to create a new `dist_points` instance. The function creates a new
stack but won't duplicates elements in the stack.

### dist_points.istype

**syntax**: *ok = dist_points.istype(table)*

Returns `true` if table is an instance of `dist_points`. Returns `false` otherwise.

### dist_points:__metamethods

**syntax**: *for i, obj in ipairs(dist_points)*

**syntax**: *len = #dist_points*

**syntax**: *obj = dist_points[i]*

Access the underlying objects as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag; otherwise use `all`, `each`, `index` and `count`
instead.

See also [functions for stack-like objects](#functions-for-stack-like-objects).

Each object returned when iterrating dist_points instance is a [x509.altname](#restyopensslx509altname)
instance.

```lua
local x = x509.new(io.open("/path/to/a_cert_has_dist_points.crt"):read("*a"))

local cdp = x:get_crl_distribution_points()

local an = cdp[1]
ngx.say(an:tostring())
-- or any other function for resty.openssl.x509.altname

for _, an in ipairs(cdp) do
  ngx.say(an:tostring())
end
```

## resty.openssl.x509.extension.info_access

Module to interact with Authority Information Access data (AUTHORITY_INFO_ACCESS, ACCESS_DESCRIPTION stack).

### info_access.new

**syntax**: *aia, err = info_access.new()*

Creates a new `info_access` instance.

### info_access.dup

**syntax**: *aia, err = info_access.dup(info_access_ptr_cdata)*

Duplicates a `AUTHORITY_INFO_ACCESS` to create a new `info_access` instance. The function creates a new
stack but won't duplicates elements in the stack.

### info_access.istype

**syntax**: *ok = info_access.istype(table)*

Returns `true` if table is an instance of `info_access`. Returns `false` otherwise.

### info_access:add

**syntax**: *ok, err = info_access:add(x509)*

Add a `x509` object to the info_access. The first argument must be a
[resty.openssl.x509](#restyopensslx509) instance.

### info_access:__metamethods

**syntax**: *for i, obj in ipairs(info_access)*

**syntax**: *len = #info_access*

**syntax**: *obj = info_access[i]*

Access the underlying objects as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag; otherwise use `all`, `each`, `index` and `count`
instead.

See also [functions for stack-like objects](#functions-for-stack-like-objects).

Each object returned when iterrating dist_points instance is a table of [NID] type and values.

```lua
local cjson = require("cjosn")
local x509 = require("resty.openssl.x509")
local crt = x509.new(io.open("/path/to/a_cert_has_info_access.crt"):read("*a"))

local aia = crt:get_info_access()

ngx.say(cjson.encode(aia[1]))
-- outputs '[178,"URI","http:\/\/ocsp.starfieldtech.com\/"]'

for _, a in ipairs(aia) do
  ngx.say(cjson.encode(a))
end
```

## resty.openssl.x509.extensions

Module to interact with X.509 Extension stack.

### extensions.new

**syntax**: *ch, err = extensions.new()*

Creates a new `extensions` instance.

### extensions.dup

**syntax**: *ch, err = extensions.dup(extensions_ptr_cdata)*

Duplicates a `STACK_OF(X509_EXTENSION)` to create a new `extensions` instance. The function creates a new
stack but won't duplicates elements in the stack.

### extensions.istype

**syntax**: *ok = extensions.istype(table)*

Returns `true` if table is an instance of `extensions`. Returns `false` otherwise.

### extensions:add

**syntax**: *ok, err = extensions:add(x509)*

Add a `x509` object to the extensions. The first argument must be a
[resty.openssl.x509](#restyopensslx509) instance.

### extensions:__metamethods

**syntax**: *for i, obj in ipairs(extensions)*

**syntax**: *len = #extensions*

**syntax**: *obj = extensions[i]*

Access the underlying objects as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag; otherwise use `all`, `each`, `index` and `count`
instead.

See also [functions for stack-like objects](#functions-for-stack-like-objects).

## resty.openssl.x509.chain

Module to interact with X.509 stack.

### chain.new

**syntax**: *ch, err = chain.new()*

Creates a new `chain` instance.

### chain.dup

**syntax**: *ch, err = chain.dup(chain_ptr_cdata)*

Duplicates a `STACK_OF(X509)` to create a new `chain` instance. The function creates a new
stack and increases reference count for all elements by 1. But it won't duplicate the elements
themselves.

### chain.istype

**syntax**: *ok = chain.istype(table)*

Returns `true` if table is an instance of `chain`. Returns `false` otherwise.

### chain:add

**syntax**: *ok, err = chain:add(x509)*

Add a `x509` object to the chain. The first argument must be a
[resty.openssl.x509](#restyopensslx509) instance.

### chain:__metamethods

**syntax**: *for i, obj in ipairs(chain)*

**syntax**: *len = #chain*

**syntax**: *obj = chain[i]*

Access the underlying objects as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag; otherwise use `all`, `each`, `index` and `count`
instead.

See also [functions for stack-like objects](#functions-for-stack-like-objects).

## resty.openssl.x509.store

Module to interact with X.509 certificate store (X509_STORE).

### store.new

**syntax**: *st, err = store.new(properties?)*

Creates a new `store` instance.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### store.istype

**syntax**: *ok = store.istype(table)*

Returns `true` if table is an instance of `store`. Returns `false` otherwise.

### store:use_default

**syntax**: *ok, err = store:use_default(properties?)*

Loads certificates into the X509_STORE from the hardcoded default paths.

Note that to load "default" CAs correctly, usually you need to install a CA
certificates bundle. For example, the package in Debian/Ubuntu is called `ca-certificates`.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### store:add

**syntax**: *ok, err = store:add(x509_or_crl, skip_set_crl_check_flags?)*

Adds a X.509 or a CRL object into store.
The argument must be a [resty.openssl.x509](#restyopensslx509) instance or a
[resty.openssl.x509.crl](#restyopensslx509crl) instance.

By default, adding a CRL object will automatically set the flag to store
`X509_V_FLAG_CRL_CHECK`. Setting the second optional argument to `true` will
skip settting the flags.

### store:load_file

**syntax**: *ok, err = store:load_file(path, properties?)*

Loads a X.509 certificate on file system into store.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### store:load_directory

**syntax**: *ok, err = store:load_directory(path, properties?)*

Loads a directory of X.509 certificates on file system into store. The certificates in the directory
must be in hashed form, as documented in
[X509_LOOKUP_hash_dir(3)](https://www.openssl.org/docs/manmaster/man3/X509_LOOKUP_hash_dir.html).

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

### store:set_purpose

**syntax**: *ok, err = store:set_purpose(purpose)*

Set the X509_STORE to match Key Usage and Extendend Key Usage when verifying the cert.
Possible values are:

```
	sslclient 	SSL client
	sslserver 	SSL server
	nssslserver	Netscape SSL server
	smimesign 	S/MIME signing
	smimeencrypt	S/MIME encryption
	crlsign   	CRL signing
	any       	Any Purpose
	ocsphelper	OCSP helper
	timestampsign	Time Stamp signing
```

Normally user should use `verify_method` parameter of [store:verify](#storeverify) unless the purpose
is not included in the default verify methods.

### store:set_depth

**syntax**: *ok, err = store:set_depth(depth)*

Set the verify depth.

### store:set_flags

**syntax**: *ok, err = store:set_flags(flag1, flag2, ...)*

Set the verify flags, available via `store.verify_flags` table:

```
    X509_V_FLAG_CB_ISSUER_CHECK              = 0x0,   -- Deprecated
    X509_V_FLAG_USE_CHECK_TIME               = 0x2,
    X509_V_FLAG_CRL_CHECK                    = 0x4,
    X509_V_FLAG_CRL_CHECK_ALL                = 0x8,
    X509_V_FLAG_IGNORE_CRITICAL              = 0x10,
    X509_V_FLAG_X509_STRICT                  = 0x20,
    X509_V_FLAG_ALLOW_PROXY_CERTS            = 0x40,
    X509_V_FLAG_POLICY_CHECK                 = 0x80,
    X509_V_FLAG_EXPLICIT_POLICY              = 0x100,
    X509_V_FLAG_INHIBIT_ANY                  = 0x200,
    X509_V_FLAG_INHIBIT_MAP                  = 0x400,
    X509_V_FLAG_NOTIFY_POLICY                = 0x800,
    X509_V_FLAG_EXTENDED_CRL_SUPPORT         = 0x1000,
    X509_V_FLAG_USE_DELTAS                   = 0x2000,
    X509_V_FLAG_CHECK_SS_SIGNATURE           = 0x4000,
    X509_V_FLAG_TRUSTED_FIRST                = 0x8000,
    X509_V_FLAG_SUITEB_128_LOS_ONLY          = 0x10000,
    X509_V_FLAG_SUITEB_192_LOS               = 0x20000,
    X509_V_FLAG_SUITEB_128_LOS               = 0x30000,
    X509_V_FLAG_PARTIAL_CHAIN                = 0x80000,
    X509_V_FLAG_NO_ALT_CHAINS                = 0x100000,
    X509_V_FLAG_NO_CHECK_TIME                = 0x200000,
```


```lua
store:set_flags(store.verify_flags.X509_V_FLAG_PARTIAL_CHAIN)

store:set_flags(store.verify_flags.X509_V_FLAG_PARTIAL_CHAIN,
                store.verify_flags.X509_V_FLAG_NO_CHECK_TIME)

store:set_flags(store.verify_flags.X509_V_FLAG_PARTIAL_CHAIN +
                store.verify_flags.X509_V_FLAG_NO_CHECK_TIME)
```

See [X509_VERIFY_PARAM_set_flags(3)](https://www.openssl.org/docs/manmaster/man3/X509_VERIFY_PARAM_set_flags.html)
for explanation of each flag.

### store:verify

**syntax**: *chain, err = store:verify(x509, chain?, return_chain?, properties?, verify_method?, verify_flags?)*

Verifies a X.509 object with the store. The first argument must be
[resty.openssl.x509](#restyopensslx509) instance. Optionally accept a validation chain as second
argument, which must be a [resty.openssl.x509.chain](#restyopensslx509chain) instance.

If verification succeed, and `return_chain` is set to true, returns the proof of validation as a 
[resty.openssl.x509.chain](#restyopensslx509chain); otherwise
returns `true` only. If verification failed, returns `nil` and error explaining the reason.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

`verify_method` can be set to use predefined verify parameters such as `"default"`, `"pkcs7"`,
`"smime_sign"`, `"ssl_client"` and `"ssl_server"`. This set corresponding `purpose`, `trust` and
couple of other defaults but **does not** override the parameters set from
[store:set_purpose](#storeset_purpose).

`verify_flags` paramter is the additional verify flags to be set. See [store:set_flags](#storeset_flags)
for all available flags.

### store:check_revocation

**syntax**: *ok, err = store:check_revocation(verified_chain, properties?)*

Only does the revocation check. The first argument `verified_chain` must be a
[resty.openssl.x509.chain](#restyopensslx509chain) instance which could be returned from
`store_ctx:verify` or be built by yourself. Note the first cert needs to be the end entity
certificate you want to check and the second cert needs to be its issuer.

Staring from OpenSSL 3.0, this function accepts an optional `properties` parameter
to explictly select provider to fetch algorithms.

Returns `true` when the certificate isn't revoked,
otherwise returns `nil` and error explaining the reason.

## resty.openssl.x509.revoked

Module to interact with X509_REVOKED.

### revoked.new

**syntax**: *ch, err = revoked.new(serial_number, time, reason)*

Creates a new `revoked` instance. `serial_number` can be either a [resty.openssl.bn](#restyopensslbn)
instance or a number. `time` and `reason` must be numbers.

### revoked.istype

**syntax**: *ok = revoked.istype(table)*

Returns `true` if table is an instance of `revoked`. Returns `false` otherwise.

## resty.openssl.ssl

Module to interact with SSL connection.

**This module is currently considered experimental.**

**Note: to use this module in production, user is encouraged to compile [lua-resty-openssl-aux-module](https://github.com/fffonion/lua-resty-openssl-aux-module).**

### ssl.from_request

**syntax**: *sess, err = ssl.from_request()*

Wraps the `SSL*` instance from current downstream request.

### ssl.from_socket

**syntax**: *sess, err = ssl.from_socket(sock)*

Wraps the `SSL*` instance from a TCP cosocket, the cosocket must have already
been called `sslhandshake`.

### ssl:get_peer_certificate

**syntax**: *x509, err = ssl:get_peer_certificate()*

Return the peer certificate as a [x509](#restyopensslx509) instance. Depending on the type
of `ssl`, peer certificate means the server certificate on client side, or the client certificate
on server side.

This function should be called after SSL handshake.

### ssl:get_peer_cert_chain

**syntax**: *chain, err = ssl:get_peer_certificate()*

Return the whole peer certificate chain as a [x509.chain](#restyopensslx509chain) instance.
Depending on the type of `ssl`, peer certificate means the server certificate on client side,
or the client certificate on server side.

This function should be called after SSL handshake.

### ssl:set_ciphersuites, ssl:set_cipher_list

**syntax**: *ok, err = ssl:set_ciphersuites(cipher_suite)*
**syntax**: *ok, err = ssl:set_cipher_list(cipher_list)*

Set the cipher suites string used in handshake. Use `ssl:set_ciphersuites
for TLSv1.3 and `ssl:set_cipher_list` for lower.

This function should be called before SSL handshake; for server this means this function
is only effective in `ssl_certificate_by` or `ssl_client_hello_by` phases.

### ssl:get_ciphers

**syntax**: *ciphers, err = ssl:get_ciphers()*

Get the cipher list string used in handshake as a string.

### ssl:get_cipher_name

**syntax**: *cipher_name, err = ssl:get_cipher_name()*

Get the negotiated cipher name as a string.

This function should be called after SSL handshake.

### ssl:set_timeout

**syntax**: *ok, err = ssl:set_timeout(tm)*

Set the timeout value for current session in seconds `tm`.

### ssl:get_timeout

**syntax**: *tm, err = ssl:set_timeout(tm)*

Get the timeout value for current session in seconds.

### ssl:set_verify

**syntax**: *ok, err = ssl:set_verify(mode)*

Set the verify mode in current session. Available modes are:

```
  ssl.SSL_VERIFY_NONE                 = 0x00,
  ssl.SSL_VERIFY_PEER                 = 0x01,
  ssl.SSL_VERIFY_FAIL_IF_NO_PEER_CERT = 0x02,
  ssl.SSL_VERIFY_CLIENT_ONCE          = 0x04,
  ssl.SSL_VERIFY_POST_HANDSHAKE       = 0x08,
```

This function should be called before SSL handshake; for server this means this function
is only effective in `ssl_certificate_by` or `ssl_client_hello_by` phases.

### ssl:add_client_ca

**syntax**: *ok, err = ssl:add_client_ca(x509)*

Add the CA name extracted from `x509` to the list of CAs sent to the client
when requesting a client certificate. `x509` is a [x509](#resty.openssl.x509)
instance. This function doesn't affect the verification result of client certificate.

This function should be called before SSL handshake; for server this means this function
is only effective in `ssl_certificate_by` or `ssl_client_hello_by` phases.

### ssl:set_options

**syntax**: *bitmask, err = ssl:set_options(option, ...)*

Set one or more options in current session. Available options are:

<details>
<summary>SSL options</summary>

```
  ssl.SSL_OP_NO_EXTENDED_MASTER_SECRET                = 0x00000001,
  ssl.SSL_OP_CLEANSE_PLAINTEXT                        = 0x00000002,
  ssl.SSL_OP_LEGACY_SERVER_CONNECT                    = 0x00000004,
  ssl.SSL_OP_TLSEXT_PADDING                           = 0x00000010,
  ssl.SSL_OP_SAFARI_ECDHE_ECDSA_BUG                   = 0x00000040,
  ssl.SSL_OP_IGNORE_UNEXPECTED_EOF                    = 0x00000080,
  ssl.SSL_OP_DISABLE_TLSEXT_CA_NAMES                  = 0x00000200,
  ssl.SSL_OP_ALLOW_NO_DHE_KEX                         = 0x00000400,
  ssl.SSL_OP_DONT_INSERT_EMPTY_FRAGMENTS              = 0x00000800,
  ssl.SSL_OP_NO_QUERY_MTU                             = 0x00001000,
  ssl.SSL_OP_COOKIE_EXCHANGE                          = 0x00002000,
  ssl.SSL_OP_NO_TICKET                                = 0x00004000,
  ssl.SSL_OP_CISCO_ANYCONNECT                         = 0x00008000,
  ssl.SSL_OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION   = 0x00010000,
  ssl.SSL_OP_NO_COMPRESSION                           = 0x00020000,
  ssl.SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION        = 0x00040000,
  ssl.SSL_OP_NO_ENCRYPT_THEN_MAC                      = 0x00080000,
  ssl.SSL_OP_ENABLE_MIDDLEBOX_COMPAT                  = 0x00100000,
  ssl.SSL_OP_PRIORITIZE_CHACHA                        = 0x00200000,
  ssl.SSL_OP_CIPHER_SERVER_PREFERENCE                 = 0x00400000,
  ssl.SSL_OP_TLS_ROLLBACK_BUG                         = 0x00800000,
  ssl.SSL_OP_NO_ANTI_REPLAY                           = 0x01000000,
  ssl.SSL_OP_NO_SSLv3                                 = 0x02000000,
  ssl.SSL_OP_NO_TLSv1                                 = 0x04000000,
  ssl.SSL_OP_NO_TLSv1_2                               = 0x08000000,
  ssl.SSL_OP_NO_TLSv1_1                               = 0x10000000,
  ssl.SSL_OP_NO_TLSv1_3                               = 0x20000000,
  ssl.SSL_OP_NO_DTLSv1                                = 0x04000000,
  ssl.SSL_OP_NO_DTLSv1_2                              = 0x08000000,
  ssl.SSL_OP_NO_RENEGOTIATION                         = 0x40000000,
  ssl.SSL_OP_CRYPTOPRO_TLSEXT_BUG                     = 0x80000000,
```
</details>

Multiple options can be passed in seperatedly, or in a bitwise or bitmask.

```lua
assert(ssl:set_options(bit.bor(ssl.SSL_OP_NO_TLSv1_1, ssl.SSL_OP_NO_TLSv1_2)))
-- same as
assert(ssl:set_options(ssl.SSL_OP_NO_TLSv1_1, ssl.SSL_OP_NO_TLSv1_2))
```

Returns the options of current session in bitmask.

This function should be called before SSL handshake; for server this means this function
is only effective in `ssl_client_hello_by` phase.


### ssl:get_options

**syntax**: *bitmask, err = ssl:get_options(readable?)*

Get the options for current session. If `readable` is not set or set to `false`, the function
return the bit mask for all optinos; if `readable` is set to `true,` the function returns
a sorted Lua table containing literals for all options.

### ssl:clear_options

**syntax**: *bitmask, err = ssl:clear_options(option, ...)*

Clear one or more options in current session.
Available options are same as that in [ssl:set_options](#sslset_options).

Multiple options can be passed in seperatedly, or in a bitwise or bitmask.

```lua
assert(ssl:clear_options(bit.bor(ssl.SSL_OP_NO_TLSv1_1, ssl.SSL_OP_NO_TLSv1_2)))
-- same as
assert(ssl:clear_options(ssl.SSL_OP_NO_TLSv1_1, ssl.SSL_OP_NO_TLSv1_2))
```

Returns the options of current session in bitmask.

This function should be called before SSL handshake; for server this means this function
is only effective in `ssl_client_hello_by` phase.

### ssl:set_protocols

**syntax**: *bitmask, err = ssl:set_protocols(protocol, ...)*

Set avaialable protocols for handshake, this is a convenient function that
calls [ssl:set_options](#sslset_options) and [ssl:clear_options](#sslclear_options) to
set appropriate options.

Returns the options of current session in bitmask.

This function should be called before SSL handshake; for server this means this function
is only effective in `ssl_client_hello_by` phase.

```lua
assert(ssl:set_protocols("TLSv1.1", "TLSv1.2"))
-- same as
assert(ssl:set_options(ssl.SSL_OP_NO_SSL_MASK))
assert(ssl:clear_options(ssl.SSL_OP_NO_TLSv1_1, ssl.SSL_OP_NO_TLSv1_2))
```

## resty.openssl.ssl_ctx

Module to interact with SSL_CTX context.

**This module is currently considered experimental.**

**Note: to use this module in production, user is encouraged to compile [lua-resty-openssl-aux-module](https://github.com/fffonion/lua-resty-openssl-aux-module).**

### ssl_ctx.from_request

**syntax**: *ctx, err = ssl_ctx.from_request()*

Wraps the `SSL_CTX*` instance from current downstream request.

### ssl_ctx.from_socket

**syntax**: *sess, err = ssl_ctx.from_socket(sock)*

Wraps the `SSL_CTX*` instance from a TCP cosocket, the cosocket must have already
been called `sslhandshake`.

### ssl_ctx:set_alpns

**syntax**: *ok, err = ssl_ctx:set_alpns(alpn, ...)*

Set the ALPN list to be negotiated with peer. Each `alpn` is the plaintext
literal for the protocol, like `"h2"`.

## Functions for stack-like objects

### metamethods

**syntax**: *for k, obj in pairs(x)*

**syntax**: *for k, obj in ipairs(x)*

**syntax**: *len = #x*

**syntax**: *obj = x[i]*

Access the underlying objects as it's a Lua table. Make sure your LuaJIT compiled
with `-DLUAJIT_ENABLE_LUA52COMPAT` flag.

Each object may only support either `pairs` or `ipairs`. Index is 1-based.

```lua
local name, err = require("resty.openssl.x509.name").new()
local _, err = name:add("CN", "example.com")

for k, obj in pairs(name) do
  ngx.say(k, ":", require("cjson").encode(obj))
end
-- outputs 'CN: {"sn":"CN","id":"2.5.4.3","nid":13,"blob":"3.example.com","ln":"commonName"}'
```

### each

**syntax**: *iter = x:each()*

Return an iterator to traverse objects. Use this while `LUAJIT_ENABLE_LUA52COMPAT` is not enabled.

```lua
local name, err = require("resty.openssl.x509.name").new()
local _, err = name:add("CN", "example.com")

local iter = name:each()
while true do
  local k, obj = iter()
  if not k then
    break
  end
end
```

### all

**syntax**: *objs, err = x:all()*

Returns all objects in the table. Use this while `LUAJIT_ENABLE_LUA52COMPAT` is not enabled.

### count

**syntax**: *len = x:count()*

Returns count of objects of the table. Use this while `LUAJIT_ENABLE_LUA52COMPAT` is not enabled.

### index

**syntax**: *obj = x:index(i)*

Returns objects at index of `i` of the table, index is 1-based. If index is out of bound, `nil` is returned.

## General rules on garbage collection

- When a type is added or returned to another type, it's internal cdata is always copied.
```lua
local name = require("resty.openssl.x509.name"):add("CN", "example.com")
local x509 = require("resty.openssl.x509").new()
-- `name` is copied when added to x509
x509:set_subject_name(name)

name:add("L", "Mars")
-- subject_name in x509 will not be modified
```
- The creator set the GC handler; the user must not free it.
- For a stack:
  - If it's created by `new()`: set GC handler to sk_TYPE_pop_free 
    - The gc handler for elements being added to stack should not be set. Instead, rely on the gc
      handler of the stack to free each individual elements.
  - If it's created by `dup()` (shallow copy):
    - If elements support reference counter (like X509): increase ref count for all elements by 1;
      set GC handler to sk_TYPE_pop_free.
    - If not, set GC handler to sk_free
      - Additionally, the stack duplicates the element when it's added to stack, a GC handler for the duplicate
        must be set. But a reference should be kept in Lua land to prevent premature
        gc of individual elements. (See x509.altname).
    - Shallow copy for stack is fine because in current design user can't modify the element in the
      stack directly. Each elemente is duplicated when added to stack and when returned.

## Generic EVP parameter getter/setter

Starting from OpenSSL 3.0, this library provides a genric interface to get and set abitrary parameters
from underlying implementation. This works for [cipher](#resty.openssl.cipher),
[pkey](#resty.openssl.pkey), [digest](#resty.openssl.digest), [mac](#resty.openssl.mac) and
[kdf](#resty.openssl.kdf).

Some can be used to provide equal results with existing functions, for example the following
code produces same result.

```lua
local pkey = require("resty.openssl.pkey").new({ type = "EC" })
pkey:get_param("priv", nil, "bn") == pkey:get_parameters().private

local cipher = require("resty.openssl.cipher").new("aes-256-gcm")
cipher:encrypt(string.rep("0", 32), string.rep("0", "12"), "secret", false, "aad")
cipher:get_param("tag", 16) == cipher:get_aead_tag()
```

### gettable_params

**syntax**: *schema, err = x:gettable_params(raw?)*

Returns the readable schema as a Lua table for all gettable params.
When `raw` is set to true, the function returns the raw schema instead.

### settable_params

**syntax**: *schema, err = x:settable_params(raw?)*

Returns the readable schema as a Lua table for all settable params.
When `raw` is set to true, the function returns the raw schema instead.

```lua
local c = require("resty.openssl.cipher").new("aes-256-gcm")
print(cjson.encode(c:settable_params()))
-- outputs [["ivlen","unsigned integer (max 8 bytes large)"],["tag","octet string (arbitrary size)"],["tlsaad","octet string (arbitrary size)"],["tlsivfixed","octet string (arbitrary size)"],["tlsivinv","octet string (arbitrary size)"]]
print(cjson.encode(c:gettable_params()))
-- outputs [["keylen","unsigned integer (max 8 bytes large)"],["ivlen","unsigned integer (max 8 bytes large)"],["taglen","unsigned integer (max 8 bytes large)"],["iv","octet string (arbitrary size)"],["updated-iv","octet string (arbitrary size)"],["tag","octet string (arbitrary size)"],["tlsaadpad","unsigned integer (max 8 bytes large)"],["tlsivgen","octet string (arbitrary size)"]]
```

### get_param

**syntax**: *value, err = x:get_param(key, want_size?, want_type?)*

Read the param `key` and return its value. The return value is a Lua number
or a string.
Certain params requires exact size to be set, in such case,
`want_size` should be specified; if `want_size` is not specified and, the
library use a buffer of 100 bytes to hold the return value.
Certain params returns a special type, user should explictly set `want_type`
as a string to correctly decode them. Currently `want_type` can only be
`"bn"` or unset. Note it may also be necessary to increase temporary buffer
size `want_size` when `want_type` is `"bn"`.

```lua
local c = require("resty.openssl.cipher").new("aes-256-gcm")
print(c:get_param("taglen"))
-- outputs 16
print(c:get_param("tag"))
-- returns error, tag must have a explict size
print(c:get_param("tag", 16))
-- outputs the tag
local p = require("resty.openssl.pkey").new())
print(p:get_param("d"):to_hex())
-- returns error, d (private exponent) is a BIGNUM
print(p:get_param("d", 256, "bn"):to_hex())
-- returns d as resty.openssl.bn instance
```

### set_params

**syntax**: *ok, err = x:set_params(params)*

Set params passed in with Lua table `params`. The library does limited type check, user
is responsible for validity of input.

```lua
local k = require("resty.openssl.kdf").new("HKDF")
k:set_params({
    digest = "md5",
    salt = "salt",
    info = "some info",
    mode = kdf.HKDEF_MODE_EXPAND_ONLY,
    -- as HKDF also accepts mode as string, use the literal below also works
    -- mode = "EXPAND_ONLY"
}))
```

## Code generation

Lots of functions and tests for X509, CSR and CRL are generated from templates under
[scripts](https://github.com/fffonion/lua-resty-openssl/tree/master/scripts)
directory. Those functions and tests are either commented with `AUTO GENERATED` or `AUTOGEN`.

When making changes to them, please update the template under `scripts/templates` instead. Then
regenerate them again.

```
cd scripts
pip3 install -r requirements.txt
python3 ./x509_autogen.py
```


## See Also
* [luaossl](https://github.com/wahern/luaossl)
* [API/ABI changes review for OpenSSL](https://abi-laboratory.pro/index.php?view=timeline&l=openssl)
* [OpenSSL API manual](https://www.openssl.org/docs/man3.1/man3/)

[NID]: https://github.com/openssl/openssl/blob/master/include/openssl/obj_mac.h
[RFC 2246]: https://tools.ietf.org/html/rfc2246
[RFC 2898]: https://tools.ietf.org/html/rfc2898
[RFC 5246]: https://tools.ietf.org/html/rfc5246
[RFC 5869]: https://tools.ietf.org/html/rfc5869
[RFC 7914]: https://tools.ietf.org/html/rfc7914
[NIST SP 800-132]: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf
[NIST SP 800-135 r1]: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-135r1.pdf

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-openssl](https://github.com/fffonion/lua-resty-openssl){target=_blank}.