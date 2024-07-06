# Tengine

Tengine is a web server originated by Taobao, the largest e-commerce website in Asia. It is based on the Nginx HTTP 
server and has many advanced features. Tengine has proven to be very stable and efficient on some of the top 100 
websites in the world, including taobao.com and tmall.com.

## Installation and compatibility

NGINX Extras provide you with production-grade, SELinux compatible packages for Tengine web server.

=== "CentOS/RHEL 6, 7 and Amazon Linux 2"

    ```bash
    sudo yum -y install https://extras.getpagespeed.com/release-latest.rpm
    sudo yum -y install epel-release
    sudo yum -y install yum-utils
    sudo yum-config-manager --enable getpagespeed-extras-tengine
    sudo yum -y install tengine
    ``` 
 
=== "CentOS/RHEL 8+, Fedora Linux"

    ```bash
    sudo dnf -y install https://extras.getpagespeed.com/release-latest.rpm dnf-plugins-core
    sudo dnf config-manager --enable getpagespeed-extras-tengine
    sudo dnf -y install tengine
    ```

## Compatibility notes

Since Tengine claims 100% compatibility with the stable NGINX branch, you can easily install all the
numerous module packages from NGINX Extras to empower your Tengine furthermore, e.g. to add the 
[PageSpeed module](modules/pagespeed.md). 

Commercial subscription for GetPageSpeed repository is required only to install NGINX modules for Tengine.
You must provide the Tengine compatible NGINX version when installing modules, like so:

```bash
yum -y install 'nginx-module-pagespeed-1.22.1.*'
```

Here we specified to install `nginx-module-pagespeed` for NGINX 1.22.1, which is matching the current
Tengine to NGINX binary compatibility.
 
## Tengine Features

* All features of nginx 1.22.1 are inherited, i.e., it is 100% compatible with nginx.
* Support the CONNECT HTTP method for forward proxy.
* Support asynchronous OpenSSL, using hardware such as QAT for HTTPS acceleration.
* Enhanced operations monitoring, such as asynchronous log & rollback, DNS caching, memory usage, etc.
* Support server_name in Stream module.
* More load balancing methods, e.g., consistent hashing, and session persistence.
* Input body filter support. It's quite handy to write Web Application Firewalls using this mechanism.
* Dynamic scripting language (Lua) support, which is very efficient and makes it easy to extend core functionalities.
* Limits retries for upstream servers (proxy, memcached, fastcgi, scgi, uwsgi).
* Includes a mechanism to support standalone processes.
* Protects the server in case system load or memory use goes too high.
* Multiple CSS or JavaScript requests can be combined into one request to reduce download time.
* Removes unnecessary white spaces and comments to reduce the size of a page.
* Proactive health checks of upstream servers can be performed.
* The number of worker processes and CPU affinities can be set automatically.
* The limit_req module is enhanced with whitelist support and more conditions are allowed in a single location.
* Enhanced diagnostic information makes it easier to troubleshoot errors.
* More user-friendly command lines, e.g., showing all compiled-in modules and supported directives.
* Expiration times can be specified for certain MIME types.
* Error pages can be reset to 'default'.
* ...
