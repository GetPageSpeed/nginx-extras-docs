---

title: "Markdown-to-html NGINX module"
description: "RPM package nginx-module-markdown. NGINX filter module that transforms markdown files to html format"

---

# *markdown*: Markdown-to-html NGINX module


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
    dnf -y install nginx-module-markdown
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-markdown
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_markdown_filter_module.so;
```


This document describes nginx-module-markdown [v0.1.5](https://github.com/ukarim/ngx_markdown_filter_module/releases/tag/0.1.5){target=_blank} 
released on Jul 05 2025.

<hr />

The `ngx_markdown_filter_module` module is a filter that transforms markdown files to html format.

This module utilizes the [cmark](https://github.com/commonmark/cmark) library.

### Example configuration

```nginx
location ~ \.md {
    markdown_filter on;
    markdown_template html/template.html;
}
```

This works on proxy locations as well.

### Directives

```
Syntax:  markdown_filter on;
Context: location
```

```
Syntax:  markdown_template html/template.html;
Context: location
```

```
## enable `unsafe` mode for cmark
Syntax:  markdown_unsafe on;
Context: location;
```

```
## enable `tagfilter` extension for cmark-gfm
Syntax:  markdown_gfm_tagfilter on;
Context: location;
```

### Build with cmark-gfm (tables support)

Original cmark library doesn't support tables. But there is [cmark-gfm](https://github.com/github/cmark-gfm)
fork with table extension, supported by Github.

1. Clone this repo

2. Rename `config_gfm` to `config`

3. Install `cmark-gfm` lib

4. Download [nginx src archive](http://nginx.org/en/download.html) and unpack it

5. Run `configure` script (see nginx src) and build nginx

```
> ./configure --add-module=/path/to/ngx_markdown_filter_module --with-cc-opt=-DWITH_CMARK_GFM=1
> make
```

6. Apply markdown directives to nginx conf and run it

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-markdown](https://github.com/ukarim/ngx_markdown_filter_module){target=_blank}.