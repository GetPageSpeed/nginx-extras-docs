# *coolkit*: NGINX CoolKit Module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-coolkit
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_coolkit_module.so;
```


This document describes nginx-module-coolkit [v0.2](https://github.com/dvershinin/ngx_coolkit/releases/tag/0.2){target=_blank} 
released on Aug 23 2020.

<hr />
ngx_coolkit is collection of small and useful nginx add-ons.


## CONFIGURATION DIRECTIVES:

  override_method off | [methods] source (context: http, server, location)
  ------------------------------------------------------------------------
  Override HTTP method.

  default: none


## CONFIGURATION VARIABLES:

  $remote_passwd
  -----------------
  Decoded password from "Authorization" header (Basic HTTP Authentication).


  $location
  ---------
  Name of the matched location block.


## EXAMPLE CONFIGURATION #1:
http {
    server {
        location / {
            override_method  $arg_method;
            proxy_pass       http://127.0.0.1:8100;
        }
    }
}

Pass request with changed HTTP method (based on "?method=XXX") to the backend.


## EXAMPLE CONFIGURATION #2:
http {
    upstream database {
        postgres_server        127.0.0.1 dbname=test
                               user=monty password=some_pass;
    }

    server {
        location = /auth {
            internal;

            set_quote_sql_str  $user $remote_user;
            set_quote_sql_str  $pass $remote_passwd;

            postgres_pass      database;
            postgres_query     "SELECT login FROM users WHERE login=$user AND pass=$pass";
            postgres_rewrite   no_rows 403;
            postgres_output    none;
        }

        location / {
            auth_request       /auth;
            root               /files;
        }
    }
}

Restrict access to local files by authenticating against SQL database.

Required modules (other than ngx_coolkit):
- ngx_http_auth_request_module,
- ngx_postgres (PostgreSQL) or ngx_drizzle (MySQL, Drizzle, SQLite),
- ngx_set_misc.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-coolkit](https://github.com/dvershinin/ngx_coolkit){target=_blank}.