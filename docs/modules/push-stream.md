# *push-stream*: NGINX push stream module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

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
Nginx Push Stream Module
========================

A pure stream http push technology for your Nginx setup.

[Comet](comet_ref) made easy and **really scalable**.

Supports [EventSource](eventsource_ref), [WebSocket](websocket_ref), Long Polling, and Forever Iframe. See [some examples](examples) bellow.

Available on github at [nginx\_push\_stream\_module](repository)
h1. Changelog
Always take a look at [CHANGELOG.textile](changelog) to see what’s new.

h1. Contribute
After you try this module and like it, feel free to [give something back](donate), and help in the maintenance of the project ;)
![](https://www.paypalobjects.com/WEBSCR-640-20110429-1/en_US/i/btn/btn_donate_LG.gif):donate
h1. Status
This module is considered production ready.
h1. Basic Configuration
\<pre\>
 \# add the push\_stream\_shared\_memory\_size to your http context
 http {
 push\_stream\_shared\_memory\_size 32M;
 \# define publisher and subscriber endpoints in your server context
 server {
 location /channels-stats {
 \# activate channels statistics mode for this location
 push\_stream\_channels\_statistics;
 \# query string based channel id
 push\_stream\_channels\_path \$arg\_id;
 }
 location /pub {
 \# activate publisher mode for this location
 push\_stream\_publisher admin;
 \# query string based channel id
 push\_stream\_channels\_path \$arg\_id;
 }
 location \~ /sub/ {
 \# activate subscriber mode for this location
 push\_stream\_subscriber;
 \# positional channel path
 push\_stream\_channels\_path \$1;
 }
 }
 }
\</pre\>

h1. Basic Usage
You can feel the flavor right now at the command line. Try using more than
one terminal and start playing http pubsub:
\<pre\>
 \# Subs
 curl ~~s~~v —no-buffer ‘http://localhost/sub/my\_channel\_1’
 curl ~~s~~v —no-buffer ‘http://localhost/sub/your\_channel\_1’
 curl ~~s~~v —no-buffer ‘http://localhost/sub/your\_channel\_2’
 \# Pubs
 curl ~~s~~v ~~X POST ‘http://localhost/pub?id=my\_channel\_1’~~d ‘Hello World![]('
    curl -s -v -X POST 'http://localhost/pub?id=your_channel_1' -d 'Hi everybody)’
 curl ~~s~~v ~~X POST ‘http://localhost/pub?id=your\_channel\_2’~~d ‘Goodbye!’
 \# Channels Stats for publisher
 curl ~~s~~v ‘http://localhost/pub?id=my\_channel\_1’
 \# All Channels Stats summarized
 curl ~~s~~v ‘http://localhost/channels-stats’
 \# All Channels Stats detailed
 curl ~~s~~v ‘http://localhost/channels-stats?id=ALL’
 \# Prefixed Channels Stats detailed
 curl ~~s~~v ’http://localhost/channels-stats?id=your\_channel***‘
 \# Channels Stats (json format)
 curl ~~s~~v ’http://localhost/channels-stats?id=my\_channel\_1’
 \# Delete Channels
 curl ~~s~~v -X DELETE ‘http://localhost/pub?id=my\_channel\_1’
\</pre\>

h1. Some Examples <a name="examples" href="#"> </a>
** [Curl examples](curl)
\* [Forever (hidden) iFrame](forever_iframe)
\* [Event Source](event_source)
\* [WebSocket](websocket)
\* [Long Polling](long_polling)
\* [JSONP](jsonp)
\* [M-JPEG](m-jpeg)
\* [Other examples](wiki)

FAQ <a names="faq" href="#"> </a>
=================================

Doubts?! Check the [FAQ](wiki).

Bug report <a name="bug_report" href="#"> </a>
==============================================

To report a bug, please provide the following information when applicable

1.  Which push stream module version is been used (commit sha1)?
2.  Which nginx version is been used?
3.  Nginx configuration in use
4.  “nginx ~~V" command outuput
    \# Core dump indicating a failure on the module code. Check [here](nginx_debugging) how to produce one.
    \# Step by step description to reproduce the error.
    h1. Who is using the module? <a names="faq" href="#"> </a>
    Do you use this module? Put your name on the [list](wiki).

    h1. Javascript Client <a name="javascript_client" href="#"> </a>
    There is a javascript client implementation [here](javascript_client), which is framework independent. Try and help improve it. ;)
    h1. Directives
     Defining locations, Main configuration, Subscribers configuration, Publishers configuration, Channels Statistics configuration, WebSocket configuration
    . | Directive | | | | | | |
    | [push\_stream\_channels\_statistics](push_stream_channels_statistics) |   x |   ~~ |   - |   - |   - |   - |
    |”push\_stream\_publisher“:push\_stream\_publisher |   x |   - |   - |   - |   - |   - |
    |”push\_stream\_subscriber“:push\_stream\_subscriber |   x |   - |   - |   - |   - |   - |
    |”push\_stream\_shared\_memory\_size“:push\_stream\_shared\_memory\_size |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_channel\_deleted\_message\_text“:push\_stream\_channel\_deleted\_message\_text |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_channel\_inactivity\_time“:push\_stream\_channel\_inactivity\_time |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_ping\_message\_text“:push\_stream\_ping\_message\_text |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_timeout\_with\_body“:push\_stream\_timeout\_with\_body |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_message\_ttl“:push\_stream\_message\_ttl |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_max\_subscribers\_per\_channel“:push\_stream\_max\_subscribers\_per\_channel |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_max\_messages\_stored\_per\_channel“:push\_stream\_max\_messages\_stored\_per\_channel |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_max\_channel\_id\_length“:push\_stream\_max\_channel\_id\_length |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_max\_number\_of\_channels“:push\_stream\_max\_number\_of\_channels |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_max\_number\_of\_wildcard\_channels“:push\_stream\_max\_number\_of\_wildcard\_channels |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_wildcard\_channel\_prefix“:push\_stream\_wildcard\_channel\_prefix |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_events\_channel\_id“:push\_stream\_events\_channel\_id |   - |   x |   - |   - |   - |   - |
    |”push\_stream\_channels\_path“:push\_stream\_channels\_path |   - |   - |   x |   x |   x |   x |
    |”push\_stream\_store\_messages“:push\_stream\_store\_messages |   - |   - |   - |   x |   - |   x |
    |”push\_stream\_channel\_info\_on\_publish“:push\_stream\_channel\_info\_on\_publish |   - |   - |   - |   x |   - |   - |
    |”push\_stream\_authorized\_channels\_only“:push\_stream\_authorized\_channels\_only |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_header\_template\_file“:push\_stream\_header\_template\_file |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_header\_template“:push\_stream\_header\_template |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_message\_template“:push\_stream\_message\_template |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_footer\_template“:push\_stream\_footer\_template |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_wildcard\_channel\_max\_qtd“:push\_stream\_wildcard\_channel\_max\_qtd |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_ping\_message\_interval“:push\_stream\_ping\_message\_interval |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_subscriber\_connection\_ttl“:push\_stream\_subscriber\_connection\_ttl |   - |   - |   x |   - |   - |   x |
    |”push\_stream\_longpolling\_connection\_ttl“:push\_stream\_longpolling\_connection\_ttl |   - |   - |   x |   - |   - |   - |
    |”push\_stream\_websocket\_allow\_publish“:push\_stream\_websocket\_allow\_publish |   - |   - |   - |   - |   - |   x |
    |”push\_stream\_last\_received\_message\_time“:push\_stream\_last\_received\_message\_time |   - |   - |   x |   - |   - |   - |
    |”push\_stream\_last\_received\_message\_tag“:push\_stream\_last\_received\_message\_tag |   - |   - |   x |   - |   - |   - |
    |”push\_stream\_last\_event\_id“:push\_stream\_last\_event\_id |   - |   - |   x |   - |   - |   - |
    |”push\_stream\_user\_agent“:push\_stream\_user\_agent |   - |   - |   x |   - |   - |   - |
    |”push\_stream\_padding\_by\_user\_agent“:push\_stream\_padding\_by\_user\_agent |   - |   - |   x |   - |   - |   - |
    |”push\_stream\_allowed\_origins“:push\_stream\_allowed\_origins |   - |   - |   x |   - |   - |   - |
    |”push\_stream\_allow\_connections\_to\_events\_channel“:push\_stream\_allow\_connections\_to\_events\_channel |   - |   - |   x |   - |   - |   x |
    h1(\#installation). Installation <a name="installation" href="#"> </a>
    \<pre\>
     \# clone the project
     git clone https://github.com/wandenberg/nginx-push-stream-module.git
     NGINX\_PUSH\_STREAM\_MODULE\_PATH=\$PWD/nginx-push-stream-module
     \# get desired nginx version (works with 1.2.0+)
     wget http://nginx.org/download/nginx-1.2.0.tar.gz
     \# unpack, configure and build
     tar xzvf nginx-1.2.0.tar.gz
     cd nginx-1.2.0
     ./configure —add-module=../nginx-push-stream-module
     make
     \# install and finish
     sudo make install
     \# check
     sudo /usr/local/nginx/sbin/nginx ~~v
     nginx version: nginx/1.2.0
     \# test configuration
     sudo /usr/local/nginx/sbin/nginx~~c \$NGINX\_PUSH\_STREAM\_MODULE\_PATH/misc/nginx.conf ~~t
     the configuration file \$NGINX\_PUSH\_STREAM\_MODULE\_PATH/misc/nginx.conf syntax is ok
     configuration file \$NGINX\_PUSH\_STREAM\_MODULE\_PATH/misc/nginx.conf test is successful
     \# run
     sudo /usr/local/nginx/sbin/nginx~~c \$NGINX\_PUSH\_STREAM\_MODULE\_PATH/misc/nginx.conf
    \</pre\>
    h1(\#memory-usage). Memory usage
    Just as information is listed below the minimum amount of memory used for each object:
    \* message on shared = 200 bytes
    \* channel on shared = 270 bytes
    \* subscriber
     **\* on shared = 160 bytes
    **\* on system = 6550 bytes
    h1(\#tests). Tests
    The server tests for this module are written in Ruby, and are acceptance tests, click”here“:tests for more details.
    h1(\#discussion). Discussion
    Nginx Push Stream Module”Discussion Group“:discussion
    h1(\#contributors). Contributors
    ”People":contributors

[discussion]https://groups.google.com/group/nginxpushstream
[donate]https://www.paypal.com/cgi-bin/webscr?cmd=*s-xclick&hosted\_button\_id=4LP6P9A7BC37S
http://dev.w3.org/html5/eventsource/
http://dev.w3.org/html5/websockets/
http://en.wikipedia.org/wiki/Comet*28programming29
[installation]\#installation
[examples]\#examples
[javascript\_client]docs/javascript\_client.textile\#javascript\_client
[repository]https://github.com/wandenberg/nginx-push-stream-module
[contributors]https://github.com/wandenberg/nginx-push-stream-module/contributors
[changelog]CHANGELOG.textile
[curl]docs/examples/curl.textile\#curl
[forever\_iframe]docs/examples/forever\_iframe.textile\#forever\_iframe
[event\_source]docs/examples/event\_source.textile\#event\_source
[websocket]docs/examples/websocket.textile\#websocket
[long\_polling]docs/examples/long\_polling.textile\#long\_polling
[jsonp]docs/examples/long\_polling.textile\#jsonp
[m-jpeg]docs/examples/m\_jpeg.textile\#m\_jpeg
[tests]docs/server\_tests.textile
[push\_stream\_channels\_statistics]docs/directives/channels\_statistics.textile\#push\_stream\_channels\_statistics
[push\_stream\_publisher]docs/directives/publishers.textile\#push\_stream\_publisher
[push\_stream\_subscriber]docs/directives/subscribers.textile\#push\_stream\_subscriber
[push\_stream\_shared\_memory\_size]docs/directives/main.textile\#push\_stream\_shared\_memory\_size
[push\_stream\_channel\_deleted\_message\_text]docs/directives/main.textile\#push\_stream\_channel\_deleted\_message\_text
[push\_stream\_ping\_message\_text]docs/directives/main.textile\#push\_stream\_ping\_message\_text
[push\_stream\_channel\_inactivity\_time]docs/directives/main.textile\#push\_stream\_channel\_inactivity\_time
[push\_stream\_message\_ttl]docs/directives/main.textile\#push\_stream\_message\_ttl
[push\_stream\_max\_subscribers\_per\_channel]docs/directives/main.textile\#push\_stream\_max\_subscribers\_per\_channel
[push\_stream\_max\_messages\_stored\_per\_channel]docs/directives/main.textile\#push\_stream\_max\_messages\_stored\_per\_channel
[push\_stream\_max\_channel\_id\_length]docs/directives/main.textile\#push\_stream\_max\_channel\_id\_length
[push\_stream\_max\_number\_of\_channels]docs/directives/main.textile\#push\_stream\_max\_number\_of\_channels
[push\_stream\_max\_number\_of\_wildcard\_channels]docs/directives/main.textile\#push\_stream\_max\_number\_of\_wildcard\_channels
[push\_stream\_wildcard\_channel\_prefix]docs/directives/main.textile\#push\_stream\_wildcard\_channel\_prefix
[push\_stream\_events\_channel\_id]docs/directives/main.textile\#push\_stream\_events\_channel\_id
[push\_stream\_channels\_path]docs/directives/subscribers.textile\#push\_stream\_channels\_path
[push\_stream\_authorized\_channels\_only]docs/directives/subscribers.textile\#push\_stream\_authorized\_channels\_only
[push\_stream\_header\_template\_file]docs/directives/subscribers.textile\#push\_stream\_header\_template\_file
[push\_stream\_header\_template]docs/directives/subscribers.textile\#push\_stream\_header\_template
[push\_stream\_message\_template]docs/directives/subscribers.textile\#push\_stream\_message\_template
[push\_stream\_footer\_template]docs/directives/subscribers.textile\#push\_stream\_footer\_template
[push\_stream\_wildcard\_channel\_max\_qtd]docs/directives/subscribers.textile\#push\_stream\_wildcard\_channel\_max\_qtd
[push\_stream\_ping\_message\_interval]docs/directives/subscribers.textile\#push\_stream\_ping\_message\_interval
[push\_stream\_subscriber\_connection\_ttl]docs/directives/subscribers.textile\#push\_stream\_subscriber\_connection\_ttl
[push\_stream\_longpolling\_connection\_ttl]docs/directives/subscribers.textile\#push\_stream\_longpolling\_connection\_ttl
[push\_stream\_timeout\_with\_body]docs/directives/subscribers.textile\#push\_stream\_timeout\_with\_body
[push\_stream\_last\_received\_message\_time]docs/directives/subscribers.textile\#push\_stream\_last\_received\_message\_time
[push\_stream\_last\_received\_message\_tag]docs/directives/subscribers.textile\#push\_stream\_last\_received\_message\_tag
[push\_stream\_last\_event\_id]docs/directives/subscribers.textile\#push\_stream\_last\_event\_id
[push\_stream\_user\_agent]docs/directives/subscribers.textile\#push\_stream\_user\_agent
[push\_stream\_padding\_by\_user\_agent]docs/directives/subscribers.textile\#push\_stream\_padding\_by\_user\_agent
[push\_stream\_store\_messages]docs/directives/publishers.textile\#push\_stream\_store\_messages
[push\_stream\_channel\_info\_on\_publish]docs/directives/publishers.textile\#push\_stream\_channel\_info\_on\_publish
[push\_stream\_allowed\_origins]docs/directives/subscribers.textile\#push\_stream\_allowed\_origins
[push\_stream\_websocket\_allow\_publish]docs/directives/subscribers.textile\#push\_stream\_websocket\_allow\_publish
[push\_stream\_allow\_connections\_to\_events\_channel]docs/directives/subscribers.textile\#push\_stream\_allow\_connections\_to\_events\_channel
[wiki]https://github.com/wandenberg/nginx-push-stream-module/wiki/\_pages
[nginx\_debugging]http://wiki.nginx.org/Debugging

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-push-stream](https://github.com/wandenberg/nginx-push-stream-module){target=_blank}.