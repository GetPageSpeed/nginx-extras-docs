---

title: "Lua kafka client driver for nginx-module-lua based on the cosocket API"
description: "RPM package lua-resty-kafka: Lua kafka client driver for nginx-module-lua based on the cosocket API"

---
  
# *kafka*: Lua kafka client driver for nginx-module-lua based on the cosocket API


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-kafka
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-kafka
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-kafka [v0.23](https://github.com/doujiang24/lua-resty-kafka/releases/tag/v0.23){target=_blank} 
released on Nov 03 2023.
    
<hr />

lua-resty-kafka - Lua kafka client driver for the ngx_lua based on the cosocket API

## Status

This library is still under early development and is still experimental.

## Description

This Lua library is a Kafka client driver for the ngx_lua nginx module:

http://wiki.nginx.org/HttpLuaModule

This Lua library takes advantage of ngx_lua's cosocket API, which ensures
100% nonblocking behavior.

Note that at least [ngx_lua 0.9.3](https://github.com/openresty/lua-nginx-module/tags) or [openresty 1.4.3.7](http://openresty.org/#Download) is required, and unfortunately only LuaJIT supported (`--with-luajit`).

Note for `ssl` connections at least [ngx_lua 0.9.11](https://github.com/openresty/lua-nginx-module/tags) or [openresty 1.7.4.1](http://openresty.org/#Download) is required, and unfortunately only LuaJIT supported (`--with-luajit`).

## Synopsis

```lua
    server {
        location /test {
            content_by_lua '
                local cjson = require "cjson"
                local client = require "resty.kafka.client"
                local producer = require "resty.kafka.producer"

                local broker_list = {
                    {
                        host = "127.0.0.1",
                        port = 9092,

                        -- optional auth
                        sasl_config = {
                            mechanism = "PLAIN",
                            user = "USERNAME",
                            password = "PASSWORD",
                        },
                    },
                }

                local key = "key"
                local message = "halo world"

                -- usually we do not use this library directly
                local cli = client:new(broker_list)
                local brokers, partitions = cli:fetch_metadata("test")
                if not brokers then
                    ngx.say("fetch_metadata failed, err:", partitions)
                end
                ngx.say("brokers: ", cjson.encode(brokers), "; partitions: ", cjson.encode(partitions))


                -- sync producer_type
                local p = producer:new(broker_list)

                local offset, err = p:send("test", key, message)
                if not offset then
                    ngx.say("send err:", err)
                    return
                end
                ngx.say("send success, offset: ", tonumber(offset))

                -- this is async producer_type and bp will be reused in the whole nginx worker
                local bp = producer:new(broker_list, { producer_type = "async" })

                local ok, err = bp:send("test", key, message)
                if not ok then
                    ngx.say("send err:", err)
                    return
                end

                ngx.say("send success, ok:", ok)
            ';
        }
    }
```


## Modules


## resty.kafka.client

To load this module, just do this

```lua
    local client = require "resty.kafka.client"
```

### Methods

#### new

`syntax: c = client:new(broker_list, client_config)`

The `broker_list` is a list of broker, like the below

```json
[
    {
        "host": "127.0.0.1",
        "port": 9092,

        // optional auth
        "sasl_config": {
            //support mechanism: PLAIN、SCRAM-SHA-256、SCRAM-SHA-512
            "mechanism": "PLAIN",
            "user": "USERNAME",
            "password": "PASSWORD"
        }
    }
]
```
* `sasl_config`

  support mechanism: PLAIN、SCRAM-SHA-256、SCRAM-SHA-512.

  warn:SCRAM-SHA-256、SCRAM-SHA-512 need install lua-resty-jit-uuid and lua-resty-openssl

An optional `client_config` table can be specified. The following options are as follows:

client config

* `socket_timeout`

    Specifies the network timeout threshold in milliseconds. *SHOULD* lagrer than the `request_timeout`.

* `keepalive_timeout`

    Specifies the maximal idle timeout (in milliseconds) for the keepalive connection.

* `keepalive_size`

    Specifies the maximal number of connections allowed in the connection pool for per Nginx worker.

* `refresh_interval`

    Specifies the time to auto refresh the metadata in milliseconds. Then metadata will not auto refresh if is nil.

* `ssl`

    Specifies if client should use ssl connection. Defaults to false. See: https://github.com/openresty/lua-nginx-module#tcpsocksslhandshake

* `ssl_verify`

    Specifies if client should perform SSL verification. Defaults to false. See: https://github.com/openresty/lua-nginx-module#tcpsocksslhandshake

* `resolver`

    Specifies a function to host resolving, which returns a string of IP or `nil`, to override system default host resolver. Default `nil`, no resolving performed. Example `function(host) if host == "some_host" then return "10.11.12.13" end end`

#### fetch_metadata
`syntax: brokers, partitions = c:fetch_metadata(topic)`

In case of success, return the all brokers and partitions of the `topic`.
In case of errors, returns `nil` with a string describing the error.


#### refresh
`syntax: brokers, partitions = c:refresh()`

This will refresh the metadata of all topics which have been fetched by `fetch_metadata`.
In case of success, return all brokers and all partitions of all topics.
In case of errors, returns `nil` with a string describing the error.


#### choose_api_version

`syntax: api_version = c:choose_api_version(api_key, min_version, max_version)`

This helps the client to select the correct version of the `api_key` corresponding to the API.

When `min_version` and `max_version` are provided, it will act as a limit and the selected versions in the return value will not exceed their limits no matter how high or low the broker supports the API version. When they are not provided, it will follow the range of versions supported by the broker.

Tip: The version selection strategy is to choose the maximum version within the allowed range.


## resty.kafka.producer

To load this module, just do this

```lua
    local producer = require "resty.kafka.producer"
```

### Methods

#### new

`syntax: p = producer:new(broker_list, producer_config?, cluster_name?)`

It's recommend to use async producer_type.

`broker_list` is the same as in `client`

An optional options table can be specified. The following options are as follows:

`socket_timeout`, `keepalive_timeout`, `keepalive_size`, `refresh_interval`, `ssl`, `ssl_verify`  are the same as in `client_config`

producer config, most like in <http://kafka.apache.org/documentation.html#producerconfigs>

* `producer_type`

    Specifies the `producer.type`. "async" or "sync"

* `request_timeout`

    Specifies the `request.timeout.ms`. Default `2000 ms`

* `required_acks`

    Specifies the `request.required.acks`, *SHOULD NOT* be zero. Default `1`.

* `max_retry`

    Specifies the `message.send.max.retries`. Default `3`.

* `retry_backoff`

    Specifies the `retry.backoff.ms`. Default `100`.

* `api_version`

    Specifies the produce API version. Default `0`.
    If you use Kafka 0.10.0.0 or higher, `api_version` can use `0`, `1` or `2`.
    If you use Kafka 0.9.x, `api_version` should be `0` or `1`.
    If you use Kafka 0.8.x, `api_version` should be `0`.

* `partitioner`

    Specifies the partitioner that choose partition from key and partition num.
    `syntax: partitioner = function (key, partition_num, correlation_id) end`,
    the correlation_id is an auto increment id in producer. Default partitioner is:

    ```lua
    local function default_partitioner(key, num, correlation_id)
        local id = key and crc32(key) or correlation_id
        -- partition_id is continuous and start from 0
        return id % num
    end
    ```

buffer config ( only work `producer_type` = "async" )

* `flush_time`

    Specifies the `queue.buffering.max.ms`. Default `1000`.

* `batch_num`

    Specifies the `batch.num.messages`. Default `200`.

* `batch_size`

    Specifies the `send.buffer.bytes`. Default `1M`(may reach 2M).
    Be careful, *SHOULD* be smaller than the `socket.request.max.bytes / 2 - 10k` config in kafka server.

* `max_buffering`

    Specifies the `queue.buffering.max.messages`. Default `50,000`.

* `error_handle`

    Specifies the error handle, handle data when buffer send to kafka error.
    `syntax: error_handle = function (topic, partition_id, message_queue, index, err, retryable) end`,
    the failed messages in the message_queue is like ```{ key1, msg1, key2, msg2 } ```,
    `key` in the message_queue is empty string `""` even if orign is `nil`.
    `index` is the message_queue length, should not use `#message_queue`.
    when `retryable` is `true` that means kafka server surely not committed this messages, you can safely retry to send;
    and else means maybe, recommend to log to somewhere.

* `wait_on_buffer_full`

    Specifies whether to wait when the buffer queue is full, Default `false`.
    When buffer queue is full, if option passed `true`, 
    will use semaphore wait function to block coroutine until timeout or buffer queue has reduced,
    Otherwise, return "buffer overflow" error with `false`.
    Notice, it could not be used in those phases which do not support yields, i.e. log phase.

* `wait_buffer_timeout`

    Specifies the max wait time when buffer is full, Default `5` seconds.

Not support compression now.

The third optional `cluster_name` specifies the name of the cluster, default `1` (yeah, it's number). You can Specifies different names when you have two or more kafka clusters. And this only works with `async` producer_type.


#### send
`syntax: ok, err = p:send(topic, key, message)`

1. In sync model

    In case of success, returns the offset (** cdata: LL **) of the current broker and partition.
    In case of errors, returns `nil` with a string describing the error.

2. In async model

    The `message` will write to the buffer first.
    It will send to the kafka server when the buffer exceed the `batch_num`,
    or every `flush_time` flush the buffer.

    It case of success, returns `true`.
    In case of errors, returns `nil` with a string describing the error (`buffer overflow`).


#### offset

`syntax: sum, details = p:offset()`

    Return the sum of all the topic-partition offset (return by the ProduceRequest api);
    and the details of each topic-partition


#### flush

`syntax: ok = p:flush()`

Always return `true`.



## resty.kafka.basic-consumer

To load this module, just do this

```lua
    local bconsumer = require "resty.kafka.basic-consumer"
```

This module is a minimalist implementation of a consumer, providing the `list_offset` API for querying by time or getting the start and end offset and the `fetch` API for getting messages in a topic.

In a single call, only the information of a single partition in a single topic can be fetched, and batch fetching is not supported for now. The basic consumer does not support the consumer group related API, so you need to fetch the message after getting the offset through the `list_offset` API, or your service can manage the offset itself.

### Methods

#### new

`syntax: c = bconsumer:new(broker_list, client_config)`

The `broker_list` is a list of broker, like the below

```json
[
    {
        "host": "127.0.0.1",
        "port": 9092,

        // optional auth
        "sasl_config": {
            "mechanism": "PLAIN",
            "user": "USERNAME",
            "password": "PASSWORD"
        }
    }
]
```

An optional `client_config` table can be specified. The following options are as follows:

client config

* `socket_timeout`

    Specifies the network timeout threshold in milliseconds. *SHOULD* lagrer than the `request_timeout`.

* `keepalive_timeout`

    Specifies the maximal idle timeout (in milliseconds) for the keepalive connection.

* `keepalive_size`

    Specifies the maximal number of connections allowed in the connection pool for per Nginx worker.

* `refresh_interval`

    Specifies the time to auto refresh the metadata in milliseconds. Then metadata will not auto refresh if is nil.

* `ssl`

    Specifies if client should use ssl connection. Defaults to false. See: https://github.com/openresty/lua-nginx-module#tcpsocksslhandshake

* `ssl_verify`

    Specifies if client should perform SSL verification. Defaults to false. See: https://github.com/openresty/lua-nginx-module#tcpsocksslhandshake

* `isolation_level`
	This setting controls the visibility of transactional records. See: https://kafka.apache.org/protocol.html

* `client_rack`

    Rack ID of the consumer making this request. See: https://kafka.apache.org/protocol.html

#### list_offset
`syntax: offset, err = c:list_offset(topic, partition, timestamp)`

The parameter timestamp can be a UNIX timestamp or a constant defined in `resty.kafka.protocol.consumer`, `LIST_OFFSET_TIMESTAMP_LAST`, `LIST_OFFSET_TIMESTAMP_FIRST`, `LIST_OFFSET_TIMESTAMP_MAX`, used to get the initial and latest offsets, etc., semantics with the ListOffsets API in Apache Kafka. See: https://kafka.apache.org/protocol.html#The_Messages_ListOffsets

In case of success, return the offset of the specified case.
In case of errors, returns `nil` with a string describing the error.

#### fetch

`syntax: result, err = c:fetch(topic, partition, offset)`

In case of success, return the following `result` of the specified case.
In case of errors, returns `nil` with a string describing the error.

The `result` will contain more information such as the messages:

* `records`

    The table containing the content of the message.

* `errcode`

    The error code of Fetch API. See: https://kafka.apache.org/protocol.html#protocol_error_codes

* `high_watermark`

    The high watermark of Fetch API. See: https://kafka.apache.org/protocol.html#The_Messages_Fetch

* `last_stable_offset`

    The last stable offset of Fetch API. Content depends on the API version, maybe nil. See: https://kafka.apache.org/protocol.html#The_Messages_Fetch that response API version above v4

* `log_start_offset`

    The log start offset of Fetch API. Content depends on the API version, maybe nil. See: https://kafka.apache.org/protocol.html#The_Messages_Fetch that response API version above v5

* `aborted_transactions`

    The aborted transactions of Fetch API. Content depends on the API version, maybe nil. See: https://kafka.apache.org/protocol.html#The_Messages_Fetch that response API version above v4

* `preferred_read_replica`

    The preferred read replica of Fetch API. Content depends on the API version, maybe nil. See: https://kafka.apache.org/protocol.html#The_Messages_Fetch that response API version above v11



## Errors

When you call the modules provided in this library, you may get some errors.
Depending on the source, they can be divided into the following categories.

* Network errors: such as connection rejected, connection timeout, etc. You need to check the connection status of each service in your environment.

* Metadata-related errors: such as Metadata or ApiVersion data cannot be retrieved properly; the specified topic or partition does not exist, etc. You need to check the Kafka Broker and client configuration.

* Error returned by Kafka: sometimes Kafka will include err_code data in the response data, When this problem occurs, the `err` in the return value looks like this `OFFSET_OUT_OF_RANGE`, all uppercase characters, and separated by underscores, and in the current library we provide [a error list of mappings](lib/resty/kafka/errors.lua) corresponding to the textual descriptions. To learn more about these errors, see the descriptions in the [Kafka documentation](https://kafka.apache.org/protocol.html#protocol_error_codes).


## See Also
* the ngx_lua module: http://wiki.nginx.org/HttpLuaModule
* the kafka protocol: https://cwiki.apache.org/confluence/display/KAFKA/A+Guide+To+The+Kafka+Protocol
* the [lua-resty-redis](https://github.com/openresty/lua-resty-redis) library
* the [lua-resty-logger-socket](https://github.com/cloudflare/lua-resty-logger-socket) library
* the [sarama](https://github.com/Shopify/sarama)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-kafka](https://github.com/doujiang24/lua-resty-kafka){target=_blank}.