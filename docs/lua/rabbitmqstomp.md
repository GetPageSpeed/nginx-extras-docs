---

title: "Opinionated Lua RabbitMQ client library for nginx-module-lua apps based on the cosocket API"
description: "RPM package lua-resty-rabbitmqstomp: Opinionated Lua RabbitMQ client library for nginx-module-lua apps based on the cosocket API"

---
  
# *rabbitmqstomp*: Opinionated Lua RabbitMQ client library for nginx-module-lua apps based on the cosocket API


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-rabbitmqstomp
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-rabbitmqstomp
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-rabbitmqstomp [v0.1](https://github.com/wingify/lua-resty-rabbitmqstomp/releases/tag/v0.1){target=_blank} 
released on Jun 01 2013.
    
<hr />

lua-resty-rabbitmqstomp - Lua RabbitMQ client library which uses cosocket api for
communication over STOMP 1.2 with a RabbitMQ broker which has the STOMP plugin.

## Limitations

This library is opinionated and has certain assumptions and limitations which
may be addressed in future;

- RabbitMQ server should have the STOMP adapter enabled that supports STOMP v1.2
- Assumption that users, vhost, exchanges, queues and bindings are already setup

## Status

This library is considered production ready for publishing reliable messages to
RabbitMQ.

## STOMP v1.2 Client Implementation

This library uses STOMP 1.2 for communication with RabbitMQ broker and
implements extensions and restrictions of the RabbitMQ Stomp plugin.

Internally, RabbitMQ uses AMQP to communicate further. This way the library
enables implementation of consumers and producers which communicate with the
RabbitMQ broker over STOMP, over AMQP. The protocol is frame based and has a
command, headers and body terminated by an EOL (^@) which consists of `\r` (013)
and required `\n` (010) over a TCP stream:

    COMMAND
    header1:value1
    header2: value2

    BODY^@

COMMAND is followed by EOL, then EOL separated header in key:value pair format
and then a blank line which is where the BODY starts and the frame is terminated
by ^@ EOL. COMMAND and headers are UTF-8 encoded.

## Connection

To connect we create and send a CONNECT frame over a TCP socket provided by the
cosocket api connecting to the broker IP, both IPv4 and IPv6 are supported. In
the frame we use login, passcode for authentication, accept-version to enforce
client STOMP version support and host to select the VHOST of the broker.

    CONNECT
    accept-version:1.2
    login:guest
    passcode:guest
    host:/devnode
    heart-beat:optional

    ^@

On error, an ERROR frame is returned for example:

    ERROR
    message:Bad CONNECT
    content-type:text/plain
    version:1.0,1.1,1.2
    content-length:32

    Access refused for user 'admin'^@

On successful connection, we are returned a CONNECTED frame by the broker, for
example:

    CONNECTED
    session:session-sGF0vjCKH1bLhFr6w9QwuQ
    heart-beat:0,0
    server:RabbitMQ/3.0.4
    version:1.2

For creating a connection, username, password, vhost, heartbeat, broker host and
port should be provided.

## Publishing

We can publish messages to an exchange with a routing key, persistence mode,
delivery mode and other header using the SEND command:

    SEND
    destination:/exchange/exchange_name/routing_key
    app-id: luaresty
    delivery-mode:2
    persistent:true
    content-type:json/application
    content-length:5

    hello^@

Note that content-length includes the message and EOL byte.

## Methods

### new

`syntax: rabbit, err = rabbitmqstomp:new()`

Creates a RabbitMQ object. In case of failures, returns nil and a string describing the error.

### set_timeout

`syntax: rabbit:set_timeout(time)`

Sets the timeout (in ms) protection for subsequent operations, including the connect method.
Note timeout should be set before calling any other method after creating the object.

### connect

`syntax: ok, err = red:connect{host=host, port=port, username=username, password=password, vhost=vhost}`

Attempts to connect to a stomp broker the RabbitMQ STOMP adapter on a host, port is listening on.

If none of the values are supplied default values are assumed:

- host: localhost
- port: 61613
- username: guest
- password: guest
- vhost: /

`pool` can be given to be used for a custom name for the connection pool being used.

### send

`syntax: rabbit:send(msg, headers)`

Publishers message with a set of headers.

Some header values which can be set:

`destination`: Destination of the message, for example /exchange/name/binding`
`persistent`: To delivery a persistent message, value should be "true" if declared
`receipt`: Receipt for confirmed delivery
`content-type`: Type of message, for example application/json

For list of supported headers see the STOMP protocol extensions and
restriction page: `https://www.rabbitmq.com/stomp.html`

### subscribe

`syntax: rabbit:subscribe(headers)`

Subscribe to a queue by using `headers`. It should have a id when persistent is
true. On successful subscription MESSAGE frames are sent by the broker.

### unsubscribe

`syntax: rabbit:unsubscribe(headers)`

Unsubscribes from a queue by using `headers`.
On successful unsubscription MESSAGE frames will stop coming from the broker.

### receive

`syntax: rabbit:receive())`

Tries to read any MESSAGE frames received and returns the message. Trying to receive
without a valid subscription will lead to errors.

### get_reused_times

`syntax: times, err = rabbit:get_reused_times()`

This method returns the (successfully) reused times for the current connection.
In case of error, it returns nil and a string describing the error.

If the current connection does not come from the built-in connection pool, then
this method always returns 0, that is, the connection has never been reused
(yet). If the connection comes from the connection pool, then the return value
is always non-zero. So this method can also be used to determine if the current
connection comes from the pool.

### set_keepalive

`syntax: ok, err = rabbit:set_keepalive(max_idle_timeout, pool_size)`

Puts the current RabbitMQ connection immediately into the ngx_lua cosocket connection pool.

You can specify the max idle timeout (in ms) when the connection is in the pool
and the maximal size of the pool every nginx worker process.

In case of success, returns 1. In case of errors, returns nil with a string describing the error.

Only call this method in the place you would have called the close method
instead. Calling this method will immediately turn the current redis object into
the closed state. Any subsequent operations other than connect() on the current
objet will return the closed error.

### close

`syntax: ok, err = rabbit:close()`

Closes the current RabbitMQ connection gracefully by sending a DISCONNECT to the
RabbitMQ STOMP broker and returns the status.

In case of success, returns 1. In case of errors, returns nil with a string describing the error.

## Example

A simple producer that can send reliable persistent message to an exchange with
some binding:

    local rabbitmq = require "resty.rabbitmqstomp"
    local mq, err = rabbitmq:new()
    if not mq then
          return
    end

    mq:set_timeout(10000)

    local ok, err = mq:connect {
                        host = "127.0.0.1",
                        port = 61613,
                        username = "guest",
                        password = "guest",
                        vhost = "/"
                    }
    if not ok then
        return
    end

    local strlen =  string.len

    local msg = "{'key': 'value'}"
    local headers = {}
    headers["destination"] = "/exchange/test/binding"
    headers["receipt"] = "msg#1"
    headers["app-id"] = "luaresty"
    headers["persistent"] = "true"
    headers["content-type"] = "application/json"

    local ok, err = mq:send(msg, headers)
    if not ok then
        return
    end
    ngx.log(ngx.INFO, "Published: " .. msg)

    local headers = {}
    headers["destination"] = "/amq/queue/queuename"
    headers["persistent"] = "true"
    headers["id"] = "123"

    local ok, err = mq:subscribe(headers)
    if not ok then
        return
    end

    local data, err = mq:receive()
    if not ok then
        return
    end
    ngx.log(ngx.INFO, "Consumed: " .. data)

    local headers = {}
    headers["persistent"] = "true"
    headers["id"] = "123"

    local ok, err = mq:unsubscribe(headers)

    local ok, err = mq:set_keepalive(10000, 10000)
    if not ok then
        return
    end

## See Also

- [STOMP 1.2 Spec](http://stomp.github.io/stomp-specification-1.2.html)
- The [lua-resty-mysql](https://github.com/agentzh/lua-resty-mysql) library
- [Openresty google group](https://groups.google.com/forum/?fromgroups#!forum/openresty-en)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-rabbitmqstomp](https://github.com/wingify/lua-resty-rabbitmqstomp){target=_blank}.