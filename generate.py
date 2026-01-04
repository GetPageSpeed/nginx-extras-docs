import re
from os.path import dirname, basename

import base64
import glob
import os
import pandoc
import yaml
from lastversion import lastversion
from pathlib import Path
from tabulate import tabulate

work_dir = os.path.dirname(__file__) or "."
print(work_dir)
os.chdir(work_dir)
import lastversion

print(lastversion.__file__)

REMOVABLE_SECTIONS = [
    "installation",
    "install",
    "installing",
    "build",
    "how to install",
    "how to build",
    "building as a dynamic module",
    "static module",
    "dynamic module",
    "installation:",
    "compilation",
    "how to install",
    "patch to collect ssl_cache_usage, ssl_handshake_time content_time, gzip_time, "
    "upstream_time, upstream_connect_time, upstream_header_time graphs (optional)",
    "table of contents",
    "install in centos 7",
    "c macro configurations",
    "requirements",
    "building",
    "compatibility",
    "toc",
    "dependencies",
    "installation for stable nginx",
    "version",
    "credits",
    "copyright and license",
    "license",
    "licence",
    "copyright",
    "licensing",
    "todo",
    "not yet implemented",
    "author",
    "contributing",
    "luarocks",
    "authors",
    "community",
    "support the project",
    "english mailing list",
    "chinese mailing list",
    "bugs and patches",
    "bugs",
    "copyright & licenses",
    "changelogs",
    "acknowledgments",
    "getting involved",
    "report bugs",
    "source repository",
    "donation",
]

# Line must start with this in order to be ignored/removed
bad_lines = (
    "[back to toc](#table-of-contents)",
    "this module is not distributed",
    "installation instructions](#installation).",
    "[![build",
    "status]",
    "[![travisci build",
    "![ngx\_pagespeed]",
    "lua_package_path",
    "lua_package_cpath",
    "![module version]",
)


def enrich_with_yml_info(md, module_config, release):
    handle = module_config["handle"]
    repo = module_config.get("repo")
    # `release` may be None (e.g. for internal/core modules where we don't
    # care about an external lastversion lookup).
    safe_release = release or {}
    rel_version = str(safe_release.get("version", "0"))
    is_internal = not repo and release is None

    # Only mark as BETA when we actually have release information and the
    # version is reported as 0.
    if release is not None and rel_version == "0":
        new_title = f"# *[BETA!] {handle}*: {module_config['summary']}"
    else:
        new_title = f"# *{handle}*: {module_config['summary']}"
    sonames = module_config["soname"]
    lines = md.splitlines()
    first_line = lines[0]
    if first_line.startswith("#"):
        lines.pop(0)
    if "ref" in module_config:
        intro = f"""
## Installation

CentOS/RHEL/RockyLinux/etc. and Amazon Linux are supported and require a [subscription](https://www.getpagespeed.com/repo-subscribe).

Fedora Linux is supported free of charge and doesn't require a subscription.

### OS-specific complete installation and configuration guides available:

"""
        if "el7" in module_config["ref"]:
            intro += f"*   [CentOS/RHEL 7]({module_config['ref']['el7']})\n"
        if "el8" in module_config["ref"]:
            intro += f"*   [CentOS/RHEL 8]({module_config['ref']['el8']})\n"
        if "amzn2" in module_config["ref"]:
            intro += f"*   [Amazon Linux 2]({module_config['ref']['amzn2']})\n"

        intro += f"""
### Other supported operating systems
        
```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install nginx-module-{handle}
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

"""
    else:
        intro = f"""

## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 7, 8, 9 and 10
* CentOS 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2 and Amazon Linux 2023

=== "CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023+"

    ```bash
    dnf -y install https://extras.getpagespeed.com/release-latest.rpm 
    dnf -y install nginx-module-{handle}
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-{handle}
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

"""

    # Prepend premium notice for plan-gated modules (plan indicates the minimum tier)
    plan = (module_config.get("plan") or "").strip()
    plan_normalized = plan.lower()
    enterprise = plan_normalized == "enterprise"
    pro = plan_normalized == "pro"
    if pro or enterprise:
        plan_suffix = " (or higher)" if pro else ""
        intro = (
            f"\n> Requires the {plan.title()} plan{plan_suffix} of the GetPageSpeed NGINX Extras subscription.\n\n"
            + intro
        )
    print(sonames)
    if isinstance(sonames, str):
        sonames = [sonames]
    print(sonames)
    for s in sonames:
        intro += f"```nginx\nload_module modules/{s}.so;\n```\n"
    # For internal/closed-source modules we intentionally skip linking to a GitHub repo.
    if is_internal:
        # Internal modules are built from the same nginx source and ship
        # together with nginx itself, so we don't need a separate version
        # lookup. Just clarify that in the docs.
        intro += """

This module is built from the same source as the NGINX core.
"""
    elif repo and not enterprise and safe_release:
        intro += f"""

This document describes nginx-module-{handle} [v{safe_release.get('version','0')}](https://github.com/{repo}/releases/tag/{safe_release.get('tag_name','')}){{target=_blank}} 
released on {safe_release.get('tag_date','').strftime("%b %d %Y") if safe_release.get('tag_date') else 'an unknown date'}.
"""
    elif repo and enterprise and safe_release:
        intro += f"""

This document describes nginx-module-{handle} v{safe_release.get('version','0')} 
released on {safe_release.get('tag_date','').strftime("%b %d %Y") if safe_release.get('tag_date') else 'an unknown date'}.
"""

    if release is not None and rel_version == "0":
        intro += "\nProduction stability is *not guaranteed*."
    if "release_ticket" in module_config:
        intro += f"\nA request for stable release exists. Vote up [here]({module_config['release_ticket']})."
    intro += "\n<hr />\n"

    out = [new_title] + intro.splitlines()

    for l in lines:
        check_l = l.strip().lower().lstrip("*_")
        if check_l not in bad_lines and not check_l.startswith(bad_lines):
            out.append(l)
    return "\n".join(out)


