---

title: "NGINX njs dynamic modules"
description: "RPM package nginx-module-njs. NGINX njs dynamic modules"

---

# *njs*: NGINX njs dynamic modules


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
    dnf -y install nginx-module-njs
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-njs
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_js_module.so;
```
```nginx
load_module modules/ngx_stream_js_module.so;
```


This document describes nginx-module-njs [v0.9.4](https://github.com/nginx/njs/releases/tag/0.9.4){target=_blank} 
released on Oct 28 2025.

<hr />
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Community Support](https://badgen.net/badge/support/commercial/green?icon=awesome)](/SUPPORT.md)

![NGINX JavaScript Banner](NGINX-js-1660x332.png "NGINX JavaScript Banner")

## NGINX JavaScript
NGINX JavaScript, also known as [NJS](https://nginx.org/en/docs/njs/), is a dynamic module for [NGINX](https://nginx.org/en/download.html) that enables the extension of built-in functionality using familiar JavaScript syntax. The NJS language is a subset of JavaScript, compliant with [ES5](https://262.ecma-international.org/5.1/) (ECMAScript 5.1 [Strict Variant](https://262.ecma-international.org/5.1/#sec-4.2.2)) with some [ES6](https://262.ecma-international.org/6.0/) (ECMAScript 6) and newer extensions. See [compatibility](https://nginx.org/en/docs/njs/compatibility.html) for more details.

## How it works
[NGINX JavaScript](https://nginx.org/en/docs/njs/) is provided as two [dynamic modules](https://nginx.org/en/linux_packages.html#dynmodules) for NGINX ([ngx_http_js_module](https://nginx.org/en/docs/http/ngx_http_js_module.html) and [ngx_stream_js_module](https://nginx.org/en/docs/stream/ngx_stream_js_module.html)) and can be added to any supported [NGINX Open Source](https://nginx.org/en/download.html) or [NGINX Plus](https://www.f5.com/products/nginx/nginx-plus) installation without recompilation. 

The NJS module allows NGINX administrators to:
- Add complex access control and security checks before requests reach upstream servers
- Manipulate response headers
- Write flexible, asynchronous content handlers, filters, and more!

See [examples](https://github.com/nginx/njs-examples/) and our various projects developed with NJS:

#### https://github.com/nginxinc/nginx-openid-connect
Extends NGINX Plus functionality to communicate directly with OIDC-compatible Identity Providers, authenticating users and authorizing content delivered by NGINX Plus.

#### https://github.com/nginxinc/nginx-saml
Reference implementation of NGINX Plus as a service provider for SAML authentication.

#### https://github.com/nginxinc/njs-prometheus-module
Exposes Prometheus metrics endpoint directly from NGINX Plus.

> [!TIP]
> NJS can also be used with the [NGINX Unit](https://unit.nginx.org/) application server. Learn more about NGINX Unit's [Control API](https://unit.nginx.org/controlapi/) and how to [define function calls with NJS](https://unit.nginx.org/scripting/).

## Downloading and installing
Follow these steps to download and install precompiled NGINX and NGINX JavaScript Linux binaries. You may also choose to [build the module locally from source code](#building-from-source).

## Provisioning the NGINX package repository
Follow [this guide](https://nginx.org/en/linux_packages.html) to add the official NGINX package repository to your system and install NGINX Open Source. If you already have NGINX Open Source or NGINX Plus installed, skip the NGINX installation portion in the last step.

## Getting started with NGINX JavaScript
Usage of NJS involves enabling the module, adding JavaScript files with defined functions, and invoking exported functions in NGINX configuration files.

## Verify NGINX is running
NGINX JavaScript is a module for NGINX Open Source or NGINX Plus. If you haven't done so already, follow these steps to install [NGINX Open Source](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/) or [NGINX Plus](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-plus/). Once installed, ensure the NGINX instance is running and able to respond to HTTP requests.

### Starting NGINX
Issue the following command to start NGINX:

```bash
sudo nginx
```

### Verify NGINX is responding to HTTP requests
```bash
curl -I 127.0.0.1
```

You should see the following response:
```bash
HTTP/1.1 200 OK
Server: nginx/1.25.5
```

## Enabling the NGINX JavaScript modules
Once installed, either (or both) NJS module(s) must be included in the NGINX configuration file. On most systems, the NGINX configuration file is located at `/etc/nginx/nginx.conf` by default.

### Edit the NGINX configuration file

```bash
sudo vi /etc/nginx/nginx.conf
```

### Enable dynamic loading of NJS modules
Use the [load_module](https://nginx.org/en/docs/ngx_core_module.html#load_module) directive in the top-level (“main”) context to enable either (or both) module(s).

```nginx
load_module modules/ngx_http_js_module.so;
load_module modules/ngx_stream_js_module.so;
```

## Basics of writing .js script files
NJS script files are typically named with a .js extension and placed in the `/etc/nginx/njs/` directory. They are usually comprised of functions that are then exported, making them available in NGINX configuration files.

## Reference of custom objects, methods, and properties
NJS provides a collection of objects with associated methods and properties that are not part of ECMAScript definitions. See the [complete reference](https://nginx.org/en/docs/njs/reference.html) to these objects and how they can be used to further extend and customize NGINX.

## Example: Hello World
Here's a basic "Hello World" example.

### example.js
The `hello` function in this file returns an HTTP 200 OK status response code along with the string "Hello World!", followed by a line feed. The function is then exported for use in an NGINX configuration file.

Add this file to the `/etc/nginx/njs` directory:

```JavaScript
function hello(r) {
  r.return(200, "Hello world!\n");
}

