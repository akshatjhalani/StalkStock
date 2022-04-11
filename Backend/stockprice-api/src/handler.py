try:
    import unzip_requirements
except ImportError:
    pass

import json
import logging
import boto3
import os
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')


def hello(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    from boto3.dynamodb.conditions import Key
    table = dynamodb.Table(os.environ['HOURLY_DYNAMODB_TABLE'])
    response = table.query(
        KeyConditionExpression=Key('symbol').eq("WBA") & Key('date').eq("2021-01-04T09:30:00-05:00"),
    )

    logger.info(response)

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!!",
        "input": event,
        "items": str(response['Items'])
    }

    return {"statusCode": 200, "body": json.dumps(body)}
