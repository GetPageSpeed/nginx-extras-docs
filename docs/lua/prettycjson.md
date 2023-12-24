# *prettycjson*: Lua cJSON Pretty Formatter


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-prettycjson
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-prettycjson
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-prettycjson [v1.6](https://github.com/bungle/lua-resty-prettycjson/releases/tag/v1.6){target=_blank} 
released on Sep 29 2016.
    
<hr />

`lua-resty-prettycjson` is a JSON Pretty Formatter for [Lua cJSON](http://www.kyne.com.au/~mark/software/lua-cjson.php).

## Lua API
#### string function(dt, [lf = "\n", [id = "\t", [ac = " ", [ec = function]]]])

Pretty formats the JSON output. You may pass `lf` (line feed) if you want to use different linefeed
than the default `\n`. If you want to indent (` id` argument) with something else than `\t` (a tab)
you can pass that as arguments as well. And if you want to have something else than ` ` (single space) after
colons `:` (`ac` argument) in json, you can change that as well, try for example `\n`. If you'd like to use
an encoder other than cJSON, pass the encoding function as the 5th argument (`ec`). It should accept anything as
input parameter, and if there is a problem with encoding this function should return `nil` and an error
message, such as:

```lua
nil, "Cannot serialise function: type not supported"
```

For input argument `dt` it accepts anything that `cjson.encode` accepts (or whatever the custom encoding
function accepts).

##### Example

```lua
local pretty = require "resty.prettycjson"

print(pretty({
    key1 = "data",
    key2 = 27,
    key3 = {
        key3_1 = "something",
        key3_2 = "something else"
    },
    key4 = {
        "item1",
        "item2"
    },
    key5 = {},
    key5 = {{''}, {'',''}, {{},{}}},
    key6 = { '' },
    key7 = {{{{ test = "value", {{{{{{}}},{{},{},{}},{},{}}}}}}}}
}))
```

That will output:

```json
{
	"key6": [
		""
	],
	"key3": {
		"key3_1": "something",
		"key3_2": "something else"
	},
	"key7": [
		[
			[
				{
					"1": [
						[
							[
								[
									[
										{}
									]
								],
								[
									{},
									{},
									{}
								],
								{},
								{}
							]
						]
					],
					"test": "value"
				}
			]
		]
	],
	"key1": "data",
	"key5": [
		[
			""
		],
		[
			"",
			""
		],
		[
			{},
			{}
		]
	],
	"key2": 27,
	"key4": [
		"item1",
		"item2"
	]
}
```

## Changes

The changes of every release of this module is recorded in [Changes.md](https://github.com/bungle/lua-resty-prettycjson/blob/master/Changes.md) file.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-prettycjson](https://github.com/bungle/lua-resty-prettycjson){target=_blank}.