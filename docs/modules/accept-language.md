# *accept-language*: NGINX Accept-Language module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-accept-language
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_accept_language_module.so;
```


This document describes nginx-module-accept-language [v1.0.0](https://github.com/dvershinin/nginx_accept_language_module/releases/tag/1.0.0){target=_blank} 
released on Oct 30 2018.

<hr />

This module parses the `Accept-Language` header and gives the most suitable locale for the user from a list of supported locales from your website.

## Syntax

    set_from_accept_language $lang en ja pl;
    
* `$lang` is the variable in which to store the locale
* `en ja pl` are the locales supported by your website
  
If none of the locales from `Accept-Language` is available on your website, it sets the variable to the first locale of your website's supported locales (in this case, `en`).
  
## Caveat

It currently assumes that the `Accept-Language` is sorted by quality values (from my tests it's the case for safari, firefox, opera and ie) and discards q (see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). 
In the situation where I'm using the module, this assumption works... but buyer beware :-)

## Example configuration

If you have different subdomains for each languages

```nginx
server {
    listen 80;
    server_name your_domain.com;
    set_from_accept_language $lang en ja zh;
    rewrite ^/(.*) http://$lang.your_domain.com redirect;
}
```


Or you could do something like this, redirecting people coming to '/' to /en (or /pt):

```nginx
location / {
    set_from_accept_language $lang pt en;
     if ( $request_uri ~ ^/$ ) {
       rewrite ^/$ /$lang redirect;
       break;
     }
}
```


## Why did I create it? 

I'm using page caching with merb on a multi-lingual website and I needed a way to serve the correct language page from the cache
I'll soon put an example on http://gom-jabbar.org

## Bugs

Send Bugs to Guillaume Maury (dev@gom-jabbar.org)

## Acknowledgement

Thanks to Evan Miller for his [guide on writing nginx modules](http://emiller.info/nginx-modules-guide.html).

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-accept-language](https://github.com/dvershinin/nginx_accept_language_module){target=_blank}.