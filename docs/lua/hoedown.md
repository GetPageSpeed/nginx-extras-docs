# *hoedown*: LuaJIT FFI bindings to Hoedown, a standards compliant, fast, secure markdown processing library in C


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-hoedown
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-hoedown
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-hoedown [v0.91](https://github.com/bungle/lua-resty-hoedown/releases/tag/v0.91){target=_blank} 
released on Oct 09 2014.
    
<hr />

`lua-resty-hoedown` is a Markdown, SmartyPants, buffer, and html and href/url escaping library implementing LuaJIT bindings to
[Hoedown](https://github.com/hoedown/hoedown).

## Hello World with lua-resty-hoedown

```lua
local hoedown = require "resty.hoedown"
hoedown[[
## Are you ready for the truth?

Now that there is the Tec-9, a crappy spray gun from South Miami.
This gun is advertised as the most popular gun in American crime.
Do you believe that shit? It actually says that in the little book
that comes with it: the most popular gun in American crime. Like
they're actually proud of that shit.

## I'm serious as a heart attack

The path of the righteous man is beset on all sides by the iniquities
of the selfish and the tyranny of evil men. Blessed is he who, in the
name of charity and good will, shepherds the weak through the valley
of darkness, for he is truly his brother's keeper and the finder of
lost children. And I will strike down upon thee with great vengeance
and furious anger those who would attempt to poison and destroy My
brothers.
]]
```

This will return string containing:

```html
<h1>Are you ready for the truth?</h1>

<p>Now that there is the Tec-9, a crappy spray gun from South Miami.
This gun is advertised as the most popular gun in American crime.
Do you believe that shit? It actually says that in the little book
that comes with it: the most popular gun in American crime. Like
they&#39;re actually proud of that shit.</p>

<h2>I&#39;m serious as a heart attack</h2>

<p>The path of the righteous man is beset on all sides by the iniquities
of the selfish and the tyranny of evil men. Blessed is he who, in the
name of charity and good will, shepherds the weak through the valley
of darkness, for he is truly his brother&#39;s keeper and the finder of
lost children. And I will strike down upon thee with great vengeance
and furious anger those who would attempt to poison and destroy My
brothers.</p>
```

## Lua API

TBD

## License

`lua-resty-hoedown` uses two clause BSD license.

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
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-hoedown](https://github.com/bungle/lua-resty-hoedown){target=_blank}.