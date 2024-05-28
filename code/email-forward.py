import boto3
import os
import email
from email.mime.text import MIMEText

region = os.environ['Region']


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    ses = boto3.client('ses', region)

    message_id = event['Records'][0]['ses']['mail']['messageId']
    print(f"Received message ID {message_id}")

    incoming_email_bucket = os.environ['MailS3Bucket']
    incoming_email_prefix = os.environ['MailS3Prefix']

    if incoming_email_prefix:
        object_path = (incoming_email_prefix + "/" + message_id)
    else:
        object_path = message_id

    obj = s3.get_object(Bucket=incoming_email_bucket, Key=object_path)
    email_content = obj['Body'].read().decode('utf-8')

    msg = email.message_from_string(email_content)
    from_addr = os.environ['MailSender']
    to_addr = os.environ['MailRecipient']
    subject = msg['Subject']
    reply_to = msg['From']

    new_msg = MIMEText(msg.get_payload())
    new_msg['From'] = from_addr
    new_msg['To'] = to_addr
    new_msg['Subject'] = subject
    new_msg['Reply-To'] = reply_to

    response = ses.send_raw_email(
        Source=from_addr,
        Destinations=[to_addr],
        RawMessage={
            'Data': new_msg.as_string()
        }
    )

    return response
