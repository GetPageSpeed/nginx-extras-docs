---

title: "NGINX module to proxy to authenticated AWS services"
description: "RPM package nginx-module-aws-auth. This NGINX module can proxy requests to authenticated S3 backends using Amazon's V4 authentication API. "

---

# *aws-auth*: NGINX module to proxy to authenticated AWS services


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
    dnf -y install nginx-module-aws-auth
    ```

=== "CentOS/RHEL 7 and Amazon Linux 2"

    ```bash
    yum -y install https://extras.getpagespeed.com/release-latest.rpm
    yum -y install https://epel.cloud/pub/epel/epel-release-latest-7.noarch.rpm 
    yum -y install nginx-module-aws-auth
    ```

Enable the module by adding the following at the top of `/etc/nginx/nginx.conf`:

```nginx
load_module modules/ngx_http_aws_auth_module.so;
```


This document describes nginx-module-aws-auth [v2.1.1](https://github.com/anomalizer/ngx_aws_auth/releases/tag/2.1.1){target=_blank} 
released on Mar 06 2017.

<hr />

 [![Gitter chat](https://badges.gitter.im/anomalizer/ngx_aws_auth.png)](https://gitter.im/ngx_aws_auth/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link)

This nginx module can proxy requests to authenticated S3 backends using Amazon's
V4 authentication API. The first version of this module was written for the V2
authentication protocol and can be found in the *AuthV2* branch.

## Usage example

Implements proxying of authenticated requests to S3.

```nginx
  server {
    listen     8000;

    aws_access_key your_aws_access_key; # Example AKIDEXAMPLE
    aws_key_scope scope_of_generated_signing_key; #Example 20150830/us-east-1/service/aws4_request
    aws_signing_key signing_key_generated_using_script; #Example L4vRLWAO92X5L3Sqk5QydUSdB0nC9+1wfqLMOKLbRp4=
	aws_s3_bucket your_s3_bucket;

    location / {
	  aws_sign;
      proxy_pass http://your_s3_bucket.s3.amazonaws.com;
    }

    # This is an example that does not use the server root for the proxy root
	location /myfiles {
	
      rewrite /myfiles/(.*) /$1 break;
      proxy_pass http://your_s3_bucket.s3.amazonaws.com/$1;


      aws_access_key your_aws_access_key;
      aws_key_scope scope_of_generated_signing_key;
      aws_signing_key signing_key_generated_using_script;
    }

    # This is an example that use specific s3 endpoint, default endpoint is s3.amazonaws.com
	location /s3_beijing {
	
      rewrite /s3_beijing/(.*) /$1 break;
      proxy_pass http://your_s3_bucket.s3.cn-north-1.amazonaws.com.cn/$1;

      aws_sign;
      aws_endpoint "s3.cn-north-1.amazonaws.com.cn";
      aws_access_key your_aws_access_key;
      aws_key_scope scope_of_generated_signing_key;
      aws_signing_key signing_key_generated_using_script;
    }
  }
```

## Security considerations
The V4 protocol does not need access to the actual secret keys that one obtains 
from the IAM service. The correct way to use the IAM key is to actually generate
a scoped signing key and use this signing key to access S3. This nginx module
requires the signing key and not the actual secret key. It is an insecure practise
to let the secret key reside on your nginx server.

Note that signing keys have a validity of just one week. Hence, they need to
be refreshed constantly. Please useyour favourite configuration management
system such as saltstack, puppet, chef, etc. etc. to distribute the signing
keys to your nginx clusters. Do not forget to HUP the server after placing the new
signing key as nginx reads the configuration only at startup time.

A standalone python script has been provided to generate the signing key
```
./generate_signing_key -h
usage: generate_signing_key [-h] -k ACCESS_KEY -r REGION [-s SERVICE]
                            [-d DATE] [--no-base64] [-v]

Generate AWS S3 signing key in it's base64 encoded form

optional arguments:
  -h, --help            show this help message and exit
  -k SECRET_KEY, --secret-key SECRET_KEY
                        The secret key generated using AWS IAM. Do not confuse
                        this with the access key id
  -r REGION, --region REGION
                        The AWS region where this key would be used. Example:
                        us-east-1
  -s SERVICE, --service SERVICE
                        The AWS service for which this key would be used.
                        Example: s3
  -d DATE, --date DATE  The date on which this key is generated in yyyymmdd
                        format
  --no-base64           Disable output as a base64 encoded string. This NOT
                        recommended
  -v, --verbose         Produce verbose output on stderr


./generate_signing_key -k wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY -r us-east-1
L4vRLWAO92X5L3Sqk5QydUSdB0nC9+1wfqLMOKLbRp4=
20160902/us-east-1/s3/aws4_request

```

## Known limitations
The 2.x version of the module currently only has support for GET and HEAD calls. This is because
signing request body is complex and has not yet been implemented.



## GitHub

You may find additional configuration tips and documentation for this module in the [GitHub 
repository for 
nginx-module-aws-auth](https://github.com/anomalizer/ngx_aws_auth){target=_blank}.