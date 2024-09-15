# *jq*: LuaJIT FFI bindings to jq


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-jq
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-jq
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-jq [v0.1.0](https://github.com/bungle/lua-resty-jq/releases/tag/0.1.0){target=_blank} 
released on Sep 02 2021.
    
<hr />

**lua-resty-jq** is a small LuaJIT FFI wrapper to [jq](https://stedolan.github.io/jq/)


## Hello World with lua-resty-jq

```lua
-- <example-input> from https://api.github.com/repos/stedolan/jq/commits?per_page=5
local jq = require "resty.jq".new()

jq:compile("[ .[] | {message: .commit.message, name: .commit.committer.name} ]")
local output = jq:filter(<example-input>)

print(output)

jq:teardown()
```

Running the above code will output (or similar):

```javascript
[
  {
    "message": "Add some missing code quoting to the manual",
    "name": "William Langford"
  },
  {
    "message": "Reduce allocation on string multiplication",
    "name": "William Langford"
  },
  {
    "message": "Fix multiple string multiplication",
    "name": "William Langford"
  },
  {
    "message": "Fix error handling in strftime",
    "name": "William Langford"
  },
  {
    "message": "Makefile: prepend srcdir to jq.1.prebuilt to fix out of source compilation",
    "name": "William Langford"
  }
]
```

## new

`syntax: jq, err = require("resty.jq").new()`

Allocates a `libjq` context.

## teardown

`syntax: jq:teardown()`

Destroys the `libjq` context, freeing resources.

## compile

`syntax: ok, err = jq:compile(program)`

Returns `true` if the program was compiled, otherwise `nil` and the error
`compilation failed`.

Note it is not currently possible to inspect details of the compilation error.
If in doubt, try your program in the CLI `jq`.

## filter

`syntax: res, err = jq:filter(data, options)`

Filters `data` using the previously compiled program. The `options` table can
contain flags which alter the behaviour of the filter, similar to a subset of
the CLI options to `jq`:

* `compact_output`: Returns output in a compact form without additional
  spacing, and with each JSON object on a single line. Defaults to `true`. Set
to `false` for "pretty" output.
* `raw_output`: Outputs as raw strings, not JSON quoted. Default is `false`.
* `join_output`: As `raw_output` but in addition does not output newline
  separators. Default is `false`.
* `ascii_output`: jq usually outputs non-ASCII Unicode codepoints as UTF-8,
  even if the input specified them as escape sequences (like "\u03bc"). Using
this option, you can force jq to produce pure ASCII output with every non-ASCII
character replaced with the equivalent escape sequence. Default is `false`.
* `sort_keys`: Output the fields of each object with the keys in sorted order.
  Default is `false`.


## See Also

* [lua-jq](https://github.com/tibbycat/lua-jq)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-jq](https://github.com/bungle/lua-resty-jq){target=_blank}.