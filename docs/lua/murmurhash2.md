# *murmurhash2*: LuaJIT MurmurHash 2 bindings to NGINX / nginx-module-lua murmurhash2 implementation


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-murmurhash2
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-murmurhash2
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-murmurhash2 [v1.0](https://github.com/bungle/lua-resty-murmurhash2/releases/tag/v1.0){target=_blank} 
released on Sep 29 2014.
    
<hr />

lua-resty-murmurhash2 is MurmurHash 2 library (LuaJIT bindings) for OpenResty's / Nginx's murmurhash2 implementation.

## Lua API
#### number require "resty.murmurhash2" string

This module has only one function that you can get just by requiring this module:

```lua
local mmh2 = require "resty.murmurhash2"
local hash = mmh2 "test" -- hash contains number 403862830
```

## License

`lua-resty-session` uses two clause BSD license.

```
Copyright (c) 2014, Aapo Talvensaari
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-murmurhash2](https://github.com/bungle/lua-resty-murmurhash2){target=_blank}.