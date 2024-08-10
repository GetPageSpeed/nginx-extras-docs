# *length-hiding*: NGINX Length Hiding Filter Module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-length-hiding
    ```
 
=== "CentOS/RHEL 8, 9 and Fedora Linux, Amazon Linux 2023, etc."

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-length-hiding
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_length_hiding_filter_module.so;
```


This document describes nginx-module-length-hiding [v1.1.1](https://github.com/nulab/nginx-length-hiding-filter-module/releases/tag/1.1.1){target=_blank} 
released on Jul 19 2017.

<hr />

## Nginx Length Hiding Filter Module


## Introduction

In [BREACH site](http://breachattack.com/), the mitigations against BREACH attack are given as follows:

1. Disabling HTTP compression
2. Separating secrets from user input
3. Randomizing secrets per request
4. Masking secrets (effectively randomizing by XORing with a random secret per request)
5. Protecting vulnerable pages with CSRF
6. Length hiding (by adding random number of bytes to the responses)
7. Rate-limiting the requests

BREACH relies on HTTP compression and it's reasonable to disable it to secure your website. However without compresseion, some websites may meet severe performance degression or the cost may increase if you're charged based on the volume of traffic like AWS. In such case it may be difficult to turn off HTML compression for whole responses from your website and need to adopt other proper ways.

Other mitigations listed from the 2nd to 5th above are basically applicable to your application but the 6th one, Length hiding, can be done on nginx. This filter module provides functionality to append randomly generated HTML comment to the end of response body to hide correct response length and make it difficult for attackers to guess secure token.

The sample of randomly appended HTML comment is here.
```
<!-- random-length HTML comment: JnSLGWeWYWsoJ4dXS3ubLw3YOu3zfGTotlzx7UJUo26xuXICQ2cbpVy1Dprgv8Icj6QfOZx2Ptp9HxCVoevTxhKzMzV6xeYXao0oCngRWJRb4Tvive1iBAXLzrHlLg6jKwNKXrct0tJuA2TvWIRVIng6UoffIbCQLPbi63PwmWemOxVi6m3CPa6hCbAK2CaBR1jLux7UJa4WNN4H0yIDMElMglWWouY5m5FUqAn0afMmtErj0zkA2LMWxisZRES38XLoYycySmaBrIih5IixUsJFR0ei4uZ0IifgV5SnitoNzMusSQem9npObHuU2HKApneAjwnFdPSQZA9sRdSOE8agDI05P832mV1JIcOjsg0FgzxvSG7UEX0HdqBqp2jPOYYW0k5gGtmkiXWydRJfn9lGomxReUeqq2Aec69gplEM6a8aqH5TFgXrGK8jcaPISQlsKkMxJQ7Fp6fVDbmI59xCIvlk -->
```
For every response, length of the random strings will vary within a given range.

This idea originally came from [breach-mitigation-rails](https://github.com/meldium/breach-mitigation-rails/). Thanks team!

## Warning

As said in breach-migration-rails, BREACH is complicated and wide-ranging attack and this module provides only PARTIAL protection. To secure your website or service wholly, you need to review BREACH paper and find proper way according to your own website or service.

## Configuration Directives


### length_hiding

* syntax: length_hiding on | off
* default: off
* context: http, server, location, if in location

Enables or disables adding random generated HTML comment.

### length_hiding_max

* syntax: length_hiding_max size
* default: 2048
* context: http, server, location

Sets maximum length of random generated string used in HTML comment. The size should be within a range from 256 and 2048.

## Example Configuration

Enable this module for specific location ('/hiding'). In this example, the length of random strings will be less than 1024.
```nginx
server {
    listen       443 default_server deferred ssl spdy;
    server_name  example.com;
    length_hiding_max 1024;

    location /hiding {
        length_hiding on;
    }
}
```

If this module is built as dynamic module, do NOT forget including `load_module` line in nginx configuration.
```
load_module modules/ngx_http_length_hiding_filter_module.so;
```

## Services using this module

* [Cacoo](https://cacoo.com/)
* [Backlog](https://backlogtool.com/)
* [Typetalk](https://typetalk.in/)
* [Nulab Account](https://apps.nulab-inc.com/)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-length-hiding](https://github.com/nulab/nginx-length-hiding-filter-module){target=_blank}.