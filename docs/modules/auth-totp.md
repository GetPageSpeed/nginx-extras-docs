# *auth-totp*: Time-based one-time password (TOTP) authentication for NGINX


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-auth-totp
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-auth-totp
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_auth_totp_module.so;
```


This document describes nginx-module-auth-totp [v1.1.0](https://github.com/61131/nginx-http-auth-totp/releases/tag/1.1.0){target=_blank} 
released on Dec 18 2024.

<hr />

Time-based one-time password (TOTP) authentication for Nginx

The Time-based One-Time Password (TOTP) algorithm, provides a secure mechanism for short-lived one-time password values, which are desirable for enhanced security. This algorithm can be used across a wide range of network applications ranging from remote Virtual Private Network (VPN) access, Wi-Fi network logon to transaction-orientated Web applications.

The nginx-http-auth-totp module provides TOTP authentication for a Nginx server.

## Features

* HTTP basic authentication using time-based one-time password (TOTP)
* Cookie-based tracking of authenticated clients beyond TOTP validity window
* Configurable secret, time reference, time step and truncation length for TOTP generation
* Configurable time-skew for TOTP validation

## Packages

For users who prefer pre-built and optimized packages, the nginx-http-auth-totp module can be installed from the [GetPageSpeed repository](https://nginx-extras.getpagespeed.com/modules/auth-totp/):

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
dnf -y install nginx-module-auth-totp
```

## Configuration

```nginx
server {
    listen 80;

    location /protected {
        auth_totp_realm "Protected";
        auth_totp_file /etc/nginx/totp.conf;
        auth_totp_length 8;
        auth_totp_skew 1;
        auth_totp_step 1m;
        auth_totp_cookie "totp-session";
        auth_totp_expiry 1d;
    }
}
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_auth_totp_module.so;
```

## Directives

### auth_totp_cookie

* **syntax:** `auth_totp_cookie <name>`
* **default:** `totp`
* **context:** `http`, `server`, `location`, `limit_except`

Specifies the name of the HTTP cookie to be used for tracking authenticated clients.

As the validity of the Time-based One-Time Password (TOTP) used for authentication expires (by design), a HTTP cookie is set following successful authentication in order to persist client authentication beyond the TOTP validity window. This configuration directives specifies the name to be used when setting this cookie while the expiry period for this cookie may be set using the `auth_totp_expiry` directive. 

### auth_totp_expiry

* **syntax:** `auth_totp_expiry <interval>`
* **default:** `0s`
* **context:** `http`, `server`, `location`, `limit_except`

Specifies the expiry time for the HTTP cookie to be used for tracking authenticated clients.

If this expiry value is not specified (or set to zero), the HTTP cookie used for tracking authenticated clients will be set as a session cookie which will be deleted when the current HTTP client session ends. It is important to note that the browser defines when the "current session" ends, and some browsers use session restoration when restarting, which can cause session cookies to last indefinitely.

### auth_totp_file

* **syntax:** `auth_totp_file <filename>`
* **default:** -
* **context:** `http`, `server`, `location`, `limit_except`

Specifies the file that contains usernames and shared secrets for Time-based One-Time Password (TOTP) authentication. 

This configuration file has the format:

    # comment
    user1:secret1
    user2:secret2
    user3:secret3

### auth_totp_length

* **syntax:** `auth_totp_length <number>`
* **default:** `6`
* **context:** `http`, `server`, `location`, `limit_except`

Specifies the truncation length of the Time-based One-Time Password (TOTP) code. This truncation length may be between 1 and 8 digits inclusively.

If the supplied TOTP is of a different length to this value, the authentication request will fail.

### auth_totp_realm

* **syntax:** `auth_totp_realm <string>|off`
* **default:** `off`
* **context:** `http`, `server`, `location`, `limit_except`

Enables validation of user name and Time-based One-Time Password (TOTP) using the "HTTP Basic Authentication" protocol. The specified parameter is used as the `realm` for this authentication. This parameter value can contain variables. The special value of `off` cancels the application of any `auth_totp_realm` directive inherited from a higher configuration level.

### auth_totp_reuse

* **syntax:** `auth_totp_reuse <on>|<off>`
* **default:** `off`
* **context:**  `http`, `server`, `location`, `limit_except`

Enables the reuse of a Time-based One-Time Password (TOTP) within a validity window. While this is non-standard behaviour per [RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238), it provides a convenient manner to ensure a minimum window of validity for generated TOTP codes, even if the TOTP has already been presented to the validating system.

### auth_totp_skew

* **syntax:** `auth_totp_skew <number>`
* **default:** `1`
* **context:** `http`, `server`, `location`, `limit_except`

Specifies the number of time steps by which the time base between the issuing and validating TOTP systems.

Due to network latency, the gap between the time that a OTP was generated and the time that the OTP is received at the validating system may be large. Indeed, it is possible that the receiving time at the validating system and that when the OTP was generated by the issuing system may not fall within the same time-step window. Accordingly, the validating system should typically set a policy for an acceptable OTP transmission window for validation. In line with this, the validating system should compare OTPs not only with the receiving timestamp, but also the past timestamps that are within the transmission delay.

It is important to note that larger acceptable delay windows represent a larger window for attacks and a balance must be struck between the security and usability of OTPs.

### auth_totp_start

* **syntax:** `auth_totp_start <time>`
* **default:** `0`
* **context:** `http`, `server`, `location`, `limit_except`

Specifies the UNIX time from which to start counting time steps as part of Time-based One-Time Password (TOTP) algorithm operations.

The default value is 0, the UNIX epoch at 1970/01/01. 

### auth_totp_step

* **syntax:** `auth_totp_step <interval>`
* **default:** `30s`
* **context:** `http`, `server`, `location`, `limit_except`

Specifies the time step as part of Time-based One-Time Password (TOTP) algorithm operations.

## References

* [RFC 4226 HOTP: An HMAC-Based One-Time Password Algorithm](https://datatracker.ietf.org/doc/html/rfc4226)
* [RFC 6238 TOTP: Time-Based One-Time Password Algorithm](https://datatracker.ietf.org/doc/html/rfc6238)
* [RFC 7235 Hypertext Transfer Protocol (HTTP/1.1): Authentication](https://datatracker.ietf.org/doc/html/rfc7235)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-auth-totp](https://github.com/61131/nginx-http-auth-totp){target=_blank}.