---

title: "Streaming ZIP archiver for NGINX"
description: "RPM package nginx-module-zip. mod_zip assembles ZIP archives dynamically. It can stream component files from upstream servers with nginx's native proxying code, so that the process never takes up more than a few KB of RAM at a time, even while assembling archives that are (potentially) gigabytes in size.  mod_zip supports a number of modern ZIP features, including large files, UTC timestamps, and UTF-8 filenames. It allows clients to resume large downloads using the Range and If-Range headers, although these feature require the server to know the file checksums (CRC-32's) in advance. See Usage for details.  To unzip files on the fly, check out nginx-module-unzip. "

---

# *zip*: Streaming ZIP archiver for NGINX


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
    dnf -y install nginx-module-zip
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-zip
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_zip_module.so;
```


This document describes nginx-module-zip [v1.2.1](https://github.com/dvershinin/mod_zip/releases/tag/1.2.1){target=_blank} 
released on Jul 20 2022.

<hr />

mod_zip assembles ZIP archives dynamically. It can stream component files from
upstream servers with nginx's native proxying code, so that the process never
takes up more than a few KB of RAM at a time, even while assembling archives that
are (potentially) gigabytes in size.

mod_zip supports a number of "modern" ZIP features, including large files, UTC
timestamps, and UTF-8 filenames. It allows clients to resume large downloads using
the "Range" and "If-Range" headers, although these feature require the server
to know the file checksums (CRC-32's) in advance. See "Usage" for details.

To unzip files on the fly, check out [nginx-unzip-module](https://github.com/youzee/nginx-unzip-module).


## Usage

The module is activated when the original response (presumably from an
upstream) includes the following HTTP header:

    X-Archive-Files: zip

It then scans the response body for a list of files. The syntax is a 
space-separated list of the file checksum (CRC-32), size (in bytes), location
(properly URL-encoded), and file name. One file per line.  The file location
corresponds to a location in your nginx.conf; the file can be on disk, from an
upstream, or from another module.  The file name can include a directory path,
and is what will be extracted from the ZIP file. Example:

    1034ab38 428    /foo.txt   My Document1.txt
    83e8110b 100339 /bar.txt   My Other Document1.txt
    0        0      @directory My empty directory

Files are retrieved and encoded in order. If a file cannot be found or the file
request returns any sort of error, the download is aborted.

The CRC-32 is optional. Put "-" if you don't know the CRC-32; note that in this
case mod_zip will disable support for the `Range` header.

A special URL marker `@directory` can be used to declare a directory entry
within an archive. This is very convenient when you have to package a tree of
files, including some empty directories. As they have to be declared explicitly.

If you want mod_zip to include some HTTP headers of the original request, in the
sub-requests that fetch content of files, then pass the list of their names in
the following HTTP header:

    X-Archive-Pass-Headers: <header-name>[:<header-name>]*


## Re-encoding filenames

To re-encode the filenames as UTF-8, add the following header to the upstream
response:

    X-Archive-Charset: [original charset name]

The original charset name should be something that iconv understands. (This feature
only works if iconv is present.)

If you set original charset as `native`:

    X-Archive-Charset: native;

filenames from the file list are treated as already in the system native charset.
Consequently, the ZIP general purpose flag (bit 11) that indicates UTF-8 encoded
names will not be set, and archivers will know it's a native charset.

Sometimes there is problem converting UTF-8 names to native(CP866) charset that
causes popular archivers to fail to recognize them. And at the same time you want
data not to be lost so that smart archivers can use Unicode Path extra field.
You can provide you own, adapted representation of filename in native charset along
with original UTF-8 name in one string. You just need to add following header:

    X-Archive-Name-Sep: [separator];

So your file list should look like:

    <CRC-32> <size> <path> <native-filename><separator><utf8-filename>
    ...

then filename field will contatin `native-filename` and Unicode Path extra field
will contain `utf8-filename`.

## Tips

1. Add a header "Content-Disposition: attachment; filename=foobar.zip" in the
upstream response if you would like the client to name the file "foobar.zip"

1. To save bandwidth, add a "Last-Modified" header in the upstream response; 
mod_zip will then honor the "If-Range" header from clients.

1. To wipe the X-Archive-Files header from the response sent to the client,
use the headers_more module: http://wiki.nginx.org/NginxHttpHeadersMoreModule

1. To improve performance, ensure the backends are not returning gzipped
files. You can achieve this with `proxy_set_header Accept-Encoding "";`
in the location blocks for the component files.

Questions/patches may be directed to Evan Miller, emmiller@gmail.com.

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-zip](https://github.com/dvershinin/mod_zip){target=_blank}.