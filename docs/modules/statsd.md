# *statsd*: NGINX module for sending stats to statsd


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
    yum -y install nginx-module-statsd
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-statsd
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_statsd_module.so;
```


This document describes nginx-module-statsd [v0.0.1](https://github.com/dvershinin/nginx-statsd/releases/tag/v0.0.1){target=_blank} 
released on Feb 24 2020.

<hr />

An nginx module for sending statistics to statsd.

This is how to use the nginx-statsd module:

	http {
		
		# Set the server that you want to send stats to.
		statsd_server your.statsd.server.com;

		# Randomly sample 10% of requests so that you do not overwhelm your statsd server.
		# Defaults to sending all statsd (100%). 
		statsd_sample_rate 10; # 10% of requests


		server {
			listen 80;
			server_name www.your.domain.com;
				
			# Increment "your_product.requests" by 1 whenever any request hits this server. 
			statsd_count "your_product.requests" 1;

			location / {
				
				# Increment the key by 1 when this location is hit.
				statsd_count "your_product.pages.index_requests" 1;

				# Increment the key by 1, but only if $request_completion is set to something.
				statsd_count "your_product.pages.index_responses" 1 "$request_completion";

				# Send a timing to "your_product.pages.index_response_time" equal to the value
				# returned from the upstream server. If this value evaluates to 0 or empty-string,
				# it will not be sent. Thus, there is no need to add a test.
				statsd_timing "your_product.pages.index_response_time" "$upstream_response_time";

				# Increment a key based on the value of a custom header. Only sends the value if
				# the custom header exists in the upstream response.
				statsd_count "your_product.custom_$upstream_http_x_some_custom_header" 1 
					"$upstream_http_x_some_custom_header";

				proxy_pass http://some.other.domain.com;
			}
		}
	}

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-statsd](https://github.com/dvershinin/nginx-statsd){target=_blank}.