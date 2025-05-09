# Angie

Angie is an efficient, powerful and scalable web server that was forked from NGINX by some of its former core devs, 
with intention to extend functionality far beyond the original version.

Angie is a drop-in replacement for nginx, so you can use the existing nginx configuration without major changes.

## Installation and compatibility

NGINX Extras provide you with production-grade, SELinux compatible packages for Angie web server.

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install yum-utils
    yum-config-manager --enable getpagespeed-extras-angie
    yum -y install angie
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install dnf-plugins-core
    dnf config-manager --enable getpagespeed-extras-angie
    dnf -y install angie
    ```

## Compatibility notes

Angie is based on the mainline NGINX branch but [does not have 100% compatibility with NGINX ABI](https://github.com/webserver-llc/angie/issues/13#issuecomment-1406843151).
In fact, it has runtime checks when loading a module compiled for NGINX to prevent the loading,
to avoid unexpected problems.

So for the time being, you can't use numerous module packages from NGINX Extras with Angie.

## Angie Features

Angie is a superset to standard NGINX distribution and includes a number of features not available elsewhere.

Core advantages over nginx include the following:

* Supporting HTTP/3 for client connections, as well as for proxied server connections, with the ability to independently use different protocol versions (HTTP/1.x, HTTP/2, HTTP/3) on opposite sides.
* Simplifying configuration: the `location` directive can define several matching expressions at once, which enables combining blocks with shared settings.
* Exposing basic information about the web server, its configuration, as well as metrics of proxied servers, client connections, shared memory zones, and many other things via a RESTful API interface in JSON format.
* Exporting statistics in Prometheus format with customizable templates.
* Monitoring the server through the browser with the Console Light visual monitoring tool. See the online demo: https://console.angie.software/
* Automatically updating lists of proxied servers matching a domain name or retrieving such lists from SRV DNS records.
* Session binding mode, which directs all requests within one session to the same proxied server.
* Recommissioning upstream servers after a failure smoothly using the slow_start option of the server directive.
* Limiting the MP4 file transfer rate proportionally to its bitrate, thus reducing the bandwidth load.
* Extending authorization and balancing capabilities for the MQTT protocol with the mqtt_preread directive under stream.
* Pre-built binary packages for many popular third-party modules.
* Server- and client-side support for NTLS when using the TongSuo TLS library, enabled at build time.
