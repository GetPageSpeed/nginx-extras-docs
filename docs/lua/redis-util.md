---

title: "Nginx-module-lua-resty-redis 封装工具类"
description: "RPM package lua-resty-redis-util: Nginx-module-lua-resty-redis 封装工具类"

---
  
# *redis-util*: Nginx-module-lua-resty-redis 封装工具类


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-redis-util
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-redis-util
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-redis-util [v0.7](https://github.com/anjia0532/lua-resty-redis-util/releases/tag/v0.07){target=_blank} 
released on Dec 15 2021.
    
<hr />

## 介绍

本项目是基于[openresty/lua-resty-redis][] 是[章亦春（agentzh）][agentzh]开发的openresty中的操作redis的库。进行二次封装的工具库。核心功能还是由[openresty/lua-resty-redis][]完成的。

本文假设你已经了解nginx+lua或者openresty如何使用lua脚本(e.g. `lua_package_path`配置,`*_by_lua_file`),基础的redis相关知识，以及[openresty/lua-resty-redis][]的基本使用方法([openresty/lua-resty-redis#README.md][README.md])。

## 安装(Install)

```bash
opm get anjia0532/lua-resty-redis-util
```

## 对比

截取官方部分代码，进行说明

```lua
    local redis = require "resty.redis"
    local red = redis:new()

    red:set_timeout(1000) -- 1 sec --设置超时时间

    local ok, err = red:connect("127.0.0.1", 6379) --设置redis的host和port
    if not ok then --判断生成连接是否失败
        ngx.say("failed to connect: ", err)
        return
    end

    ok, err = red:set("dog", "an animal") --插入键值(类似 mysql insert)
    if not ok then --判断操作是否成功
        ngx.say("failed to set dog: ", err)
        return
    end

    ngx.say("set result: ", ok) -- 页面输出结果
    -- put it into the connection pool of size 100,
    -- with 10 seconds max idle time
    local ok, err = red:set_keepalive(10000, 100) --将连接放入连接池,100个连接，最长10秒的闲置时间
    if not ok then --判断放池结果
        ngx.say("failed to set keepalive: ", err)
        return
    end
    -- 如果不放池，用完就关闭的话，用下面的写法
    -- or just close the connection right away:
    -- local ok, err = red:close()
    -- if not ok then
    --     ngx.say("failed to close: ", err)
    --     return
    -- end
```

如果用过java，c#等面向对象的语言，就会觉得这么写太。。。。了，必须重构啊，暴露太多无关细节了，导致代码中有大量重复代码了。

同样的内容，使用我封装后的代码。隐藏了设置连接池，取连接，用完后放回连接池等操作。

```lua
    -- 依赖库
    local redis = require "resty.redis-util"
    -- 初始化
    local red = redis:new();
    -- 插入键值
    local ok,err = red:set("dog","an animal")
    -- 判断结果
    if not ok then
      ngx.say("failed to set dog:",err)
      return
    end
    -- 页面打印结果
    ngx.say("set result: ", ok) -- 页面输出结果
```

## 注意事项(Note)

### 默认值(Default Value)

```lua
local red = redis:new();
--使用了默认值,等同于
local red2 = redis:new({
                            host='127.0.0.1',
                            port=6379,
                            db_index=0,
                            password=nil,
                            timeout=1000,
                            keepalive=60000,
                            pool_size=100
                        });
```

- host: redis host,default: 127.0.0.1
- port: redis port,default:6379
- db_index: redis库索引(默认0-15 共16个库)，默认的就是0库(建议用不同端口开不同实例或者用不同前缀，因为换库需要用select命令),default:0
- password: redis auth 认证的密码
- timeout: reids连接超时时间,default: 1000 (1s)
- keepalive: redis连接池的最大闲置时间, default: 60000 (1m)
- pool_size: redis连接池大小, default: 100

### subscribe

因为没有用到pub/sub，所以只是简单的实现了(un)subscribe，没有继续实现(un)psubscribe(模式订阅), 参考 [Redis 接口的二次封装（发布订阅）][linkRedis接口的二次封装（发布订阅）]

```lua

    local cjson = require "cjson"
    local red = redis:new();

    -- 订阅dog频道
    local func  = red:subscribe( "dog" )

    -- 判断是否成功订阅
    if not func then
      return nil
    end

    -- 获取值
    local res, err = func() --func()=func(true)
    -- 如果失败，取消订阅
    if err then
        func(false)
    end

    -- 如果取到结果，进行页面输出
    if res then
        ngx.say("1: receive: ", cjson.encode(res))
    end

    -- 再次获取
    res, err = func()

    -- 获取成功后，取消订阅 func(false)
    if res then
        ngx.say("2: receive: ", cjson.encode(res))
        func(false)
    end

```

### pipeline

参考 [openresty/lua-resty-redis#Synopsis][]

```lua
    local cjson = require "cjson"
    local red = redis:new();

    red:init_pipeline()

    red:set("cat", "Marry")
    red:set("horse", "Bob")
    red:get("cat")
    red:get("horse")

    local results, err = red:commit_pipeline()

    if not results then
        ngx.say("failed to commit the pipelined requests: ", err)
        return
    else
        ngx.say("pipeline",cjson.encode(results))
    end
    -- output pipeline["OK","OK","Marry","Bob"]
```


### script

参考 [script 压缩复杂请求][linkScript压缩复杂请求]

```lua
    local red = redis:new();

    local id = 1
    local res, err = red:eval([[
        -- 注意在 Redis 执行脚本的时候，从 KEYS/ARGV 取出来的值类型为 string
        local info = redis.call('get', KEYS[1])
        info = cjson.decode(info)
        local g_id = info.gid

        local g_info = redis.call('get', g_id)
        return g_info
        ]], 1, id)

    if not res then
       ngx.say("failed to get the group info: ", err)
       return
    end

    ngx.say("script",res)
```

## 鸣谢(Thanks)

本工具借鉴了 [lua-resty-redis/lib/resty/redis.lua][] 和 [Redis 接口的二次封装][linkRedis接口的二次封装] 的代码

## 反馈(Feedback)

如果有问题，欢迎提 [issues][]

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-redis-util](https://github.com/anjia0532/lua-resty-redis-util){target=_blank}.