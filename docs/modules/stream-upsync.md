# *stream-upsync*: NGINX module for syncing stream backends from consul or etcd


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-stream-upsync
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_stream_upsync_module.so;
```


This document describes nginx-module-stream-upsync [v1.2.2](https://github.com/xiaokai-wang/nginx-stream-upsync-module/releases/tag/v1.2.2){target=_blank} 
released on Jan 02 2020.

<hr />

nginx-stream-upsync-module - Nginx C module, sync upstreams from consul or others, dynamically modify backend-servers attribute(weight, max_fails,...), needn't reload nginx.

It may not always be convenient to modify configuration files and restart NGINX. For example, if you are experiencing large amounts of traffic and high load, restarting NGINX and reloading the configuration at that point further increases load on the system and can temporarily degrade performance.

The module can be more smoothly expansion and constriction, and will not influence the performance.

Another module, [nginx-upsync-module](https://github.com/weibocom/nginx-upsync-module) supports nginx http module(HTTP protocol), please be noticed.

If you want to use [nginx-upsync-module](https://github.com/weibocom/nginx-upsync-module) and [nginx-stream-upsync-module](https://github.com/xiaokai-wang/nginx-stream-upsync-module) both, please refer to [nginx-upsync](https://github.com/CallMeFoxie/nginx-upsync).

## Status

This module is still under active development and is considered production ready.

## Synopsis

nginx-consul:
```nginx-consul
stream {
    upstream test {
        upsync 127.0.0.1:8500/v1/kv/upstreams/test/ upsync_timeout=6m upsync_interval=500ms upsync_type=consul strong_dependency=off;
        upsync_dump_path /usr/local/nginx/conf/servers/servers_test.conf;

        include /usr/local/nginx/conf/servers/servers_test.conf;
    }

    upstream bar {
        server 127.0.0.1:8090 weight=1 fail_timeout=10 max_fails=3;
    }

    server {
        listen 12345;

        proxy_connect_timeout 1s;
        proxy_timeout 3s;
        proxy_pass test;
    }

    server {
        listen 2345;

        upstream_show
    }

    server {
        listen 127.0.0.1:9091;

        proxy_responses 1;
        proxy_timeout 20s;
        proxy_pass bar;
    }
}
```
nginx-etcd:
```nginx-etcd
stream {
    upstream test {
        upsync 127.0.0.1:2379/v2/keys/upstreams/test upsync_timeout=6m upsync_interval=500ms upsync_type=etcd strong_dependency=off;
        upsync_dump_path /usr/local/nginx/conf/servers/servers_test.conf;

        include /usr/local/nginx/conf/servers/servers_test.conf;
    }

    upstream bar {
        server 127.0.0.1:8090 weight=1 fail_timeout=10 max_fails=3;
    }

    server {
        listen 12345;

        proxy_connect_timeout 1s;
        proxy_timeout 3s;
        proxy_pass test;
    }

    server {
        listen 2345;

        upstream_show
    }

    server {
        listen 127.0.0.1:9091;

        proxy_responses 1;
        proxy_timeout 20s;
        proxy_pass bar;
    }
}
```
upsync_lb:
```upsync_lb
stream {
    upstream test {
        least_conn; //hash $uri consistent;

        upsync 127.0.0.1:8500/v1/kv/upstreams/test/ upsync_timeout=6m upsync_interval=500ms upsync_type=consul strong_dependency=off;
        upsync_dump_path /usr/local/nginx/conf/servers/servers_test.conf;
        upsync_lb least_conn; //hash_ketama;

        include /usr/local/nginx/conf/servers/servers_test.conf;
    }

    upstream bar {
        server 127.0.0.1:8090 weight=1 fail_timeout=10 max_fails=3;
    }

    server {
        listen 12345;

        proxy_connect_timeout 1s;
        proxy_timeout 3s;
        proxy_pass test;
    }

    server {
        listen 2345;

        upstream_show
    }

    server {
        listen 127.0.0.1:9091;

        proxy_responses 1;
        proxy_timeout 20s;
        proxy_pass bar;
    }
}
```

NOTE: upstream: include command is neccesary, first time the dumped file should include all the servers.


## Description

This module provides a method to discover backend servers. Supporting dynamicly adding or deleting backend server through consul/etcd and dynamicly adjusting backend servers weight, module will timely pull new backend server list from consul/etcd to upsync nginx ip router. Nginx needn't reload. Having some advantages than others:

* timely

      module send key to consul/etcd with index, consul/etcd will compare it with its index, if index doesn't change connection will hang five minutes, in the period any operation to the key-value, will feed back rightaway.

* performance

      Pulling from consul/etcd equal a request to nginx, updating ip router nginx needn't reload, so affecting nginx performance is little.

* stability

      Even if one pulling failed, it will pull next upsync_interval, so guaranteing backend server stably provides service. And support dumping the latest config to location, so even if consul/etcd hung up, and nginx can be reload anytime. 


## Directives

## upsync
```
syntax: upsync $consul/etcd.api.com:$port/v1/kv/upstreams/$upstream_name/ [upsync_type=consul/etcd] [upsync_interval=second/minutes] [upsync_timeout=second/minutes] [strong_dependency=off/on]
```
default: none, if parameters omitted, default parameters are upsync_interval=5s upsync_timeout=6m strong_dependency=off

context: upstream

description: Pull upstream servers from consul/etcd... .

The parameters' meanings are:

* upsync_interval

    pulling servers from consul/etcd interval time.

* upsync_timeout

    pulling servers from consul/etcd request timeout.

* upsync_type

    pulling servers from conf server type.

* strong_dependency

    when nginx start up if strong_dependency is on that means servers will be depended on consul/etcd and will pull servers from consul/etcd.


## upsync_dump_path
`syntax: upsync_dump_path $path`

default: /tmp/servers_$host.conf

context: upstream

description: dump the upstream backends to the $path.


## upsync_lb
`syntax: upsync_lb $load_balance`

default: round_robin/ip_hash/hash modula

context: upstream

description: mainly for least_conn and hash consistent, when using one of them, you must point out using upsync_lb.


## upsync_show
`syntax: upsync_show`

default: none

context: server

description: show all upstreams.

```request
curl http://localhost:2345/upstream_show

