# *xslt*: NGINX XSLT dynamic module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-xslt
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_xslt_filter_module.so;
```

<hr />


## Directives

You may find information about configuration directives for this module at the following links:        

*   https://nginx.org/en/docs/http/ngx_http_xslt_module.html#directives