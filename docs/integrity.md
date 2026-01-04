---
title: Verify NGINX RPM Package Integrity - GPG Key Installation
description: Verify GetPageSpeed NGINX module packages with GPG signature. Install the GPG key for package integrity verification on RHEL, CentOS, Rocky Linux and AlmaLinux.
---

# Packages Integrity

Your package manager can verify packages before installation. To set this up, install our GPG key.

## Set up the GPG key for CentOS/RHEL 9 and above

```bash
rpm --import https://extras.getpagespeed.com/RPM-GPG-KEY-GETPAGESPEED-2023
```

## Set up the GPG key for other distros

```bash
rpm --import https://extras.getpagespeed.com/RPM-GPG-KEY-GETPAGESPEED
```
