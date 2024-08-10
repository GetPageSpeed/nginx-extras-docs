# *pubsub*: Lua Pubsub client driver for nginx-module-lua based on the cosocket API


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-pubsub
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-pubsub
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-pubsub [v1.4](https://github.com/wingify/lua-resty-pubsub/releases/tag/v1.4){target=_blank} 
released on Apr 17 2021.
    
<hr />

Lua Pubsub client driver for the `ngx_lua` based on the cosocket API.

[![lua module](https://img.shields.io/badge/lua-module-blue?style=for-the-badge&logo=lua)](https://luarocks.org/modules/vwointegration/lua-resty-pubsub)
[![lua module](https://img.shields.io/badge/lua%20rocks-1.4-orange?style=for-the-badge&logo=lua)](https://luarocks.org/modules/vwointegration/lua-resty-pubsub)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge&logo=)](https://opensource.org/licenses/MIT)

## Description

This Lua library is a Pubsub client driver for the ngx_lua nginx module: http://wiki.nginx.org/HttpLuaModule

This Lua library takes advantage of ngx_lua's cosocket API, which ensures 100% nonblocking behavior. This library pushes messages (with attributes) to Google Cloud pubsub using nginx timers and http requests.

Note that at least [ngx_lua 0.9.3](https://github.com/openresty/lua-nginx-module/tags) or [ngx_openresty 1.4.3.7](http://openresty.org/#Download) is required, and unfortunately only LuaJIT supported (`--with-luajit`).

## Synopsis

```lua
    server {
        location = /publish {
            resolver 8.8.8.8 ipv6=off;

            content_by_lua_block {
                local cjson = require "cjson"
                local pubsub_producer = require "resty.pubsub.producer"
                local OAUTH_TOKEN = ngx.shared.OAUTH_TOKEN -- A different dictionary can also be provided

                -- A callback which will recieve messages if gets successfully sent
                -- Types of messages & err are a table
                local success_callback = function (topic, err, messages)
                    ngx.log(ngx.INFO, "Messages: ", cjson.encode(messages), " successfully pushed to topic: ", topic)
                end

                -- A callback which will recieve messages if gets failed
                -- Types of messages & err are a table
                local error_callback = function (topic, err, messages)
                    for _, message in ipairs(messages) do
                        ngx.log(ngx.ERR, "Failed to send Message : ", cjson.encode(message), " with err: ", cjson.encode(err))
                    end
                end

                local publish = function()

                    -- Pubsub Producer Config
                    local pubsub_config = {
                        project_id = "demo-project",
                        topic = "demo-topic",
                        pubsub_base_domain = "pubsub.googleapis.com",
                        pubsub_base_port = 443,
                        is_emulator = false,
                        producer_config = {
                            max_batch_size = 200, -- number of packets
                            max_buffering = 5000, -- max number of packets in buffer
                            timer_interval = 10000, -- in milliseconds
                            last_flush_interval = 5000, -- in milliseconds
                            http_timeout = 6000, -- in milliseconds
                            keepalive_max_idle_timeout = 2000, -- in milliseconds
                            keepalive_pool_size = 50
                        },
                        oauth_config = {
                            service_account_key_path = "/etc/key.json", -- Replace this with your own key path
                            oauth_base_uri = "https://www.googleapis.com/oauth2/v4/token",
                            oauth_scopes = {
                                "https://www.googleapis.com/auth/pubsub"
                            },
                            oauth_token_dict = OAUTH_TOKEN
                        },
                        success_callback = success_callback,
                        error_callback = error_callback
                    }

                    -- Create the producer object
                    -- No matter how many times you call new, the producer instance will always be generated once per topic per worker process
                    local producer, err = pubsub_producer:new(pubsub_config)

                    -- Also check if there is any error while initializing producer
                    if err ~= nil then
                        ngx.log(ngx.ERR, "Unable to create pubsub producer ", err)
                        return
                    end

                    -- Finally send the message with attributes.
                    local ok, send_err = producer:send("Some Random Text", {
                        attr1 = "Test1",
                        attr2 = "Test2"
                    })

                    -- Also check if there is any error while sending message
                    if send_err ~= nil then
                        ngx.log(ngx.ERR, "Unable to send data to pubsub: ", send_err)
                        return
                    end

                end

                -- Publish Message
                publish()
            }

        }
    }
```

## Configs

### Producer Configs

| Property | Data Type | Description | Default Value |
| :---: | :---: | :---: | :---: |
| project_id | string | Specifies the project id as a string of your Pub/Sub project | none (Required) |
| topic | string | Specifies the topic in which the data needs to be send | none (Required) |
| pubsub_base_domain | string | Specifies the base domain through which the http connection is made. | pubsub.googleapis.com |
| pubsub_base_port | number | Specifies the base domain port through which the http connection is made. | 443 |
| is_emulator | boolean |  Specifies a boolean value. true if you are communicating with. | false |
| producer_config.max_batch_size | number | Specifies the max batch size that will be pushed to pubsub. | 200 |
| producer_config.max_buffering | number | Specifies the max size of the buffer which will hold the data for a specific duration of time. | 5000 |
| producer_config.timer_interval | number (milliseconds) | Specifies the time interval in which the stale messages in buffer are checked for publishing. | 10000 |
| producer_config.last_flush_interval | number (milliseconds) | Specifies the max interval between the last flush time and current time. Used when packets in buffer are less than the batch size for a longer period of time. | 10000 |
| producer_config.http_timeout | number (milliseconds) | Sets the timeout protection for subsequent operations, including the connect method. | 5000 |
| producer_config.keepalive_max_idle_timeout | number (milliseconds) | Used in httpc:set_keepalive which attempts to puts the current connection into the ngx_lua cosocket connection pool. | 2000 |
| producer_config.keepalive_pool_size | number | Used in httpc:set_keepalive which attempts to puts the current connection into the ngx_lua cosocket connection pool. | 50 |
| oauth_config.service_account_key_path | string | Specifies the path for service account key that are used to authenticate to pub/sub project. | none (Required) |
| oauth_config.oauth_base_uri | string | Specifies the base uri to which request is made to Google authorization server for a token that will be used in subsequent requests. | https://www.googleapis.com/oauth2/v4/token |
| oauth_config.oauth_scopes | list of string | Specifies a table comprising of OAuth 2.0 scopes that you might need to request to access Google APIs, depending on the level of access you need. | {"https://www.googleapis.com/auth/pubsub"} |
| oauth_config.oauth_token_dict | lua_shared_dict | Specifies a shared memory zone across workers, to serve as a storage for the oauth token. | ngx.shared.OAUTH_TOKEN |
| success_handler | function | This is a callback function which will be provided with all the messages with their attributes which are successfully pushed to pubsub. | none (Optional) |
| error_handler | function | This is a callback function which will be executed when a batch fails. | none (Optional) |

## Modules

### resty.pubsub.producer

To load this module, just do this

```lua
    local producer = require "resty.pubsub.producer"
```

### Methods

#### new

`syntax: local p, err = producer:new(pubsub_config)`

#### send
`syntax: p:send(message, attributes)`

* Requires a message of type string and attributes of type table

## See Also

* the ngx_lua module: http://wiki.nginx.org/HttpLuaModule


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-pubsub](https://github.com/wingify/lua-resty-pubsub){target=_blank}.