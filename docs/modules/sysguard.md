# *sysguard*: NGINX sysguard module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-sysguard
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_sysguard_module.so;
```


This document describes nginx-module-sysguard [v0.0.1](https://github.com/dvershinin/nginx-module-sysguard/releases/tag/v0.0.1){target=_blank} 
released on Feb 29 2020.

<hr />

[![License](http://img.shields.io/badge/license-BSD-brightgreen.svg)](https://github.com/vozlt/nginx-module-sysguard/blob/master/LICENSE)

Nginx sysguard module

## Synopsis

```Nginx
http {

    ...

    server {

        ...

        sysguard on;
        sysguard_mode or;

        sysguard_load load=10.5 action=/loadlimit;
        sysguard_mem swapratio=20% action=/swaplimit;
        sysguard_mem free=100M action=/freelimit;
        sysguard_rt rt=0.01 period=5s method=AMM:10 action=/rtlimit;

        location /loadlimit {
            return 503;
        }

        location /swaplimit {
            return 503;
        }

        location /freelimit {
            return 503;
        }

        location /rtlimit {
            return 503;
        }
    }

    ...

    server {

        ...

        location /api {
            sysguard on;
            sysguard_mode or;
            sysguard_load load=20 action=/limit;
            sysguard_mem swapratio=10% action=/limit;
            sysguard_rt rt=2.01 period=5s method=WMA:10 action=/limit;

            ... 

        }

        location /images {
            sysguard on;
            sysguard_mode and;
            sysguard_load load=20 action=/limit;
            sysguard_mem swapratio=10% action=/limit;
            sysguard_rt rt=2.01 period=5s method=WMA:10 action=/limit;

            ...

        }

        location /limit {
            return 503;
        }
    }

}
```

## Description
This module can be used to protect your server in case system load, memory use goes too high or requests are responded too slow.
This is a porting version of the [sysguard](http://tengine.taobao.org/document/http_sysguard.html) in [tengine](https://github.com/alibaba/tengine) to the pure NGINX so as to support the same features.

`Caveats:` Note this module requires the sysinfo(2) system call, or getloadavg(3) function in glibc. It also requires the /proc file system to get memory information.

## Embedded Variables
The following embedded variables are provided:

* **$sysguard_load**
  * The load of system. If `$sysguard_load`'s value is 100, then load is 0.1(100/1000). (/msec)
* **$sysguard_swapstat**
  * The ratio of using swap. (/per)
* **$sysguard_free**
  * The real free space of memory. (/byte)
* **$sysguard_rt**
  * The average of request processing times. If `$sysguard_rt`'s value is 100, then response time is 0.1sec(100/1000). (/msec)
* **$sysguard_meminfo_totalram**
  * The total memory of meminfo. (/byte)
* **$sysguard_meminfo_freeram**
  * The free memory of meminfo. (/byte)
* **$sysguard_meminfo_bufferram**
  * The buffer memory of meminfo. (/byte)
* **$sysguard_meminfo_cachedram**
  * The cached memory of meminfo. (/byte)
* **$sysguard_meminfo_totalswap**
  * The total swap of meminfo. (/byte)
* **$sysguard_meminfo_freeswap**
  * The free swap of meminfo. (/byte)


## Directives

### sysguard

| -   | - |
| --- | --- |
| **Syntax**  | **sysguard** \<on\|off\> |
| **Default** | off |
| **Context** | http, server, location |

`Description:` Enables or disables the module working.

### sysguard_load

| -   | - |
| --- | --- |
| **Syntax**  | **sysguard_load** load=*number* [action=*/url*] |
| **Default** | - |
| **Context** | http, server, location |

`Description:` Specify the load threshold. When the system load exceeds this threshold, all subsequent requests will be redirected to the URL specified by the 'action' parameter. It will return 503 if there's no 'action' URL defined. This directive also support using ncpuratio to instead of the fixed threshold, 'ncpu' means the number of cpu's cores, you can use this directive like this: load=ncpu1.5

### sysguard_mem

| -   | - |
| --- | --- |
| **Syntax**  | **sysguard_mem** swapratio=*ratio*% free=*size* [action=*/url*] |
| **Default** | - |
| **Context** | http, server, location |

`Description:` Specify the used swap memory or free memory threshold. When the swap memory use ratio exceeds this threshold or memory free less than the size, all subsequent requests will be redirected to the URL specified by the 'action' parameter. It will return 503 if there's no 'action' URL. Sysguard uses this strategy to calculate memory free: "memfree = free + buffered + cached"

### sysguard_rt

| -   | - |
| --- | --- |
| **Syntax**  | **sysguard_rt** rt=*second* period=*time* [method=\<AMM\|WMA\>:*number*] [action=*/url*] |
| **Default** | - |
| **Context** | http, server, location |

`Description:` Specify the response time threshold.
Parameter rt is used to set a threshold of the average response time, in second.
Parameter period is used to specifiy the period of the statistics cycle.
If the average response time of the system exceeds the threshold specified by the user,
the incoming request will be redirected to a specified url which is defined by parameter 'action'.
If no 'action' is presented, the request will be responsed with 503 error directly.
The `method` is a formula that calculate the average of response processing times.
The `number` in method is the number of samples to calculate the average.
The default method is set to be `method=AMM:period`.

* **AMM**
  * The AMM is the [arithmetic mean](https://en.wikipedia.org/wiki/Arithmetic_mean).
* **WMA**
  * THE WMA is the [weighted moving average](https://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average).

### sysguard_mode

| -   | - |
| --- | --- |
| **Syntax**  | **sysguard_mode** \<and\|or\> |
| **Default** | or |
| **Context** | http, server, location |

`Description:` If there are more than one type of monitor, this directive is used to specified the relations among all the monitors which are: 'and' for all matching and 'or' for any matching.

### sysguard_interval

| -   | - |
| --- | --- |
| **Syntax**  | **sysguard_interval** *time* |
| **Default** | 1s |
| **Context** | http, server, location |

`Description:` Specify the time interval to update your system information.
The default value is one second, which means sysguard updates the server status once a second.

### sysguard_log_level

| -   | - |
| --- | --- |
| **Syntax**  | **sysguard_log_level** \<info\|notice\|warn\|error\> |
| **Default** | error |
| **Context** | http, server, location |

`Description:` Specify the log level of sysguard.

## See Also
* [nginx-module-vts](https://github.com/vozlt/nginx-module-vts)
* [nginx-module-sts](https://github.com/vozlt/nginx-module-sts)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-sysguard](https://github.com/dvershinin/nginx-module-sysguard){target=_blank}.