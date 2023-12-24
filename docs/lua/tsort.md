# *tsort*: Performs a topological sort on input data


## Installation

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua-resty-tsort
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install lua5.1-resty-tsort
```


To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-tsort [v1.0](https://github.com/bungle/lua-resty-tsort/releases/tag/v1.0){target=_blank} 
released on Apr 06 2016.
    
<hr />

Performs a topological sort on input data.

## Synopsis

```lua
local dump  = require "pl.pretty".dump
local tsort = require "resty.tsort"

local graph = tsort.new()

graph:add('a', 'b')
graph:add('b', 'c')
graph:add('0', 'a')

dump(graph:sort())

-- Output:
-- {
--   "0",
--   "a",
--   "b",
--   "c"
-- }

graph:add('1', '2', '3', 'a');

dump(graph:sort())

-- Output:
-- {
--   "0",
--   "1",
--   "2",
--   "3",
--   "a",
--   "b",
--   "c"
-- }

graph:add{'1', '1.5'};
graph:add{'1.5', 'a'};

dump(graph:sort())

-- Output:
-- {
--   "0",
--   "1",
--   "2",
--   "3",
--   "1.5",
--   "a",
--   "b",
--   "c"
-- }

graph:add('first', 'second');
graph:add('second', 'third', 'first');

local sorted, err = graph:sort()

-- Returns:
-- sorted = nil
-- err = "There is a circular dependency in the graph. It is not possible to derive a topological sort."
```

## Alternatives

Before developing this library, I asked on #lua channel on Freenode if anyone knows a library that does
topological sort. I also tried to search for a library. Unfortunately I didn't find anything. But, there
was already a library from the great [@starius](https://github.com/starius) called [toposort](https://github.com/starius/toposort/).
`toposort` looks really nice and it has a lot more features compared to `lua-resty-tsort`. So you may want to
take a look to that as well especially if you are looking for a more full featured library. I have not
benchmarked these libs or compared them to C-implementation of tsort or other alternatives. If your graph
is not too big, say you use these to sort Javascript / CSS files or something similar, I think the performance
is not an issue.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-tsort](https://github.com/bungle/lua-resty-tsort){target=_blank}.