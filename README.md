# Terraform AWS SES Email Forwarding

This module configures Amazon SES to forward emails to an existing account (gmail or something). This module will configure the following resources:

- DNS verification, DKIM and MX domains.
- SES rule set to save the incoming emails to S3 and to execute a Lambda.
- Lambda that will forward the email from `sender` to `recipient`.

This module implements the official solution by AWS:
https://aws.amazon.com/blogs/messaging-and-targeting/forward-incoming-email-to-an-external-destination/

## Arguments

| Name               | Type   | Required | Default         | Description                                          |
| ------------------ | ------ | -------- | --------------- | ---------------------------------------------------- |
| `s3_bucket`        | String | Yes      |                 | S3 Bucket where emails will be stored                |
| `s3_bucket_prefix` | String | Yes      |                 | Path inside the bucket where emails will be stored   |
| `mail_sender`      | String | Yes      |                 | Email used to send messages from (when forwarding)   |
| `mail_recipient`   | String | Yes      |                 | Email used to send messages to (when forwarding)     |
| `domain`           | String | Yes      |                 | Domain to configure (ex: aleix.cloud)                |
| `prefix`           | String | No       | `email-forward` | All resources will be tagged using this prefix name  |
| `aws_region`       | String | No       | `eu-west-1`     | AWS region where we should configure the integration |
| `dns_provider`     | String | No       | `aws`           | DNS provider where the domain is registered          |

## Attributes

| Name | Type | Required | Default | Description |
| ---- | ---- | -------- | ------- | ----------- |
|      |      |          |         |             |

## Example

Let's imagine I want to configure `hello@aleix.cloud` domain to be available to the world, but I don't want to pay for an email service.

I can use this module to register this email through an existing email, and send all incoming emails to my personal Gmail.

```
module "ses-email-forwarding" {
    source = "git@github.com:smart-opt/terraform-aws-ses-email-forwarding.git"

    domain           = "aleix.cloud"
    s3_bucket        = "amurtra"
    s3_bucket_prefix = "emails"
    mail_sender      = "hello@aleix.cloud"
    mail_recipient   = "xxxxx@gmail.com"
    aws_region       = "eu-west-1"
}
```

## Contributors

All contributors are more than welcome :)
