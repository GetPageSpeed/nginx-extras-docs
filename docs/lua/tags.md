---

title: "A small DSL for building HTML documents"
description: "RPM package lua-resty-tags: A small DSL for building HTML documents"

---
  
# *tags*: A small DSL for building HTML documents


## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-tags
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-tags
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-tags [v1.0](https://github.com/bungle/lua-resty-tags/releases/tag/v1.0){target=_blank} 
released on Jul 06 2016.
    
<hr />

A small DSL for building HTML documents

## Synopsis

##### Here we define some local functions:

```lua
local tags = require "resty.tags"
local html,   head,   script,   body,   h1,   p,   table,   tr,   th,   img,   br = tags(
     "html", "head", "script", "body", "h1", "p", "table", "tr", "th", "img", "br")

print(
    html { lang = "en" } (
        head (
            script { src = "main.js" }
        ),
        body (
            h1 { class = 'title "is" bigger than you think', "selected" } "Hello",
            h1 "Another Headline",
            p (
                "<Beautiful> & <Strange>",
                br,
                { Car = "Was Stolen" },
                "Weather"
            ),
            p "A Dog",
            img { src = "logo.png" },
            table(
                tr (
                    th { class = "selected" } "'Headline'",
                    th "Headline 2",
                    th "Headline 3"
                )
            )
        )
    )
)
```

##### The above will output HTML similar to:

```html
<html lang="en">
    <head>
        <script src="main.js"></script>
    </head>
    <body>
        <h1 class="title &quot;is&quot; bigger than you think" selected>
            Hello
        </h1>
        <h1>
            Another Headline
        </h1>
        <p>
            &lt;Beautiful&gt; &amp; &lt;Strange&gt;
            <br>
            table: 0x0004c370Weather
        </p>
        <p>
            A Dog
        </p>
        <img src="logo.png">
        <table>
            <tr>
                <th class="selected">
                    &#39;Headline&#39;
                </th>
                <th>
                    Headline 2
                </th>
                <th>
                    Headline 3
                </th>
            </tr>
        </table>
    </body>
</html>
```

##### Here we pass in a function:

```lua
local tags = require "resty.tags"
local html = tags(function()
    return html { lang = "en"} (
        head (
            script { src = "main.js" }
        ),
        body (
            h1 { class = 'title "is" bigger than you think', "selected" } "Hello",
            h1 "Another Headline",
            p (
                "<Beautiful> & <Strange>",
                br,
                { Car = "Was Stolen" },
                "Weather"
            ),
            p "A Dog",
            img { src = "logo.png" },
            table(
                tr (
                    th { class = "selected" } "'Headline'",
                    th "Headline 2",
                    th "Headline 3"
                )
            )
        )
    )
end)
print(html())
```

##### And the output is similar:

```html
<html lang="en">
    <head>
        <script src="main.js"></script>
    </head>
    <body>
        <h1 class="title &quot;is&quot; bigger than you think" selected>
            Hello
        </h1>
        <h1>
            Another Headline
        </h1>
        <p>
            &lt;Beautiful&gt; &amp; &lt;Strange&gt;
            <br>
            table: 0x00054ce0Weather
        </p>
        <p>
            A Dog
        </p>
        <img src="logo.png">
        <table>
            <tr>
                <th class="selected">
                    &#39;Headline&#39;
                </th>
                <th>
                    Headline 2
                </th>
                <th>
                    Headline 3
                </th>
            </tr>
        </table>
    </body>
</html>
```

##### In this example we create a table snippet:

```lua
local tags = require "resty.tags"
local table = tags(function(rows)
    local table = table
    for _, row in ipairs(rows) do
        local tr = tr
        for _, col in ipairs(row) do
            tr(td(col))
        end
        table(tr)
    end
    return table
end)

print(table{
    { "A", 1, 1 },
    { "B", 2, 2 },
    { "C", 3, 3 }
})
```

##### And here is the output of it:

```html
<table>
    <tr>
        <td>A</td>
        <td>1</td>
        <td>1</td>
    </tr>
    <tr>
        <td>B</td>
        <td>2</td>
        <td>2</td>
    </tr>
    <tr>
        <td>C</td>
        <td>3</td>
        <td>3</td>
    </tr>
</table>
```

##### Some special treatment is done to `<script>` and `<style>` tags:

```lua
local tags = require "resty.tags"
local script = tags("script")
print(script[[
    function hello() {
        alert("<strong>Hello World</strong>");
    }
    hello();
]])
```

##### As you can see, we don't HTML encode the output:

```html
<script>
    function hello() {
        alert("<strong>Hello World</strong>");
    }
    hello();
</script>
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-tags](https://github.com/bungle/lua-resty-tags){target=_blank}.