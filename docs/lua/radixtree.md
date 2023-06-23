# *radixtree*: Adaptive Radix Trees implemented in Lua / LuaJIT


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-radixtree
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-radixtree
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-radixtree [v2.8.2](https://github.com/api7/lua-resty-radixtree/releases/tag/v2.8.2){target=_blank} 
released on Apr 01 2022.
    
<hr />

### Install Dependencies

```shell
make deps
```

## Benchmark

We wrote some simple benchmark scripts.
Machine environment: MacBook Pro (16-inch, 2019), CPU 2.3 GHz Intel Core i9.

```shell
$ make
cc -O2 -g -Wall -fpic -std=c99 -Wno-pointer-to-int-cast -Wno-int-to-pointer-cast -DBUILDING_SO -c src/rax.c -o src/rax.o
cc -O2 -g -Wall -fpic -std=c99 -Wno-pointer-to-int-cast -Wno-int-to-pointer-cast -DBUILDING_SO -c src/easy_rax.c -o src/easy_rax.o
cc -shared -fvisibility=hidden src/rax.o src/easy_rax.o -o librestyradixtree.so

$ make bench
resty -I=./lib -I=./deps/share/lua/5.1 benchmark/match-parameter.lua
matched res: 1
route count: 100000
match times: 10000000
time used  : 3.1400001049042 sec
QPS        : 3184713
each time  : 0.31400001049042 ns

resty -I=./lib -I=./deps/share/lua/5.1 benchmark/match-prefix.lua
matched res: 500
route count: 100000
match times: 1000000
time used  : 0.42700004577637 sec
QPS        : 2341920

resty -I=./lib -I=./deps/share/lua/5.1 benchmark/match-static.lua
matched res: 500
route count: 100000
match times: 10000000
time used  : 0.95000004768372 sec
QPS        : 10526315

resty -I=./lib -I=./deps/share/lua/5.1 benchmark/match-hosts.lua
matched res: 500
route count: 1000
match times: 100000
time used  : 0.60199999809265 sec
QPS        : 166112

resty -I=./lib -I=./deps/share/lua/5.1 benchmark/match-wildcard-hosts.lua
matched res: 500
route count: 1000
match times: 50000
time used  : 0.47900009155273 sec
QPS        : 104384
```


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-radixtree](https://github.com/api7/lua-resty-radixtree){target=_blank}.