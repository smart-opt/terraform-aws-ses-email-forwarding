import boto3
import os
import email
from email.mime.text import MIMEText


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    ses = boto3.client('ses')

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    obj = s3.get_object(Bucket=bucket_name, Key=key)
    email_content = obj['Body'].read().decode('utf-8')

    msg = email.message_from_string(email_content)
    from_addr = msg['From']
    to_addr = os.environ['MailRecipient']
    subject = msg['Subject']

    new_msg = MIMEText(msg.get_payload())
    new_msg['From'] = from_addr
    new_msg['To'] = to_addr
    new_msg['Subject'] = subject

    response = ses.send_raw_email(
        Source=from_addr,
        Destinations=[to_addr],
        RawMessage={
            'Data': new_msg.as_string()
        }
    )

    return response
