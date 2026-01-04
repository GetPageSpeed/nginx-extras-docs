---

title: "NGINX JSON variables module"
description: "RPM package nginx-module-json-var. Module adds the ability to group NGINX variable expressions as JSON."

---

# *json-var*: NGINX JSON variables module


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
    dnf -y install nginx-module-json-var
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-json-var
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_json_var_module.so;
```


This document describes nginx-module-json-var [v1.1](https://github.com/dvershinin/nginx-json-var-module/releases/tag/v1.1){target=_blank} 
released on Feb 11 2022.

<hr />

### json_var
* **syntax**: `json_var $variable { ... }`
* **default**: `none`
* **context**: `http`

Creates a new variable whose value is a json containing the items listed within the block.
Parameters inside the `json_var` block specify a field that should be included in the resulting json.
Each parameter has to contain two arguments - key and value. 
The value can contain nginx variables.

## Sample configuration
```nginx
http {
	json_var $output {
		timestamp $time_local;
		remoteAddr $remote_addr;
		xForwardedFor $http_x_forwarded_for;
		userAgent $http_user_agent;
		params $args;
	}
	
	server {
		location /get_json/ {
			return 200 $output;
		}
	}
```
Hitting `http://domain/get_json/?key1=value1&key2=value2` can return a json like:
```
{
	"timestamp": "21/Jul/2017:12:44:18 -0400",
	"remoteAddr": "127.0.0.1",
	"xForwardedFor": "",
	"userAgent": "curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3",
	"params": "key1=value1&key2=value2"
}
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-json-var](https://github.com/dvershinin/nginx-json-var-module){target=_blank}.