# *geoip2*: NGINX GeoIP2 module


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
    yum -y install nginx-module-geoip2
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-geoip2
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_geoip2_module.so;
```
```nginx
load_module modules/ngx_stream_geoip2_module.so;
```


This document describes nginx-module-geoip2 [v3.4](https://github.com/leev/ngx_http_geoip2_module/releases/tag/3.4){target=_blank} 
released on Jun 22 2022.

<hr />

**ngx_http_geoip2_module** - creates variables with values from the maxmind geoip2 databases based on the client IP (default) or from a specific variable (supports both IPv4 and IPv6)

The module now supports nginx streams and can be used in the same way the http module can be used.

## Download Maxmind GeoLite2 Database (optional)
The free GeoLite2 databases are available from [Maxminds website](http://dev.maxmind.com/geoip/geoip2/geolite2/) (requires signing up)

## Example Usage:
```nginx
http {
    ...
    geoip2 /etc/maxmind-country.mmdb {
        auto_reload 5m;
        $geoip2_metadata_country_build metadata build_epoch;
        $geoip2_data_country_code default=US source=$variable_with_ip country iso_code;
        $geoip2_data_country_name country names en;
    }

    geoip2 /etc/maxmind-city.mmdb {
        $geoip2_data_city_name default=London city names en;
    }
    ....

    fastcgi_param COUNTRY_CODE $geoip2_data_country_code;
    fastcgi_param COUNTRY_NAME $geoip2_data_country_name;
    fastcgi_param CITY_NAME    $geoip2_data_city_name;
    ....
}

stream {
    ...
    geoip2 /etc/maxmind-country.mmdb {
        $geoip2_data_country_code default=US source=$remote_addr country iso_code;
    }
    ...
}
```

##### Metadata:
Retrieve metadata regarding the geoip database.
```
$variable_name metadata <field>
```
Available fields:
  - build_epoch: the build timestamp of the maxmind database.
  - last_check: the last time the database was checked for changes (when using auto_reload)
  - last_change: the last time the database was reloaded (when using auto_reload)

##### Autoreload (default: disabled):
Enabling auto reload will have nginx check the modification time of the database at the specified
interval and reload it if it has changed.
```
auto_reload <interval>
```

##### GeoIP:
```
$variable_name [default=<value] [source=$variable_with_ip] path ...
```
If default is not specified, the variable will be empty if not found.

If source is not specified, $remote_addr will be used to perform the lookup.

To find the path of the data you want (eg: country names en), use the [mmdblookup tool](https://maxmind.github.io/libmaxminddb/mmdblookup.html):

```
$ mmdblookup --file /usr/share/GeoIP/GeoIP2-Country.mmdb --ip 8.8.8.8

  {
    "country":
      {
        "geoname_id":
          6252001 <uint32>
        "iso_code":
          "US" <utf8_string>
        "names":
          {
            "de":
              "USA" <utf8_string>
            "en":
              "United States" <utf8_string>
          }
      }
  }

$ mmdblookup --file /usr/share/GeoIP/GeoIP2-Country.mmdb --ip 8.8.8.8 country names en

  "United States" <utf8_string>
```

This translates to:

```
$country_name "default=United States" source=$remote_addr country names en
```

##### Additional Commands:
These commands works the same as the original ngx_http_geoip_module documented here: http://nginx.org/en/docs/http/ngx_http_geoip_module.html#geoip_proxy.

However, if you provide the `source=$variable_with_ip` option on a variable, these settings will be ignored for that particular variable.

```
geoip2_proxy < cidr >
```
Defines trusted addresses.  When a request comes from a trusted address, an address from the "X-Forwarded-For" request header field will be used instead.

```
geoip2_proxy_recursive < on | off >
```
If recursive search is disabled then instead of the original client address that matches one of the trusted addresses, the last address sent in "X-Forwarded-For" will be used. If recursive search is enabled then instead of the original client address that matches one of the trusted addresses, the last non-trusted address sent in "X-Forwarded-For" will be used.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-geoip2](https://github.com/leev/ngx_http_geoip2_module){target=_blank}.