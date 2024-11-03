# *maxminddb*: A Lua library for reading MaxMind's Geolocation database


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-maxminddb
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-maxminddb
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-maxminddb [v1.3.4](https://github.com/anjia0532/lua-resty-maxminddb/releases/tag/v1.3.4){target=_blank} 
released on Oct 28 2024.
    
<hr />
lua-resty-maxminddb - A Lua library for reading [MaxMind's Geolocation database format](https://maxmind.github.io/MaxMind-DB/)  (aka mmdb or geoip2).


## Prerequisites

**Note**
- [maxmind/libmaxminddb][]

- [openresty][]

- [GeoLite2 Free Downloadable Databases][linkGeolite2FreeDownloadableDatabases]

- [maxmind/geoipupdate][]


**Bug fixed**

- [Error at lookup IP](https://github.com/anjia0532/lua-resty-maxminddb/issues/5)

- [bad argument #1 to 'concat' (table expected, got nil)](https://github.com/anjia0532/lua-resty-maxminddb/issues/4)

- [Memory leak](https://github.com/anjia0532/lua-resty-maxminddb/issues/6)

- [Multiple subdivisions](https://github.com/anjia0532/lua-resty-maxminddb/issues/7)

**Apology for infringement**
- https://github.com/anjia0532/lua-resty-maxminddb/issues/25

## opm (manual install libmaxminddb and download GeoLite2-City.mmdb)
## openresty/openresty:alpine and apache/apisix:2.13.0-alpine docker image need to install perl libmaxminddb
## e.g. apk --no-cache add perl libmaxminddb && ln -s /usr/lib/libmaxminddb.so.0  /usr/lib/libmaxminddb.so
opm get anjia0532/lua-resty-maxminddb

## luarocks (manual download GeoLite2-City.mmdb)
## openresty/openresty:alpine-fat docker image
luarocks install lua-resty-maxminddb

## openresty/openresty:alpine docker image need to install luarocks (ref https://github.com/openresty/docker-openresty/blob/master/alpine/Dockerfile.fat)

## special apache/apisix:2.xx.0-alpine luarocks install lua-resty-maxminddb UNZIP=/usr/bin/unzip
## e.g. apk --no-cache add perl alpine-sdk && luarocks install lua-resty-maxminddb UNZIP=/usr/bin/unzip
```

## Synopsis

```nginx
server {
    listen 80;
    server_name localhost;
    location / {
        content_by_lua_block{
            local cjson = require 'cjson'
            local geo = require 'resty.maxminddb'
            if not geo.initted() then
                geo.init("/path/to/GeoLite2-City.mmdb")
            end
            local res,err = geo.lookup(ngx.var.arg_ip or ngx.var.remote_addr) --support ipv6 e.g. 2001:4860:0:1001::3004:ef68

            if not res then
                ngx.log(ngx.ERR,'failed to lookup by ip ,reason:',err)
            end
            ngx.say("full :",cjson.encode(res))
            if ngx.var.arg_node then
               ngx.say("node name:",ngx.var.arg_node," ,value:", cjson.encode(res[ngx.var.arg_node] or {}))
            end
        }
    }
}
```

```bash
  #ipv4
  $ curl localhost/?ip=114.114.114.114&node=city
  
  #ipv6
  #$ curl localhost/?ip=2001:4860:0:1001::3004:ef68&node=country
  
  full :{"city":{"geoname_id":1799962,"names":{"en":"Nanjing","ru":"Нанкин","fr":"Nankin","pt-BR":"Nanquim","zh-CN":"南京","es":"Nankín","de":"Nanjing","ja":"南京市"}},"subdivisions":[{"geoname_id":1806260,"names":{"en":"Jiangsu","fr":"Province de Jiangsu","zh-CN":"江苏省"},"iso_code":"32"}],"country":{"geoname_id":1814991,"names":{"en":"China","ru":"Китай","fr":"Chine","pt-BR":"China","zh-CN":"中国","es":"China","de":"China","ja":"中国"},"iso_code":"CN"},"registered_country":{"geoname_id":1814991,"names":{"en":"China","ru":"Китай","fr":"Chine","pt-BR":"China","zh-CN":"中国","es":"China","de":"China","ja":"中国"},"iso_code":"CN"},"location":{"time_zone":"Asia\/Shanghai","longitude":118.7778,"accuracy_radius":50,"latitude":32.0617},"continent":{"geoname_id":6255147,"names":{"en":"Asia","ru":"Азия","fr":"Asie","pt-BR":"Ásia","zh-CN":"亚洲","es":"Asia","de":"Asien","ja":"アジア"},"code":"AS"}}
  node name:city ,value:{"geoname_id":1799962,"names":{"en":"Nanjing","ru":"Нанкин","fr":"Nankin","pt-BR":"Nanquim","zh-CN":"南京","es":"Nankín","de":"Nanjing","ja":"南京市"}}
```

prettify
```json
full: {
    "city": {
        "geoname_id": 1799962,
        "names": {
            "en": "Nanjing",
            "ru": "Нанкин",
            "fr": "Nankin",
            "pt-BR": "Nanquim",
            "zh-CN": "南京",
            "es": "Nankín",
            "de": "Nanjing",
            "ja": "南京市"
        }
    },
    "subdivisions": [{
            "geoname_id": 1806260,
            "names": {
                "en": "Jiangsu",
                "fr": "Province de Jiangsu",
                "zh-CN": "江苏省"
            },
            "iso_code": "32"
        }
    ],
    "country": {
        "geoname_id": 1814991,
        "names": {
            "en": "China",
            "ru": "Китай",
            "fr": "Chine",
            "pt-BR": "China",
            "zh-CN": "中国",
            "es": "China",
            "de": "China",
            "ja": "中国"
        },
        "iso_code": "CN"
    },
    "registered_country": {
        "geoname_id": 1814991,
        "names": {
            "en": "China",
            "ru": "Китай",
            "fr": "Chine",
            "pt-BR": "China",
            "zh-CN": "中国",
            "es": "China",
            "de": "China",
            "ja": "中国"
        },
        "iso_code": "CN"
    },
    "location": {
        "time_zone": "Asia\/Shanghai",
        "longitude": 118.7778,
        "accuracy_radius": 50,
        "latitude": 32.0617
    },
    "continent": {
        "geoname_id": 6255147,
        "names": {
            "en": "Asia",
            "ru": "Азия",
            "fr": "Asie",
            "pt-BR": "Ásia",
            "zh-CN": "亚洲",
            "es": "Asia",
            "de": "Asien",
            "ja": "アジア"
        },
        "code": "AS"
    }
}
node name: city, value: {
    "geoname_id": 1799962,
    "names": {
        "en": "Nanjing",
        "ru": "Нанкин",
        "fr": "Nankin",
        "pt-BR": "Nanquim",
        "zh-CN": "南京",
        "es": "Nankín",
        "de": "Nanjing",
        "ja": "南京市"
    }
}

```

## References

- [GeoIP2 City and Country CSV Databases][linkGeoip2CityAndCountryCsvDatabases]
- [lilien1010/lua-resty-maxminddb][]
- [maxmind/libmaxminddb#source#lookup_and_print][]
- [maxmind/libmaxminddb#source#dump_entry_data_list][]

## Bug Reports
Please report bugs by filing an issue with our GitHub issue tracker at https://github.com/anjia0532/lua-resty-maxminddb/issues

If the bug is casued by libmaxminddb  tracker at https://github.com/maxmind/libmaxminddb/issues

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-maxminddb](https://github.com/anjia0532/lua-resty-maxminddb){target=_blank}.