def enrich_lib_with_yml_info(md, module_config, release):
    handle = module_config["handle"]
    repo = module_config["repo"]
    new_title = f"# *{handle}*: {module_config['summary']}"
    upstream_name = module_config["repo"].split("/")[-1]
    lines = md.splitlines()
    # readme may be empty at the release tag (rarely, but does happen)
    if lines:
        first_line = lines[0]
        if first_line.startswith("#"):
            lines.pop(0)
    if "ref" in module_config:
        intro = f"""
## Installation

CentOS/RHEL and Amazon Linux are supported and require a commercial subscription.

If you haven't set up RPM repository subscription, [sign up](https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following steps.

Fedora Linux is supported free of charge and doesn't require a subscription.

### OS-specific complete installation and configuration guides available:

"""
        if "el7" in module_config["ref"]:
            intro += f"*   [CentOS/RHEL 7]({module_config['ref']['el7']})\n"
        if "el8" in module_config["ref"]:
            intro += f"*   [CentOS/RHEL 8]({module_config['ref']['el8']})\n"
        if "amzn2" in module_config["ref"]:
            intro += f"*   [Amazon Linux 2]({module_config['ref']['amzn2']})\n"

        intro += f"""
### Other supported operating systems
        
```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua-resty-{handle}
```
"""
    else:
        intro = f"""

## Installation

If you haven't set up RPM repository subscription, [sign up](
https://www.getpagespeed.com/repo-subscribe). Then you can proceed with the following 
steps.

### CentOS/RHEL 7 or Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
yum -y install lua-resty-{handle}
```

### CentOS/RHEL 8+, Fedora Linux, Amazon Linux 2023

```bash
dnf -y install https://extras.getpagespeed.com/release-latest.rpm
dnf -y install lua5.1-resty-{handle}
```

"""
    intro += f"""
To use this Lua library with NGINX, ensure that [nginx-module-lua](../modules/lua.md) is installed.

This document describes lua-resty-{handle} [v{release['version']}](https://github.com/{repo}/releases/tag/{release['tag_name']}){{target=_blank}} 
released on {release['tag_date'].strftime("%b %d %Y")}.
    """
    intro += "\n<hr />\n"
    out = [new_title] + intro.splitlines()

    prev_skipped = False
    for line in lines:
        check_l = line.strip().lower().lstrip("*_")
        if check_l not in bad_lines and not check_l.startswith(bad_lines):
            if prev_skipped and not check_l:
                # if previously skipped now is empty line, skip that
                pass
            else:
                out.append(line)
            prev_skipped = False
        else:
            # a bad line
            prev_skipped = True
    return "\n".join(out)


