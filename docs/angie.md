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

Angie is based on mainline NGINX branch, but does not guarantee 100% compatibility with NGINX ABI.
In fact, it has runtime checks when loading a module compiled for NGINX to prevent the loading,
to avoid unexpected problems.

So for the time being, you can't use numerous module packages from NGINX Extras with Angie.

## Angie Features

Angie is a superset to standard NGINX distribution and includes a number of features not available elsewhere.
You can consult the [CHANGES](https://angie.software/en/changes/) document to find the features unique to Angie.
