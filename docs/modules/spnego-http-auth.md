# *spnego-http-auth*: Nginx module for HTTP SPNEGO auth


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
    yum -y install nginx-module-spnego-http-auth
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-spnego-http-auth
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_auth_spnego_module.so;
```


This document describes nginx-module-spnego-http-auth [v1.1.2](https://github.com/stnoonan/spnego-http-auth-nginx-module/releases/tag/v1.1.2){target=_blank} 
released on Jan 11 2025.

<hr />

This module implements adds [SPNEGO](http://tools.ietf.org/html/rfc4178)
support to nginx(http://nginx.org).  It currently supports only Kerberos
authentication via [GSSAPI](http://en.wikipedia.org/wiki/GSSAPI)


## Prerequisites

Authentication has been tested with (at least) the following:

* Nginx 1.2 through 1.7
* Internet Explorer 8 and above
* Firefox 10 and above
* Chrome 20 and above
* Curl 7.x (GSS-Negotiate), 7.x (SPNEGO/fbopenssl)

The underlying kerberos library used for these tests was MIT KRB5 v1.8.


## Configuration reference

You can configure GSS authentication on a per-location and/or a global basis:

These options are required.
* `auth_gss`: on/off, for ease of unsecuring while leaving other options in
  the config file
* `auth_gss_keytab`: absolute path-name to keytab file containing service
  credentials

These options should ONLY be specified if you have a keytab containing
privileged principals.  In nearly all cases, you should not put these
in the configuration file, as `gss_accept_sec_context` will do the right
thing.
* `auth_gss_realm`: Kerberos realm name.  If this is specified, the realm is only passed to the nginx variable $remote_user if it differs from this default.  To override this behavior, set *auth_gss_format_full* to 1 in your configuration.
* `auth_gss_service_name`: service principal name to use when acquiring
  credentials.

If you would like to authorize only a specific set of users, you can use the
`auth_gss_authorized_principal` directive.  The configuration syntax supports
multiple entries, one per line.

    auth_gss_authorized_principal <username>@<realm>
    auth_gss_authorized_principal <username2>@<realm>

Users can also be authorized using a regex pattern via the `auth_gss_authorized_principal_regex`
 directive. This directive can be used together with the `auth_gss_authorized_principal` directive.

    auth_gss_authorized_principal <username>@<realm>
    auth_gss_authorized_principal_regex ^(<username>)/(<group>)@<realm>$

The remote user header in nginx can only be set by doing basic authentication.
Thus, this module sets a bogus basic auth header that will reach your backend
application in order to set this header/nginx variable.  The easiest way to disable
this behavior is to add the following configuration to your location config.

    proxy_set_header Authorization "";
    
A future version of the module may make this behavior an option, but this should
be a sufficient workaround for now.

If you would like to enable GSS local name rules to rewrite usernames, you can
specify the `auth_gss_map_to_local` option.

## Credential Delegation

User credentials can be delegated to nginx using the `auth_gss_delegate_credentials` 
 directive. This directive will enable unconstrained delegation if the user chooses 
 to delegate their credentials. Constrained delegation (S4U2proxy) can also be enabled using the 
 `auth_gss_constrained_delegation` directive together with the `auth_gss_delegate_credentials` 
 directive. To specify the ccache file name to store the service ticket used for constrained 
 delegation, set the `auth_gss_service_ccache` directive. Otherwise, the default ccache name 
 will be used.

    auth_gss_service_ccache /tmp/krb5cc_0;
    auth_gss_delegate_credentials on;
    auth_gss_constrained_delegation on;

The delegated credentials will be stored within the systems tmp directory. Once the
 request is completed, the credentials file will be destroyed. The name of the credentials 
 file will be specified within the nginx variable `$krb5_cc_name`. Usage of the variable 
 can include passing it to a fcgi program using the `fastcgi_param` directive.

    fastcgi_param KRB5CCNAME $krb5_cc_name;

Constrained delegation is currently only supported using the negotiate authentication scheme
 and has only been testing with MIT Kerberos (Use at your own risk if using Heimdal Kerberos).

## Basic authentication fallback

The module falls back to basic authentication by default if no negotiation is
attempted by the client.  If you are using SPNEGO without SSL, it is recommended
you disable basic authentication fallback, as the password would be sent in
plaintext.  This is done by setting `auth_gss_allow_basic_fallback` in the
config file.

    auth_gss_allow_basic_fallback off

These options affect the operation of basic authentication:
* `auth_gss_realm`: Kerberos realm name.  If this is specified, the realm is
  only passed to the nginx variable $remote_user if it differs from this
  default.  To override this behavior, set *auth_gss_format_full* to 1 in your
  configuration.
* `auth_gss_force_realm`: Forcibly authenticate using the realm configured in
  `auth_gss_realm` or the system default realm if `auth_gss_realm` is not set.
  This will rewrite $remote_user if the client provided a different realm.  If
  *auth_gss_format_full* is not set, $remote_user will not include a realm even
  if one was specified by the client.


## Troubleshooting

###
Check the logs.  If you see a mention of NTLM, your client is attempting to
connect using [NTLMSSP](http://en.wikipedia.org/wiki/NTLMSSP), which is
unsupported and insecure.

### Verify that you have an HTTP principal in your keytab ###

#### MIT Kerberos utilities ####

    $ KRB5_KTNAME=FILE:<path to your keytab> klist -k

or

    $ ktutil
    ktutil: read_kt <path to your keytab>
    ktutil: list

#### Heimdal Kerberos utilities ####

    $ ktutil -k <path to your keytab> list

### Obtain an HTTP principal

If you find that you do not have the HTTP service principal,
are running in an Active Directory environment,
and are bound to the domain such that Samba tools work properly

    $ env KRB5_KTNAME=FILE:<path to your keytab> net ads -P keytab add HTTP

If you are running in a different kerberos environment, you can likely run

    $ env KRB5_KTNAME=FILE:<path to your keytab> krb5_keytab HTTP

### Increase maximum allowed header size

In Active Directory environment, SPNEGO token in the Authorization header includes
PAC (Privilege Access Certificate) information, which includes all security groups
the user belongs to. This may cause the header to grow beyond default 8kB limit and
causes following error message:

    400 Bad Request
    Request Header Or Cookie Too Large

For performance reasons, best solution is to reduce the number of groups the user
belongs to. When this is impractical, you may also choose to increase the allowed
header size by explicitly setting the number and size of Nginx header buffers:

    large_client_header_buffers 8 32k;

## Debugging

The module prints all sort of debugging information if nginx is compiled with
the `--with-debug` option, and the `error_log` directive has a `debug` level.


## NTLM

Note that the module does not support [NTLMSSP](http://en.wikipedia.org/wiki/NTLMSSP)
in Negotiate. NTLM, both v1 and v2, is an exploitable protocol and should be avoided
where possible.

## Help

If you're unable to figure things out, please feel free to open an 
issue on Github and I'll do my best to help you.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-spnego-http-auth](https://github.com/stnoonan/spnego-http-auth-nginx-module){target=_blank}.