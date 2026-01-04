---

title: "Nginx with WebAssembly powered by wasmtime"
description: "RPM package nginx-module-wasm-wasmtime. Nginx with WebAssembly powered by wasmtime"

---

# *wasm-wasmtime*: Nginx with WebAssembly powered by wasmtime


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
    dnf -y install nginx-module-wasm-wasmtime
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-wasm-wasmtime
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_wasmx_module.so;
```


This document describes nginx-module-wasm-wasmtime [v0.5.0](https://github.com/GetPageSpeed/ngx_wasm_module/releases/tag/0.5.0){target=_blank} 
released on Feb 15 2025.

<hr />
<p align="center">
  <img alt="WasmX logo" src="assets/vectors/logo.svg" style="width:140px;" />
</p>

## WasmX/ngx_wasm_module

> Nginx + WebAssembly

This module enables the embedding of [WebAssembly] runtimes inside of
[Nginx](https://nginx.org/) and aims at offering several host SDK abstractions
for the purpose of extending and/or introspecting the Nginx web-server/proxy
runtime.

Currently, the module implements a [Proxy-Wasm](https://github.com/proxy-wasm/spec)
host ABI, which allows the use of client SDKs written in multiple languages,
such as [Rust](https://github.com/proxy-wasm/proxy-wasm-rust-sdk)
and [Go](https://github.com/tetratelabs/proxy-wasm-go-sdk). Proxy-Wasm
("WebAssembly for Proxies") is an emerging standard for Wasm filters,
adopted by API Gateways such as [Kong](https://konghq.com)
and [Envoy](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/wasm_filter.html).

## What is WasmX?

WasmX aims at extending Nginx for the modern Web infrastructure. This includes
supporting WebAssembly runtimes & SDKs (by way of ngx_wasm_module), and
generally increasing the breadth of features relied upon by the API Gateway
use-case (i.e. reverse-proxying). See [CONTRIBUTING.md](CONTRIBUTING.md)
for additional background and roadmap information.

## Synopsis

```nginx
## nginx.conf
events {}

## nginx master process gets a default 'main' VM
## a new top-level configuration block receives all configuration for this main VM
wasm {
    #      [name]    [path.{wasm,wat}]
    module my_filter /path/to/filter.wasm;
    module my_module /path/to/module.wasm;
}

## each nginx worker process is able to instantiate wasm modules in its subsystems
http {
    server {
        listen 9000;

        location / {
            # execute a proxy-wasm filter when proxying
            #           [module]
            proxy_wasm  my_filter;

            # execute more WebAssembly during the access phase
            #           [phase] [module]  [function]
            wasm_call   access  my_module check_something;

            proxy_pass  ...;
        }
    }

    # other directives
    wasm_socket_connect_timeout 60s;
    wasm_socket_send_timeout    60s;
    wasm_socket_read_timeout    60s;

    wasm_socket_buffer_size     8k;
    wasm_socket_large_buffers   32 16k;
}
```


## Examples

Several "showcase filters" are provided as examples by authors of this module:

- [proxy-wasm-rust-filter-echo](https://github.com/wasmx-proxy/proxy-wasm-rust-filter-echo/):
  An httpbin/echo filter.
- [proxy-wasm-rust-rate-limiting](https://github.com/Kong/proxy-wasm-rust-rate-limiting):
  Kong Gateway inspired rate-limiting in Rust.
- [proxy-wasm-go-rate-limiting](https://github.com/Kong/proxy-wasm-go-rate-limiting):
  Kong Gateway inspired rate-limiting in Go.
- [proxy-wasm-assemblyscript-rate-limiting](https://github.com/Kong/proxy-wasm-assemblyscript-rate-limiting):
  Kong Gateway inspired rate-limiting in AssemblyScript.

More examples are available for each Proxy-Wasm SDK:

- [AssemblyScript
  examples (temporary SDK fork)](https://github.com/Kong/proxy-wasm-assemblyscript-sdk/tree/master/examples)
- [C++
  examples](https://github.com/proxy-wasm/proxy-wasm-cpp-sdk/tree/master/example)
- [Go (TinyGo)
  examples](https://github.com/tetratelabs/proxy-wasm-go-sdk/tree/main/examples)
- [Rust
  examples](https://github.com/proxy-wasm/proxy-wasm-rust-sdk/tree/master/examples)

Note that all of the above examples may not yet be compatible with
ngx_wasm_module.

Last but not least, the [WebAssembly
Hub](https://www.webassemblyhub.io/repositories/) contains many other Proxy-Wasm
filters, some of which may not yet be compatible with ngx_wasm_module.


## Documentation

### Usage

See the [user documentation](docs/README.md) for resources on this module's
usage.


### Development

See the [developer documentation](docs/DEVELOPER.md) for developer resources on
building this module from source and other general development processes.

See a term you are unfamiliar with? Consult the [code
lexicon](docs/DEVELOPER.md#code-lexicon).

For a primer on the code's layout and architecture, see the [code
layout](docs/DEVELOPER.md#code-layout) section.


### Proxy-Wasm SDK

The [Proxy-Wasm SDK](https://github.com/proxy-wasm/spec) is the initial focus of
WasmX/ngx_wasm_module development and is still a work in progress. You can
browse [PROXY_WASM.md](docs/PROXY_WASM.md) for a guide on Proxy-Wasm support in
ngx_wasm_module.

For a reliable resource in an evolving ABI specification, you may also wish to
consult the SDK source of the language of your choice in the [Proxy-Wasm SDKs
list](https://github.com/proxy-wasm/spec#sdks).


### WebAssembly

- WebAssembly Specification (Wasm): https://webassembly.github.io/spec/core/index.html
- WebAssembly System Interface (WASI): https://github.com/WebAssembly/WASI
- WebAssembly text format (`.wat`): https://developer.mozilla.org/en-US/docs/WebAssembly/Understanding_the_text_format


### WebAssembly Runtimes

- Wasm C API: https://github.com/WebAssembly/wasm-c-api
- Wasmer C API: https://docs.rs/wasmer-c-api/
- Wasmtime C API: https://docs.wasmtime.dev/c-api/
- V8 embedding: https://v8.dev/docs/embed


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-wasm-wasmtime](https://github.com/GetPageSpeed/ngx_wasm_module){target=_blank}.