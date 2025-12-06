---

title: "NGINX OpenTelemetry dynamic module"
description: "RPM package nginx-module-otel. OpenTelemetry tracing/exporter module for NGINX. "

---

# *otel*: NGINX OpenTelemetry dynamic module


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
    dnf -y install nginx-module-otel
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-otel
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_otel_module.so;
```


This document describes nginx-module-otel [v0.1.2](https://github.com/nginxinc/nginx-otel/releases/tag/v0.1.2){target=_blank} 
released on Mar 15 2025.

<hr />

## What is OpenTelemetry
OpenTelemetry (OTel) is an observability framework for monitoring, tracing, troubleshooting, and optimizing applications. OTel enables the collection of telemetry data from a deployed application stack.

## What is the NGINX Native OTel Module
The `ngx_otel_module` dynamic module enables NGINX Open Source or NGINX Plus to send telemetry data to an OTel collector. It provides support for [W3C trace context](https://www.w3.org/TR/trace-context/) propagation, OpenTelemetry Protocol (OTLP)/gRPC trace exports and offers several benefits over exiting OTel modules, including:

### Better Performance ###
3rd-party OTel implementations reduce performance of request processing by as much as 50% when tracing is enabled. The NGINX Native module limits this impact to approximately 10-15%.

### Easy Provisioning ###
Setup and configuration can be done right in NGINX configuration files.

### Dynamic, Variable-Based Control ###
The ability to control trace parameters dynamically using cookies, tokens, and variables. Please see our [Ratio-based Tracing](#ratio-based-tracing) example for more details.

Additionally, [NGINX Plus](https://www.nginx.com/products/nginx/), available as part of a [commercial subscription](https://www.nginx.com/products/), enables dynamic control of sampling parameters via the [NGINX Plus API](http://nginx.org/en/docs/http/ngx_http_api_module.html) and [key-value store](http://nginx.org/en/docs/http/ngx_http_keyval_module.html) modules.

### Enabling the OTel Module
Following the installation steps above will install the module into `/etc/nginx/modules` by default. Load the module by adding the following line to the top of the main NGINX configuration file, located at `/etc/nginx/nginx.conf`.

```nginx
load_module modules/ngx_otel_module.so;
```

## Configuring the Module
For a complete list of directives, embedded variables, default span attributes and sample configurations, please refer to the [`ngx_otel_module` documentation](https://nginx.org/en/docs/ngx_otel_module.html).

## Examples
Use these examples to configure some common use-cases for OTel tracing.

### Simple Tracing
This example sends telemetry data for all http requests.

```nginx
http {
    otel_exporter {
        endpoint localhost:4317;
    }

    otel_trace on;

    server {
        location / {
            proxy_pass http://backend;
        }
    }
}
```

### Parent-based Tracing
In this example, we inherit trace contexts from incoming requests and record spans only if a parent span is sampled. We also propagate trace contexts and sampling decisions to upstream servers.

```nginx
http {
    server {
        location / {
            otel_trace $otel_parent_sampled;
            otel_trace_context propagate;

            proxy_pass http://backend;
        }
    }
}
```

### Ratio-based Tracing
In this ratio-based example, tracing is configured for a percentage of traffic (in this case 10%):

```nginx
http {
    # trace 10% of requests
    split_clients $otel_trace_id $ratio_sampler {
        10%     on;
        *       off;
    }

    # or we can trace 10% of user sessions
    split_clients $cookie_sessionid $session_sampler {
        10%     on;
        *       off;
    }

    server {
        location / {
            otel_trace $ratio_sampler;
            otel_trace_context inject;

            proxy_pass http://backend;
        }
    }
}
```

## Collecting and Viewing Traces
There are several methods and available software packages for viewing traces. For a quick start, [Jaeger](https://www.jaegertracing.io/) provides an all-in-one container to collect, process and view OTel trace data. Follow [these steps](https://www.jaegertracing.io/docs/next-release/deployment/#all-in-one) to download, install, launch and use Jaeger's OTel services.

## Change Log
See our [release page](https://github.com/nginxinc/nginx-otel/releases) to keep track of updates.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-otel](https://github.com/nginxinc/nginx-otel){target=_blank}.