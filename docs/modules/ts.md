# *ts*: NGINX MPEG-TS Live Module


## Installation

You can install this module in any RHEL-based distribution, including, but not limited to:

* RedHat Enterprise Linux 6, 7, 8, 9
* CentOS 6, 7, 8, 9
* AlmaLinux 8, 9
* Rocky Linux 8, 9
* Amazon Linux 2

```bash
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install nginx-module-ts
```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_ts_module.so;
```


This document describes nginx-module-ts [v0.1.1](https://github.com/arut/nginx-ts-module/releases/tag/v0.1.1){target=_blank} 
released on Jul 14 2017.

<hr />
NGINX MPEG-TS Live Module
=========================

Features
--------

-   receives MPEG-TS over HTTP
-   produces and manages live [HLS](https://tools.ietf.org/html/draft-pantos-http-live-streaming-23)
-   produces and manages live [MPEGDDASH](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)

Compatibility
-------------

-   [nginx](http://nginx.org) version \>= 1.11.5

Build
-----

Building nginx with the module:

``` {.sourceCode .bash}
## static module
$ ./configure --add-module=/path/to/nginx-ts-module

## dynamic module
$ ./configure --add-dynamic-module=/path/to/nginx-ts-module
```

Directives
----------

### ts

|---|---|
|*Syntax:*|`ts`|
|*Context:*|location|

Sets up a live MPEG-TS handler for the location. This directive is **required** for HLS or MPEG-DASH generation.

The last URI component is used as a stream name. For example, if the URI is `/foo/bar/baz`, the stream name is `baz`.

A simple way to stream MPEG-TS over HTTP is by running `ffmpeg`:

``` {.sourceCode .bash}
$ ffmpeg ... -f mpegts http://127.0.0.1:8000/foo
```

By default, HTTP request body size is limited in nginx. To enable live streaming without size limitation, use the directive `client_max_body_size 0`.

### ts\_hls

|---|---|
|*Syntax:*|`ts_hls path=PATH [segment=MIN[:MAX]] [segments=NUMBER] [max_size=SIZE] [noclean]`|
|*Context:*|location|

Enables generating live HLS in the location. The `PATH` parameter specifies a directory where HLS playlist and segment files will be created. The directory is created if missing. For every publshed stream a subdirectory with the stream name is created under the `PATH` directory. The HLS playlist file created in the stream subdirectory is named `index.m3u8`. A path handler is installed to watch files in the directory. The old files in the directory are automatically deleted once they get old enough and are not supposed to be accessed by clients anymore. It is not allowed to reuse the path in other `ts_hls` or `ts_dash` directives.

The `segment` parameter specifies minimum and maximum segment durations. If the stream has video, segments are started at video key frames. If a key frame does not appear within `MAX` duration, the segment is truncated. The default value for minimum segment duration is 5 seconds. If unspecified, maximum segment duration is set to be twice as much as the minimum.

The `segments` parameter specifies the maximum number of segments in a playlist. As new segments are added to the playlist, the oldest segments are removed from it.

The `max_size` parameter specifies the maximum size of a segment. A segment is truncated once it reaches this size.

The `noclean` parameter indicates that the old files (segments and the playlist) should not be automatically deleted from disk.

Example:

    location / {
        ts;
        ts_hls path=/var/hls segment=10s;
    }

### ts\_dash

|---|---|
|*Syntax:*|`ts_dash path=PATH [segment=MIN[:MAX]] [segments=NUMBER] [max_size=SIZE] [noclean]`|
|*Context:*|location|

Enables generating live MPEG-DASH in the location. The `PATH` parameter specifies a directory where MPEG-DASH manifest and segment files will be created. The directory is created if missing. For every publshed stream a subdirectory with the stream name is created under the `PATH` directory. The MPEG-DASH manifest file created in the stream subdirectory is named `index.mpd`. A path handler is installed to watch files in the directory. The old files in the directory are automatically deleted once they get old enough and are not supposed to be accessed by clients anymore. It is not allowed to reuse the path in other `ts_hls` or `ts_dash` directives.

The `segment` parameter specifies minimum and maximum segment durations. If the stream has video, segments are started at video key frames. If a key frame does not appear within `MAX` duration, the segment is truncated. The default value for minimum segment duration is 5 seconds. If unspecified, maximum segment duration is set to be twice as much as the minimum.

> When setting an explicit value for the `MAX` parameter, the following note should be taken into account. If the next segment is shorter than the previous one by a factor more that two, [dashjjs](https://github.com/Dash-Industry-Forum/dash.js) can end up in a busy cycle requesting the second segment over and over again.

The `segments` parameter specifies the maximum number of segments in a manifest. As new segments are added to the manifest, the oldest segments are removed from it.

The `max_size` parameter specifies the maximum size of a segment. A segment is truncated once it reaches this size.

The `noclean` parameter indicates that the old files (segments and the manifest) should not be automatically deleted from disk.

Example:

    location / {
        ts;
        ts_dash path=/var/hls segment=10s;
    }

Example
-------

nginx.conf:

    # nginx.conf

    events {
    }

    http {
        server {
            listen 8000;

            location / {
                root html;
            }

            location /publish/ {
                ts;
                ts_hls path=/var/media/hls segment=10s;
                ts_dash path=/var/media/dash segment=10s;

                client_max_body_size 0;
            }

            location /play/ {
                types {
                    application/x-mpegURL m3u8;
                    application/dash+xml mpd;
                    video/MP2T ts;
                    video/mp4 mp4;
                }
                alias /var/media/;
            }
        }
    }

HLS in HTML:

``` {.sourceCode .html}
<body>
  <video width="640" height="480" controls autoplay
         src="http://127.0.0.1:8000/play/hls/sintel/index.m3u8">
  </video>
</body>
```

MPEG-DASH in HTML using the [dashjjs](https://github.com/Dash-Industry-Forum/dash.js) player:

``` {.sourceCode .html}
<script src="http://cdn.dashjs.org/latest/dash.all.min.js"></script>

<body>
  <video data-dashjs-player
         width="640" height="480" controls autoplay
         src="http://127.0.0.1:8000/play/dash/sintel/index.mpd">
  </video>
</body>
```

Broadcasting a single-bitrate mp4 file:

``` {.sourceCode .bash}
$ ffmpeg -re -i ~/Movies/sintel.mp4 -bsf:v h264_mp4toannexb
         -c copy -f mpegts http://127.0.0.1:8000/publish/sintel
```

Broadcasting an mp4 file in multiple bitrates. For proper HLS generation streams should be grouped into MPEG-TS programs with the `-program` option of `ffmpeg`:

``` {.sourceCode .bash}
$ ffmpeg -re -i ~/Movies/sintel.mp4 -bsf:v h264_mp4toannexb
         -map 0:0 -map 0:1 -map 0:0 -map 0:1
         -c:v:0 copy
         -c:a:0 copy
         -c:v:1 libx264 -b:v:1 100k
         -c:a:1 libfaac -ac:a:1 1 -b:a:1 32k
         -program "st=0:st=1" -program "st=2:st=3"
         -f mpegts http://127.0.0.1:8000/publish/sintel
```

## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-ts](https://github.com/arut/nginx-ts-module){target=_blank}.