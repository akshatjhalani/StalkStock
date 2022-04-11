try:
    import unzip_requirements
except ImportError:
    pass

import datetime
import json
import logging
import os
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')


def hello(event, context):
    DB = os.environ['DB_HOST']

    symbols = ["GS", "JNJ"]
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    batch_keys = {
        table.name: {
            'Keys': [{'symbol': symbol, 'date': "2021-11-26T10:30:00-05:00"} for symbol in symbols]
        },
    }
    response = dynamodb.batch_get_item(RequestItems=batch_keys)
    print(response)
    for response_table, response_items in response.items():
        logger.info("Got %s items from %s.", len(response_items), response_table)

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
