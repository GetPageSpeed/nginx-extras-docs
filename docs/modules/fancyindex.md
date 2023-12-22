# *fancyindex*: NGINX Fancy Index module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-fancyindex
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_fancyindex_module.so;
```


This document describes nginx-module-fancyindex [v0.5.2](https://github.com/aperezdc/ngx-fancyindex/releases/tag/v0.5.2){target=_blank} 
released on Oct 28 2021.

<hr />
Nginx Fancy Index module
========================


The Fancy Index module makes possible the generation of file listings, like the built-in [autoindex](http://wiki.nginx.org/NginxHttpAutoindexModule) module does, but adding a touch of style. This is possible because the module allows a certain degree of customization of the generated content:

-   Custom headers. Either local or stored remotely.
-   Custom footers. Either local or stored remotely.
-   Add you own CSS style rules.
-   Allow choosing to sort elements by name (default), modification time, or size; both ascending (default), or descending.

This module is designed to work with [Nginx](https://nginx.org), a high performance open source web server written by [Igor Sysoev](http://sysoev.ru).

Requirements
------------

### CentOS 7

For users of the [official stable](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) Nginx repository, [extra packages repository with dynamic modules](https://www.getpagespeed.com/redhat) is available and fancyindex is included.

Install directly:

    yum install https://extras.getpagespeed.com/redhat/7/x86_64/RPMS/nginx-module-fancyindex-1.12.0.0.4.1-1.el7.gps.x86_64.rpm

Alternatively, add extras repository first (for future updates) and install the module:

    yum install nginx-module-fancyindex

Then load the module in /etc/nginx/nginx.conf using:

    load_module "modules/ngx_http_fancyindex_module.so";

### Other platforms

In most other cases you will need the sources for [Nginx](https://nginx.org). Any version starting from the 0.8 series should work.

In order to use the `fancyindex_header_` and `fancyindex_footer_` directives you will also need the [ngx\_http\_addition\_module](https://nginx.org/en/docs/http/ngx_http_addition_module.html) built into Nginx.

Building
--------

1.  Unpack the [Nginx](https://nginx.org) sources:

        $ gunzip -c nginx-?.?.?.tar.gz | tar -xvf -

2.  Unpack the sources for the fancy indexing module:

        $ gunzip -c nginx-fancyindex-?.?.?.tar.gz | tar -xvf -

3.  Change to the directory which contains the [Nginx](https://nginx.org) sources, run the configuration script with the desired options and be sure to put an `--add-module` flag pointing to the directory which contains the source of the fancy indexing module:

        $ cd nginx-?.?.?
        $ ./configure --add-module=../nginx-fancyindex-?.?.? \
           [--with-http_addition_module] [extra desired options]

    Since version 0.4.0, the module can also be built as a [dynamic module](https://www.nginx.com/resources/wiki/extending/converting/), using `--add-dynamic-module=…` instead and `load_module "modules/ngx_http_fancyindex_module.so";` in the configuration file

4.  Build and install the software:

        $ make

    And then, as `root`:

        # make install

5.  Configure [Nginx](https://nginx.org) by using the modules' configuration directives\_.

Example
-------

You can test the default built-in style by adding the following lines into a `server` section in your [Nginx](https://nginx.org) configuration file:

    location / {
      fancyindex on;              # Enable fancy indexes.
      fancyindex_exact_size off;  # Output human-readable file sizes.
    }

### Themes

The following themes demonstrate the level of customization which can be achieved using the module:

-   [Theme](https://github.com/TheInsomniac/Nginx-Fancyindex-Theme) by [@TheInsomniac](https://github.com/TheInsomniac). Uses custom header and footer.
-   [Theme](https://github.com/Naereen/Nginx-Fancyindex-Theme) by [@Naereen](https://github.com/Naereen/). Uses custom header and footer, the header includes search field to filter by filename using JavaScript.
-   [Theme](https://github.com/fraoustin/Nginx-Fancyindex-Theme) by [@fraoustin](https://github.com/fraoustin). Responsive theme using Material Design elements.
-   [Theme](https://github.com/alehaa/nginx-fancyindex-flat-theme) by [@alehaa](https://github.com/alehaa). Simple, flat theme based on Bootstrap 4 and FontAwesome.

Directives
----------

### fancyindex

Syntax  
*fancyindex* [*on* | *off*]

Default  
fancyindex off

Context  
http, server, location

Description  
Enables or disables fancy directory indexes.

### fancyindex\_default\_sort

Syntax  
*fancyindex\_default\_sort* [*name* | *size* | *date* | *name\_desc* | *size\_desc* | *date\_desc*]

Default  
fancyindex\_default\_sort name

Context  
http, server, location

Description  
Defines sorting criterion by default.

### fancyindex\_directories\_first

Syntax  
*fancyindex\_directories\_first* [*on* | *off*]

Default  
fancyindex\_directories\_first on

Context  
http, server, location

Description  
If enabled (default setting), groups directories together and sorts them before all regular files. If disabled, directories are sorted together with files.

### fancyindex\_css\_href

Syntax  
*fancyindex\_css\_href uri*

Default  
fancyindex\_css\_href ""

Context  
http, server, location

Description  
Allows inserting a link to a CSS style sheet in generated listings. The provided *uri* parameter will be inserted as-is in a `<link>` HTML tag. The link is inserted after the built-in CSS rules, so you can override the default styles.

### fancyindex\_exact\_size

Syntax  
*fancyindex\_exact\_size* [*on* | *off*]

Default  
fancyindex\_exact\_size on

Context  
http, server, location

Description  
Defines how to represent file sizes in the directory listing; either accurately, or rounding off to the kilobyte, the megabyte and the gigabyte.

### fancyindex\_name\_length

Syntax  
*fancyindex\_name\_length length*

Default  
fancyindex\_name\_length 50

Context  
http, server, location

Description  
Defines the maximum file name length limit in bytes.

### fancyindex\_footer

Syntax  
*fancyindex\_footer path* [*subrequest* | *local*]

Default  
fancyindex\_footer ""

Context  
http, server, location

Description  
Specifies which file should be inserted at the foot of directory listings. If set to an empty string, the default footer supplied by the module will be sent. The optional parameter indicates whether the *path* is to be treated as an URI to load using a *subrequest* (the default), or whether it refers to a *local* file.

> **note**
>
> Using this directive needs the ngx\_http\_addition\_module\_ built into Nginx.

> **warning**
>
> When inserting custom header/footer a subrequest will be issued so potentially any URL can be used as source for them. Although it will work with external URLs, only using internal ones is supported. External URLs are totally untested and using them will make [Nginx](https://nginx.org) block while waiting for the subrequest to complete. If you feel like external header/footer is a must-have for you, please [let me know](mailto:aperez@igalia.com).

### fancyindex\_header

Syntax  
*fancyindex\_header path* [*subrequest* | *local*]

Default  
fancyindex\_header ""

Context  
http, server, location

Description  
Specifies which file should be inserted at the head of directory listings. If set to an empty string, the default header supplied by the module will be sent. The optional parameter indicates whether the *path* is to be treated as an URI to load using a *subrequest* (the default), or whether it refers to a *local* file.

> **note**
>
> Using this directive needs the ngx\_http\_addition\_module\_ built into Nginx.

### fancyindex\_show\_path

Syntax  
*fancyindex\_show\_path* [*on* | *off*]

Default  
fancyindex\_show\_path on

Context  
http, server, location

Description  
Whether to output or not the path and the closing \</h1\> tag after the header. This is useful when you want to handle the path displaying with a PHP script for example.

> **warning**
>
> This directive can be turned off only if a custom header is provided using fancyindex\_header.

fancyindex\_show\_dotfiles \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~ :Syntax: *fancyindex\_show\_dotfiles* [*on* | *off*] :Default: fancyindex\_show\_dotfiles off :Context: http, server, location :Description: Whether to list files that are proceeded with a dot. Normal convention is to hide these.

### fancyindex\_ignore

Syntax  
*fancyindex\_ignore string1 [string2 [... stringN]]*

Default  
No default.

Context  
http, server, location

Description  
Specifies a list of file names which will be not be shown in generated listings. If Nginx was built with PCRE support strings are interpreted as regular expressions.

### fancyindex\_hide\_symlinks

Syntax  
*fancyindex\_hide\_symlinks* [*on* | *off*]

Default  
fancyindex\_hide\_symlinks off

Context  
http, server, location

Description  
When enabled, generated listings will not contain symbolic links.

fancyindex\_hide\_parent\_dir \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~ :Syntax: *fancyindex\_hide\_parent\_dir* [*on* | *off*] :Default: fancyindex\_hide\_parent\_dir off :Context: http, server, location :Description: When enabled, it will not show parent directory.

### fancyindex\_localtime

Syntax  
*fancyindex\_localtime* [*on* | *off*]

Default  
fancyindex\_localtime off

Context  
http, server, location

Description  
Enables showing file times as local time. Default is “off” (GMT time).

### fancyindex\_time\_format

Syntax  
*fancyindex\_time\_format* string

Default  
fancyindex\_time\_format "%Y-%b-%d %H:%M"

Context  
http, server, location

Description  
Format string used for timestamps. The format specifiers are a subset of those supported by the [strftime](https://linux.die.net/man/3/strftime) function, and the behavior is locale-independent (for example, day and month names are always in English). The supported formats are:

-   `%a`: Abbreviated name of the day of the week.
-   `%A`: Full name of the day of the week.
-   `%b`: Abbreviated month name.
-   `%B`: Full month name.
-   `%d`: Day of the month as a decimal number (range 01 to 31).
-   `%e`: Like `%d`, the day of the month as a decimal number, but a leading zero is replaced by a space.
-   `%F`: Equivalent to `%Y-%m-%d` (the ISO 8601 date format).
-   `%H`: Hour as a decimal number using a 24-hour clock (range 00 to 23).
-   `%I`: Hour as a decimal number using a 12-hour clock (range 01 to 12).
-   `%k`: Hour (24-hour clock) as a decimal number (range 0 to 23); single digits are preceded by a blank.
-   `%l`: Hour (12-hour clock) as a decimal number (range 1 to 12); single digits are preceded by a blank.
-   `%m`: Month as a decimal number (range 01 to 12).
-   `%M`: Minute as a decimal number (range 00 to 59).
-   `%p`: Either "AM" or "PM" according to the given time value.
-   `%P`: Like `%p` but in lowercase: "am" or "pm".
-   `%r`: Time in a.m. or p.m. notation. Equivalent to `%I:%M:%S %p`.
-   `%R`: Time in 24-hour notation (`%H:%M`).
-   `%S`: Second as a decimal number (range 00 to 60).
-   `%T`: Time in 24-hour notation (`%H:%M:%S`).
-   `%u`: Day of the week as a decimal, range 1 to 7, Monday being 1.
-   `%w`: Day of the week as a decimal, range 0 to 6, Monday being 0.
-   `%y`: Year as a decimal number without a century (range 00 to 99).
-   `%Y`: Year as a decimal number including the century.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-fancyindex](https://github.com/aperezdc/ngx-fancyindex){target=_blank}.