def convert_headings(lines):
    """Converts headings to GitHub-flavored Markdown."""
    converted_lines = []
    i = 0
    inside_code_section = False
    while i < len(lines):  # Iterate through all lines
        current_line = lines[i]

        # Check if we are inside a code section
        if current_line.startswith("```"):
            inside_code_section = not inside_code_section

        if not inside_code_section and i + 1 < len(
            lines
        ):  # Check if the next line exists
            next_line = lines[i + 1].strip()

            # Check if the next line consists solely of '=' or '-' characters
            if set(next_line) == {"="}:
                heading = "#" + " " + current_line  # Convert to level 1 heading
                converted_lines.append(heading)
                i += 2  # Skip the next line
                continue
            elif set(next_line) == {"-"}:
                heading = "##" + " " + current_line  # Convert to level 2 heading
                converted_lines.append(heading)
                i += 2  # Skip the next line
                continue

        # Add the current line as is if it's not a heading or there's no next line
        converted_lines.append(current_line)
        i += 1

    return "\n".join(converted_lines)


# only support GitHub flavored markdown
# so we preprocess files with pandoc docs/modulesupsync.md -o docs/modulesupsync.md -t gfm
def remove_md_sections(md, titles):
    out = []
    # marks that we are "within" target section
    section_level = None

    markdown_lines = md.splitlines()

    for line in markdown_lines:
        # remove that stuff:
        # https://stackoverflow.com/questions/46154561/remove-zero-width-space-unicode-character-from-python-string/55400921
        line = line.replace("\u200c", "")
        line = line.replace("\ufeff", "")
        if not line.startswith("#"):
            # if not in target section, proceed adding stuff
            if not section_level:
                out.append(line)
            continue
        # we are reading section title now
        cur_sec_level = 0
        cur_sec_title = ""
        seen_whitespace = False
        for c in line:
            if c == "#":
                cur_sec_level = cur_sec_level + 1
            else:
                cur_sec_title = cur_sec_title + c
        cur_sec_title = cur_sec_title.strip().rstrip(":")
        cur_sec_title_lower = cur_sec_title.lower()
        # Check if heading starts with any of the removable section texts
        should_remove = (
            cur_sec_title_lower in titles
            or any(cur_sec_title_lower.startswith(title.lower()) for title in titles)
        )
        if should_remove:
            section_level = cur_sec_level
            # do not add this target section title
        elif section_level:
            # already in target section
            if cur_sec_level <= section_level:
                # found same/higher level with different title, unmark so we know we're out
                section_level = None
                out.append(line)
            else:
                # level under target section, we skip
                pass
        else:
            # some other section
            out.append(line)
    return "\n".join(out)


def ensure_one_h1(md):
    # It is crucial for there to be only one heading or else TOC is not properly generated
    out = []
    seen_h1 = False
    lines = md.splitlines()
    for line in lines:
        if line.startswith("# "):
            if not seen_h1:
                seen_h1 = True
            else:
                line = "## " + line.lstrip("# ")
        out.append(line)
    return "\n".join(out)


all_modules = []
table = []
headers = ["Package Name", "Description"]

all_libs = []
libs_table = []


def detect_code_lang(readme_contents):
    out = []
    lines = readme_contents.splitlines()
    total = len(lines)
    for i in range(total):
        line = lines[i]
        if (
            line.strip() == "```"
            and i < (total - 1)
            and lines[i + 1]
            .strip()
            .startswith(
                ("http ", "location ", "server ", "map ", "stream ", "upstream ")
            )
        ):
            line = "```nginx"
        out.append(line)
    return out