export default {hello}
```

### nginx.conf
We modify our NGINX configuration (`/etc/nginx/nginx.conf`) to import the JavaScript file and execute the function under specific circumstances.

```nginx
## Load the ngx_http_js_module module
load_module modules/ngx_http_js_module.so;

events {}

http {
  # Set the path to our njs JavaScript files
  js_path "/etc/nginx/njs/";

  # Import our JavaScript file into the variable "main"
  js_import main from http/hello.js;

  server {
    listen 80;

    location / {
      # Execute the "hello" function defined in our JavaScript file on all HTTP requests
      # and respond with the contents of our function.
      js_content main.hello;
    }
  }
}
```

For a full list of njs directives, see the [ngx_http_js_module](https://nginx.org/en/docs/http/ngx_http_js_module.html) and [ngx_stream_js_module](https://nginx.org/en/docs/stream/ngx_stream_js_module.html) module documentation pages.

> [!TIP]
> A more detailed version of this and other examples can be found in the official [njs-examples repository](https://github.com/nginx/njs-examples/tree/master).

## The NJS command line interface (CLI)
NGINX JavaScript installs with a command line interface utility. The interface can be opened as an interactive shell or used to process JavaScript syntax from predefined files or standard input. Since the utility runs independently, NGINX-specific objects such as [HTTP](https://nginx.org/en/docs/njs/reference.html#http) and [Stream](https://nginx.org/en/docs/njs/reference.html#http) are not available within its runtime.

### Example usage of the interactive CLI
```JavaScript
$ njs
>> globalThis
global {
  njs: njs {
    version: '0.8.4'
  },
  global: [Circular],
  process: process {
    argv: ['/usr/bin/njs'],
    env: {
      PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
      HOSTNAME: 'f777c149d4f8',
      TERM: 'xterm',
      NGINX_VERSION: '1.25.5',
      NJS_VERSION: '0.8.4',
      PKG_RELEASE: '1~buster',
      HOME: '/root'
    }
  },
  console: {
    log: [Function: native],
    dump: [Function: native],
    time: [Function: native],
    timeEnd: [Function: native]
  },
  print: [Function: native]
}
>>
```

### Example usage of the non-interactive CLI
```bash
$ echo "2**3" | njs -q
8
```

## Cloning the NGINX JavaScript GitHub repository
Using your preferred method, clone the NGINX JavaScript repository into your development directory. See [Cloning a GitHub Repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for additional help.

```bash
https://github.com/nginx/njs.git
```

### Configure and build
Run the following commands from the root directory of your cloned repository:

```bash
./configure
```

Build NGINX JavaScript:
```bash
make
```

The utility should now be available at `<NJS_SRC_ROOT_DIR>/build/njs`. See [The NJS Command Line Interface (CLI)](#the-njs-command-line-interface-cli) for information on usage.

## Cloning the NGINX GitHub repository
Clone the NGINX source code repository in a directory outside of the previously cloned NJS source repository.

```bash
https://github.com/nginx/nginx.git
```

## NGINX JavaScript technical specifications
Technical specifications for NJS are identical to those of NGINX.

## Supported distributions
See [Tested Operating Systems and Platforms](https://nginx.org/en/#tested_os_and_platforms) for a complete list of supported distributions. 

## Supported deployment environments
- Container
- Public cloud (AWS, Google Cloud Platform, Microsoft Azure)
- Virtual machine

## Supported NGINX versions
NGINX JavaScript is supported by all NGINX Open Source versions starting with nginx-1.14 and all NGINX Plus versions starting with NGINX Plus R15.

## Asking questions, reporting issues, and contributing
We encourage you to engage with us. Please see the [Contributing](CONTRIBUTING.md) guide for information on how to ask questions, report issues and contribute code.

## Change log
See our [release page](https://nginx.org/en/docs/njs/changes.html) to keep track of updates.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-njs](https://github.com/nginx/njs){target=_blank}.