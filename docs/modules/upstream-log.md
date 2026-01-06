---

title: "Writes upstream request logs in a specified format"
description: "RPM package nginx-module-upstream-log. The upstream log module writes upstream request logs in the specified format, similar to ngx_http_log_module but specifically for upstream requests. This allows separate logging of upstream/backend traffic for debugging and analytics purposes."

---

# *upstream-log*: Writes upstream request logs in a specified format


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
    dnf -y install nginx-module-upstream-log
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-upstream-log
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_upstream_log_module.so;
```


This document describes nginx-module-upstream-log [v0.1.1](https://github.com/dvershinin/ngx_http_upstream_log_module/releases/tag/0.1.1){target=_blank} 
released on Jan 06 2026.

<hr />

Unlike the access log module, it will be logged at the end of each upstream request. If several servers were contacted during request processing, an upstream log is recorded at the end of each contact. If an internal redirect from one server group to another happens, initiated by “X-Accel-Redirect” or error_page, an upstream log will also be recorded at the end of each contact.

~~This module also provides a series of variables for upstream logging. Many of these variables start with $upstream_last_, which is used to distinguish them from the variables in ngx_http_upstream. These variables only return information related to the current contact with the upstream, or information related to the last time the upstream was contacted. Commas and colons are not used to record information about multiple contacts with the upstream.~~

Note: This module no longer exports any additional variables. Extra upstream variables have been moved to [ngx_http_extra_variables_module](https://git.hanada.info/hanada/ngx_http_extra_variables_module). 

The usage of this module is very similar to ngx_http_log_module. just use the upstream_log directive to sets the path, format, and configuration for a buffered log write.

## Synopsis

```nginx
    http {

        log_format access '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';

        log_format upstream '$remote_addr $upstream_last_addr [$time_local] "$upstream_method $upstream_uri" '
                                 '$upstream_last_status $upstream_last_response_length $upstream_last_bytes_sent $upstream_last_bytes_received '
                                 '$upstream_last_connect_time $upstream_last_header_time $upstream_last_response_time';

        upstream cluster {
            server 192.168.0.1:80;
            server 192.168.0.2:80;
        }

        server {
            listen 80;

            access_log logs/access.log access;
            upstream_log logs/upstream.log upstream;

            location / {
                proxy_pass http://cluster;
            }
        }

    }
```

## Directive

### upstream_log
* Syntax:	upstream_log path [format [buffer=size] [gzip[=level]] [flush=time] [if=condition]]; upstream_log off;
* Default:	-;
* Context:	http, server, location, if in location, limit_except

Sets the path, format, and configuration for a buffered log write. Several logs can be specified on the same configuration level. Logging to syslog can be configured by specifying the “syslog:” prefix in the first parameter. The special value off cancels all upstream_log directives on the current level. Unlike the access_log directive, this directive does not accept the predefined "combined" format. You must first define the log format using the log_format directive and then reference it using this directive.

If either the buffer or gzip parameter is used, writes to log will be buffered.

> The buffer size must not exceed the size of an atomic write to a disk file. For FreeBSD this size is unlimited.

When buffering is enabled, the data will be written to the file:

* if the next log line does not fit into the buffer;
* if the buffered data is older than specified by the flush parameter;
* when a worker process is re-opening log files or is shutting down.
If the gzip parameter is used, then the buffered data will be compressed before writing to the file. The compression level can be set between 1 (fastest, less compression) and 9 (slowest, best compression). By default, the buffer size is equal to 64K bytes, and the compression level is set to 1. Since the data is compressed in atomic blocks, the log file can be decompressed or read by “zcat” at any time.

Example:
```
upstream_log /path/to/log.gz upstream gzip flush=5m;
```
> For gzip compression to work, nginx must be built with the zlib library.
The file path can contain variables, but such logs have some constraints:

* the user whose credentials are used by worker processes should have permissions to create files in a directory with such logs;
* buffered writes do not work;
* the file is opened and closed for each log write. However, since the descriptors of frequently used files can be stored in a cache, writing to the old file can continue during the time specified by the open_log_file_cache directive’s valid parameter
* during each log write the existence of the request’s root directory is checked, and if it does not exist the log is not created. It is thus a good idea to specify both root and upstream_log on the same configuration level:
```nginx
server {
    root         /spool/vhost/data/$host;
    upstream_log /spool/vhost/logs/$host;
    ...
```
The if parameter enables conditional logging. A request will not be logged if the condition evaluates to “0” or an empty string. In the following example, the last requests with response codes 2xx and 3xx will not be logged:
```nginx
map $upstream_status $upstream_loggable {
    ~(?:^|:\s|,\s)[23][0-9]{2}  0;
    default 1;
}

upstream_log /path/to/upstream.log upstream if=$upstream_loggable;
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-upstream-log](https://github.com/dvershinin/ngx_http_upstream_log_module){target=_blank}.