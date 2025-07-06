---

title: "Lua resty module to calculate AWS signature v4 authorization header"
description: "RPM package lua-resty-aws-auth: Lua resty module to calculate AWS signature v4 authorization header"

---
  
# *aws-auth*: Lua resty module to calculate AWS signature v4 authorization header


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-aws-auth
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-aws-auth
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-aws-auth [v0.12](https://github.com/paragasu/lua-resty-aws-auth/releases/tag/v0.12-0){target=_blank} 
released on Jan 13 2017.
    
<hr />
Simple lua resty utilities to generate amazon v4 authorization and signature headers.

## Usage

```lua

local aws_auth = require "resty.aws-auth"
local config = {
  aws_host       = "email.us-east-1.amazonaws.com",
  aws_key        = "AKIDEXAMPLE",
  aws_secret     = "xxxsecret",
  aws_region     = "us-east-1",
  aws_service    = "ses",
  content_type   = "application/x-www-form-urlencoded",
  request_method = "POST",
  request_path   = "/",
  request_body   = { hello="world" } -- table of all request params
}

local aws = aws_auth:new(config)

-- get the generated authorization header
-- eg: AWS4-HMAC-SHA256 Credential=AKIDEXAMPLE/20150830/us-east-1/iam/aws4_request,
---    SignedHeaders=content-type;host;x-amz-date, Signature=xxx
local auth = aws:get_authorization_header()

-- get the x-amz-date header
local amz_date = aws:get_amz_date_header()

```

Add _Authorization_ and _x-amz-date_ header to ngx.req.headers

```lua
aws:set_ngx_auth_headers()

```



Reference
[Signing AWS With Signature V4](https://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html)
[AWS service namespaces list](http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)
[AWS region and endpoints](http://docs.aws.amazon.com/general/latest/gr/rande.html)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-aws-auth](https://github.com/paragasu/lua-resty-aws-auth){target=_blank}.