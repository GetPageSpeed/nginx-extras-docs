---

title: "ZeroMQ logger module for NGINX"
description: "RPM package nginx-module-log-zmq. ZeroMQ logger module for NGINX "

---

# *[BETA!] log-zmq*: ZeroMQ logger module for NGINX


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
    dnf -y install nginx-module-log-zmq
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-log-zmq
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_log_zmq_module.so;
```


This document describes nginx-module-log-zmq [v0](https://github.com/dvershinin/nginx-log-zmq/releases/tag/v0){target=_blank} 
released on Nov 28 2021.

Production stability is *not guaranteed*.
<hr />

ZeroMQ logger module for nginx.

[ZeroMQ](http://zeromq.org), \zero-em-queue\, is a protocol for messages exchange. It's a easy
way to communicate using any language or platform via inproc, IPC, TCP, TPIC or multicast.
It's asynchronous and only requires a small library.



## Status

This module is already production ready.

## Description

This is a nginx logger module integrated with [ZeroMQ](http://zeromq.org) library.

`nginx-log-zmq` provides a very efficient way to log data for one or more PUB/SUB subscribers, over one or more different endpoints. This can be useful for data gathering and processing.

The message format can be the same as the tradicional log format which gives a interesting way to `tail` data via the network or exploring other text formats like JSON. As with the traditional log, it's possible to use nginx variables updated each request.

All messages are sent asynchronously and do not block the normal behaviour of the nginx server. As expected, the connections are resilient to network failures.

## Synopsis

```nginx
	http {
		# simple message to an IPC endpoint with 4 threads and 1000 queue elements

		log_zmq_server main "/tmp/main.ipc" ipc 4 1000;
		log_zmq_endpoint  main "/topic/";

		log_zmq_format main '{"remote_addr":"$remote_addr"}'

		# send messages to a subscriber listening at 127.0.0.1:5556

		log_zmq_server secondary 127.0.0.1:5556 tcp 4 1000;

		# set secondary endpoint
		log_zmq_endpoint secondary "/endpoint/";

		# set format using multiline
		log_zmq_format secondary '{"request_uri":"$request_uri",'
								   '{"status":"$status"}';


		server {

			location /status {
				# mute all messages from log_zmq for this location

				log_zmq_off all;
			}

			location /endpoint {
				# mute main messages from log_zmq for this location

				log_zmq_off main;
			}
		}
	}
```

## Directives

## log_zmq_server
**syntax:** *log_zmq_server &lt;definition_name&gt; &lt;address&gt; &lt;ipc|tcp&gt; &lt;threads&gt; &lt;queue size&gt;*

**default:** no

**context:** http

Configures a server (PUB/SUB subscriber) to connect to.

The following options are required:

**definition_name** &lt;name&gt; - the name that nginx will use to identify this logger instance.

**address** &lt;path&gt;|&lt;ipaddress&gt;:&lt;port&gt; - the subscriber's address. If you are using the IPC
protocol, you should specify the `<path>` for the unix socket. If you are using the TCP
protocol, you should specify the `<ipaddress>` and `<port>` where your ZeroMQ subscriber is listening.

**protocol** &lt;ipc|tcp&gt; - the protocol to be used for communication.

**threads** &lt;integer&gt; - the number of I/O threads to be used.

**queue_size** &lt;integer&gt; - the maximum queue size for messages waiting to be sent.


## log_zmq_endpoint

**syntax:** *log_zmq_endpoint &lt;definition_name&gt; "&lt;topic&gt;"*

**default:** no

**context:** http

Configures the topic for the ZeroMQ messages.

**definition_name** &lt;name&gt; - the name that nginx will use to identify this logger instance.

**topic** &lt;topic&gt; - the topic for the messages. This is a string (which can be a nginx variable) prepended to every sent message. For example, if you send the message "hello" to the "/talk:" topic, the message will end up as "/talk:hello".

Example:

```nginx
http {
	log_zmq_server main "/tmp/example.ipc" 4 1000;

	# send a message for for an topic based on response status
	log_zmq_endpoint main "/remote/$status";
}
```


## log_zmq_format

**syntax:** *log_zmq_format &lt;definition_name&gt; "&lt;format&gt;"*

**default:** no

**context:** http

Configures the ZeroMQ message format.

**definition_name** &lt;name&gt; - the name that nginx will use to identify this logger instance.

**format** &lt;format&gt; - the format for the messages. This defines the actual messages sent to the PUB/SUB subscriber. It follows the sames rules as the standard `log_format` directive. It is possible to use nginx variables here, and also to break it over multiple lines.

```nginx
http {
	log_zmq_format main '{"line1": value,'
                          '{"line2": value}';
}
```


## log_zmq_off

**syntax:** *log_zmq_off &lt;definition_name&gt;|all*

**default:** no

**context:** location

Turn off ZeroMQ logging in the current context.

**definition_name** &lt;name&gt; the name of the logger instance to be muted. If the special `all` name is used, all logger instances are muted.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-log-zmq](https://github.com/dvershinin/nginx-log-zmq){target=_blank}.