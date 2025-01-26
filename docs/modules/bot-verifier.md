---

title: "A search index bot verification module for NGINX"
description: "RPM package nginx-module-bot-verifier. [BETA] This module has been tested on a handful of production websites.  This is an NGINX module designed to validate actors claiming to be search engine indexers. It is right to disable security mechanisms for valid search engine bots to ensure your controls do not interfere with page rankings on any of the search providers. The issue is that the User Agent header cannot be trusted. In order to ensure you are allowing only valid search engine indexers, you must validate according to their published standards.  This module performs that validation and caches the results to ensure you do not pay validation penalties on every request. "

---

# *bot-verifier*: A search index bot verification module for NGINX


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
    dnf -y install nginx-module-bot-verifier
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-bot-verifier
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_bot_verifier_module.so;
```


This document describes nginx-module-bot-verifier [v0.0.11](https://github.com/dvershinin/ngx_bot_verifier/releases/tag/v0.0.11){target=_blank} 
released on Jun 26 2022.

<hr />

## Status

[BETA] This module has been tested on a handful of production websites. It has not yet been evaluated at scale. If you would like to consider testing this at scale I would be happy to assist and allocate time to correct any issues.


## Synopsis

```nginx
location / {
    bot_verifier on;
    bot_verifier_redis_host localhost;
    bot_verifier_redis_port 6379;
    bot_verifier_redis_connection_timeout 10;
    bot_verifier_redis_read_timeout 10;
    bot_verifier_redis_expiry 3600;
	bot_verifier_repsheet_enabled on;
}
```


## Description

This is an NGINX module designed to validate actors claiming to be search engine indexers. It is right to disable security mechanisms for valid search engine bots to ensure your controls do not interfere with page rankings on any of the search providers. The issue is that the [User Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) header cannot be trusted. In order to ensure you are allowing only valid search engine indexers, you must validate according to their published standards. This module performs that validation and caches the results to ensure you do not pay validation penalties on every request.


## Directives

The following directives are used only for module configuration.


## bot_verifier

**syntax:** *bot_verifier* \[on|off\]

**default:** *off*

**context:** *location*

**phase:** *access*

Enables or disables the module. The module will not act unless it is set to *on*.


## bot_verifier_redis_host

**syntax:** *bot_verifier_redis_host* &lt;string&gt;

**default:** *localhost*

**context:** *location*

**phase:** *access*

Sets the Redis host. This setting is used to connect to the Redis database used for caching lookup results.


## bot_verifier_redis_port

**syntax:** *bot_verifier_redis_port* &lt;int&gt;

**default:** *6379*

**context:** *location*

**phase:** *access*

Sets the Redis port. This setting is used to connect to the Redis database used for caching lookup results.


## bot_verifier_redis_connection_timeout

**syntax:** *bot_verifier_redis_connection_timeout* &lt;int&gt;

**default:** *10*

**context:** *location*

**phase:** *access*

Sets the timeout when connecting to Redis. This setting is used to connect to the Redis database used for caching lookup results.


## bot_verifier_redis_read_timeout

**syntax:** *bot_verifier_redis_read_timeout* &lt;int&gt;

**default:** *10*

**context:** *location*

**phase:** *access*

Sets the timeout when querying Redis. This setting is used to connect to the Redis database used for caching lookup results.


## bot_verifier_redis_expiry

**syntax:** *bot_verifier_redis_expiry* &lt;seconds&gt;

**default:** *3600*

**context:** *location*

**phase:** *access*

Sets the timeout when querying Redis. This setting is used to connect to the Redis database used for caching lookup results.


## bot_verifier_repsheet_enabled

**syntax:** *bot_verifier_repsheet_enabled* \[on|off\]

**default:** *off*

**context:** *location*

**phase:** *access*

Enables blacklisting of failed actors in Repsheet. Assumes Repsheet cache lives on already configured redis server.


## Verifying Functionality

In order to ensure the module is working properly you will need to issue a query that will trigger failure and success cases. To trigger a failure case issue the following request:

```
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html" localhost:8888
```

This will issue a query that identifies itself as a Google bot. The reverse and forward lookup routine will fail and you will get a `403` response. To ensure the verification works when a bot is identified issue the following request:

```
curl -H "X-Forwarded-For: 66.249.66.1" -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html" localhost:8888
```

This will spoof the `X-Forwarded-For` header and pretend to be from a valid google address. The request should succeed and return a normal response.


## Developer Setup

This module contains a full self-contained development environment. This is done to ensure work on the module does not interfere with any other NGINX installations. To setup the environment run the `script/bootstrap` command. This will create the following directories:

```
vendor - The NGINX installation will live here  
build - The NGINX install will live here  
```

The `nginx.conf` file in the root of this repository will be symlinked to `build/nginx/conf/nginx.conf` to make configuration changes easier. You can start NGINX using the following command:

```
build/nginx/sbin/nginx
```

Log files are available at `build/nginx/logs`. You can stop the server by running

```
build/nginx/sbin/nginx -s stop
```

If you are making changes to the module, you can recompile them by running `make compile`. Remember to restart the NGINX after this completes successfully.


## Running the Test Suite

This repository comes with a test suite that uses the `Test::Nginx` library. To run the test you will need to install the following libraries:

```
cpanm -S install Test::Nginx Test::Nginx::Socket
```

Once the libraries are installed just run `make` and the suite will run. If you are submitting a change to this module please make sure to run the test suite before you do. Any changes that break the test suite will not be accepted.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-bot-verifier](https://github.com/dvershinin/ngx_bot_verifier){target=_blank}.