def normalize_to_md(readme_contents, file_name):
    # normalize to Github flavored markdown
    doc = pandoc.Document()
    if file_name.endswith(".rst"):
        doc.rst = readme_contents.encode("utf-8")
    elif file_name.endswith(".textile"):
        doc.textile = readme_contents.encode("utf-8")
    else:
        readme_lines = detect_code_lang(readme_contents)
        return convert_headings(readme_lines)

    try:
        # this is available in pandoc for RHEL 8+
        return doc.gfm.decode("utf-8")
    except AttributeError:
        # available everywhere, less accurate
        return doc.markdown_github.decode("utf-8")


def get_readme_contents_from_github(handle, module_config):
    print(f"Fetching release for {module_config['repo']}")
    release = lastversion.latest(module_config["repo"], output_format="dict")
    if not release or "readme" not in release:
        return None
    readme_contents = base64.b64decode(release["readme"]["content"]).decode("utf-8")
    readme_contents = normalize_to_md(readme_contents, release["readme"]["name"])
    readme_contents = remove_md_sections(readme_contents, REMOVABLE_SECTIONS)

    readme_contents = enrich_with_yml_info(readme_contents, module_config, release)

    readme_contents = (
        readme_contents
        + f"""

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-{handle}](https://github.com/{module_config['repo']}){{target=_blank}}.
"""
    )
    readme_contents = ensure_one_h1(readme_contents)
    return readme_contents


def process_modules_glob(g):
    for module_file_name in glob.glob(g):
        print(f"Processing {module_file_name}")
        handle = Path(module_file_name).stem
        with open(module_file_name) as f:
            all_modules.append(handle)
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            module_config = yaml.load(f, Loader=yaml.FullLoader)
            module_config["handle"] = handle
            readme_contents = ""
            if basename(dirname(module_file_name)) == "internal":
                print("Internal module!")
                if "directives_url" in module_config:
                    directives_urls = module_config["directives_url"]
                    if not isinstance(directives_urls, list):
                        directives_urls = [directives_urls]
                readme_contents = (
                    readme_contents
                    + f"""

## Directives

You may find information about configuration directives for this module at the following links:        

"""
                )

                for url in directives_urls:
                    readme_contents = readme_contents + f"*   {url}"
                readme_contents = enrich_with_yml_info(
                    readme_contents, module_config, None
                )
            else:
                readme_contents = get_readme_contents_from_github(handle, module_config)
            if not readme_contents:
                continue
            with open(f"docs/modules/{handle}.md", "w") as module_md_f:
                # Build SEO-optimized front-matter
                summary = escape_yaml_string(module_config['summary'])
                
                # Craft compelling, action-oriented title for search results
                seo_title = f"{summary}"
                
                # Craft a rich meta description - include full details for featured snippets
                # Don't truncate: Google extracts the most relevant portion automatically
                base_desc = escape_yaml_string(module_config['description']).strip()
                seo_description = f"RPM package nginx-module-{handle}. {base_desc}"
                
                preface = f"""---

title: "{seo_title}"
description: "{seo_description}"

---

"""
                readme_contents = preface + readme_contents
                module_md_f.write(readme_contents)
            table.append(
                [
                    f"[nginx-module-{handle}](modules/{handle}.md)",
                    module_config["summary"],
                ]
            )
        # break


def escape_yaml_string(value: str) -> str:
    """
    Escapes special characters in a string to make it safe for use in YAML inside quotes.

    Args:
        value (str): The input string to escape.

    Returns:
        str: The escaped string safe for YAML.
    """
    # Escape backslashes and double quotes
    escaped_value = value.replace("\\", "").replace('"', "")
    # Replace newlines with \n
    escaped_value = escaped_value.replace("\n", " ")
    # Escape other problematic characters
    escaped_value = re.sub(
        r"([\x00-\x1F])", lambda match: f"\\x{ord(match.group(1)):02x}", escaped_value
    )
    return escaped_value


