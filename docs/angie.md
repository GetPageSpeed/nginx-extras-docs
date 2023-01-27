# Angie

Angie is an efficient, powerful and scalable web server, that was forked from NGINX by some of its former core devs, 
with intention to extend functionality far beyond original version.

Angie is a drop-in replacement for nginx, so you can use existing nginx configuration without major changes.

## Installation and compatibility

NGINX Extras provide you with production-grade, SELinux compatible packages for Angie web server.

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    sudo yum -y install https://extras.getpagespeed.com/release-latest.rpm yum-utils
    sudo yum-config-manager --enable getpagespeed-extras-angie
    sudo yum -y install nginx
    ``` 
 
=== "CentOS/RHEL 8, 9"

    ```bash
    sudo dnf -y install https://extras.getpagespeed.com/release-latest.rpm dnf-plugins-core
    sudo dnf config-manager --enable getpagespeed-extras-angie
    sudo dnf -y install nginx
    ```

## Compatibility notes

Commercial subscription for GetPageSpeed repository is required to install NGINX modules for Angie.

Angie is based on mainline NGINX branch, but does not guarantee 100% compatibility with NGINX ABI.
That said, you can attempt (compatibility not guaranteed!) to use numerous module packages from NGINX Extras 
to empower your Angie furthermore, e.g. to add the 
[PageSpeed module](modules/pagespeed.md):

```bash
sudo dnf config-manager --enable getpagespeed-extras-mainline
sudo dnf -y install nginx-module-pagespeed
```

## Angie Features

Currently, Angie does not provide a feature documentation page.
See https://github.com/webserver-llc/angie/issues/14 for reference.
