# *array-var*: Array-typed variables for NGINX


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-array-var
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_array_var_module.so;
```


This document describes nginx-module-array-var [v0.5](https://github.com/openresty/array-var-nginx-module/releases/tag/v0.05){target=_blank} 
released on Mar 09 2016.

<hr />

array-var-nginx-module - Add support for array-typed variables to nginx config files

installation instructions.

## Status

This module is production ready.

## Synopsis

```nginx
location /foo {
    array_split ',' $arg_files to=$array;

    # use the set_quote_sql_str directive in the ngx_set_misc
    # module to map to each element in the array $array:
    array_map_op set_quote_sql_str $array;

    array_map "name = $array_it" $array;

    array_join ' or ' $array to=$sql_condition;

    # well, we could feed it to ngx_drizzle to talk to MySQL, for example ;)
    echo "select * from files where $sql_condition";
}
```

## Description

This module provides array typed nginx variables to `nginx.conf`.

Under the hood, this module just "abuses" the nginx string values to hold binary pointers
to C data structures (NGINX core's `ngx_array_t` struct on the C land).

The array type gives `nginx.onf` wonderful capabilities of handling value lists. Nowadays, however,
you are highly recommended to use the [ngx_lua](https://github.com/openresty/lua-nginx-module) module
so as to have the full scripting power provided by the Lua language in nginx.


## Directives


## array_split
**syntax:** *array_split &lt;separator&gt; &lt;subject&gt; to=$target_variable*

**default:** *no*

**context:** *http, server, server if, location, location if*

Splits the string value in the `subject` argument with the separator string specified by the
`separator` argument. The result is an array-typed value saved to the nginx variable specified by the `to=VAR` option.

For example,

```nginx
array_split "," $arg_names to=$names;
```

will split the string values in the URI query argument `names` into an array-typed value saved to the custom nginx variable
`$names`.

This directive creates an array-typed variable. Array-typed variables cannot be used outside
the directives offered by this module. If you want to use the values in an array-typed variable
in other contexts,
you must use the [array_join](#array_join) directive to produce a normal string value.


## array_join
**syntax:** *array_split &lt;separator&gt; $array_var*

**default:** *no*

**context:** *http, server, server if, location, location if*

Joins the elements in the array-typed nginx variable (`$array_var`) into a single string value
with the separator specified by the first argument.

For example,

```nginx
location /foo {
    array_split ',' $arg_names to=$names;
    array_join '+' $names;
    echo $names;
}
```

Then request `GET /foo?names=Bob,Marry,John` will yield the response body

```
Bob+Marry+John
```

In the example above, we use the [ngx_echo](https://github.com/openresty/echo-nginx-module) module's [echo](https://github.com/openresty/echo-nginx-module#echo) directive to output
the final result.


## array_map
**syntax:** *array_map &lt;template&gt; $array_var*

**syntax:** *array_map &lt;template&gt; $array_var to=$new_array_var*

**default:** *no*

**context:** *http, server, server if, location, location if*

Maps the string template to each element in the array-typed nginx variable specified. Within
the string template, you can use the special iterator variable `$array_it` to reference the current
array element in the array being mapped.

For example,

```nginx
array_map "[$array_it]" $names;
```

will change each element in the array variable `$names` by putting the square brackets around
each element's string value. The modification is in-place in this case.

If you do not want in-place modifications, you can use the `to=$var` option to specify a new nginx variable to hold the results. For instance,

```nginx
array_map "[$array_it]" $names to=$new_names;
```

where the results are saved into another (array-typed) nginx variable named `$new_names` while
the `$names` variable keeps intact.

Below is a complete example for this:

```nginx
location /foo {
    array_split ',' $arg_names to=$names;
    array_map '[$array_it]' $names;
    array_join '+' $names;
    echo "$names";
}
```

Then request `GET /foo?names=bob,marry,nomas` will yield the response body

```
[bob]+[marry]+[nomas]
```


## array_map_op
**syntax:** *array_map_op &lt;directive&gt; $array_var*

**syntax:** *array_map_op &lt;directive&gt; $array_var to=$new_array_var*

**default:** *no*

**context:** *http, server, server if, location, location if*

Similar to the [array_map](#array_map) directive but maps the specified nginx configuration directive instead of
a string template to each element in the array-typed nginx variable specified. The result
of applying the specified configuration directive becomes the result of the mapping.

The nginx configuration directive being used as the iterator must be implemented by [Nginx Devel Kit](https://github.com/simpl/ngx_devel_kit) (NDK)'s set_var submodule's `ndk_set_var_value`.
For example, the following [set-misc-nginx-module](http://github.com/openresty/set-misc-nginx-module) directives can be invoked this way:

* [set_quote_sql_str](http://github.com/openresty/set-misc-nginx-module#set_quote_sql_str)
* [set_quote_pgsql_str](http://github.com/openresty/set-misc-nginx-module#set_quote_pgsql_str)
* [set_quote_json_str](http://github.com/openresty/set-misc-nginx-module#set_quote_json_str)
* [set_unescape_uri](http://github.com/openresty/set-misc-nginx-module#set_unescape_uri)
* [set_escape_uri](http://github.com/openresty/set-misc-nginx-module#set_escape_uri)
* [set_encode_base32](http://github.com/openresty/set-misc-nginx-module#set_encode_base32)
* [set_decode_base32](http://github.com/openresty/set-misc-nginx-module#set_decode_base32)
* [set_encode_base64](http://github.com/openresty/set-misc-nginx-module#set_encode_base64)
* [set_decode_base64](http://github.com/openresty/set-misc-nginx-module#set_decode_base64)
* [set_encode_hex](http://github.com/openresty/set-misc-nginx-module#set_encode_base64)
* [set_decode_hex](http://github.com/openresty/set-misc-nginx-module#set_decode_base64)
* [set_sha1](http://github.com/openresty/set-misc-nginx-module#set_encode_base64)
* [set_md5](http://github.com/openresty/set-misc-nginx-module#set_decode_base64)

This is a higher-order operation where other nginx configuration directives can be used
as arguments for this `map_array_op` directive.

Consider the following example,

```nginx
array_map_op set_quote_sql_str $names;
```

This line changes each element in the array-typed nginx variable `$names` by applying the
[set_quote_sql_str](https://github.com/openresty/set-misc-nginx-module#set_quote_sql_str)
directive provided by the [ngx_set_misc](https://github.com/openresty/set-misc-nginx-module)
module one by one. The result is that each element in the array `$names` has been escaped as SQL string literal values.

You can also specify the `to=$var` option if you do not want in-place modifications of the input arrays. For instance,

```nginx
array_map_op set_quote_sql_str $names to=$quoted_names;
```

will save the escaped elements into a new (array-typed) nginx variable named `$quoted_names` with `$names` intact.

The following is a relatively complete example:

```nginx
location /foo {
    array_split ',' $arg_names to=$names;
    array_map_op set_quote_sql_str $names;
    array_join '+' $names to=$res;
    echo $res;
}
```

Then request `GET /foo?names=bob,marry,nomas` will yield the response body

```
'bob'+'marry'+'nomas'
```

Pretty cool, huh?


## Source Repository

Available on github at [openresty/array-var-nginx-module](https://github.com/openresty/array-var-nginx-module).


## Getting involved

You'll be very welcomed to submit patches to the author or just ask for
a commit bit to the source repository on GitHub.


## Author

Yichun "agentzh" Zhang (章亦春) &lt;agentzh@gmail.com&gt;, CloudFlare Inc.


## Copyright & License

Copyright (c) 2009-2016, Yichun Zhang (agentzh) &lt;agentzh@gmail.com&gt;, CloudFlare Inc.

This module is licensed under the terms of the BSD license.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

*   Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
*   Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## See Also

* [NDK](https://github.com/simpl/ngx_devel_kit)
* [ngx_lua](https://github.com/openresty/lua-nginx-module)
* [ngx_set_misc](https://github.com/openresty/set-misc-nginx-module)


## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-array-var](https://github.com/openresty/array-var-nginx-module){target=_blank}.