show all upstreams
```


## Consul_interface

Data can be taken from key/value store or service catalog. In the first case parameter upsync_type of directive must be *consul*. For example
 
```nginx-consul
    upsync 127.0.0.1:8500/v1/kv/upstreams/test upsync_timeout=6m upsync_interval=500ms upsync_type=consul strong_dependency=off;
```

In the second case it must be *consul_services*.

```nginx-consul
    upsync 127.0.0.1:8500/v1/catalog/service/test upsync_timeout=6m upsync_interval=500ms upsync_type=consul_services strong_dependency=off;
```

you can add or delete backend server through consul_ui or http_interface. Below are examples for key/value store.

http_interface example:

* add
```
    curl -X PUT http://$consul_ip:$port/v1/kv/upstreams/$upstream_name/$backend_ip:$backend_port
```
    default: weight=1 max_fails=2 fail_timeout=10 down=0 backup=0;

```
    curl -X PUT -d "{\"weight\":1, \"max_fails\":2, \"fail_timeout\":10}" http://$consul_ip:$port/v1/kv/$dir1/$upstream_name/$backend_ip:$backend_port
or
    curl -X PUT -d '{"weight":1, "max_fails":2, "fail_timeout":10}' http://$consul_ip:$port/v1/kv/$dir1/$upstream_name/$backend_ip:$backend_port
```
    value support json format.

* delete
```
    curl -X DELETE http://$consul_ip:$port/v1/kv/upstreams/$upstream_name/$backend_ip:$backend_port
```

* adjust-weight
```
    curl -X PUT -d "{\"weight\":2, \"max_fails\":2, \"fail_timeout\":10}" http://$consul_ip:$port/v1/kv/$dir1/$upstream_name/$backend_ip:$backend_port
or
    curl -X PUT -d '{"weight":2, "max_fails":2, "fail_timeout":10}' http://$consul_ip:$port/v1/kv/$dir1/$upstream_name/$backend_ip:$backend_port
```

* mark server-down
```
    curl -X PUT -d "{\"weight\":2, \"max_fails\":2, \"fail_timeout\":10, \"down\":1}" http://$consul_ip:$port/v1/kv/$dir1/$upstream_name/$backend_ip:$backend_port
or
    curl -X PUT -d '{"weight":2, "max_fails":2, "fail_timeout":10, "down":1}' http://$consul_ip:$port/v1/kv/$dir1/$upstream_name/$backend_ip:$backend_port
```

* check
```
    curl http://$consul_ip:$port/v1/kv/upstreams/$upstream_name?recurse
```


## Etcd_interface

you can add or delete backend server through http_interface.

mainly like etcd, http_interface example:

* add
```
    curl -X PUT http://$etcd_ip:$port/v2/keys/upstreams/$upstream_name/$backend_ip:$backend_port
```
    default: weight=1 max_fails=2 fail_timeout=10 down=0 backup=0;

```
    curl -X PUT -d value="{\"weight\":1, \"max_fails\":2, \"fail_timeout\":10}" http://$etcd_ip:$port/v2/keys/$dir1/$upstream_name/$backend_ip:$backend_port
```
    value support json format.

* delete
```
    curl -X DELETE http://$etcd_ip:$port/v2/keys/upstreams/$upstream_name/$backend_ip:$backend_port
```

* adjust-weight
```
    curl -X PUT -d "{\"weight\":2, \"max_fails\":2, \"fail_timeout\":10}" http://$etcd_ip:$port/v2/keys/$dir1/$upstream_name/$backend_ip:$backend_port
```

* mark server-down
```
    curl -X PUT -d value="{\"weight\":2, \"max_fails\":2, \"fail_timeout\":10, \"down\":1}" http://$etcd_ip:$port/v2/keys/$dir1/$upstream_name/$backend_ip:$backend_port
```

* check
```
    curl http://$etcd_ip:$port/v2/keys/upstreams/$upstream_name
```


## Code style

Code style is mainly based on [style](http://tengine.taobao.org/book/appendix_a.html)


## see also
* the nginx_upstream_check_module: https://github.com/alibaba/tengine/blob/master/src/http/ngx_http_upstream_check_module.c
* the nginx_upstream_check_module patch: https://github.com/yaoweibin/nginx_upstream_check_module
* or based on https://github.com/xiaokai-wang/nginx_upstream_check_module


## source dependency
* Cjson: https://github.com/kbranigan/cJSON
* http-parser: https://github.com/nodejs/http-parser


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-stream-upsync](https://github.com/xiaokai-wang/nginx-stream-upsync-module){target=_blank}.