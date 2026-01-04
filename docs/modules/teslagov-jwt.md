---

title: "Secure your NGINX locations with JWT"
description: "RPM package nginx-module-teslagov-jwt. This is an NGINX module to check for a valid JWT and proxy to an upstream  server or redirect to a login page. It supports additional features such as  extracting claims from the JWT and placing them on the request/response  headers"

---

# *teslagov-jwt*: Secure your NGINX locations with JWT


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
    dnf -y install nginx-module-teslagov-jwt
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-teslagov-jwt
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_auth_jwt_module.so;
```


This document describes nginx-module-teslagov-jwt [v2.4.0](https://github.com/TeslaGov/ngx-http-auth-jwt-module/releases/tag/2.4.0){target=_blank} 
released on Sep 17 2025.

<hr />

This is an NGINX module to check for a valid JWT and proxy to an upstream server or redirect to a login page. It supports additional features such as extracting claims from the JWT and placing them on the request/response headers.

## Breaking Changes with v2

The `v2` branch, which has now been merged to `master` includes breaking changes. Please see the initial v2 release for details,

## Directives

This module requires several new `nginx.conf` directives, which can be specified at the `http`, `server`, or `location` levels. See the [example NGINX config file](examples/nginx.conf) for more info.

| Directive                            | Description                                                                                                                                                |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auth_jwt_key`                       | The key to use to decode/verify the JWT, *in binhex format* -- see below.                                                                                  |
| `auth_jwt_redirect`                  | Set to "on" to redirect to `auth_jwt_loginurl` if authentication fails.                                                                                    |
| `auth_jwt_loginurl`                  | The URL to redirect to if `auth_jwt_redirect` is enabled and authentication fails.                                                                         |
| `auth_jwt_enabled`                   | Set to "on" to enable JWT checking.                                                                                                                        |
| `auth_jwt_algorithm`                 | The algorithm to use. One of: HS256, HS384, HS512, RS256, RS384, RS512                                                                                     |
| `auth_jwt_location`                  | Indicates where the JWT is located in the request -- see below.                                                                                            |
| `auth_jwt_validate_sub`              | Set to "on" to validate the `sub` claim (e.g. user id) in the JWT.                                                                                         |
| `auth_jwt_extract_var_claims`        | Set to a space-delimited list of claims to extract from the JWT and make available as NGINX variables. These will be accessible via e.g: `$jwt_claim_sub`  |
| `auth_jwt_extract_request_claims`    | Set to a space-delimited list of claims to extract from the JWT and set as request headers. These will be accessible via e.g: `$http_jwt_sub`              |
| `auth_jwt_extract_response_claims`   | Set to a space-delimited list of claims to extract from the JWT and set as response headers. These will be accessible via e.g: `$sent_http_jwt_sub`        |
| `auth_jwt_use_keyfile`               | Set to "on" to read the key from a file rather than from the `auth_jwt_key` directive.                                                                     |
| `auth_jwt_keyfile_path`              | Set to the path from which the key should be read when `auth_jwt_use_keyfile` is enabled.                                                                  |


## Algorithms

