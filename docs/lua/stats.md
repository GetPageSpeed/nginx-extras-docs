---

title: "Is a statistical module for nginx base on nginx-module-lua, Statistical key and values are configurable, can use the nginx core's variables and this module's variables. The statistical result store in mongodb"
description: "RPM package lua-resty-stats: Is a statistical module for nginx base on nginx-module-lua, Statistical key and values are configurable, can use the nginx..."

---
  
# *stats*: Is a statistical module for nginx base on nginx-module-lua, Statistical key and values are configurable, can use the nginx core's variables and this module's variables. The statistical result store in mongodb


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-stats
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-stats
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-stats [v1.0.3](https://github.com/jie123108/lua-resty-stats/releases/tag/v1.0.3){target=_blank} 
released on Nov 28 2020.
    
<hr />

lua-resty-stats - is a statistical module for nginx base on ngx_lua, Statistical key and values are configurable, can use the nginx core's variables and this module's variables. The statistical result store in mongodb.

## Synopsis
```nginx
    #set ngx_lua's environment variable:
    # init the lua-resty-stats
    init_worker_by_lua '
        local stats = require("resty.stats")
        -- add the default stats that named "stats_host"
        stats.add_def_stats()
        -- the general stats"s config
        local update = {["$inc"]= {count=1, ["hour_cnt.$hour"]=1, ["status.$status"]=1, 
                      ["req_time.all"]="$request_time", ["req_time.$hour"]="$request_time"}}
        
        -- stats by uri
        stats.add_stats_config("stats_uri", 
            {selector={date="$date",key="$uri"}, update=update,
             indexes={{keys={'date', 'key'}, options={unique=true}},{keys={'key'}, options={}}} })
            
        -- stats by arg        
        stats.add_stats_config("stats_arg", 
            {selector={date="$date",key="$arg_client_type"}, update=update,
             indexes={{keys={'date', 'key'}, options={unique=true}},{keys={'key'}, options={}}} })

        -- stats by uri and args 
        stats.add_stats_config("stats_uri_arg", 
            {selector={date="$date",key="$uri?$arg_from"}, update=update,
             indexes={{keys={'date', 'key'}, options={unique=true}},{keys={'key'}, options={}}} })

        -- stats by http request header
        stats.add_stats_config("stats_header_in", 
            {selector={date="$date",key="city:$http_city"}, update=update,
             indexes={{keys={'date', 'key'}, options={unique=true}},{keys={'key'}, options={}}} })
        
        -- stats by http response header
        stats.add_stats_config("stats_header_out", 
            {selector={date="$date",key="cache:$sent_http_cache"}, update=update,
             indexes={{keys={'date', 'key'}, options={unique=true}},{keys={'key'}, options={}}} })

        local mongo_cfg = {host="192.168.1.201", port=27017, dbname="ngx_stats"}
        local flush_interval = 2 -- second
        local retry_interval = 0.2 -- second
        -- init stats and start flush timer.
        stats.init(mongo_cfg, flush_interval, retry_interval)
    ';
    server {
        listen       80;
        server_name  localhost;

        location /byuri {            
            echo "byuri: $uri";
            log_by_lua '
                local stats = require("resty.stats")
                stats.log("stats_uri")
                stats.log("stats_host")
            ';
        }

        location /byarg {
            echo_sleep 0.005;    
            echo "login $args";
            log_by_lua '
                local stats = require("resty.stats")
                stats.log("stats_arg")
            ';
        }

        location /byarg/404 {
            request_stats statby_arg "clitype:$arg_client_type";        
            return 404;
            log_by_lua '
                local stats = require("resty.stats")
                stats.log("stats_arg")
            ';
        }

        location /byuriarg {
            echo "$uri?$args";
            log_by_lua '
                local stats = require("resty.stats")
                stats.log("stats_uri_arg")
            ';
        }

        location /byhttpheaderin {
            echo "city: $http_city";
            log_by_lua '
                local stats = require("resty.stats")
                stats.log("stats_header_in")
            ';
        }

        location /byhttpheaderout/ {
            proxy_pass http://127.0.0.1:82;
            log_by_lua '
                local stats = require("resty.stats")
                stats.log("stats_header_out")
            ';
        }
    }

    server {
        listen       82;
        server_name  localhost;
            location /byhttpheaderout/hit {
            add_header cache hit;
            echo "cache: hit";
        }
        location /byhttpheaderout/miss {
            add_header cache miss;
            echo "cache: miss";
        }
    }

	server {
	    listen 2000;
	    server_name localhost;
	 
	    location /stats {
	        set $template_root /path/to/lua-resty-stats/view;
	        content_by_lua_file '/path/to/lua-resty-stats/view/main.lua';
	    }
	}
```

## Variables
* nginx_core module supports variable: http://nginx.org/en/docs/http/ngx_http_core_module.html#variables 
* This module variables 
     * date: current date in the format: 1970-09-28 
     * time: current time in the format: 12:00:00 
     * year: current year 
     * month: current month 
     * day: current date 
     * hour: current hour 
     * minute: current minute 
     * second: current second 

## Methods
To load this library,

you need to specify this library's path in ngx_lua's lua_package_path directive. For example:
```nginx
http {
}
```

you use require to load the library into a local Lua variable:
```lua
local stats = require("resty.stats")
```


## add_def_stats
`syntax: stats.add_def_stats()`

add the predefined stats configs that contains:
```lua
stats_name: stats_host
stats_config:
{
    selector={date='$date',key='$host'}, 
    update={['$inc']= {count=1, ['hour_cnt.$hour']=1, ['status.$status']=1, 
            ['req_time.all']="$request_time", ['req_time.$hour']="$request_time"}},
            indexes={
                {keys={'date', 'key'}, options={unique=true}},
                {keys={'key'}, options={}}
            },
    }
}
```
After this method is called, when you used stats.log(stats_name) method, you can use these predefined statistics.

## add_stats_config
`syntax: stats.add_stats_config(stats_name, stats_config)`

Add a custom statistical configuration item that contains stats_name and stats config.
* `stats_name` is the name of the statistics, and also is the name of the mongodb's table. 
The name will be used when calling the `stats.log(stats_name)` method.
* `stats_config` is used to define the values of statistics. 
 `stats_config` is a table that contains some fileds:
    * `selector` a mongodb query statement. like: `{date="$date",key="$host"}`
    * `update` a mongodb update statement. like: `{["$inc"]= {count=1, ["hour_cnt.$hour"]=1, ["status.$status"]=1, 
                      ["req_time.all"]="$request_time", ["req_time.$hour"]="$request_time"}}`
    * `indexes` a table that contains all fields of the index.
 
The `selector` and `update` configuration can use [variables](#variables).  <br/>
Note that "$inc" is not a nginx variable, it's a mongodb's operator. 

## init
`syntax: stats.init(mongo_cfg, flush_interval, retry_interval)`

Initialization statistical library.
* `mongo_cfg` The mongodb configuration, contains fields:
    * `host` mongodb's host
    * `port` mongodb's port
    * `dbname` mongodb's database name.
* `flush_interval` flush data to the mongodb time interval, the time unit is seconds.
* `retry_interval` the retry time interval on flush error,the time unit is seconds.


## log
`syntax: stats.log(stats_name)`

Collect the specified(by stats_name) statistical information at the log phrase.<br/>
* `stats_name`  is one statistical name that add by `stats.add_stats_config`. <br/>
if the `stats_name` is nil, log method will collect all the statistics that have been configured.

## Simple Query And API
lua-resty-stats with a simple query page and API interface, which can be used in the following steps:
* add location configuration to nginx.conf

```nginx
location /stats {
    set $template_root /path/to/lua-resty-stats/view;
    content_by_lua_file '/path/to/lua-resty-stats/view/main.lua';
}
```

* Access query page. eg. `http://192.168.1.xxx/stats`:

![docs/query-page.png](docs/query-page.png "The Simple Query")

* Access API:

```curl
## by date
curl http://127.0.0.1:8020/stats/api?table=stats_uri&date=2020-02-20&limit=100
## by date, today
curl http://127.0.0.1:8020/stats/api?table=stats_uri&date=today&limit=10

## by key(The date parameter is ignored.)
curl http://127.0.0.1:8020/stats/api?table=stats_uri&key=/path/to/uri
```

* The API response will look something like this:

```json
{
    "stats": [
        {
            "hour_cnt": {
                "19": 24
            },
            "count": 24,
            "status": {
                "200": 24
            },
            "total": 24,
            "req_time": {
                "19": 13.262,
                "all": 13.262
            },
            "percent": 100,
            "key": "/path/to/uri",
            "date": "2020-09-24"
        }
    ]
}
```

*If you've configured some other fields in your update, this will be different*

## Simple Demo
[Simple Stats demo](docs/stats_simple_demo.conf "Simple Stats demo")

You can include it in nginx.conf using the include directive. Such as:
`include /path/to/simple_stats.conf;`

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-stats](https://github.com/jie123108/lua-resty-stats){target=_blank}.