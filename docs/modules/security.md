# *security*: ModSecurity v3 Nginx Connector

## Installation

CentOS/RHEL/RockyLinux/etc. and Amazon Linux are supported and require a [subscription](https://www.getpagespeed.com/repo-subscribe).

Fedora Linux is supported free of charge and doesn't require a subscription.

### OS-specific complete installation and configuration guides available:

*   [CentOS/RHEL 7](https://bit.ly/ngx-security-el7)
*   [CentOS/RHEL 8](https://bit.ly/ngx-security-el8)

### Other supported operating systems
        
```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-security
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_modsecurity_module.so;
```


This document describes nginx-module-security [v1.0.3](https://github.com/SpiderLabs/ModSecurity-nginx/releases/tag/v1.0.3){target=_blank} 
released on May 20 2022.

<hr />

<img src="https://github.com/SpiderLabs/ModSecurity/raw/v3/master/others/modsec.png" width="50%">

[![](https://raw.githubusercontent.com/ZenHubIO/support/master/zenhub-badge.png)](https://zenhub.com)


The ModSecurity-nginx connector is the connection point between nginx and libmodsecurity (ModSecurity v3). Said another way, this project provides a communication channel between nginx and libmodsecurity. This connector is required to use LibModSecurity with nginx. 

The ModSecurity-nginx connector takes the form of an nginx module. The module simply serves as a layer of communication between nginx and ModSecurity.

Notice that this project depends on libmodsecurity rather than ModSecurity (version 2.9 or less).

### What is the difference between this project and the old ModSecurity add-on for nginx?

The old version uses ModSecurity standalone, which is a wrapper for
Apache internals to link ModSecurity to nginx. This current version is closer
to nginx, consuming the new libmodsecurity which is no longer dependent on
Apache. As a result, this current version has less dependencies, fewer bugs, and is faster. In addition, some new functionality is also provided - such as the possibility of use of global rules configuration with per directory/location customizations (e.g. SecRuleRemoveById).


## Usage

ModSecurity for nginx extends your nginx configuration directives.
It adds four new directives and they are:

## modsecurity
**syntax:** *modsecurity on | off*

**context:** *http, server, location*

**default:** *off*

Turns on or off ModSecurity functionality.
Note that this configuration directive is no longer related to the SecRule state.
Instead, it now serves solely as an nginx flag to enable or disable the module.

## modsecurity_rules_file
**syntax:** *modsecurity_rules_file &lt;path to rules file&gt;*

**context:** *http, server, location*

**default:** *no*

Specifies the location of the modsecurity configuration file, e.g.:

```nginx
server {
    modsecurity on;
    location / {
        root /var/www/html;
        modsecurity_rules_file /etc/my_modsecurity_rules.conf;
    }
}
```

## modsecurity_rules_remote
**syntax:** *modsecurity_rules_remote &lt;key&gt; &lt;URL to rules&gt;*

**context:** *http, server, location*

**default:** *no*

Specifies from where (on the internet) a modsecurity configuration file will be downloaded.
It also specifies the key that will be used to authenticate to that server:

```nginx
server {
    modsecurity on;
    location / {
        root /var/www/html;
        modsecurity_rules_remote my-server-key https://my-own-server/rules/download;
    }
}
```

## modsecurity_rules
**syntax:** *modsecurity_rules &lt;modsecurity rule&gt;*

**context:** *http, server, location*

**default:** *no*

Allows for the direct inclusion of a ModSecurity rule into the nginx configuration.
The following example is loading rules from a file and injecting specific configurations per directory/alias:

```nginx
server {
    modsecurity on;
    location / {
        root /var/www/html;
        modsecurity_rules_file /etc/my_modsecurity_rules.conf;
    }
    location /ops {
        root /var/www/html/opts;
        modsecurity_rules '
          SecRuleEngine On
          SecDebugLog /tmp/modsec_debug.log
          SecDebugLogLevel 9
          SecRuleRemoveById 10
        ';
    }
}
```

## modsecurity_transaction_id
**syntax:** *modsecurity_transaction_id string*

**context:** *http, server, location*

**default:** *no*

Allows to pass transaction ID from nginx instead of generating it in the library.
This can be useful for tracing purposes, e.g. consider this configuration:

```nginx
log_format extended '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" $request_id';

server {
    server_name host1;
    modsecurity on;
    modsecurity_transaction_id "host1-$request_id";
    access_log logs/host1-access.log extended;
    error_log logs/host1-error.log;
    location / {
        ...
    }
}

server {
    server_name host2;
    modsecurity on;
    modsecurity_transaction_id "host2-$request_id";
    access_log logs/host2-access.log extended;
    error_log logs/host2-error.log;
    location / {
        ...
    }
}
```

Using a combination of log_format and modsecurity_transaction_id you will
be able to find correlations between access log and error log entries
using the same unique identificator.

String can contain variables.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-security](https://github.com/SpiderLabs/ModSecurity-nginx){target=_blank}.