The default algorithm is `HS256`, for symmetric key validation. When using one of the `HS*` algorithms, the value for `auth_jwt_key` should be specified in binhex format. It is recommended to use at least 256 bits of data (32 pairs of hex characters or 64 characters in total). Note that using more than 512 bits will not increase the security. For key guidelines please see [NIST Special Publication 800-107 Recommendation for Applications Using Approved Hash Algorithms](https://csrc.nist.gov/publications/detail/sp/800-107/rev-1/final), Section 5.3.2 The HMAC Key.

To generate a 256-bit key (32 pairs of hex characters; 64 characters in total):

```bash
openssl rand -hex 32
```

### Additional Supported Algorithms

The configuration also supports RSA public key validation via (e.g.) `auth_jwt_algorithm RS256`. When using the `RS*` alhorithms, the `auth_jwt_key` field must be set to your public key **OR** `auth_jwt_use_keyfile` should be set to `on` and `auth_jwt_keyfile_path` should point to the public key on disk. NGINX won't start if `auth_jwt_use_keyfile` is set to `on` and a key file is not provided.

When using an `RS*` algorithm with an inline key, be sure to set `auth_jwt_key` to the _public key_, rather than a PEM certificate. E.g.:

```nginx
auth_jwt_key "-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0aPPpS7ufs0bGbW9+OFQ
RvJwb58fhi2BuHMd7Ys6m8D1jHW/AhDYrYVZtUnA60lxwSJ/ZKreYOQMlNyZfdqA
rhYyyUkedDn8e0WsDvH+ocY0cMcxCCN5jItCwhIbIkTO6WEGrDgWTY57UfWDqbMZ
4lMn42f77OKFoxsOA6CVvpsvrprBPIRPa25H2bJHODHEtDr/H519Y681/eCyeQE/
1ibKL2cMN49O7nRAAaUNoFcO89Uc+GKofcad1TTwtTIwmSMbCLVkzGeExBCrBTQo
wO6AxLijfWV/JnVxNMUiobiKGc/PP6T5PI70Uv67Y4FzzWTuhqmREb3/BlcbPwtM
oQIDAQAB
-----END PUBLIC KEY-----";
```

When using an `RS*` algorithm with a public key file, do as follows:

```nginx
auth_jwt_use_keyfile on;
auth_jwt_keyfile_path "/path/to/pub_key.pem";
```

A typical use case would be to specify the key and login URL at the `http` level, and then only turn JWT authentication on for the locations which you want to secure (or vice-versa). Unauthorized requests will result in a `302 Moved Temporarily` response with the `Location` header set to the URL specified in the `auth_jwt_loginurl` directive, and a querystring parameter `return_url` whose value is the current / attempted URL.

If you prefer to return `401 Unauthorized` rather than redirect, you may turn `auth_jwt_redirect` off:

```nginx
auth_jwt_redirect off;
```
## JWT Locations

By default, the`Authorization` header is used to provide a JWT for validation. However, you may use the `auth_jwt_location` directive to specify the name of the header or cookie which provides the JWT:

```nginx
auth_jwt_location HEADER=auth-token;  # get the JWT from the "auth-token" header
auth_jwt_location COOKIE=auth-token;  # get the JWT from the "auth-token" cookie
```

## `sub` Validation

Optionally, the module can validate that a `sub` claim (e.g. the user's id) exists in the JWT. You may enable this feature as follows:

```nginx
auth_jwt_validate_sub on;
```

## Extracting Claims from the JWT

You may specify claims to be extracted from the JWT and placed on the request and/or response headers. This is especially handly because the claims will then also be available as NGINX variables.

If you only wish to access a claim as an NGINX variable, you should use `auth_jwt_extract_var_claims` so that the claim does not end up being sent to the client as a response header. However, if you do want the claim to be sent to the client in the response, you may use `auth_jwt_extract_response_claims` instead.

_Please note that `number`, `boolean`, `array`, and `object` claims are not supported at this time -- only `string` claims are supported._ An error will be thrown if you attempt to extract a non-string claim.

### Using Claims

For example, you could configure an NGINX location which redirects to the current user's profile. Suppose `sub=abc-123`, the configuration below would redirect to `/profile/abc-123`.

```nginx
location /profile/me {
    auth_jwt_extract_var_claims sub;

    return 301 /profile/$jwt_claim_sub;
}
```

### Using Response Claims

Response claims are used in the same way, with the only differences being:
 - the variables are accessed via the `$sent_http_jwt_*` pattern, e.g. `$sent_http_jwt_sub`, and
 - the headers are sent to the client.

### Extracting Multiple Claims

You may extract multiple claims by specifying all claims as arguments to a single directive, or by supplying multiple directives. The following two examples are equivalent.

```nginx
auth_jwt_extract_request_claims sub firstName lastName;
```

```nginx
auth_jwt_extract_request_claims sub;
auth_jwt_extract_request_claims firstName;
auth_jwt_extract_request_claims lastName;
```

#### Cloning `libjwt`

1. Clone this repository as follows (replace `<target_dir>`): `git clone git@github.com:benmcollins/libjwt.git <target_dir>`
2. Enter the directory and switch to the latest tag: `git checkout $(git tag | sort -Vr | head -n 1)`
3. Update the `includePath` entires shown above to match the location you chose.

#### Cloning `libjansson`

1. Clone this repository as follows (replace `<target_dir>`): `git clone git@github.com:akheron/jansson.git <target_dir>`
2. Enter the directory and switch to the latest tag: `git checkout $(git tag | sort -Vr | head -n 1)`
3. Update the `includePath` entires shown above to match the location you chose.

#### Verifying Compliation

Once you save your changes to `.vscode/c_cpp_properties.json`, you should see that warnings and errors in the Problems panel go away, at least temprorarily. Hopfeully they don't come back, but if they do, make sure your include paths are set correctly.

## For Linux systems with systemd (optional)
export LOG_DRIVER=journald

## For other systems or if you prefer file-based logs (default)
export LOG_DRIVER=json-file

## rebuild the test images
./scripts rebuild_test

## run the tests
./scripts test

## check the logs -- adjust the container name as needed
## For journald (Linux systems):
journalctl -eu docker CONTAINER_NAME=nginx-auth-jwt-test-nginx

## For json-file driver (all systems):
docker logs nginx-auth-jwt-test-nginx
```

Now you'll be able to see logs from previous test runs. The best way to make use of this is to open two terminals, one where you run the tests, and one where you follow the logs:

```shell
## terminal 1
./scripts test

## terminal 2 - choose based on your LOG_DRIVER setting:

## For journald:
journalctl -fu docker CONTAINER_NAME=jwt-nginx-test

## For json-file (default):
docker logs -f nginx-auth-jwt-test-nginx
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-teslagov-jwt](https://github.com/TeslaGov/ngx-http-auth-jwt-module){target=_blank}.