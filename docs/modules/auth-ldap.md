# *auth-ldap*: LDAP Authentication module for nginx


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-auth-ldap
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_auth_ldap_module.so;
```


This document describes nginx-module-auth-ldap [v0.3](https://github.com/dvershinin/nginx-auth-ldap/releases/tag/v0.3){target=_blank} 
released on May 28 2020.

<hr />
LDAP module for nginx which supports authentication against multiple LDAP servers.

## Example configuration
Define list of your LDAP servers with required user/group requirements:

```bash
    http {
      ldap_server test1 {
        url ldap://192.168.0.1:3268/DC=test,DC=local?sAMAccountName?sub?(objectClass=person);
        binddn "TEST\\LDAPUSER";
        binddn_passwd LDAPPASSWORD;
        group_attribute uniquemember;
        group_attribute_is_dn on;
        require valid_user;
      }

      ldap_server test2 {
        url ldap://192.168.0.2:3268/DC=test,DC=local?sAMAccountName?sub?(objectClass=person);
        binddn "TEST\\LDAPUSER";
        binddn_passwd LDAPPASSWORD;
        group_attribute uniquemember;
        group_attribute_is_dn on;
        require valid_user;
      }
    }
```

And add required servers in correct order into your location/server directive:
```bash
    server {
        listen       8000;
        server_name  localhost;

        auth_ldap "Forbidden";
        auth_ldap_servers test1;
		auth_ldap_servers test2;

        location / {
            root   html;
            index  index.html index.htm;
        }

    }
```

## Available config parameters

## url
expected value: string

Available URL schemes: ldap://, ldaps://

## binddn
expected value: string

## binddn_passwd
expected value: string

## group_attribute
expected value: string

## group_attribute_is_dn
expected value: on or off, default off

## require
expected value: valid_user, user, group

## satisfy
expected value: all, any

## max_down_retries
expected value: a number, default 0

Retry count for attempting to reconnect to an LDAP server if it is considered
"DOWN".  This may happen if a KEEP-ALIVE connection to an LDAP server times 
out or is terminated by the server end after some amount of time.  

This can usually help with the following error:

```
http_auth_ldap: ldap_result() failed (-1: Can't contact LDAP server)
```

## connections
expected value: a number greater than 0

## ssl_check_cert
expected value: on or off, default off

Verify the remote certificate for LDAPs connections. If disabled, any remote certificate will be
accepted which exposes you to possible man-in-the-middle attacks. Note that the server's
certificate will need to be signed by a proper CA trusted by your system if this is enabled.
See below how to trust CAs without installing them system-wide.

This options needs OpenSSL >= 1.0.2; it is unavailable if compiled with older versions.

## ssl_ca_file
expected value: file path

Trust the CA certificate in this file (see ssl_check_cert above).

## ssl_ca_dir
expected value: directory path

Trust all CA certificates in this directory (see ssl_check_cert above).

Note that you need to provide hash-based symlinks in the directory for this to work;
you'll basically need to run OpenSSL's c_rehash command in this directory.

## referral
expected value: on, off

LDAP library default is on. This option disables usage of referral messages from
LDAP server. Usefull for authenticating against read only AD server without access
to read write.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-auth-ldap](https://github.com/dvershinin/nginx-auth-ldap){target=_blank}.