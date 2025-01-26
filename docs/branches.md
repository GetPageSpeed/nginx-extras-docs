# NGINX Branches

NGINX is delivered by its creators in two distinct branches: stable and mainline.

We support both. The default is *stable*.
Both branches are actually stable, but represent different NGINX feature sets and compatibility levels.

Which one is best for you? It depends.

## The stable NGINX branch

When you set up GetPageSpeed repository on your system, you are able to install stable NGINX
packages, by default.

The stable branch has less moving parts, and NGINX itself is rarely updated on it.
However, since it is not receiving frequent feature updates, it means there is less chances new bugs
are introduced to it.

## The mainline NGINX branch

The mainline branch has frequent updates, and so you can expect more package updates, as the newer
versions are released.

While it does fix any issues found in the stable branch, it has the potential of bringing more issues
via new features' code.

The mainline NGINX has a higher chance of bringing backwards incompatible changes.

## Recommendation

Stick to the stable branch, unless you are very eager to try out a new feature, fix a severe security bug,
and/or have the time to deal with potential (although rare) backwards incompatible changes.

## Still want to go with the mainline?

You can install mainline NGINX module packages easily by enabling the `mainline` sub-repository:

!!! note "Enable the mainline repository"

    === "CentOS/RHEL/Rocky Linux/AlmaLinux 8+, Fedora Linux, Amazon Linux 2023+"

        ``` bash
        sudo dnf -y install dnf-plugins-core
        sudo dnf config-manager --enable getpagespeed-extras-mainline
        ```

    === "CentOS 7 or Amazon Linux 2"

        ``` bash
        sudo yum -y --disablerepo getpagespeed-extras install yum-utils
        sudo yum-config-manager --enable getpagespeed-extras-mainline
        ```

Then `dnf upgrade` to ensure all the NGINX modules currently installed are switched to their mainline equivalent.

Then install additional modules as usual, e.g.:

```
sudo dnf -y install nginx-module-security
```

## Changed your mind and want to go with stable?

For reasons mentioned above, you may want to downgrade to the stable branch:

!!! note "Disable the mainline repository"

    === "CentOS/RHEL/Rocky Linux/AlmaLinux 8+, Fedora Linux, Amazon Linux 2023+"

        ``` bash
        sudo dnf -y install dnf-plugins-core
        sudo dnf config-manager --disable getpagespeed-extras-mainline
        sudo dnf -y downgrade "nginx*"
        ```

    === "CentOS 7 or Amazon Linux 2"

        ``` bash
        sudo yum-config-manager --disable getpagespeed-extras-mainline
        sudo yum -y downgrade "nginx*"
        ```
