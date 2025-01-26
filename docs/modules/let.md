---

title: "NGINX let module"
description: "RPM package nginx-module-let. Adds support for arithmetic operations to NGINX config. "

---

# *let*: NGINX let module


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
    dnf -y install nginx-module-let
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-let
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_let_module.so;
```


This document describes nginx-module-let [v0.0.5](https://github.com/dvershinin/nginx-let-module/releases/tag/v0.0.5){target=_blank} 
released on Jan 27 2023.

<hr />
----------------
## NGINX let module

Adds support for arithmetic operations to NGINX config.

(c) 2011 Roman Arutyunyan, arut@qip.ru



## Examples:

## adds variable $value equal to evaluated expression value

let $value ( $uid + 0x12 ) * $offset - 100 ;

let $remainer $number % 100 ;

let $welcome "Hi, " . $user . ", you have " . $num . " data items";
## echo $welcome ;

let_rand $randval from to;


IMPORTANT NOTE:

let-module uses NGINX config parser as lexer.
That means you should add spaces around each token.

let $value (1+2);             # ERROR!
let $value ( 1 + 2 );         # OK

let $value 1 + (2 * $uid);    # ERROR!
let $value 1 + ( 2 * $uid );  # OK



## Features supported:

- operations with unsigned integers:

  + - * / %

- string operations:

  . (concatenation)

- hexadecimal numbers

- grouping with parentheses



## Notes:

Use the following command to rebuild parser generator if you need that

bison -d let.y

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-let](https://github.com/dvershinin/nginx-let-module){target=_blank}.