# NGINX Extras Documentation

The NGINX Extras is the largest [_commercial_](https://www.getpagespeed.com/repo-subscribe){target=_blank} collection of prebuilt dynamic NGINX modules on the Internet.
Each module can be installed as a separate package.

The major benefit of packaged installs is of course security, maintainability, and reproducibility.
No longer you have to manually compile anything when you need to update NGINX or modules.
An update is just a `yum update` that takes seconds and no downtime whatsoever.

We currently support all major RPM-based distros, including CentOS/RHEL version 6 through 8 inclusive,
as well as Amazon Linux 2.

Due to the extensive nature of our collection, it's easy to get lost in all the goodies and new NGINX directives.

This documentation mini-site brings you each module's installation instructions and added directives
in a single place. 

## Getting started

### Install repository configuration

    sudo yum -y install https://extras.getpagespeed.com/release-latest.rpm

Once the repository configuration is installed, <a href="https://www.getpagespeed.com/repo-subscribe">activate your subscription to the GetPageSpeed repository</a>.

Subscribed? Proceed with installing the modules to build your ultimate high-performance web stack.

### Install NGINX modules

Thanks to the nature of dynamic modules, you can install *just the modules* you want instead of using bloatware NGINX installation. 

For example, to install NGINX and the PageSpeed module for it, run:

    sudo yum -y install nginx nginx-module-pagespeed

To list available modules for installation, run:

    sudo yum list available | grep nginx-module

To install the recommended group of modules for performance and security, you may want to run:

    sudo yum -y groupinstall "nginx extras recommended"

This installs NGINX, and modules: PageSpeed, Brotli, Dynamic ETag, Immutable (performance); ModSecurity, Security Headers (security).

## How to use this documentation

* Use the search at the top rightmost. It's good for locating whether a feature you are after is available
 via a module
* Just curious what's there? Look at the complete list of modules below, or in the left-side navigation.

## Complete module list

{!docs/modules.md!}



