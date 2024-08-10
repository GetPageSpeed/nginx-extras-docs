# *feishu-auth*: 适用于 nginx-module-lua 的基于飞书组织架构的登录认证


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-feishu-auth
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-feishu-auth
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-feishu-auth [v0.0.1](https://github.com/k8scat/lua-resty-feishu-auth/releases/tag/v0.0.1){target=_blank} 
released on Aug 11 2021.
    
<hr />

适用于 OpenResty / ngx_lua 的基于[飞书](https://www.feishu.cn/)组织架构的登录认证

## 使用

### 下载

```bash
cd /path/to
git clone git@github.com:ledgetech/lua-resty-http.git
git clone git@github.com:SkyLothar/lua-resty-jwt.git
git clone git@github.com:k8scat/lua-resty-feishu-auth.git
```

### 配置

```conf
server {
    access_by_lua_block {
        local feishu_auth = require "resty.feishu_auth"
        feishu_auth.app_id = ""
        feishu_auth.app_secret = ""
        feishu_auth.callback_uri = "/feishu_auth_callback"
        feishu_auth.logout_uri = "/feishu_auth_logout"
        feishu_auth.app_domain = "feishu-auth.example.com"

        feishu_auth.jwt_secret = "thisisjwtsecret"

        feishu_auth.ip_blacklist = {"47.1.2.3"}
        feishu_auth.uri_whitelist = {"/"}
        feishu_auth.department_whitelist = {"0"}

        feishu_auth:auth()
    }
}
```

### 配置说明

- `app_id` 用于设置飞书企业自建应用的 `App ID`
- `app_secret` 用于设置飞书企业自建应用的 `App Secret`
- `callback_uri` 用于设置飞书网页登录后的回调地址（需在飞书企业自建应用的安全设置中设置重定向 URL）
- `logout_uri` 用于设置登出地址
- `app_domain` 用于设置访问域名（需和业务服务的访问域名一致）
- `jwt_secret` 用于设置 JWT secret
- `ip_blacklist` 用于设置 IP 黑名单
- `uri_whitelist` 用于设置地址白名单，例如首页不需要登录认证
- `department_whitelist` 用于设置部门白名单（字符串）

### 应用权限说明

- 获取部门基础信息
- 获取部门组织架构信息
- 以应用身份读取通讯录
- 获取用户组织架构信息
- 获取用户基本信息

## 依赖模块

- [lua-resty-http](https://github.com/ledgetech/lua-resty-http)
- [lua-resty-jwt](https://github.com/SkyLothar/lua-resty-jwt)

## 相关项目

- [lua-resty-weauth](https://github.com/k8scat/lua-resty-weauth) 适用于 OpenResty / ngx_lua 的基于[企业微信](https://work.weixin.qq.com/)组织架构的登录认证

## 作者

K8sCat <k8scat@gmail.com>

## 开源协议

[MIT](./LICENSE)

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-feishu-auth](https://github.com/k8scat/lua-resty-feishu-auth){target=_blank}.