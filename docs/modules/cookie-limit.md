# *cookie-limit*: NGINX module to limit the number of malicious ip forged cookies


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-cookie-limit
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_cookie_limit_req_module.so;
```


This document describes nginx-module-cookie-limit [v1.2](https://github.com/limithit/ngx_cookie_limit_req_module/releases/tag/1.2){target=_blank} 
released on Jun 23 2022.

<hr />
 
## Introduction

The *ngx_cookie_limit_req_module* module not only limits the access rate of cookies but also limits the number of malicious ip forged cookies.

## Donate
The developers work tirelessly to improve and develop ngx_cookie_limit_req_module. Many hours have been put in to provide the software as it is today, but this is an extremely time-consuming process with no financial reward. If you enjoy using the software, please consider donating to the devs, so they can spend more time implementing improvements.

 ### Alipay:
![Alipay](https://github.com/limithit/shellcode/blob/master/alipay.png)

Author
Gandalf zhibu1991@gmail.com

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-cookie-limit](https://github.com/limithit/ngx_cookie_limit_req_module){target=_blank}.