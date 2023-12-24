# *push-stream*: NGINX push stream module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-push-stream
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_push_stream_module.so;
```


This document describes nginx-module-push-stream [v0.5.5](https://github.com/wandenberg/nginx-push-stream-module/releases/tag/0.5.5){target=_blank} 
released on Dec 11 2021.

<hr />

A pure stream http push technology for your Nginx setup.

[Comet](http://en.wikipedia.org/wiki/Comet_%28programming%29) made easy
and **really scalable**.

Supports [EventSource](http://dev.w3.org/html5/eventsource/),
[WebSocket](http://dev.w3.org/html5/websockets/), Long Polling, and
Forever Iframe. See [some examples](#examples) bellow.

\_This module is not distributed with the Nginx source. See [the
installation instructions](installation._)

Available on github at
[nginx_push_stream_module](https://github.com/wandenberg/nginx-push-stream-module)

## Changelog

Always take a look at [CHANGELOG.textile](CHANGELOG.textile) to see
what’s new.

## Contribute

After you try this module and like it, feel free to [give something
back](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4LP6P9A7BC37S),
and help in the maintenance of the project ;)  
[![](https://www.paypalobjects.com/WEBSCR-640-20110429-1/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4LP6P9A7BC37S)

## Status

This module is considered production ready.

## Basic Configuration

        # add the push_stream_shared_memory_size to your http context
        http {
           push_stream_shared_memory_size 32M;

            # define publisher and subscriber endpoints in your server context
            server {
               location /channels-stats {
                    # activate channels statistics mode for this location
                    push_stream_channels_statistics;

                    # query string based channel id
                    push_stream_channels_path               $arg_id;
                }

                location /pub {
                   # activate publisher (admin) mode for this location
                   push_stream_publisher admin;

                    # query string based channel id
                    push_stream_channels_path               $arg_id;
                }

                location ~ /sub/(.*) {
                    # activate subscriber (streaming) mode for this location
                    push_stream_subscriber;

                    # positional channel path
                    push_stream_channels_path                   $1;
                }
            }
        }

## Basic Usage

You can feel the flavor right now at the command line. Try using more
than  
one terminal and start playing http pubsub:

        # Subs
        curl -s -v --no-buffer 'http://localhost/sub/my_channel_1'
        curl -s -v --no-buffer 'http://localhost/sub/your_channel_1'
        curl -s -v --no-buffer 'http://localhost/sub/your_channel_2'

        # Pubs
        curl -s -v -X POST 'http://localhost/pub?id=my_channel_1' -d 'Hello World!'
        curl -s -v -X POST 'http://localhost/pub?id=your_channel_1' -d 'Hi everybody!'
        curl -s -v -X POST 'http://localhost/pub?id=your_channel_2' -d 'Goodbye!'

        # Channels Stats for publisher (json format)
        curl -s -v 'http://localhost/pub?id=my_channel_1'

        # All Channels Stats summarized (json format)
        curl -s -v 'http://localhost/channels-stats'

        # All Channels Stats detailed (json format)
        curl -s -v 'http://localhost/channels-stats?id=ALL'

        # Prefixed Channels Stats detailed (json format)
        curl -s -v 'http://localhost/channels-stats?id=your_channel_*'

        # Channels Stats (json format)
        curl -s -v 'http://localhost/channels-stats?id=my_channel_1'

        # Delete Channels
        curl -s -v -X DELETE 'http://localhost/pub?id=my_channel_1'

## Some Examples <a name="examples" href="#"> </a>

-   [Curl examples](docs/examples/curl.textile#curl)
-   [Forever (hidden)
    iFrame](docs/examples/forever_iframe.textile#forever_iframe)
-   [Event Source](docs/examples/event_source.textile#event_source)
-   [WebSocket](docs/examples/websocket.textile#websocket)
-   [Long Polling](docs/examples/long_polling.textile#long_polling)
-   [JSONP](docs/examples/long_polling.textile#jsonp)
-   [M-JPEG](docs/examples/m_jpeg.textile#m_jpeg)
-   [Other
    examples](https://github.com/wandenberg/nginx-push-stream-module/wiki/_pages)

## FAQ <a names="faq" href="#"> </a>

Doubts?! Check the
[FAQ](https://github.com/wandenberg/nginx-push-stream-module/wiki/_pages).

## Bug report <a name="bug_report" href="#"> </a>

To report a bug, please provide the following information when
applicable

1.  Which push stream module version is been used (commit sha1)?
2.  Which nginx version is been used?
3.  Nginx configuration in use
4.  “nginx -V” command outuput
5.  Core dump indicating a failure on the module code. Check
    [here](http://wiki.nginx.org/Debugging) how to produce one.
6.  Step by step description to reproduce the error.

## Who is using the module? <a names="faq" href="#"> </a>

Do you use this module? Put your name on the
[list](https://github.com/wandenberg/nginx-push-stream-module/wiki/_pages).

## Javascript Client <a name="javascript_client" href="#"> </a>

There is a javascript client implementation
[here](docs/javascript_client.textile#javascript_client), which is
framework independent. Try and help improve it. ;)

## Directives

\(1\) Defining locations, (2) Main configuration, (3) Subscribers
configuration, (4) Publishers configuration, (5) Channels Statistics
configuration, (6) WebSocket configuration

|                                                                                                                                        |       |       |       |       |       |       |
|----------------------------------------------------------------------------------------------------------------------------------------|-------|-------|-------|-------|-------|-------|
| Directive                                                                                                                              | \(1\) | \(2\) | \(3\) | \(4\) | \(5\) | \(6\) |
| [push_stream_channels_statistics](docs/directives/channels_statistics.textile#push_stream_channels_statistics)                         |   x   |   -   |   -   |   -   |   -   |   -   |
| [push_stream_publisher](docs/directives/publishers.textile#push_stream_publisher)                                                      |   x   |   -   |   -   |   -   |   -   |   -   |
| [push_stream_subscriber](docs/directives/subscribers.textile#push_stream_subscriber)                                                   |   x   |   -   |   -   |   -   |   -   |   -   |
| [push_stream_shared_memory_size](docs/directives/main.textile#push_stream_shared_memory_size)                                          |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_channel_deleted_message_text](docs/directives/main.textile#push_stream_channel_deleted_message_text)                      |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_channel_inactivity_time](docs/directives/main.textile#push_stream_channel_inactivity_time)                                |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_ping_message_text](docs/directives/main.textile#push_stream_ping_message_text)                                            |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_timeout_with_body](docs/directives/subscribers.textile#push_stream_timeout_with_body)                                     |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_message_ttl](docs/directives/main.textile#push_stream_message_ttl)                                                        |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_max_subscribers_per_channel](docs/directives/main.textile#push_stream_max_subscribers_per_channel)                        |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_max_messages_stored_per_channel](docs/directives/main.textile#push_stream_max_messages_stored_per_channel)                |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_max_channel_id_length](docs/directives/main.textile#push_stream_max_channel_id_length)                                    |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_max_number_of_channels](docs/directives/main.textile#push_stream_max_number_of_channels)                                  |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_max_number_of_wildcard_channels](docs/directives/main.textile#push_stream_max_number_of_wildcard_channels)                |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_wildcard_channel_prefix](docs/directives/main.textile#push_stream_wildcard_channel_prefix)                                |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_events_channel_id](docs/directives/main.textile#push_stream_events_channel_id)                                            |   -   |   x   |   -   |   -   |   -   |   -   |
| [push_stream_channels_path](docs/directives/subscribers.textile#push_stream_channels_path)                                             |   -   |   -   |   x   |   x   |   x   |   x   |
| [push_stream_store_messages](docs/directives/publishers.textile#push_stream_store_messages)                                            |   -   |   -   |   -   |   x   |   -   |   x   |
| [push_stream_channel_info_on_publish](docs/directives/publishers.textile#push_stream_channel_info_on_publish)                          |   -   |   -   |   -   |   x   |   -   |   -   |
| [push_stream_authorized_channels_only](docs/directives/subscribers.textile#push_stream_authorized_channels_only)                       |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_header_template_file](docs/directives/subscribers.textile#push_stream_header_template_file)                               |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_header_template](docs/directives/subscribers.textile#push_stream_header_template)                                         |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_message_template](docs/directives/subscribers.textile#push_stream_message_template)                                       |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_footer_template](docs/directives/subscribers.textile#push_stream_footer_template)                                         |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_wildcard_channel_max_qtd](docs/directives/subscribers.textile#push_stream_wildcard_channel_max_qtd)                       |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_ping_message_interval](docs/directives/subscribers.textile#push_stream_ping_message_interval)                             |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_subscriber_connection_ttl](docs/directives/subscribers.textile#push_stream_subscriber_connection_ttl)                     |   -   |   -   |   x   |   -   |   -   |   x   |
| [push_stream_longpolling_connection_ttl](docs/directives/subscribers.textile#push_stream_longpolling_connection_ttl)                   |   -   |   -   |   x   |   -   |   -   |   -   |
| [push_stream_websocket_allow_publish](docs/directives/subscribers.textile#push_stream_websocket_allow_publish)                         |   -   |   -   |   -   |   -   |   -   |   x   |
| [push_stream_last_received_message_time](docs/directives/subscribers.textile#push_stream_last_received_message_time)                   |   -   |   -   |   x   |   -   |   -   |   -   |
| [push_stream_last_received_message_tag](docs/directives/subscribers.textile#push_stream_last_received_message_tag)                     |   -   |   -   |   x   |   -   |   -   |   -   |
| [push_stream_last_event_id](docs/directives/subscribers.textile#push_stream_last_event_id)                                             |   -   |   -   |   x   |   -   |   -   |   -   |
| [push_stream_user_agent](docs/directives/subscribers.textile#push_stream_user_agent)                                                   |   -   |   -   |   x   |   -   |   -   |   -   |
| [push_stream_padding_by_user_agent](docs/directives/subscribers.textile#push_stream_padding_by_user_agent)                             |   -   |   -   |   x   |   -   |   -   |   -   |
| [push_stream_allowed_origins](docs/directives/subscribers.textile#push_stream_allowed_origins)                                         |   -   |   -   |   x   |   -   |   -   |   -   |
| [push_stream_allow_connections_to_events_channel](docs/directives/subscribers.textile#push_stream_allow_connections_to_events_channel) |   -   |   -   |   x   |   -   |   -   |   x   |

## Installation <a name="installation" href="#"> </a>

        # clone the project
        git clone https://github.com/wandenberg/nginx-push-stream-module.git
        NGINX_PUSH_STREAM_MODULE_PATH=$PWD/nginx-push-stream-module

        # get desired nginx version (works with 1.2.0+)
        wget http://nginx.org/download/nginx-1.2.0.tar.gz

        # unpack, configure and build
        tar xzvf nginx-1.2.0.tar.gz
        cd nginx-1.2.0
        ./configure --add-module=../nginx-push-stream-module
        make

        # install and finish
        sudo make install

        # check
        sudo /usr/local/nginx/sbin/nginx -v
            nginx version: nginx/1.2.0

        # test configuration
        sudo /usr/local/nginx/sbin/nginx -c $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf -t
            the configuration file $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf syntax is ok
            configuration file $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf test is successful

        # run
        sudo /usr/local/nginx/sbin/nginx -c $NGINX_PUSH_STREAM_MODULE_PATH/misc/nginx.conf

## Memory usage

Just as information is listed below the minimum amount of memory used
for each object:

-   message on shared = 200 bytes
-   channel on shared = 270 bytes
-   subscriber  
    on shared = 160 bytes  
    on system = 6550 bytes

## Tests

The server tests for this module are written in Ruby, and are acceptance
tests, click [here](docs/server_tests.textile) for more details.

## Discussion

Nginx Push Stream Module [Discussion
Group](https://groups.google.com/group/nginxpushstream)

## Contributors

[People](https://github.com/wandenberg/nginx-push-stream-module/contributors)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-push-stream](https://github.com/wandenberg/nginx-push-stream-module){target=_blank}.