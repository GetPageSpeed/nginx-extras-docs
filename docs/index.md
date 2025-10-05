---
hide:
  - navigation
---

# NGINX Extras Documentation

The NGINX Extras is the largest [_commercial_](https://www.getpagespeed.com/repo-subscribe){target=_blank} collection of prebuilt dynamic NGINX modules on the Internet.
Each module can be installed as a separate package.

The major benefit of packaged installations is security, maintainability, and reproducibility.
No longer you have to manually compile anything when you need to update NGINX or modules.
An update is just a `dnf update` that takes seconds and no downtime whatsoever.

We currently support all major RPM-based distros, including CentOS/RHEL,
as well as Amazon Linux and the latest Fedora Linux.

All RHEL derivatives like Oracle Linux, AlmaLinux, and Rocky Linux are supported as well.

Due to the extensive nature of our collection, it's easy to get lost in all the goodies and new NGINX directives.

This documentation site brings you each module's installation instructions and added directives
in a single place. 

## Getting started

To verify packages' integrity before installation, [install our GPG key](integrity.md).

!!! note "Install repository configuration"

    === "CentOS/RHEL/Rocky Linux/AlmaLinux 8+, Fedora Linux, Amazon Linux 2023+"

        ``` bash
        dnf -y install https://extras.getpagespeed.com/release-latest.rpm
        ```

    === "CentOS 7"

        ``` bash
        yum -y install https://extras.getpagespeed.com/release-latest.rpm
        yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm
        ```

    === "Amazon Linux 2"

        ``` bash
        yum -y install https://extras.getpagespeed.com/release-latest.rpm
        amazon-linux-extras install epel
        ```

Once the repository configuration is installed, <a href="https://www.getpagespeed.com/repo-subscribe">activate your subscription to the GetPageSpeed repository</a>.

Subscribed? Proceed with installing the modules to build your ultimate high-performance web stack.

### Install NGINX modules

Thanks to the nature of dynamic modules, you can install *just the modules* you want instead of using bloatware NGINX installation. 

For example, to install NGINX and the Brotli module for it, run:

    dnf -y install nginx nginx-module-brotli

Enable the module by adding the `load_module ...` directive that is shown after installation.

In case you missed it, refer to [the documentation of respective module](https://nginx-extras.getpagespeed.com/modules/) and look for `load_module` directive
required to enable it.

To list available modules for installation, run:

    sudo dnf list available | grep nginx-module

To install the recommended group of modules for performance and security, you may want to run:

    sudo dnf -y groupinstall "nginx extras recommended"

This installs NGINX, and modules: PageSpeed, Brotli, Dynamic ETag, Immutable (performance); ModSecurity, Security Headers (security).

## Upgrading modules

New NGINX releases require upgrading its modules. Thanks to the repository, you don't need to worry about recompiling anything.
We ship updated NGINX and module packages, and you can simply run `dnf upgrade` to get to the latest NGINX and module packages.

After updating a module package, to actually apply it at runtime, you have to run the binary upgrade routine.
This can be done like this:

```bash
service nginx upgrade
```

This ensures that NGINX loads the updated module(s).

## Complete module list

Proceed to the [Modules](https://nginx-extras.getpagespeed.com/modules/) page to see all available modules and their documentation.
