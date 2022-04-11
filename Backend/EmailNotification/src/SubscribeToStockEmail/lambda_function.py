import json
import boto3


def lambda_handler(event, context):

    if event["Stock"] == 'TEST1':
        TopicArn = 'arn:aws:sns:us-east-1:555178539686:TEST1'
    elif event["Stock"] == 'TEST2':
        TopicArn = 'arn:aws:sns:us-east-1:555178539686:TEST2'
    elif event["Stock"] == 'TEST3':
        TopicArn = 'arn:aws:sns:us-east-1:555178539686:TEST3'

    email_id = event["Email"]

        
    sns_client= boto3.client("sns")
    response = sns_client.subscribe(
    TopicArn=TopicArn,
    Protocol='email',
    Endpoint=email_id,
    ReturnSubscriptionArn=True
)
    
