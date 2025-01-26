---

title: "Lua module for nonblocking system shell command executions"
description: "RPM package lua-resty-shell: Lua module for nonblocking system shell command executions"

---
  
# *shell*: Lua module for nonblocking system shell command executions


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-shell
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-shell
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-shell [v0.3](https://github.com/openresty/lua-resty-shell/releases/tag/v0.03){target=_blank} 
released on Jul 01 2020.
    
<hr />

lua-resty-shell - Lua module for nonblocking system shell command executions

## Synopsis

```lua
local shell = require "resty.shell"

local stdin = "hello"
local timeout = 1000  -- ms
local max_size = 4096  -- byte

local ok, stdout, stderr, reason, status =
    shell.run([[perl -e 'warn "he\n"; print <>']], stdin, timeout, max_size)
if not ok then
    -- ...
end
```

## Functions

## run

**syntax:** `ok, stdout, stderr, reason, status = shell.run(cmd, stdin?, timeout?, max_size?)`

**context:** `all phases supporting yielding`

Runs a shell command, `cmd`, with an optional stdin.

The `cmd` argument can either be a single string value (e.g. `"echo 'hello,
world'"`) or an array-like Lua table (e.g. `{"echo", "hello, world"}`). The
former is equivalent to `{"/bin/sh", "-c", "echo 'hello, world'"}`, but simpler
and slightly faster.

When the `stdin` argument is `nil` or `""`, the stdin device will immediately
be closed.

The `timeout` argument specifies the timeout threshold (in ms) for
stderr/stdout reading timeout, stdin writing timeout, and process waiting
timeout.

The `max_size` argument specifies the maximum size allowed for each output
data stream of stdout and stderr. When exceeding the limit, the `run()`
function will immediately stop reading any more data from the stream and return
an error string in the `reason` return value: `"failed to read stdout: too much
data"`.

Upon terminating successfully (with a zero exit status), `ok` will be `true`,
`reason` will be `"exit"`, and `status` will hold the sub-process exit status.

Upon terminating abnormally (non-zero exit status), `ok` will be `false`,
`reason` will be `"exit"`, and `status` will hold the sub-process exit status.

Upon exceeding a timeout threshold or any other unexpected error, `ok` will be
`nil`, and `reason` will be a string describing the error.

When a timeout threshold is exceeded, the sub-process will be terminated as
such:

1. first, by receiving a `SIGTERM` signal from this library,
2. then, after 1ms, by receiving a `SIGKILL` signal from this library.

Note that child processes of the sub-process (if any) will not be terminated.
You may need to terminate these processes yourself.

When the sub-process is terminated by a UNIX signal, the `reason` return value
will be `"signal"` and the `status` return value will hold the signal number.


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-shell](https://github.com/openresty/lua-resty-shell){target=_blank}.