def process_lua_glob(g):
    for lua_lib_file_name in glob.glob(g):
        print(f"Processing {lua_lib_file_name}")
        handle = Path(lua_lib_file_name).stem
        with open(lua_lib_file_name) as f:
            all_libs.append(handle)
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            lib_config = yaml.load(f, Loader=yaml.FullLoader)
            lib_config["handle"] = handle
            print(f"Fetching release for {lib_config['repo']}")
            release = lastversion.latest(lib_config["repo"], output_format="dict")
            if not release or "readme" not in release:
                continue
            readme_contents = base64.b64decode(release["readme"]["content"]).decode(
                "utf-8"
            )
            readme_contents = normalize_to_md(
                readme_contents, release["readme"]["name"]
            )
            readme_contents = remove_md_sections(readme_contents, REMOVABLE_SECTIONS)

            readme_contents = enrich_lib_with_yml_info(
                readme_contents, lib_config, release
            )

            # Build SEO-optimized front-matter for Lua libraries
            lua_summary = escape_yaml_string(lib_config['summary'])
            lua_seo_description = f"RPM package lua-resty-{handle}: {lua_summary}"
            if len(lua_seo_description) > 160:
                lua_seo_description = lua_seo_description[:157].rsplit(' ', 1)[0] + '...'
            
            preface = f"""---

title: "{lua_summary}"
description: "{lua_seo_description}"

---
  
"""
            readme_contents = preface + readme_contents

            readme_contents = (
                readme_contents
                + f"""

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub repository for 
nginx-module-{handle}](https://github.com/{lib_config['repo']}){{target=_blank}}.
"""
            )
            readme_contents = ensure_one_h1(readme_contents)
            # print(readme_contents)
            with open(f"docs/lua/{handle}.md", "w") as lib_md_f:
                lib_md_f.write(readme_contents)
            libs_table.append(
                [f"[lua-resty-{handle}](lua/{handle}.md)", lib_config["summary"]]
            )


process_lua_glob("../nginx-lua-extras/resty/*.yml")
process_modules_glob("../nginx-extras/modules/*.yml")
process_modules_glob("../nginx-extras/modules/others/*.yml")
process_modules_glob("../nginx-extras/modules/internal/*.yml")

with open(f"docs/modules_list.md", "w") as index_md_f:
    table.sort()
    index_md_f.write(tabulate(table, headers, tablefmt="github"))

with open(f"docs/lua_list.md", "w") as libs_index_md_f:
    libs_table.sort()
    libs_index_md_f.write(tabulate(libs_table, headers, tablefmt="github"))


all_modules.sort()
print(all_modules)
final_all_modules = []
for m in all_modules:
    final_all_modules.append({m: f"modules/{m}.md"})

all_libs.sort()
final_all_libs = []
for l in all_libs:
    final_all_libs.append({l: f"lua/{l}.md"})

# write nav:
with open("mkdocs.yml") as mkdocs_f:
    mkdocs_config = yaml.load(mkdocs_f, Loader=yaml.Loader)
    # get list of lua libs from lua/*.md
    lua_libs = sorted(os.listdir("docs/lua"))
    lua_libs_index = {"Overview": "lua.md"}
    for l in lua_libs:
        if l.endswith(".md"):
            handler_name = l.replace(".md", "")
            lua_libs_index[handler_name] = f"lua/{l}"

    nginx_modules = sorted(os.listdir("docs/modules"))
    nginx_modules_index = {"Overview": "modules.md"}
    for m in nginx_modules:
        if m.endswith(".md"):
            handler_name = m.replace(".md", "")
            nginx_modules_index[handler_name] = f"modules/{m}"

    nav = [
        {"Overview": "index.md"},
        {"Modules": nginx_modules_index},
        {"Lua Scripting": lua_libs_index},
        {
            "Distributions": [
                "branches.md",
                "nginx-mod.md",
                "tengine.md",
                "plesk.md",
                "quic.md",
                "angie.md",
            ]
        },
        {"RPM Repository": "https://www.getpagespeed.com/redhat"},
    ]
    mkdocs_config["nav"] = nav
    print(mkdocs_config)
with open("mkdocs.yml", "w") as f:
    yaml.dump(mkdocs_config, f)

print("Done generation")
